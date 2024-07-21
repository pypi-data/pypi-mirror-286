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

from typing import Sequence

from knext.builder.auto_extract.base import Splitter
from knext.common.base.runnable import Input, Output

from knext.builder.auto_extract.model.chunk import Chunk
from knext.builder.auto_extract.model.chunk import ChunkTypeEnum


class MockSplitter(Splitter):
    file_name: str

    def __init__(self, file_name: str, **kwargs):
        super().__init__(file_name=file_name, **kwargs)


    def invoke(self, input: Input) -> Sequence[Output]:
        cutted = []
        chunk1 = Chunk(type=ChunkTypeEnum.Text, chunk_header="个人介绍", chunk_name="周杰伦#个人介绍#0", chunk_id="b26026cbb59577b7b412a3f1023caf23559facf8ca57a49daa4ddc24fb4a0445", content="周杰伦（Jay Chou），1979年1月18日出生于台湾省新北市，祖籍福建省永春县，华语流行乐男歌手、音乐人、演员、导演、编剧，毕业于淡江中学。")
        cutted.append(chunk1.to_dict())
        chunk2 = Chunk(type=ChunkTypeEnum.Text, chunk_header="早年经历", chunk_name="周杰伦#早年经历#1", chunk_id="00c84ad03e7417f8c4473996334301c76643f6640557d4a3abb6a645d6b73957", content="周杰伦出生于台湾省新北市，祖籍福建省泉州市永春县。4岁的时候，母亲叶惠美把他送到淡江山叶幼儿音乐班学习钢琴。初中二年级时，父母因性格不合离婚，周杰伦归母亲叶惠美抚养。中考时，没有考上普通高中，同年，因为擅长钢琴而被淡江中学第一届音乐班录取。高中毕业以后，两次报考台北大学音乐系均没有被录取，于是开始在一家餐馆打工。")
        cutted.append(chunk2.to_dict())
        return cutted

if __name__ == '__main__':
    a = MockSplitter({"file_name":"/openspg_venv/lib/python3.8"})
    print(a.invoke(""))
