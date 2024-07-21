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

import json
import re
import os


from typing import List, Dict
import concurrent.futures
from knext.builder.auto_extract.base import Extractor
from knext.builder.auto_extract.model.chunk import Chunk
from knext.builder.auto_extract.utils.utils import retry
from knext.builder.auto_extract.model.sub_graph import SubGraph
from knext.builder.auto_extract.splitter import (
    PDFDocSplitter,
    CSVDocSplitter,
    MarkDownDocSplitter,
)
from knext.builder.auto_extract.post_processor.post_processor import PostProcessor
from knext.builder.auto_extract.common.llm_client import LLMClient

from knext.builder.auto_extract.common.prompt.exp_prompt import *
from knext.builder.operator import SPGRecord


class EntityRelationEventExtractor(Extractor):
    def __init__(self, project_id, **kwargs):
        self.job_conf = kwargs.get(
            "job_conf",
            {
                "model_conf": [
                    {
                        "model_name": "qwen",
                        "lora_name": None,
                        "use_pre": False,
                    }
                ],
                "name": "娱乐明星周杰伦",
            },
        )
        self.llm_clients = [
            LLMClient.from_config_name(
                x["model_name"],
                use_pre=x["use_pre"],
            )
            for x in self.job_conf["model_conf"]
        ]
        self.name = self.job_conf.get("name", "")

        self.prompts = {
            "ee": EntityExtractPrompt,
            "ee2": EntityExtractPromptV2,
            "eae": EntityAttributesExtractPrompt,
            "ere": EntityRelationExtractPrompt,
            "eve": EventExtractPrompt,
        }
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=8)

    def get_prompt(self, prompt_name):
        return self.prompts[prompt_name](self.name)

    @retry(tries=3)
    def _extract(self, llm_client, prompt_name, prompt_args, **kwargs):

        prompt_op = self.get_prompt(prompt_name)
        prompt = prompt_op.build_prompt(prompt_args)
        llm_output = llm_client.remote_inference(prompt)
        print(f"extract input: \n{prompt}\nextract output:\n {llm_output}")
        raw_result = prompt_op.parse_result(
            {"result": [llm_output], "content": prompt_args["input"]}
        )
        if raw_result is None:
            raise ValueError(f"failed to run extraction, input: {prompt}")
        spg_records = prompt_op.result_to_spgrecord(raw_result)
        return raw_result, spg_records

    def pextract(self, args: List[List]):
        all_futs = []
        for prompt_info in args:
            prompt_name, prompt_args = prompt_info
            futs = []
            for llm_client in self.llm_clients:
                fut = self.executor.submit(
                    self._extract,
                    llm_client=llm_client,
                    prompt_name=prompt_name,
                    prompt_args=prompt_args,
                )
                futs.append(fut)
            all_futs.append(futs)
        return [[x.result() for x in futs] for futs in all_futs]

    def invoke(self, chunks: List[Chunk]):
        """
        - extract all entities
        - extract all entities properties
        - extract all entity relations
        - extract all events
        """
        spg_records = []
        for chunk in chunks:
            if len(chunk.content) < 50:
                continue
            chunk_record = SPGRecord("Chunk")
            chunk_record.upsert_property("name", chunk.name)
            chunk_record.upsert_property("content", chunk.content)
            chunk_spg_records = [chunk_record]
            content = chunk.content
            # entitiy extract
            prompt_name = "ee"
            prompt_args = {
                "input": content.lower(),
                # "entity_types": {
                #     "人物": "具有特定身份、角色或特征的个人",
                #     "地点": "特定的地理位置或场所",
                #     "机构": "人或团体的集合，如政府机构、公司、学校、社团、俱乐部等",
                #     "作品": "文学、艺术、科学或其他领域的创作",
                #     "媒体": "传播信息的媒介，如报纸、杂志、出版物、广播、电视等",
                #     "演出": "在观众面前进行的现场表演活动，如演唱会等",
                #     "场馆": "用于举行活动的地点",
                #     "奖项": "对个人或团体在某一领域或活动中表现卓越的认可和奖励",
                # },
            }
            entity_extract_output = self.pextract([[prompt_name, prompt_args]])[0]
            all_entities = []
            all_entity_spg_records = []
            dedup = set()
            for entities, entity_spg_records in entity_extract_output:
                for entity, entity_spg_record in zip(entities, entity_spg_records):
                    name = entity_spg_record.get_property("name")
                    if name not in dedup:
                        dedup.add(name)
                        all_entities.append(entity)
                        all_entity_spg_records.append(entity_spg_record)

            chunk_spg_records += all_entity_spg_records

            # remove entity description in the following extraction
            for item in all_entities:
                item.pop("描述", None)
            print(f"all entities: {all_entities}")

            args = []
            for prompt_name in ["eae", "ere", "eve"]:
                args.append(
                    [prompt_name, {"input": content.lower(), "entities": all_entities}]
                )

            extract_output = self.pextract(args)
            for task_output in extract_output:  # task level
                for model_output in task_output:  # model level
                    chunk_spg_records += model_output[1]

            # # entitiy extract 2
            # prompt_op = self.prompts["ee2"]
            # prompt_args = {
            #     "input": content.lower(),
            #     "entity_types": {
            #         "人物": "具有特定身份、角色或特征的个人",
            #         "地点": "特定的地理位置或场所",
            #         "机构": "人或团体的集合，如政府机构、公司、学校、社团、俱乐部等",
            #         "作品": "文学、艺术、科学或其他领域的创作",
            #         "演出": "在观众面前进行的现场表演活动，如演唱会等",
            #         "场馆": "用于举行活动的地点",
            #         "奖项": "对个人或团体在某一领域或活动中表现卓越的认可和奖励，如台湾金曲奖，",
            #     },
            #     "entities": entities,
            # }
            # entities_2, entity_spg_records_2 = self._extract(prompt_op, prompt_args)
            # chunk_spg_records += prompt_op.result_to_spgrecord(entities_2)

            # old = set([x["名称"] for x in entities])
            # print(f"old entites: {old}")
            # for item in entities_2:
            #     if item["名称"] not in old:
            #         entities.append(item)
            # print(f"new entities: {entities}")

            # # entity properties extract
            # prompt_op = self.prompts["eae"]
            # prompt_args = {"input": content.lower(), "entities": entities}
            # _, spg_records = self._extract(prompt_op, prompt_args)
            # chunk_spg_records += spg_records

            # # entity relation extract
            # prompt_op = self.prompts["ere"]
            # prompt_args = {"input": content.lower(), "entities": entities}
            # _, spg_records = self._extract(prompt_op, prompt_args)
            # chunk_spg_records += spg_records

            # # event extract
            # prompt_op = self.prompts["eve"]
            # prompt_args = {"input": content.lower(), "entities": entities}
            # _, spg_records = self._extract(prompt_op, prompt_args)
            # chunk_spg_records += spg_records

            for spg_record in chunk_spg_records:
                spg_record.upsert_property("chunk", chunk.name)

            spg_records += chunk_spg_records
        return spg_records


if __name__ == "__main__":

    # manual
    file_name = "../data/baike-person-zhoujielun.md"

    splitter = MarkDownDocSplitter(cut_depth=2)
    cutted = splitter.invoke(
        file_name=file_name,
        user_query="",
    )

    job_conf = {
        "model_conf": [
            {
                "model_name": "deepseek",
                "lora_name": None,
                "use_pre": False,
            },
        ],
        "name": "娱乐明星周杰伦",
    }

    extractor = EntityRelationEventExtractor(0, job_conf=job_conf)
    spg_records = []
    for i in cutted:
        spg_records += extractor.invoke(i)

    print(f"there are {len(spg_records)} records extracted")
    with open("exp.json", "w") as writer:
        tmp = [x.to_dict() for x in spg_records]
        writer.write(json.dumps(tmp, ensure_ascii=False, indent=4))
