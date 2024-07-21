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
from typing import List, Dict
from knext.schema.model.schema_helper import SPGTypeName
from knext.builder.operator.spg_record import SPGRecord
from knext.builder.operator.builtin.auto_prompt import AutoPrompt


class ConstraintPrompt(AutoPrompt):
    template_zh: str = ""
    template_en: str = ""

    def __init__(self, **kwargs):
        types_list = kwargs.get("types_list", [])
        language = kwargs.get("language", "zh")
        with_description = kwargs.get("with_description", False)
        split_num = kwargs.get("split_num", 4)
        project_id = kwargs.get("project_id", None)
        super().__init__(types_list, project_id=project_id)
        if language == "zh":
            self.template = self.template_zh
        else:
            self.template = self.template_en
        self.with_description = with_description
        self.split_num = split_num

        self._init_render_variables()
        self._render()

        self.params = kwargs

    def build_prompt(self, variables: Dict[str, str]) -> List[str]:
        instructions = []
        for schema in self.schema_list:
            instructions.append(
                json.dumps(
                    {
                        "instruction": self.template,
                        "constraint": schema,
                        "input": variables.get("input"),
                    },
                    ensure_ascii=False,
                )
            )
        return instructions

    def parse_response(self, response: str) -> List[SPGRecord]:
        raise NotImplementedError

    def _render(self):
        raise NotImplementedError


class ConstraintKGPrompt(ConstraintPrompt):
    template_zh: str = """你是一个图谱知识抽取的专家, 基于constraint 定义的schema，从input 中抽取出所有的实体及其属性，input中未明确提及的属性返回NAN，以标准json 格式输出，结果返回list"""

    def __init__(
            self,
            entity_types: List[SPGTypeName],
            language: str = "zh",
            split_num: int = 4,
            project_id: int = None
    ):
        super().__init__(
            types_list=entity_types,
            language=language,
            split_num=split_num,
            project_id=project_id
        )

    def parse_response(self, response: str, **kwargs) -> List[SPGRecord]:
        types = kwargs.get("types", [])
        idx = kwargs.get("idx", 0)
        type_en = types[idx]
        if isinstance(response, str):
            try:
                response = json.loads(response)
            except json.decoder.JSONDecodeError:
                print("ConstraintKGPrompt response JSONDecodeError error.")
                return []
        if type(response) != list:
            print("ConstraintKGPrompt response type error.")
            return []

        standard_response = []
        spg_records = []
        object_spg_records = []
        for type_value in response:
            if isinstance(type_value, dict) and len(type_value) == 1 and type_en in type_value:
                if "properties" in type_value[type_en]:
                    properties = type_value[type_en]["properties"]
                else:
                    properties = type_value[type_en]
            else:
                properties = type_value
            standard_properties = {}
            for prop_name, prop_value in properties.items():
                if not prop_value or prop_value == "NAN":
                    continue
                if isinstance(prop_value, list):
                    prop_value = ','.join(prop_value)
                prop_value = prop_value.replace("《", "").replace("》", "").replace("'", "`")
                standard_properties[prop_name] = prop_value
            standard_response.append(standard_properties)
        for type_value in standard_response:
            for attr_en, attr_value in type_value.items():
                if attr_en in self.property_info_en[type_en]:
                    _, _, object_type = self.property_info_en[type_en].get(attr_en)
                    if object_type not in ["Text", "Integer", "Float"]:
                        if isinstance(attr_value, list):
                            attr_value = ','.join(attr_value)
                        attr_value = re.split("[,，、;；]", attr_value)
                        for _value in attr_value:
                            object_spg_records.append(SPGRecord(object_type).upsert_properties({"name": _value}))
                        type_value[attr_en] = ",".join(attr_value)
            _dict = {"spgTypeName": type_en, "properties": type_value}
            spg_record = SPGRecord.from_dict(_dict)
            spg_records.append(spg_record)
        return spg_records + object_spg_records

    def _render(self):
        spo_list = []
        for spg_type in self.spg_types:
            constraint = {"desc": (f"{spg_type.name_zh}" if not spg_type.desc else f"{spg_type.name_zh}，{spg_type.desc}")}
            properties = {}
            properties.update({v.name : (f"{v.name_zh}" if not v.desc else f"{v.name_zh}，{v.desc}") for k, v in spg_type.properties.items() if k not in ["id", "description", "stdId", "basicInfo", "otherInfo"]})
            properties.update({f"{v.name}#{v.object_type_name}" : (f"{v.name_zh}，类型是{v.object_type_name_zh}" if not v.desc else f"{v.name_zh}，{v.desc}，类型是{v.object_type_name_zh}") for k, v in spg_type.relations.items() if not v.is_dynamic and k not in ["isA"]})
            constraint.update({"properties": properties})
            spo_list.append({spg_type.name: constraint})

        self.schema_list = spo_list


