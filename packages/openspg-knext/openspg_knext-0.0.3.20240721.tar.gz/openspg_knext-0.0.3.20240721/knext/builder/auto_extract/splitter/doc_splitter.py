# -*- coding: utf-8 -*-
# Copyright 2023 OpenSPG Authors
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except
# in compliance with the License. You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License
# is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
# or implied.
import os
import re
import hashlib
import markdown
import base64
import pandas as pd
from bs4 import BeautifulSoup, Tag
from typing import Any, List, Dict, Union
from langchain_community.document_loaders import PyPDFLoader

from knext.common.retriever import Retriever
from knext.builder.auto_extract.base import Splitter
from knext.builder.auto_extract.model.chunk import Chunk, ChunkTypeEnum
from knext.builder.auto_extract.common.parser.table_data_parser import TableDataParser
from knext.builder.auto_extract.common.textrank import textrank
from knext.builder.auto_extract.common.llm_client import LLMClient


class DocSplitter(Splitter):
    def __init__(self, **kwargs):

        # Chinese/ASCII characters
        self.kept_char_pattern = pattern = re.compile(
            r"[^\u4e00-\u9fa5\u3000-\u303F\uFF01-\uFF0F\uFF1A-\uFF20\uFF3B-\uFF40\uFF5B-\uFF65\x00-\x7F]+"
        )
        self.kwargs = kwargs
        llm_client = self.kwargs.get("llm_client", None)
        if llm_client is not None:
            self.llm_client = llm_client
        else:
            llm_client_conf = self.kwargs.get("llm_client_conf", None)
            if llm_client_conf is not None:

                self.llm_client = LLMClient.from_config(llm_client_conf)
            else:
                self.llm_client = None

    def get_basename(self, file_name: str):
        base, ext = os.path.splitext(os.path.basename(file_name))
        return base

    def split_sentence(self, content):
        sentence_delimiters = "。？?！!；;\n"
        output = []
        start = 0
        for idx, char in enumerate(content):
            if char in sentence_delimiters:
                end = idx
                tmp = content[start : end + 1].strip()
                if len(tmp) > 0:
                    output.append(tmp)
                start = idx + 1
        res = content[start:]
        if len(res) > 0:
            output.append(res)
        return output

    def filter_text(self, text):
        filtered_text = re.sub(self.kept_char_pattern, "", text)
        return filtered_text

    def slide_window_chunk(
        self,
        content: Union[str, List[str]],
        chunk_size: int = 2000,
        window_length: int = 300,
        sep: str = "\n",
        prefix: str = "SlideWindow",
    ) -> List[Chunk]:

        if isinstance(content, str):
            content = self.split_sentence(content)
        splitted = []
        cur = []
        cur_len = 0
        for sentence in content:
            if cur_len + len(sentence) > chunk_size:
                splitted.append(cur)
                tmp = []
                cur_len = 0
                for item in cur[::-1]:
                    tmp.append(item)
                    cur_len += len(item)
                    if cur_len > window_length:
                        break
                cur = tmp[::-1]

            cur.append(sentence)
            cur_len += len(sentence)
        if len(cur) > 0:
            splitted.append(cur)

        output = []
        for idx, sentences in enumerate(splitted):
            chunk_name = f"{prefix}#{idx}"
            chunk = Chunk(
                type=ChunkTypeEnum.Text,
                chunk_header="",
                chunk_name=chunk_name,
                chunk_id=Chunk.generate_hash_id(chunk_name),
                content=sep.join(sentences),
            )
            output.append(chunk)
        return output

    def semantic_chunk(
        self,
        content: str,
        chunk_size: int = 1000,
        example: Union[Dict, List[Dict]] = {},
        prefix: str = "SemanticChunk",
    ) -> List[Chunk]:
        if self.llm_client is None:
            raise ValueError("llm client not found")
        from knext.builder.auto_extract.common.prompt.user_defined_prompts import (
            SemanticSegPrompt,
        )

        prompt_op = SemanticSegPrompt()
        prompt_args = {"input": content}
        if len(example) > 0:
            prompt_args["example"] = example
        message = prompt_op.build_prompt(prompt_args)
        print(f"message = {message}")
        result = self.llm_client.remote_inference(message)
        print(f"result[{type(result)}] = {result}")
        tmp = {
            "content": content,
            "result": result,
        }
        splitted = prompt_op.parse_result(tmp)
        print(f"splitted = {splitted}")
        chunks = []
        for item in splitted:
            if len(item["content"]) < chunk_size:
                chunk = Chunk(
                    type=ChunkTypeEnum.Text,
                    chunk_header="",
                    chunk_name=f"{prefix}#{item['name']}",
                    chunk_id=Chunk.generate_hash_id(item["name"]),
                    content=item["content"],
                    abstract=item["name"],
                )
                chunks.append(chunk)
            else:
                print("chunk over size")
                chunks.extend(
                    self.semantic_chunk(
                        item["content"], chunk_size, example, f"{prefix}#SubLevel"
                    )
                )
        return chunks

    def txt_split(
        self, content: str, basename: str, semantic_split: bool, split_length: int
    ) -> List[Chunk]:
        chapters = []
        max_len = 0
        paragraphs = []
        for line in content.split("\n"):
            line = line.strip()
            if len(line) == 0:
                continue
            if line.startswith("$$"):
                line = line[2:]
                chapters.append(len(paragraphs))
            paragraphs.append(line)
            max_len = max(max_len, len(line))
        print(f"max_len = {max_len}")
        chapters.append(len(paragraphs))
        book = {}
        if len(chapters) > 1:
            for i in range(len(chapters) - 1):
                start = chapters[i]
                end = chapters[i + 1]
                chapter_name = paragraphs[start]
                book[chapter_name] = paragraphs[start + 1 : end]
        else:
            book[basename] = paragraphs

        cutted = []
        for k, v in book.items():
            if k == basename:
                prefix = basename
            else:
                prefix = f"{basename}#{k}"
            if semantic_split:
                cutted.extend(
                    self.semantic_chunk("".join(v), split_length, prefix=prefix)
                )
            else:
                cutted.extend(
                    self.slide_window_chunk(
                        "".join(v), split_length, 100, prefix=prefix
                    )
                )
        return cutted

    def _invoke(
        self, file_name: str, user_query: str, semantic_split: bool, split_length: int
    ) -> List[List[Chunk]]:
        with open(file_name, "r") as file:
            content = file.read()
        basename = self.get_basename(file_name)
        return [
            [x] for x in self.txt_split(content, basename, semantic_split, split_length)
        ]

    def invoke(self, file_name: str, user_query: str, **kwargs) -> List[List[Chunk]]:
        semantic_split = kwargs.get("semanticSplit", False)
        builder_index = kwargs.get("builderIndex", False)
        split_length = kwargs.get("splitLength", 500)
        chunks = self._invoke(file_name, user_query, semantic_split, split_length)

        if builder_index:
            for chunk_group in chunks:
                for chunk in chunk_group:
                    if not semantic_split and chunk.type == ChunkTypeEnum.Text:
                        abstract = textrank(self.split_sentence(chunk.content))
                        chunk.abstract = abstract
        return chunks


