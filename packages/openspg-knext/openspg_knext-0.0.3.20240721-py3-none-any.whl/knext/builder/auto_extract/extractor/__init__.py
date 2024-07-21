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

from knext.builder.auto_extract.extractor.baike_extractor import BaikeExtractor
from knext.builder.auto_extract.extractor.table_extractor import TableExtractor
from knext.builder.auto_extract.extractor.user_defined_extractor import (
    GovernmentAffairsExtractor,
    UserManualExtractor,
)


__all__ = [
    "BaikeExtractor",
    "TableExtractor",
    "GovernmentAffairsExtractor",
    "UserManualExtractor",
]
