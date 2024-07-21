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
import hashlib
import time
from enum import Enum
from typing import Union, Dict, Any


class ChunkTypeEnum(str, Enum):
    Table = "TABLE"
    Text = "TEXT"


class Chunk:
    def __init__(
        self,
        type: ChunkTypeEnum,
        chunk_header: str,
        chunk_name: str,
        chunk_id: str,
        content: Union[str, Dict],
        abstract: str = "",
    ):
        self.type = type
        self.header = chunk_header
        self.name = chunk_name
        self.id = chunk_id
        self.content = content
        self.abstract = abstract

    @staticmethod
    def generate_hash_id(value):
        value = f"{value}{time.time()}"
        if isinstance(value, str):
            value = value.encode("utf-8")
        hasher = hashlib.sha256()
        hasher.update(value)
        return hasher.hexdigest()

    def __str__(self):
        tmp = {
            "header": self.header,
            "name": self.name,
            "id": self.id,
            "content": self.content
            if len(self.content) <= 64
            else self.content[:64] + " ...",
        }
        return f"<Chunk>: {tmp}"

    __repr__ = __str__

    def to_dict(self):
        return {
            "type": self.type.value,
            "header": self.header,
            "name": self.name,
            "id": self.id,
            "content": self.content,
        }

    @classmethod
    def from_dict(cls, input_: Dict[str, Any]):
        return cls(
            input_.get("type"),
            input_.get("header"),
            input_.get("name"),
            input_.get("id"),
            input_.get("content"),
            input_.get("abstract", ""),
        )