class CSVDocSplitter(DocSplitter):
    def cut(
        self,
        dict_content: Dict[str, str],
        index: int,
        semantic_split: bool,
        split_length: int,
    ):
        output = []
        for k, v in dict_content.items():
            if semantic_split:
                tmp = self.semantic_chunk(v, split_length, prefix=f"{index}#{k}")
            else:
                tmp = self.slide_window_chunk(v, split_length, 100, prefix=f"{index}#{k}")
            for item in tmp:
                item.header = k
                output.append(item)
        return output

    def _invoke(
        self, file_name: str, user_query: str, semantic_split: bool, split_length: int
    ) -> List[List[Chunk]]:
        output = []
        data = pd.read_csv(file_name)
        for i in range(len(data)):
            dict_content = data.loc[i]
            cutted = self.cut(dict_content.to_dict(), i, semantic_split, split_length)
            output.append(cutted)
        return output


class PDFDocSplitter(DocSplitter):
    def process_single_page(
        self,
        page: str,
        watermark: str,
        remove_header: bool = False,
        remove_footnote: bool = False,
    ):
        lines = page.split("\n")
        if remove_header:
            lines = lines[1:]
        if remove_footnote:
            lines = lines[:-1]
        cleaned = []
        for line in lines:
            line = line.strip().replace(watermark, "")
            if len(line) > 0:
                cleaned.append(line)
        return cleaned

    def _invoke(
        self, file_name: str, user_query: str, semantic_split: bool, split_length: int
    ) -> List[List[Chunk]]:

        if not file_name.endswith(".pdf"):
            raise ValueError(f"please provide a pdf file, got {file_name}")

        loader = PyPDFLoader(file_name)
        pages = loader.load_and_split()

        cleaned_pages = [
            self.process_single_page(x.page_content, "", False, True) for x in pages
        ]
        sentences = []
        for cleaned_page in cleaned_pages:
            sentences += cleaned_page
        basename = self.get_basename(file_name)
        if semantic_split:
            chunks = self.semantic_chunk(
                "".join(sentences), split_length, prefix=basename
            )
        else:
            chunks = self.slide_window_chunk(
                "".join(sentences), split_length, 100, prefix=basename
            )
        return [[x] for x in chunk]


