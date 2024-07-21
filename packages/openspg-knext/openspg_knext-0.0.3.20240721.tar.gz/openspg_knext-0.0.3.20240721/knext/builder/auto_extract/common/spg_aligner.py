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
import os
import csv
from typing import List, Dict, Any, Union

from knext.builder.auto_extract.common.llm_client import LLMClient
from knext.builder.operator import PromptOp, SPGRecord
from knext.schema.client import SchemaClient

PWD = os.path.dirname(__file__)


class PropertyAlignPrompt(PromptOp):
    template = """
在以下所有属性中，找出和[${source_schema}]意思最相近的一个，并以json格式返回，返回格式：{"norm_prop":}。若不存在返回{"norm_prop": "NAN"}。
${target_schema}
    """

    def build_prompt(self, variables: Dict[str, Any]) -> str:
        return self.template.replace("${source_schema}", str(variables.get("source_schema"))).replace("${target_schema", str(variables.get("target_schema")))

    def parse_response(self, response: str, **kwargs):
        if isinstance(response, str):
            response = json.loads(response)
        return response.get("norm_prop", "NAN")


class TypeAlignPrompt(PromptOp):
    template = """
在以下所有实体类型中，找出[${source_schema}]最可能属于哪一个实体类型的子类型，并以json格式返回，返回格式：{"norm_type":}。若不存在返回{"norm_type": "NAN"}。
${target_schema}
    """

    def build_prompt(self, variables: Dict[str, Any]) -> str:
        return self.template.replace("${source_schema}", str(variables.get("source_schema"))).replace("${target_schema", str(variables.get("target_schema")))

    def parse_response(self, response: str, **kwargs):
        if isinstance(response, str):
            response = json.loads(response)
        return response.get("norm_type", "NAN")


