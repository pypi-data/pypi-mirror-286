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
from typing import List, Sequence

from knext.builder.auto_extract.base import PostProcessor
from knext.builder.operator import SPGRecord
from knext.builder.auto_extract.model.sub_graph import SubGraph
from knext.common.base.runnable import Input, Output
from knext.schema.client import SchemaClient
from knext.schema.model.base import ConstraintTypeEnum


class DefaultPostProcessor(PostProcessor):

    def __init__(self, project_id: int, **kwargs):
        super().__init__(project_id=project_id, **kwargs)
        self.spg_types = SchemaClient(project_id=project_id).create_session().spg_types

    def merge(self, spg_records: List[SPGRecord]):
        merged_spg_records = {}
        for record in spg_records:
            key = f"{record.spg_type_name}#{record.get_property('name', '')}"
            if key not in merged_spg_records:
                merged_spg_records[key] = record
            else:
                old_record = merged_spg_records[key]
                for prop_name, prop_value in record.properties.items():
                    if prop_name not in old_record.properties:
                        old_record.properties[prop_name] = prop_value
                    else:
                        prop = self.spg_types.get(record.spg_type_name).properties.get(prop_name)
                        if not prop:
                            continue
                        if prop.object_type_name not in ['Text', "Integer", "Float"] or prop.constraint.get(ConstraintTypeEnum.MultiValue):
                            old_value = old_record.properties.get(prop_name)
                            if not prop_value:
                                prop_value = ""
                            prop_value_list = (prop_value + ',' + old_value if old_value else prop_value).split(',')
                            old_record.properties[prop_name] = ','.join(list(set(prop_value_list)))
                        elif prop_name in ["basicInfo", "otherInfo"]:
                            old_infos = json.loads(old_record.properties.get(prop_name, "{}"))
                            infos = json.loads(record.properties.get(prop_name, "{}"))
                            old_infos.update(infos)
                            old_record.properties[prop_name] = json.dumps(old_infos, ensure_ascii=False)
                        else:
                            old_record.properties[prop_name] = prop_value

        return list(merged_spg_records.values())

    def filter(self, spg_records: List[SPGRecord]):
        filtered_spg_records = []
        for record in spg_records:
            if not record.get_property("name") or record.get_property("name") == "NAN":
                continue
            if record.spg_type_name in ["Text", "Integer", "Float"]:
                continue
            filtered_spg_records.append(record)

        filtered_spg_records = list(set(filtered_spg_records))
        return filtered_spg_records

    def link(self):
        pass

    def invoke(self, spg_records: List[SPGRecord]) -> List[SubGraph]:
        spg_records = self.filter(spg_records)
        spg_records = self.merge(spg_records)
        print(spg_records)
        subgraph = SubGraph.from_spg_record(self.spg_types, spg_records)
        return subgraph

    def batch(self, inputs: List[Input]) -> Sequence[Output]:
        pass

