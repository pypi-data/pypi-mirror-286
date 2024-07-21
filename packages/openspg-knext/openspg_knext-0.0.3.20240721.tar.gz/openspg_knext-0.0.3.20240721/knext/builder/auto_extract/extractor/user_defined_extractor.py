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
import traceback
from typing import List, Dict

from knext.builder.auto_extract.base import Extractor
from knext.builder.auto_extract.model.chunk import Chunk
from knext.builder.auto_extract.model.sub_graph import SubGraph
from knext.builder.auto_extract.splitter import (
    PDFDocSplitter,
    CSVDocSplitter,
    MarkDownDocSplitter,
)
from knext.builder.auto_extract.post_processor.post_processor import PostProcessor
from knext.builder.auto_extract.common.llm_client import LLMClient

# from knext.builder.auto_extract.llm_client import MayaHttpClient
# from nscommon.maya.maya_service.maya_service_client import MayaServiceClient
from knext.builder.auto_extract.common.prompt.user_defined_prompts import *
from knext.builder.operator import SPGRecord


def get_features(message: str, lora_name: str = None):
    feature = {
        "message": message,
        "max_input_len": 10240,
        "max_output_len": 10240,
        "lora_name": lora_name,
    }
    return [feature]


def extract_json_content(text):
    # 正则表达式匹配 json 和之间的内容
    pattern = r"```json\s+(.*?)\s+```"
    # 使用re.search找到第一个匹配的内容
    match = re.search(pattern, text, re.DOTALL)
    if match:
        # 返回匹配的内容
        return match.group(1)
    else:
        return text


class GovernmentAffairsExtractor(Extractor):
    def __init__(self, project_id, **kwargs):
        self.job_conf = kwargs.get(
            "job_conf",
            {
                "model_conf": {
                    "model_name": "deepseek",
                    "lora_name": None,
                    "use_pre": True,
                },
            },
        )
        self.llm_client = LLMClient.from_config_name(
            self.job_conf["model_conf"]["model_name"],
            use_pre=self.job_conf["model_conf"]["use_pre"],
        )
        self.entry_name_key = self.job_conf.get("entry_name_key", "GovernmentService")
        self.location_key = self.job_conf.get("location_key", "AdministrativeArea")
        self.apply_req_key = self.job_conf.get("apply_req_key", "applyCondition")
        self.file_req_key = self.job_conf.get("file_req_key", "files")

        self.apply_req_prompt = QwenApplyReqPrompt()
        self.file_req_prompt = QwenFileReqPrompt()

    def parse_location(self, location):
        locs = location.split("-")
        output = []
        for loc in locs:
            tmp = SPGRecord("AdministrativeArea")
            tmp.upsert_property("name", loc)
            output.append(tmp)
        if len(output) > 1:
            for i in range(1, len(output)):
                output[i].upsert_property(
                    "locateIn", output[i - 1].get_property("name")
                )
        return output, locs[-1]

    def invoke(self, chunks: List[Chunk]):
        spg_records = []
        apply_req_chunks = []
        file_req_chunks = []
        kept_props = {}
        for chunk in chunks:
            header = chunk.header
            if header == self.entry_name_key:
                kept_props["GovernmentService"] = chunk.content
            elif header == self.apply_req_key:
                apply_req_chunks.append(chunk)
            elif header in self.file_req_key:
                file_req_chunks.append(chunk)
            elif header == self.location_key:
                kept_props["AdministrativeArea"] = chunk.content
            else:
                kept_props[header] = chunk.content.strip()

        spg_records = []
        full_location = kept_props.pop("AdministrativeArea")
        locations, location_name = self.parse_location(full_location)
        spg_records += locations
        kept_props["location"] = location_name

        entry_name = kept_props.pop("GovernmentService")
        service_name = f"{location_name}-{entry_name}"
        kept_props["name"] = service_name

        service_record = SPGRecord("GovernmentService")
        service_record.upsert_properties(kept_props)
        spg_records.append(service_record)
        # extract apply_req

        for chunk in apply_req_chunks:
            try:
                chunk_record = SPGRecord("Chunk")
                index = chunk.name.split("#")[-1]
                chunk_name = f"{full_location}#{entry_name}受理条件原文#{index}"
                chunk_record.upsert_property("name", chunk_name)
                chunk_record.upsert_property("content", chunk.content)
                chunk_spg_records = []
                message = self.apply_req_prompt.build_prompt(chunk.content)
                result = self.llm_client.remote_inference(message)
                tmp = {
                    "GovernmentService": service_name,
                    "AdministrativeArea": location_name,
                    "content": chunk.content,
                    "result": [result],
                }
                chunk_spg_records += self.apply_req_prompt.parse_response(tmp)
                for spg_record in chunk_spg_records:
                    spg_record.upsert_property("chunk", chunk_name)
                chunk_spg_records.append(chunk_record)
                spg_records += chunk_spg_records
            except Exception as e:
                print(f"failed to extract chunk {chunk}, info: {e}")
                traceback.print_exc()
        # extract file_req
        for chunk in file_req_chunks:
            try:
                chunk_record = SPGRecord("Chunk")
                index = chunk.name.split("#")[-1]
                chunk_name = f"{full_location}#{entry_name}办理所需条件原文#{index}"
                chunk_record.upsert_property("name", chunk_name)
                chunk_record.upsert_property("content", chunk.content)
                chunk_spg_records = []

                message = self.file_req_prompt.build_prompt(chunk.content)
                result = self.llm_client.remote_inference(message)
                tmp = {
                    "GovernmentService": service_name,
                    "AdministrativeArea": location_name,
                    "content": chunk.content,
                    "result": [result],
                }
                chunk_spg_records += self.file_req_prompt.parse_response(tmp)
                for spg_record in chunk_spg_records:
                    spg_record.upsert_property("chunk", chunk_name)
                chunk_spg_records.append(chunk_record)

                spg_records += chunk_spg_records
            except Exception as e:
                print(f"failed to extract chunk {chunk}, info: {e}")
                traceback.print_exc()
        for spg_record in spg_records:
            spg_record._spg_type_name = f"GOV.{spg_record._spg_type_name}"
        return spg_records


