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
import copy
import numpy as np

from typing import List, Dict
import concurrent.futures
from knext.builder.auto_extract.base import Extractor
from knext.builder.auto_extract.model.chunk import Chunk, ChunkTypeEnum
from knext.builder.auto_extract.common.llm_client import LLMClient
from knext.builder.operator import SPGRecord
from knext.builder.operator.op import PromptOp
from tenacity import retry, stop_after_attempt, wait_exponential


class Prompt(PromptOp):
    def __init__(self):
        self.prompt = {}

    def parse_result(self, line):
        return []

    def build_prompt(self, variables: Dict[str, str]) -> str:
        template = copy.deepcopy(self.prompt)

        if isinstance(variables, str):
            variables = {"input": variables}
        template.update(variables)
        self.variables = variables
        return json.dumps(template, ensure_ascii=False)

    def result_to_spgrecord(self, result: List):
        raise NotImplemented("result_to_spgrecord not implemented.")

    def parse_response(self, response: str, **kwargs) -> List[SPGRecord]:
        result = self.parse_result(response)
        if result is None:
            return result
        if len(result) > 0:
            return self.result_to_spgrecord(result)
        return []


class EntityExtractPrompt(Prompt):
    def __init__(self, name: str):
        self.prompt = {
            "instruction": f"input字段是{name}的一部分内容，我需要基于其构建一个知识图谱。请你参考example中的示例，抽取出所有的类型在entity_types字段中的命名实体，返回命名实体的名称与类型。请返回json list格式输出结果。不要输出任何非json格式的内容，如额外的解释说明。",
            "entity_types": {
                "人群": "特定人群或个体，如灵活就业人员、个体工商户、自由职业者等。",
                # "日期": "具体日期或时间段，如2023年12月25日、每月20日。",
                "地点": "地理位置或行政区域，如成都市、本市等。",
                "组织机构": "具有法人资格的单位或组织，如政府机构、企业、协会等。",
                "政策文件": "政府或相关机构发布的具有法律效力的正式文件。",
                "家庭成员": "家庭中的成员，如本人，子女，父母，配偶。",
                "金融账户": "个人或机构在银行或其他金融机构开设的账户。",
                "金融概念": "与金融相关的专业术语或概念，如住房公积金、缴存账户、缴存基数、缴存比例等。",
                "金融操作": "与金融交易或管理相关的操作，如缴存、提取、封存等。",
                "政务事项": "政务相关的服务服务事项，如住房公积金、社会保险等。",
                "业务流程": "业务处理流程或步骤，如办理账户设立、申请调整、办理停缴、办理个人信息变更业务。",
                "法律法规": "法律条款、规定或管理办法。",
                "经济活动": "经济行为或活动，如购买住房、租赁住房、支付房租等。",
                "证明文件": "用于证明某些事实或情况的文件，如纳税记录、银行账户流水、资产材料等。",
                "其他": "不在以上定义中的其他所有实体。",
            },
            "example": {
                "input": """
一、灵活就业人员本人与配偶只能设立一个缴存账户，经查询住建部住房公积金监管服务平台，在异地公积金中心已设立账户并正常缴存的，应当先办理异地账户的封存手续。
二、灵活就业人员住房公积金每月缴存一次，月缴存额为缴存基数乘以缴存比例（元以下四舍五入），每月20日（含，遇节假日提前，下同）在缴存使用协议约定的扣款账户中存足缴存金额，由公积金中心扣收。当月未缴存的，不再办理补缴手续；已缴存的，不得办理退缴手续。疫情期间可以申请办理缓缴手续。
                """,
                "output": [
                    {"类型": "组织机构", "名称": "住建部住房公积金监管服务平台"},
                    {"类型": "人群", "名称": "灵活就业人员"},
                    {"类型": "家庭成员", "名称": "本人"},
                    {"类型": "家庭成员", "名称": "配偶"},
                    {"类型": "金融机构", "名称": "异地公积金中心"},
                    {"类型": "金融账户", "名称": "缴存账户"},
                    # {"类型": "日期", "名称": "每月20日"},
                    {"类型": "政务事项", "名称": "住房公积金"},
                    {"类型": "金融操作", "名称": "封存手续"},
                    {"类型": "金融操作", "名称": "扣收"},
                    {"类型": "金融操作", "名称": "补缴手续"},
                    {"类型": "金融操作", "名称": "退缴手续"},
                    {"类型": "金融操作", "名称": "缓缴手续"},
                    {"类型": "其他", "名称": "疫情"},
                ],
            },
            "input": "",
        }

    def standardize_entity(self, entity: Dict):
        if not isinstance(entity, dict):
            return None
        name = entity.get("名称", "").lower()
        type_ = entity.get("类型", "")
        if len(name) == 0:
            return None
        entity_types = self.variables.get("entity_types", None)
        if entity_types and type_ not in entity_types:
            return None
        return {
            "名称": name,
            "类型": type_,
        }

    def parse_result(self, result):
        content = result["content"]
        llm_output = result["result"]
        output = []
        for item in llm_output:
            try:
                if isinstance(item, str):
                    item = json.loads(item)
                if isinstance(item, dict) and "output" in item:
                    item = item["output"]
                for entity in item:
                    tmp = self.standardize_entity(entity)
                    if isinstance(tmp, dict):
                        name = tmp["名称"]
                        if len(name) >= 1 and len(name) <= 20:
                            output.append(name)
            except Exception as e:
                print(f"failed to parse llm output: {item}, info: {e}")
                return None
        return output

    def result_to_spgrecord(self, result: List):
        return []


