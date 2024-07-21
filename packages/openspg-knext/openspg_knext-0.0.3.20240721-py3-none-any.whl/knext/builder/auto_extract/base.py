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


from abc import ABC
from typing import Type, Dict, Union, Sequence, List

from knext.builder.auto_extract.model.chunk import Chunk
from knext.builder.operator import SPGRecord
from knext.builder.auto_extract.model.sub_graph import SubGraph
from knext.common.base.component import Runnable
from knext.common.base.runnable import Input, Output, Other


class Splitter(Runnable, ABC):
    file_name: str

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def input_types(self) -> Type[Input]:
        return Union[Dict, str]

    def output_types(self) -> Type[Output]:
        return Chunk

    @classmethod
    def from_config(cls):
        return Splitter()

    def _handle(self, input: Union[str, Dict], user_query: str) -> Sequence[Dict]:
        _input = input
        _output = self.invoke(_input, user_query)
        return [[_o.to_dict() for _o in o] for o in _output]

    def __rshift__(self, other: Other):
        pass


class Extractor(Runnable, ABC):
    project_id: int

    def __init__(self, project_id, **kwargs):
        self.project_id = project_id
        super().__init__(**kwargs)

    def input_types(self) -> Type[Input]:
        return Chunk

    def output_types(self) -> Type[Output]:
        return SPGRecord

    def _handle(self, input: Dict) -> Sequence[Dict]:
        _input = [self.input_types().from_dict(i) for i in input]
        _output = self.invoke(_input)
        return [_o.to_dict() for _o in _output]

    @classmethod
    def from_config(cls):
        return Extractor()

    def __rshift__(self, other: Other):
        pass


class PostProcessor(Runnable, ABC):
    project_id: int

    def __init__(self, project_id: int, **kwargs):
        self.project_id = project_id
        super().__init__(**kwargs)

    def input_types(self) -> Type[Input]:
        return SPGRecord

    def output_types(self) -> Type[Output]:
        return SubGraph

    def _handle(self, input: Sequence[Dict]) -> Dict:
        _input = [self.input_types().from_dict(i) for i in input]
        _output = self.invoke(_input)
        return _output.to_dict()

    @classmethod
    def from_config(cls):
        return PostProcessor()

    def __rshift__(self, other: Other):
        pass