class MarkDownDocSplitter(DocSplitter):

    ALL_LEVELS = [f"h{x}" for x in range(1, 7)]

    def to_text(self, level_tags):
        content = []
        for item in level_tags:
            if isinstance(item, list):
                content.append(self.to_text(item))
            else:
                header, tag = item
                if not isinstance(tag, Tag):
                    continue
                if tag.name == "table":
                    continue
                elif tag.name in self.ALL_LEVELS:
                    content.append(
                        f"{header}-{tag.text}" if len(header) > 0 else tag.text
                    )
                else:
                    content.append(tag.text)
        # print("to_text: ", level_tags, content)
        return "\n".join(content)

    def extract_table(self, level_tags, header=""):
        tables = []
        for idx, item in enumerate(level_tags):
            if isinstance(item, list):
                tables += self.extract_table(item, header)
            else:
                tag = item[1]
                if not isinstance(tag, Tag):
                    continue
                if tag.name in self.ALL_LEVELS:
                    header = f"{header}-{tag.text}" if len(header) > 0 else tag.text

                if tag.name == "table":
                    if idx - 1 >= 0:
                        context = level_tags[idx - 1]
                        if isinstance(context, tuple):
                            tables.append((header, context[1].text, tag))
                    else:
                        tables.append((header, "", tag))
        return tables

    def parse_level_tags(self, level_tags, level, parent_header="", cur_header=""):
        if len(level_tags) == 0:
            return []
        output = []
        prefix_tags = []
        while len(level_tags) > 0:
            tag = level_tags[0]
            if tag.name in self.ALL_LEVELS:
                break
            else:
                prefix_tags.append((parent_header, level_tags.pop(0)))
        if len(prefix_tags) > 0:
            output.append(prefix_tags)

        cur = []
        while len(level_tags) > 0:
            tag = level_tags[0]
            if tag.name not in self.ALL_LEVELS:
                cur.append((parent_header, level_tags.pop(0)))
            else:

                if tag.name > level:
                    # found sublevel
                    cur += self.parse_level_tags(
                        level_tags,
                        tag.name,
                        f"{parent_header}-{cur_header}"
                        if len(parent_header) > 0
                        else cur_header,
                        tag.name,
                    )
                elif tag.name == level:
                    # stop current level
                    if len(cur) > 0:
                        output.append(cur)
                    cur = [(parent_header, level_tags.pop(0))]
                    cur_header = tag.text
                else:
                    if len(cur) > 0:
                        output.append(cur)
                    return output
        if len(cur) > 0:
            output.append(cur)
        return output

    def cut(self, level_tags, cur_level, final_level):
        output = []
        if cur_level == final_level:
            cur_prefix = []
            for sublevel_tags in level_tags:
                if (
                    isinstance(sublevel_tags, tuple)
                    and sublevel_tags[1].name != "table"
                ):
                    cur_prefix.append(sublevel_tags[1].text)
                else:
                    break
            cur_prefix = "\n".join(cur_prefix)

            if len(cur_prefix) > 0:
                output.append(cur_prefix)
            for sublevel_tags in level_tags:
                if isinstance(sublevel_tags, list):
                    output.append(cur_prefix + "\n" + self.to_text(sublevel_tags))
            return output
        else:
            cur_prefix = []
            for sublevel_tags in level_tags:
                # if not isinstance(sublevel_tags, list):
                if (
                    isinstance(sublevel_tags, tuple)
                    and sublevel_tags[1].name != "table"
                ):
                    cur_prefix.append(sublevel_tags[1].text)
                else:
                    break
            cur_prefix = "\n".join(cur_prefix)
            if len(cur_prefix) > 0:
                output.append(cur_prefix)

            for sublevel_tags in level_tags:
                if isinstance(sublevel_tags, list):
                    output += self.cut(sublevel_tags, cur_level + 1, final_level)
            return output

    def _invoke(
        self, file_name: str, user_query: str, semantic_split: bool, split_length: int
    ) -> List[List[Chunk]]:

        basename = self.get_basename(file_name)
        cut_depth = self.kwargs.get("cut_depth", 1)
        with open(file_name, "r") as reader:
            content = reader.read()
        html_content = markdown.markdown(
            content, extensions=["markdown.extensions.tables"]
        )

        soup = BeautifulSoup(html_content, "html.parser")
        top_level = None
        all_levels = [f"h{x}" for x in range(1, 11)]
        for level in self.ALL_LEVELS:
            tmp = soup.find_all(level)
            if len(tmp) > 0:
                top_level = level
                break
        # no level info found, degenerate to text chunk
        if top_level is None:
            chunks = self.txt_split(soup.text, basename, semantic_split, split_length)
            return [[x] for x in chunks]
        tags = []

        for tag in soup.children:
            if isinstance(tag, Tag):
                tags.append(tag)

        level_tags = self.parse_level_tags(tags, top_level)
        cutted = self.cut(level_tags, 0, cut_depth)

        chunks = []

        for idx, content in enumerate(cutted):
            prefix = f"{basename}#{idx}"
            if len(content) <= split_length:
                print("DONOT split")
                chunks.append(
                    Chunk(
                        type=ChunkTypeEnum.Text,
                        chunk_header="",
                        chunk_name=prefix,
                        chunk_id=Chunk.generate_hash_id(prefix),
                        content=content,
                    )
                )
            else:
                print("need further split")
                if semantic_split:
                    chunks.extend(
                        self.semantic_chunk(content, split_length, prefix=prefix)
                    )
                else:
                    chunks.extend(
                        self.slide_window_chunk(
                            content, split_length, 100, prefix=prefix
                        )
                    )

        entity_info = user_query.split("-")
        top_entity_name = ""
        top_entity_type = ""
        if len(entity_info) > 2:
            top_entity_name = entity_info[-1]
            top_entity_type = entity_info[-2]

        # process tables
        for idx, table_info in enumerate(self.extract_table(level_tags)):
            header, context, table = table_info
            table = TableDataParser.parse_table(table)
            table["context"] = context
            table["top_entity_name"] = top_entity_name
            table["top_entity_type"] = top_entity_type
            chunk_name = f"{header}#{idx}"
            chunks.append(
                Chunk(
                    type=ChunkTypeEnum.Table,
                    chunk_header=header,
                    chunk_name=chunk_name,
                    chunk_id=Chunk.generate_hash_id(chunk_name),
                    content=table,
                )
            )
        return [[x] for x in chunks]