class KeywordsExtractPrompt(Prompt):
    def __init__(self, name: str):
        self.prompt = {
            "instruction": f"input字段是{name}的一部分内容，我需要基于其构建文本索引。请你参考example中的示例，抽取并返回所有的关键词。重要提示：1. 你需要运用你关于{name}的背景知识，判断在该场景下哪些更适合作为关键词！！请返回json list格式输出结果。不要输出任何非json格式的内容，如额外的解释说明。",
            "example": {
                "input": """
一、灵活就业人员本人只能设立一个缴存账户，经查询住建部住房公积金监管服务平台，在异地公积金中心已设立账户并正常缴存的，应当先办理异地账户的封存手续。
二、灵活就业人员住房公积金每月缴存一次，月缴存额为缴存基数乘以缴存比例（元以下四舍五入），每月20日（含，遇节假日提前，下同）在缴存使用协议约定的扣款账户中存足缴存金额，由公积金中心扣收。当月未缴存的，不再办理补缴手续；已缴存的，不得办理退缴手续。
                """,
                "output": [
                    "灵活就业人员",
                    "缴存账户",
                    "住建部",
                    "住房公积金监管服务平台",
                    "异地公积金中心",
                    "账户封存手续",
                    "住房公积金",
                    "月缴存额",
                    "缴存基数",
                    "缴存比例",
                    "扣款账户",
                    "公积金中心",
                    "补缴手续",
                    "退缴手续",
                ],
            },
            "input": "",
        }

    def parse_result(self, result):
        content = result["content"]
        llm_output = result["result"]
        output = []
        for item in llm_output:
            try:
                if isinstance(item, str):
                    item = json.loads(item)
                if isinstance(item, dict) and "output" in item:
                    item = item["output"]
                for keyword in item:
                    if (
                        isinstance(keyword, str)
                        and len(keyword) >= 1
                        and len(keyword) <= 20
                    ):
                        output.append(keyword)
            except Exception as e:
                print(f"failed to parse llm output: {item}, info: {e}")
                return None
        return output

    def result_to_spgrecord(self, result: List):
        return []


class EventExtractPrompt(Prompt):
    def __init__(self, name):
        self.prompt = {
            "instruction": "input字段是公积金政策文件的一部分内容，entities字段是input字段中抽取的实体。请帮我从input字段中抽取出其中包含在events列表中的所有事项，以及事项的时间、地点、主客体等基础信息。请将结果以json list格式返回，具体请遵从example字段中给出的示例。注意，example只是给出了较少的示例，并未涵盖所有需要抽取的事项；由于你很可能会遗漏事件！，所以请尽可能多的抽取事件。",
            "schema": {
                "名称": "事项名称",
                "实体": "事项设计的实体，需要出现在entities字段中。多个实体使用list表示，如果没有主体，则为空list。",
            },
            "example": {
                "input": "2000年11月7日，在杨峻荣的推荐下，周杰伦发行个人首张音乐专辑《Jay》。\n                2002年，周杰伦凭借专辑《范特西》中的歌曲《爱在西元前》获得第12届台湾金曲奖最佳作曲人奖。\n\n                ",
                "entities": [
                    "杨峻荣",
                    "周杰伦",
                    "昆凌",
                    "《Jay》",
                    "《范特西》",
                    "《爱在西元前》",
                    "台湾金曲奖",
                    "昆凌",
                    "英国",
                    "台湾",
                    "汶川",
                    "广州",
                    "重庆梁平",
                ],
                "output": [
                    {"名称": "周杰伦发行首张音乐专辑", "实体": ["周杰伦", "《Jay》", "杨峻荣"]},
                    {
                        "名称": "周杰伦获得第12届台湾金曲奖最佳作曲人奖与最佳专辑奖",
                        "类型": "获奖记录",
                        "实体": [
                            "周杰伦",
                            "台湾金曲奖",
                            "台湾",
                            "最佳作曲人奖",
                            "最佳专辑奖",
                            "《范特西》",
                            "《爱在西元前》",
                        ],
                    },
                ],
            },
            "input": "",
            "entities": "",
        }

    def standardize_event(self, event: Dict):
        if not isinstance(event, dict):
            return None
        event_name = event.get("名称", "")
        entities = event.get("主体", [])
        if isinstance(entities, str):
            entities = [entities]
        standard_entities = []

        for entity in entities:
            if entity in self.variables["entities"]:
                standard_entities.append(entity)

        if len(event_name) == 0 or len(standard_entities) == 0:
            return None

        return {
            "name": event_name,
            "entities": standard_entities,
        }

    def parse_result(self, result: Dict):
        content = result["content"]
        llm_output = result["result"]
        output = []
        for item in llm_output:
            try:
                if isinstance(item, str):
                    item = json.loads(item)

                if isinstance(item, dict) and "output" in item:
                    item = item["output"]
                for entity in item:
                    if isinstance(entity, dict):
                        output.append(entity)
            except Exception as e:
                print(f"failed to parse llm output: {item}, info: {e}")
                return None
        return output

    def result_to_spgrecord(self, result: List):
        return []