if __name__ == '__main__':
    op = DefaultPostProcessor(project_id=3)
    spg_records = [{'properties': {'name': '浙江省'},
 'relations': {},
 'spgTypeName': 'GOV.AdministrativeArea'}, {'properties': {'locateIn': '浙江省', 'name': '宁波市'},
 'relations': {},
 'spgTypeName': 'GOV.AdministrativeArea'}, {'properties': {'locateIn': '宁波市', 'name': '宁海县'},
 'relations': {},
 'spgTypeName': 'GOV.AdministrativeArea'}, {'properties': {'chunk': '03155c46c067cf1199712ca81f616222fceec3b189e5b524e8f951ae6bb388c5,725c77cdabef661c24e8a80debdd42d1c7f9a5e9fd13e09ecba8f52fcdadafe9',
                'completionTime': '无',
                'conditions': '公章刻制业务受理条件-设有单独的公章刻制间,公章刻制业务受理条件-设有存放成品公章的保管库房或保险柜,公章刻制业务受理条件-安装、配备与印章治安管理信息系统要求相适应的采集、上传等设施设备',
                'cost': '无',
                'location': '宁海县',
                'name': '宁海县-公章刻制业特种行业许可证核发（一般程序）',
                'requiredMaterial': '营业执照,设有单独的公章刻制间以及存放成品公章的保管库房或者保险柜的说明材料,安装、配备与印章治安管理信息系统要求相适应的采集、上传等设施设备的说明材料',
                'subService': '[]',
                'telephone': '无',
                'workHours': '法定工作日，夏令时：上午8:00~11:30 '
                             '下午14:00~17:00；冬令时：上午8:00~11:30 下午13:30~16:30。'},
 'relations': {},
 'spgTypeName': 'GOV.GovernmentService'}, {'properties': {'chunk': '725c77cdabef661c24e8a80debdd42d1c7f9a5e9fd13e09ecba8f52fcdadafe9',
                'constraint': '必须满足',
                'name': '公章刻制业务受理条件-设有单独的公章刻制间',
                'value': '是'},
 'relations': {},
 'spgTypeName': 'GOV.ApplyCondition'}, {'properties': {'chunk': '725c77cdabef661c24e8a80debdd42d1c7f9a5e9fd13e09ecba8f52fcdadafe9',
                'constraint': '必须满足',
                'name': '公章刻制业务受理条件-设有存放成品公章的保管库房或保险柜',
                'value': '是'},
 'relations': {},
 'spgTypeName': 'GOV.ApplyCondition'}, {'properties': {'chunk': '725c77cdabef661c24e8a80debdd42d1c7f9a5e9fd13e09ecba8f52fcdadafe9',
                'constraint': '必须满足',
                'name': '公章刻制业务受理条件-安装、配备与印章治安管理信息系统要求相适应的采集、上传等设施设备',
                'value': '是'},
 'relations': {},
 'spgTypeName': 'GOV.ApplyCondition'}, {'properties': {'content': '（一）设有单独的公章刻制间以及存放成品公章的保管库房或者保险柜；（二）安装、配备与印章治安管理信息系统要求相适应的采集、上传等设施设备。',
                'info': 'applyCondition#0',
                'name': '725c77cdabef661c24e8a80debdd42d1c7f9a5e9fd13e09ecba8f52fcdadafe9'},
 'relations': {},
 'spgTypeName': 'GOV.Chunk'}, {'properties': {'chunk': '03155c46c067cf1199712ca81f616222fceec3b189e5b524e8f951ae6bb388c5',
                'name': '营业执照',
                'numberOfCopies': '0',
                'prerequisite': '宁海县-公章刻制业特种行业许可证核发（一般程序）',
                'requires': '无'},
 'relations': {},
 'spgTypeName': 'GOV.Material'}, {'properties': {'chunk': '03155c46c067cf1199712ca81f616222fceec3b189e5b524e8f951ae6bb388c5',
                'name': '设有单独的公章刻制间以及存放成品公章的保管库房或者保险柜的说明材料',
                'numberOfCopies': '0',
                'prerequisite': '宁海县-公章刻制业特种行业许可证核发（一般程序）',
                'requires': '无'},
 'relations': {},
 'spgTypeName': 'GOV.Material'}, {'properties': {'chunk': '03155c46c067cf1199712ca81f616222fceec3b189e5b524e8f951ae6bb388c5',
                'name': '安装、配备与印章治安管理信息系统要求相适应的采集、上传等设施设备的说明材料',
                'numberOfCopies': '0',
                'prerequisite': '宁海县-公章刻制业特种行业许可证核发（一般程序）',
                'requires': '无'},
 'relations': {},
 'spgTypeName': 'GOV.Material'}, {'properties': {'content': '营业执照|_|设有单独的公章刻制间以及存放成品公章的保管库房或者保险柜的说明材料|_|安装、配备与印章治安管理信息系统要求相适应的采集、上传等设施设备的说明材料',
                'info': 'files#0',
                'name': '03155c46c067cf1199712ca81f616222fceec3b189e5b524e8f951ae6bb388c5'},
 'relations': {},
 'spgTypeName': 'GOV.Chunk'}]
    print(op._handle(spg_records))