if __name__ == "__main__":
    data_dir = "../data/"

    llm_client = LLMClient.from_config_name("deepseek", use_pre=False)

    splitter = DocSplitter(llm_client=llm_client)
    file_name = "zhengce.txt"
    chunks = splitter.invoke(
        os.path.join(data_dir, file_name), "政策文件", builderIndex=True
    )
    for chunk in chunks:
        print("*" * 80)
        print(chunk[0].name, "###", chunk[0].content, "###", chunk[0].abstract)

    chunks = splitter.invoke(
        os.path.join(data_dir, file_name), "政策文件", semanticSplit=True, builderIndex=True
    )
    for chunk in chunks:
        print("*" * 80)
        print(chunk[0].name, "###", chunk[0].content, "###", chunk[0].abstract)

    # file_name = "benzi-key.pdf"
    # loader = PyPDFLoader(os.path.join(data_dir, file_name))
    # pages = loader.load_and_split()
    # content = [x.page_content for x in pages]
    # content = "\n".join(content)
    #
    # cutted = splitter.semantic_chunk(content)
    #
    # splitter = PDFDocSplitter()
    # file_name = "benzi-key.pdf"
    # cutted = splitter.invoke(file_name=os.path.join(data_dir, file_name))
    #

    splitter = CSVDocSplitter(llm_client=llm_client)
    import pandas as pd

    cutted = splitter.invoke(
        os.path.join(data_dir, "GovernmentServiceForm.csv"),
        "政务",
        builderIndex=True,
        semanticSplit=False,
        splitLength=150,
    )
    print(cutted)
    splitter = MarkDownDocSplitter(llm_client=llm_client)
    chunks = splitter.invoke(
        os.path.join(data_dir, "baike-person-wangxiaobo.md"),
        "百科-人物-王小波",
        semanticSplit=True,
        splitLength=200,
        builderIndex=True,
    )
    for chunk in chunks:
        print("*" * 80)
        print(chunk[0].name, "###", chunk[0].content, "###", chunk[0].abstract)