class IndexExtractor(Extractor):
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
                "name": "政策文件",
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
            "entity": EntityExtractPrompt,
            "keyword": KeywordsExtractPrompt,
            "event": EventExtractPrompt,
        }
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=10)

    def get_prompt(self, prompt_name):
        return self.prompts[prompt_name](self.name)

    @retry(
        stop=stop_after_attempt(5), wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    def _extract(self, llm_client, prompt_name, prompt_args, **kwargs):

        prompt_op = self.get_prompt(prompt_name)
        prompt = prompt_op.build_prompt(prompt_args)
        llm_output = llm_client.remote_inference(prompt)
        print(
            f"task: {prompt_name}\nextract input: \n{prompt}\nextract output:\n {llm_output}"
        )
        raw_result = prompt_op.parse_result(
            {"result": [llm_output], "content": prompt_args["input"]}
        )
        if raw_result is None:
            raise ValueError(f"failed to run extraction, input: {prompt}")
        return raw_result

    def extract(self, chunk):
        record = {
            "title": chunk.name,
            "text": chunk.content,
            "passage": "\n".join([chunk.name, chunk.content]),
        }

        prompt_args = {"input": chunk.content}
        entities = self._extract(self.llm_clients[0], "entity", prompt_args)
        print(f"entities = {entities}")

        # prompt_args = {"input": chunk.content}
        # keywords = self._extract(self.llm_clients[0], "keyword", prompt_args)
        # print(f"keywords = {keywords}")
        # extracted_entities = list(set(entities + keywords))
        extracted_entities = list(set(entities))

        prompt_args = {"input": chunk.content, "entities": extracted_entities}
        events = self._extract(self.llm_clients[0], "event", prompt_args)
        print(f"events = {events}")
        extracted_triples = []
        for event in events:
            event_name = event["名称"]
            entities = event["实体"]
            extracted_entities.append(event_name)
            for entity in entities:
                extracted_triples.append([event_name, "contains", entity])
        record["extracted_entities"] = extracted_entities
        record["extracted_triples"] = extracted_triples
        return record

    def pextract(self, chunks):
        futs = []
        for chunk in chunks:
            fut = self.executor.submit(self.extract, chunk=chunk)
            futs.append(fut)
        return [x.result() for x in futs]

    def invoke(self, chunks: List[Chunk]):
        """
        - extract all entities
        - extract all keywords
        - extract all entity relations
        - extract all events
        """
        result = self.pextract(chunks)
        output = {
            "docs": result,
            "ents_by_doc": [],
            "avg_ent_chars": np.nan,
            "avg_ent_words": np.nan,
            "current_cost": 0.0,
            "approx_total_cost": 0.0,
        }
        return output


if __name__ == "__main__":
    workdir = os.path.expanduser("~/Src/libs/data/policy_files/")
    data = []
    with open(os.path.join(workdir, "processed.json"), "r") as reader:
        content = json.loads(reader.read())
        for line in content:
            data.append(
                Chunk(
                    type=ChunkTypeEnum.Text,
                    chunk_header="",
                    chunk_name=line["title"],
                    chunk_id=line["idx"],
                    content=line["text"],
                )
            )

    job_conf = {
        "model_conf": [
            {
                "model_name": "deepseek",
                "lora_name": None,
                "use_pre": False,
            },
        ],
        "name": "公积金政策文件",
    }

    extractor = IndexExtractor(0, job_conf=job_conf)

    output = extractor.invoke(data)
    with open(os.path.join(workdir, "zhengce-deepseek-output-v2.json"), "w") as writer:
        writer.write(json.dumps(output, ensure_ascii=False, indent=4))