class UserManualExtractor(Extractor):
    def __init__(self, project_id, **kwargs):
        self.job_conf = kwargs.get(
            "job_conf",
            {
                "model_conf": {
                    "model_name": "qwen",
                    "lora_name": None,
                    "use_pre": False,
                },
                "manual_name": "奔驰汽车",
            },
        )
        self.llm_client = LLMClient.from_config_name(
            self.job_conf["model_conf"]["model_name"],
            use_pre=self.job_conf["model_conf"]["use_pre"],
        )
        manual_name = self.job_conf.get("manual_name", "")

        self.prompts = {
            "qwen_manual_qe": QwenUserManualQuestionExtractPrompt(manual_name),
            "qwen_manual_ee": QwenUserManualEntityExtractPrompt(manual_name),
            "qwen_manual_eae": QwenUserManualEntityAttributesExtractPrompt(manual_name),
            "qwen_manual_ese": QwenUserManualEntityStateExtractPrompt(manual_name),
            "qwen_manual_eve": QwenUserManualEventExtractPrompt(manual_name),
            "qwen_manual_ere": QwenUserManualEntityRelationExtractPrompt(manual_name),
        }

    def invoke(self, chunks: List[Chunk]):
        """
        - extract all entities
        - extract all entities properties
        - extract all entities states
        - extract all entity relations
        - extract all affairs
        """
        spg_records = []
        for chunk in chunks:
            chunk_record = SPGRecord("Chunk")
            chunk_record.upsert_property("name", chunk.id)
            chunk_record.upsert_property("info", chunk.name)
            chunk_record.upsert_property("content", chunk.content)
            chunk_spg_records = [chunk_record]
            content = chunk.content
            # entitiy extract
            prompt_op = self.prompts["qwen_manual_ee"]

            msg = {
                "input": content,
                "entity_types": {
                    "设备": "设备通常指的是单个的、独立的物理或电子组件",
                    "系统": "完成某个功能的组件集合",
                    "耗材": "日常使用过程中会被消耗、磨损或用尽的物品",
                },
            }
            prompt = prompt_op.build_prompt(
                {
                    "input": content,
                    "entity_types": {
                        "设备": "设备通常指的是单个的、独立的物理或电子组件",
                        "系统": "完成某个功能的组件集合",
                        "耗材": "日常使用过程中会被消耗、磨损或用尽的物品",
                    },
                }
            )

            print(f"entity extract prompt:\n {prompt}")

            llm_output = self.llm_client.remote_inference(prompt)
            print(f"entity extract output:\n {llm_output}")
            entities = prompt_op.parse_result(
                {"result": [llm_output], "content": content}
            )
            if len(entities) == 0:
                print(f"no entity found, skip extraction...")
                continue
            chunk_spg_records += prompt_op.result_to_spgrecord(entities)

            # remove entity description in the following extraction
            for item in entities:
                item.pop("简介", None)

            # entity properties extract
            # prompt_op = self.prompts["qwen_manual_eae"]
            # prompt = prompt_op.build_prompt({"input": content, "entities": entities})
            # llm_output = self.llm_client.remote_inference(prompt)
            # print(f"entity properties extract output:\n {llm_output}")
            # entitiy_attrs = prompt_op.parse_result(
            #     {"result": [llm_output], "content": content}
            # )
            # chunk_spg_records += prompt_op.result_to_spgrecord(entitiy_attrs)

            # entity state extrat
            # prompt_op = self.prompts["qwen_manual_ese"]
            # prompt = prompt_op.build_prompt({"input": content, "entities": entities})

            # llm_output = self.llm_client.remote_inference(prompt)
            # print(f"entity state extract output:\n {llm_output}")

            # entitiy_attrs = prompt_op.parse_result(
            #     {"result": [llm_output], "content": content}
            # )
            # chunk_spg_records += prompt_op.result_to_spgrecord(entitiy_attrs)

            # entity relation extract
            prompt_op = self.prompts["qwen_manual_ere"]

            prompt = prompt_op.build_prompt({"input": content, "entities": entities})
            llm_output = self.llm_client.remote_inference(prompt)
            print(f"entity relation extract output:\n {llm_output}")
            entitiy_attrs = prompt_op.parse_result(
                {"result": [llm_output], "content": content}
            )
            chunk_spg_records += prompt_op.result_to_spgrecord(entitiy_attrs)

            # event extract
            prompt_op = self.prompts["qwen_manual_eve"]
            prompt = prompt_op.build_prompt({"input": content, "entities": entities})
            llm_output = self.llm_client.remote_inference(prompt)
            print(f"event extract output:\n {llm_output}")
            entitiy_attrs = prompt_op.parse_result(
                {"result": [llm_output], "content": content}
            )
            chunk_spg_records += prompt_op.result_to_spgrecord(entitiy_attrs)
            for spg_record in chunk_spg_records:
                spg_record.upsert_property("chunk_id", chunk.id)
            spg_records += chunk_spg_records
        return spg_records


