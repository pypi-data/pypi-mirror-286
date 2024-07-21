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

from typing import Sequence

from knext.builder.auto_extract.base import Extractor
from knext.common.base.runnable import Input, Output
from typing import List

from knext.builder.auto_extract.model.chunk import Chunk

PWD = os.path.dirname(__file__)


class MockExtractor(Extractor):
    project_id: int
    models: List[str]

    def __init__(self, project_id: int, **kwargs):
        super().__init__(project_id=project_id, **kwargs)

    def invoke(self, input: Input) -> Sequence[Output]:

        input = Chunk.from_dict(input)
        print(input.content)

        cutted = []
        cutted.append({'properties': {'name': '1979年1月18日'},'relations': {}, 'spgTypeName': 'Demo2.Time'})
        cutted.append({'properties': {'name': '台湾省新北市'}, 'relations': {}, 'spgTypeName': 'Demo2.Place'})
        cutted.append({'properties': {'name': '福建省永春县'}, 'relations': {}, 'spgTypeName': 'Demo2.Place'})
        cutted.append({'properties': {'name': '华语流行乐男歌手'}, 'relations': {}, 'spgTypeName': 'Demo2.Role'})
        cutted.append({'properties': {'name': '音乐人'}, 'relations': {}, 'spgTypeName': 'Demo2.Role'})
        cutted.append({'properties': {'name': '华语流行乐男歌手'}, 'relations': {}, 'spgTypeName': 'Demo2.Role'})
        cutted.append({'properties': {'name': '演员'}, 'relations': {}, 'spgTypeName': 'Demo2.Role'})
        cutted.append({'properties': {'name': '音乐人'}, 'relations': {}, 'spgTypeName': 'Demo2.Role'})
        cutted.append({'properties': {'name': '华语流行乐男歌手'}, 'relations': {}, 'spgTypeName': 'Demo2.Role'})
        cutted.append({'properties': {'name': '导演'}, 'relations': {}, 'spgTypeName': 'Demo2.Role'})
        cutted.append({'properties': {'name': '演员'}, 'relations': {}, 'spgTypeName': 'Demo2.Role'})
        cutted.append({'properties': {'name': '音乐人'}, 'relations': {}, 'spgTypeName': 'Demo2.Role'})
        cutted.append({'properties': {'name': '华语流行乐男歌手'}, 'relations': {}, 'spgTypeName': 'Demo2.Role'})
        cutted.append({'properties': {'name': '编剧'}, 'relations': {}, 'spgTypeName': 'Demo2.Role'})
        cutted.append({'properties': {'name': '导演'}, 'relations': {}, 'spgTypeName': 'Demo2.Role'})
        cutted.append({'properties': {'name': '演员'}, 'relations': {}, 'spgTypeName': 'Demo2.Role'})
        cutted.append({'properties': {'name': '音乐人'}, 'relations': {}, 'spgTypeName': 'Demo2.Role'})
        cutted.append({'properties': {'name': '华语流行乐男歌手'}, 'relations': {}, 'spgTypeName': 'Demo2.Role'})
        cutted.append({'properties': {'name': '淡江中学'}, 'relations': {}, 'spgTypeName': 'Demo2.Organization'})
        cutted.append({'properties': {'additionalName': 'Jay Chou','birthDate': '1979年1月18日','birthPlace': '台湾省新北市','graduatedSchool': '淡江中学','major': '编剧,导演,演员,音乐人,华语流行乐男歌手','name': '周杰伦','nativePlace': '福建省永春县'}, 'relations': {}, 'spgTypeName': '人物'})
        cutted.append({'properties': {'name': '台湾省新北市'}, 'relations': {}, 'spgTypeName': 'Demo2.Time'})
        cutted.append({'properties': {'name': '福建省泉州市永春县'}, 'relations': {}, 'spgTypeName': 'Demo2.Place'})
        cutted.append({'properties': {'name': '淡江山叶幼儿音乐班'}, 'relations': {}, 'spgTypeName': 'Text'})
        cutted.append({'properties': {'name': '钢琴'}, 'relations': {}, 'spgTypeName': 'Text'})
        cutted.append({'properties': {'name': '淡江山叶幼儿音乐班'}, 'relations': {}, 'spgTypeName': 'Text'})
        cutted.append({'properties': {'name': '淡江中学第一届音乐班'}, 'relations': {}, 'spgTypeName': 'Text'})
        cutted.append({'properties': {'name': '钢琴'}, 'relations': {}, 'spgTypeName': 'Text'})
        cutted.append({'properties': {'name': '淡江山叶幼儿音乐班'}, 'relations': {}, 'spgTypeName': 'Text'})
        cutted.append({'properties': {'name': '两次报考台北大学音乐系均没有被录取'}, 'relations': {}, 'spgTypeName': 'Text'})
        cutted.append({'properties': {'name': '淡江中学第一届音乐班'}, 'relations': {}, 'spgTypeName': 'Text'})
        cutted.append({'properties': {'name': '钢琴'}, 'relations': {}, 'spgTypeName': 'Text'})
        cutted.append({'properties': {'name': '淡江山叶幼儿音乐班'}, 'relations': {}, 'spgTypeName': 'Text'})
        cutted.append({'properties': {'name': '一家餐馆'}, 'relations': {}, 'spgTypeName': 'Demo2.Organization'})
        cutted.append({'properties': {'birthDate': '台湾省新北市','educationLevel': '两次报考台北大学音乐系均没有被录取,淡江中学第一届音乐班,钢琴,淡江山叶幼儿音乐班','name': '周杰伦','nativePlace': '福建省泉州市永春县','workUnit': '一家餐馆'}, 'relations': {}, 'spgTypeName': '人物'})
        return cutted