class ConstraintEEPrompt(ConstraintPrompt):
    template_zh: str = "你是一个图谱知识抽取的专家, 基于constraint 定义的schema，从input 中抽取出所有的事件及其属性，input中未明确提及的属性返回NAN，以标准json 格式输出，结果返回list"

    def __init__(
            self,
            event_types: List[SPGTypeName],
            language: str = "zh",
            with_description: bool = False,
            split_num: int = 4,
            project_id: int = None
    ):
        super().__init__(
            types_list=event_types,
            language=language,
            with_description=with_description,
            split_num=split_num,
            project_id=project_id
        )

    def parse_response(self, response: str, **kwargs) -> List[SPGRecord]:
        types = kwargs.get("types", [])
        idx = kwargs.get("idx", 0)
        type_en = types[idx]

        if isinstance(response, str):
            try:
                response = json.loads(response)
            except json.decoder.JSONDecodeError:
                print("ConstraintEEPrompt response JSONDecodeError error.")
                return []
        if type(response) != list:
            print("ConstraintEEPrompt response type error.")
            return []

        standard_response = []
        spg_records = []
        object_spg_records = []
        for type_value in response:
            if isinstance(type_value, dict) and len(type_value) == 1 and type_en in type_value:
                if "properties" in type_value[type_en]:
                    properties = type_value[type_en]["properties"]
                else:
                    properties = type_value[type_en]
            else:
                properties = type_value
            standard_properties = {}
            for prop_name, prop_value in properties.items():
                if not prop_value or prop_value == "NAN":
                    continue
                if isinstance(prop_value, list):
                    prop_value = ','.join(prop_value)
                prop_value = prop_value.replace("《", "").replace("》", "").replace("'", "`")
                standard_properties[prop_name] = prop_value
            standard_response.append(standard_properties)
        for type_value in standard_response:
            for attr_en, attr_value in type_value.items():
                if attr_en in self.property_info_en[type_en]:
                    _, _, object_type = self.property_info_en[type_en].get(attr_en)
                    if object_type not in ["Text", "Integer", "Float"]:
                        if isinstance(attr_value, list):
                            attr_value = ','.join(attr_value)
                        attr_value = re.split("[,，、;；]", attr_value)
                        for _value in attr_value:
                            object_spg_records.append(SPGRecord(object_type).upsert_properties({"name": _value}))
                        type_value[attr_en] = ",".join(attr_value)
            type_zh, _ = self.spg_type_schema_info_en[type_en]
            sub_type_zh = type_value.get('eventType', "")
            event_summary = type_value.get('eventSummary', "")
            type_value["name"] = f"{type_zh}-{sub_type_zh}-{event_summary}"
            _dict = {"spgTypeName": type_en, "properties": type_value}
            spg_record = SPGRecord.from_dict(_dict)
            spg_records.append(spg_record)
        return spg_records + object_spg_records

    def _render(self):
        event_list = []
        for spg_type in self.spg_types:
            constraint = {
                "desc": (f"{spg_type.name_zh}" if not spg_type.desc else f"{spg_type.name_zh}，{spg_type.desc}")}
            properties = {}
            properties.update({v.name: (f"{v.name_zh}" if not v.desc else f"{v.name_zh}，{v.desc}") for k, v in
                               spg_type.properties.items() if k not in ["id", "description", "name", "eventTime"]})
            properties.update({f"{v.name}#{v.object_type_name}": (
                f"{v.name_zh}，类型是{v.object_type_name_zh}" if not v.desc else f"{v.name_zh}，{v.desc}，类型是{v.object_type_name_zh}")
                               for k, v in spg_type.relations.items() if
                               not v.is_dynamic})
            constraint.update({"properties": properties})
            event_list.append({spg_type.name: constraint})
        self.schema_list = event_list


if __name__ == '__main__':
    op1 = ConstraintKGPrompt(["PRE1.Person"], project_id=7)
    print(op1.parse_response("", types=["PRE1.Person"]))
    op2 = ConstraintEEPrompt(["PRE1.PersonExperienceEvent"], project_id=7)
    print(op2.parse_response("", types=["PRE1.PersonExperienceEvent"]))
