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
from typing import List

from knext.builder.auto_extract.base import PostProcessor

from knext.builder.operator import SPGRecord
from knext.builder.auto_extract.model.sub_graph import SubGraph

PWD = os.path.dirname(__file__)


class MockPostProcessor(PostProcessor):

    def __init__(self, project_id: int, **kwargs):
        super().__init__(project_id=project_id, **kwargs)


    def invoke(self, spg_records: List[SPGRecord]) -> SubGraph:
        print(spg_records)
        for record in spg_records:
            print(record)

        cutted = {'resultNodes': [{'id': 0, 'name': '1979年1月18日', 'label': 'Demo2.Time', 'properties': {'name': '1979年1月18日'}}, {'id': 1, 'name': '台湾省新北市', 'label': 'Demo2.Place', 'properties': {'name': '台湾省新北市'}}, {'id': 8, 'name': '淡江中学', 'label': 'Demo2.Organization', 'properties': {'name': '淡江中学'}}, {'id': 9, 'name': '周杰伦', 'label': 'Demo2.Person', 'properties': {'name': '周杰伦', 'nativePlace': '福建省泉州市永春县,福建省永春县', 'major': '编剧,导演,演员,音乐人,华语流行乐男歌手', 'basicInfo': '{"学校": "淡江山叶幼儿音乐班", "擅长": "钢琴", "家人": "母亲叶惠美", "职位": "在一家餐馆打工"}'}}], 'resultEdges': [{'id': 140212634735744, 'from': 9, 'to': 8, 'fromType': 'Demo2.Person', 'toType': 'Demo2.Organization', 'label': 'graduatedSchool', 'properties': {}}, {'id': 140212634741264, 'from': 9, 'to': 0, 'fromType': 'Demo2.Person', 'toType': 'Demo2.Time', 'label': 'birthDate', 'properties': {}}, {'id': 140212634740160, 'from': 9, 'to': 1, 'fromType': 'Demo2.Person', 'toType': 'Demo2.Place', 'label': 'birthPlace', 'properties': {}}]}
        return cutted