class SPGAligner:

    def __init__(self, project_id: int):
        self.project_id = project_id
        self.entity_is = self._parse_semantic_graph_to_entity_is()
        self.entity_has = self._parse_semantic_graph_to_entity_has()
        self.property_has = self._parse_semantic_graph_to_property_has()
        self._init_render_variables()
        self.property_align_prompt = PropertyAlignPrompt()
        self.type_align_prompt = TypeAlignPrompt()
        self.llm = LLMClient.from_config_name("deepseek")
        self.root_entities = [k for k, v in self.entity_is.items() if len(v) == 1]

    def _init_render_variables(self):
        schema_session = SchemaClient(project_id=self.project_id).create_session()
        self.spg_types = schema_session.spg_types.values()
        self.property_info_zh = {}
        self.property_info_en = {}
        self.relation_info_zh = {}
        self.relation_info_en = {}
        self.spg_type_schema_info_en = {
            "Text": ("文本", None),
            "Integer": ("整型", None),
            "Float": ("浮点型", None),
        }
        self.spg_type_schema_info_zh = {
            "文本": ("Text", None),
            "整型": ("Integer", None),
            "浮点型": ("Float", None),
        }
        for spg_type in self.spg_types:
            self.property_info_zh[spg_type.name_zh] = {}
            self.relation_info_zh[spg_type.name_zh] = {}
            self.property_info_en[spg_type.name] = {}
            self.relation_info_en[spg_type.name] = {}
            for _rel in spg_type.relations.values():
                if _rel.is_dynamic:
                    continue
                self.relation_info_zh[spg_type.name_zh][_rel.name_zh] = (
                    _rel.name,
                    _rel.desc,
                    _rel.object_type_name,
                )
                self.relation_info_en[spg_type.name][_rel.name] = (
                    _rel.name_zh,
                    _rel.desc,
                    _rel.object_type_name,
                )
            for _prop in spg_type.properties.values():
                self.property_info_zh[spg_type.name_zh][_prop.name_zh] = (
                    _prop.name,
                    _prop.desc,
                    _prop.object_type_name,
                )
                self.property_info_en[spg_type.name][_prop.name] = (
                    _prop.name_zh,
                    _prop.desc,
                    _prop.object_type_name,
                )
        for _type in self.spg_types:
            self.spg_type_schema_info_zh[_type.name_zh] = (_type.name, _type.desc)
            self.spg_type_schema_info_en[_type.name] = (_type.name_zh, _type.desc)

    def _parse_semantic_graph_to_entity_is(self):
        data_dict = {}
        with open(os.path.join(PWD, "../semantic_graph/semantic_graph_files_concept_tree.csv"), newline='', encoding='utf-8') as csvfile:
            csvreader = csv.reader(csvfile)
            next(csvreader)
            for row in csvreader:
                key = row[2]
                value = row[0].split('-')
                data_dict[key] = value
        return data_dict

    def _parse_semantic_graph_to_property_has(self):
        data_dict = {}
        with open(os.path.join(PWD, "../semantic_graph/semantic_graph_files_has_property_rel.csv"), newline='', encoding='utf-8') as csvfile:
            csvreader = csv.reader(csvfile)
            next(csvreader)
            for row in csvreader:
                key = row[0]
                value = row[2]
                if key not in data_dict:
                    data_dict[key] = [value]
                else:
                    data_dict[key].append(value)
        return data_dict

    def _parse_semantic_graph_to_entity_has(self):
        data_dict = {}
        with open(os.path.join(PWD, "../semantic_graph/semantic_graph_files_has_concept_rel.csv"), newline='', encoding='utf-8') as csvfile:
            csvreader = csv.reader(csvfile)
            next(csvreader)
            for row in csvreader:
                key = row[0]
                value = row[2]
                if key not in data_dict:
                    data_dict[key] = [value]
                else:
                    data_dict[key].append(value)
        return data_dict

    def property_zh_to_en(self, spg_type_name_zh, property_name_zh):
        name_en, _, _ = self.property_info_zh[spg_type_name_zh][property_name_zh]
        return name_en

    def property_en_to_zh(self, spg_type_name_en, property_name_en):
        name_zh, _, _ = self.property_info_en[spg_type_name_en][property_name_en]
        return name_zh

    def type_zh_to_en(self, spg_type_name_zh):
        if spg_type_name_zh not in self.spg_type_schema_info_zh or spg_type_name_zh == "NAN":
            return "Text"
        name_en, _ = self.spg_type_schema_info_zh[spg_type_name_zh]
        return name_en

    def type_en_to_zh(self, spg_type_name_en):
        if spg_type_name_en not in self.spg_type_schema_info_en or spg_type_name_en == "NAN":
            return "文本"
        name_zh, _, _ = self.spg_type_schema_info_en[spg_type_name_en]
        return name_zh

    def spo_align_by_service(self, spo_list):
        entities = {}
        for spo in spo_list:
            s, s_type, p, o, o_type = spo.get("subject", ""), spo.get("subject_type", ""), spo.get("predicate",
                                                                                                   ""), spo.get(
                "object", ""), spo.get("object_type", "")
            key = f"{s}#{s_type}"
            if key not in entities:
                entities[key] = SPGRecord(s_type).upsert_property("name", s)
            else:
                entities[key].append_property(f"{p}#{o_type}", o)
        return entities.values()

    def parse_to_spo_list(self, spg_records: List[SPGRecord]):
        spo_list = []
        for spg_record in spg_records:
            s = spg_record.get_property("name")
            spg_record.remove_property("name")
            s_type = spg_record.spg_type_name
            print(spg_record)
            for rel_name, rel_value in spg_record.relations.items():
                p = rel_name.split('#')[0]
                o_type = rel_name.split('#')[1]
                o = rel_value
                spo_list.append({
                    "subject": s,
                    "subject_type": s_type,
                    "predicate": p,
                    "object": o,
                    "object_type": o_type,
                })
            for prop_name, prop_value in spg_record.properties.items():
                p = prop_name.split('#')[0]
                o_type = prop_name.split('#')[1]
                o = prop_value
                spo_list.append({
                    "subject": s,
                    "subject_type": s_type,
                    "predicate": p,
                    "object": o,
                    "object_type": o_type,
                })

        return spo_list

    def spo_align(self, spo_list: Union[List[Dict], str]) -> List[list]:
        _cache = {}
        spo_aligned_list = []
        if isinstance(spo_list, str):
            spo_list = json.loads(spo_list)
        for spo in spo_list:
            s, s_type, p, o, o_type = spo.get("subject", ""), spo.get("subject_type", ""), spo.get("predicate", ""), spo.get("object", ""), spo.get("object_type", "")
            # 第一步，对齐s_type/o_type。先从语义图中找，不存在则调用模型进行分类并补充至语义图中。
            s_top_types, o_top_types = self.entity_is.get(s_type, []), self.entity_is.get(o_type, [])
            if not s_top_types:
                if s_type in _cache:
                    aligned_s = _cache[s_type]
                else:
                    aligned_s = self.type_align(s_type, self.root_entities)
                if not aligned_s or aligned_s == "NAN":
                    _cache[s_type] = "NAN"
                    continue
                s_top_types = [aligned_s, s_type]
                print(s_top_types)
                self.entity_is[s_type] = s_top_types
            if not o_top_types:
                if o_type in _cache:
                    aligned_o = _cache[o_type]
                else:
                    aligned_o = self.type_align(o_type, self.root_entities)
                if not aligned_o or aligned_o == "NAN":
                    _cache[o_type] = "NAN"
                o_top_types = [aligned_o, o_type]
                self.entity_is[o_type] = o_top_types
            print(s_type, "---[type_aligner]--->", self.entity_is[s_type][0])
            print(o_type, "---[type_aligner]--->", self.entity_is[o_type][0])
            _cache[s_type] = self.entity_is[s_type][0]
            _cache[o_type] = self.entity_is[o_type][0]
            # 第二步，对齐predicate。先从语义图中找到s_type和其到根类型上的所有属性，若p不属于其中，则调用模型进行分类并补充至语义图中。
            attributes = []
            for _type in s_top_types:
                attributes.extend(self.entity_has.get(_type, []))
                attributes.extend(self.property_has.get(_type, []))
            attributes = list(set(attributes))
            if p not in attributes:
                if f"{s_type}#{p}" in _cache:
                    aligned_p = _cache[f"{s_type}#{p}"]
                else:
                    aligned_p = self.property_align(p, attributes)
                    if not aligned_p or aligned_p == "NAN":
                        _cache[f"{s_type}#{p}"] = "NAN"
                        aligned_p = p
                    if s_type not in self.property_has:
                        self.property_has[s_type] = [aligned_p]
                    else:
                        self.property_has[s_type].append(aligned_p)
            else:
                aligned_p = p
            print(p, "---[property_aligner]--->", aligned_p)
            _cache[f"{s_type}#{p}"] = aligned_p
            print([s, s_top_types[0], aligned_p, o, o_top_types[0]])
            spo_aligned_list.append([s, s_top_types[0], aligned_p, o, o_top_types[0]])

        return spo_aligned_list

    def type_align(self, type_name, candidate):
        """
        根据开放抽取出的s/o的type，标准化为顶点类型，例如导演->人物
        """

        source_schema = type_name
        target_schema = candidate

        aligned_type = self.llm.invoke({"source_schema": source_schema, "target_schema": target_schema},
                                                 self.type_align_prompt)

        if isinstance(aligned_type, list) and len(aligned_type) > 0:
            return aligned_type[0]
        else:
            return aligned_type

    def property_align(self, property_name, candidate):
        """
        根据开放抽取出的s_type和p，在s_type下的所有属性中，找到最相似的属性，并将p标准化为该属性。
        理想状态是通过语义图的同义词能力，当前先调用模型进行分类。
        """
        source_schema = property_name
        target_schema = candidate

        aligned_property = self.llm.invoke({"source_schema": source_schema, "target_schema": target_schema}, self.property_align_prompt)

        if isinstance(aligned_property, list) and len(aligned_property) > 0:
            return aligned_property[0]
        else:
            return aligned_property

    def invoke(self):
        pass


if __name__ == '__main__':
    op = SPGAligner(project_id=3)
    spo_list = op.parse_to_spo_list("")
    print(spo_list)
    print(op.spo_align(spo_list))
