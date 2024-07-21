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
# os.environ["KNEXT_HOST_ADDR"] = "http://110.76.3.163:8887"

from knext.builder.auto_extract.extractor.table_extractor import TableExtractor
from knext.builder.auto_extract.extractor.text_extractor import TextExtractor
from knext.builder.auto_extract.model.chunk import ChunkTypeEnum
from knext.builder.auto_extract.common.llm_client import LLMClient

from knext.builder.auto_extract.base import Extractor
from knext.builder.operator import SPGRecord
from knext.common.base.runnable import Input, Output
from typing import List, Sequence

PWD = os.path.dirname(__file__)


class BaikeExtractor(Extractor):
    project_id: int
    models: str

    def __init__(self, project_id: int, **kwargs):
        super().__init__(project_id=project_id, **kwargs)
        gpt_client = LLMClient.from_config(
            config=os.path.join(PWD, "../config/gpt3_5.json")
        )
        gpt4_client = LLMClient.from_config(
            config=os.path.join(PWD, "../config/gpt4.json")
        )
        qwen_client = LLMClient.from_config(
            config=os.path.join(PWD, "../config/qwen.json"), use_pre=False
        )
        humming_client = LLMClient.from_config(
            config=os.path.join(PWD, "../config/humming.json"), use_pre=False
        )
        deepseek_client = LLMClient.from_config(
            config=os.path.join(PWD, "../config/deepseek.json")
        )
        self.clients = {
            "gpt-3.5-turbo": gpt_client,
            "gpt-4": gpt4_client,
            "humming": humming_client,
            "qwen": qwen_client,
            "deepseek-chat": deepseek_client,
        }
        self.text_extractor = TextExtractor(project_id, [self.clients[m] for m in self.models.split(',')], top_entity_type="人物")
        self.table_extractor = TableExtractor(project_id)

    def invoke(self, input: Input) -> Sequence[Output]:
        """
        Schema约束+开放抽取：
        1. 从SPGServer端查询SpgTypes，进行schema约束的实体和事件抽取。
        2. 进行实体开放抽取。
            2.1 使用SPOPrompt抽取(s,s_type,p,o,o_type)五元组
            (周杰伦，歌手->艺人->人物，出生地点->出生地，台湾，地点->区域地点)
            2.2 通过SPGAligner将s_type和o_type标准化到顶端类型
            2.3 通过SPGAligner将p标准化到s_type存在的属性上。
                对于平台侧存在的属性，直接映射到对应字段上。
                对于平台侧不存在但语义图存在的属性，转成json并存储到basicInfo字段中。
                对于平台侧不存在且语义图也不存在的属性，即对齐失败的属性，转成json并存储到otherInfo字段中。
        """

        chunk = input
        if chunk[0].type == ChunkTypeEnum.Text:
            records = self.text_extractor.invoke(chunk)
        elif chunk[0].type == ChunkTypeEnum.Table:
            records = self.table_extractor.invoke(chunk)
        else:
            raise ValueError(f"Unsupported chunk type: {chunk[0].type}")

        return records

    def batch(self, inputs: List[Input]) -> Sequence[Output]:
        records = []
        for input in inputs:
            records.extend(self.invoke(input))
        return records