if __name__ == "__main__":
    # gonvernment
    import pandas as pd

    file_name = "../data/GovernmentServiceForm.csv"

    extractor = GovernmentAffairsExtractor(0)

    splitter = CSVDocSplitter()
    data = splitter.invoke(file_name, "")
    spg_records = []

    for i in range(len(data)):
        print(f"start to extract {i}th data")
        extracted = extractor.invoke(data[i])
        spg_records += extracted
        print(f"Done extract {i} th data:\n {extracted}")

    print(f"there are {len(spg_records)} records extracted")
    print(spg_records)
    with open("zhengwu.json", "w") as writer:
        tmp = [x.to_dict() for x in spg_records]
        writer.write(json.dumps(tmp, ensure_ascii=False, indent=4))

    # manual
    file_name = "../data/benzi-key.pdf"

    splitter = PDFDocSplitter()
    cutted = splitter.invoke(
        file_name=file_name,
        user_query="",
    )

    extractor = UserManualExtractor(0)
    spg_records = []
    for i in cutted:
        spg_records += extractor.invoke(i)

    print(f"there are {len(spg_records)} records extracted")
    print(spg_records)
    with open("manual.json", "w") as writer:
        tmp = [x.to_dict() for x in spg_records]
        writer.write(json.dumps(tmp, ensure_ascii=False, indent=4))
