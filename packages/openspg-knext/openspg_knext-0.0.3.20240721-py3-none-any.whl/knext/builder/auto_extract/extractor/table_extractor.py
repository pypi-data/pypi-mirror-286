# coding: utf8

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
import traceback
from typing import Dict, List, Sequence, Union

import json5

from knext.builder.auto_extract.common.spg_aligner import SPGAligner
from knext.builder.auto_extract.model.chunk import Chunk
from knext.builder.operator import SPGRecord
from knext.builder.auto_extract.model.sub_graph import SubGraph
from knext.common.base.component import Runnable
from knext.common.base.runnable import Input, Output, Other

from knext.builder.auto_extract.base import Extractor
from knext.builder.auto_extract.common.prompt.free_prompt import SPOPrompt
from knext.builder.operator.builtin.table_analyze_prompt import (
    TableSchemaAnalyzePrompt,
)
from knext.common.base.runnable import Input, Output
import os
from typing import List

from knext.builder.operator import OneKE_KGPrompt, OneKE_EEPrompt
from knext.builder.auto_extract.common.llm_client import LLMClient
from knext.common.decorators import retry
from knext.schema.client import SchemaClient
from knext.schema.model.base import SpgTypeEnum

PWD = os.path.dirname(__file__)


class Cell:
    def __init__(self, text):
        self.text = self.get_text_from_markdown(text)
        self.link = self.get_link_from_markdown()

    def get_text_from_markdown(self, text):
        # TODO
        return text

    def get_link_from_markdown(self, text):
        # TODO
        return text

    def is_blank_cell(self, text):
        # TODO
        return text.strip() in ["", "/", "-"]

    def split_cell(self):
        # TODO
        return [self]


# class TableHeaderMetadata
class Table:
    def __init__(self,
                 top_entity_name,
                 top_entity_type,
                 context,
                 caption,
                 headers,
                 header_position,
                 header_len,
                 data: Union[List[list], str],  # with/without header
                 llm_client,
                 ):
        self.raw_data = data  # 存一份原始数据
        self.data: List[List[Cell]] = [[]]  # TODO 这里转换成 Cell表达, 之后都基于这个数据继续开发了
        # 这里其实还缺一个header的索引
        # self.pure_text_table = self.to_pure_text_table(self.data)

        self._to_standard_table(llm_client=llm_client)

    def _to_standard_table(self, llm_client: LLMClient = None,
                           force_infer_header=False,
                           force_infer_top_entity=False,
                           ):
        # 在这里去串标准化流程
        table_type_header_info = self.get_table_type_and_header_meta(llm_client)

        table_type = table_type_header_info.get("table_type", None)

        if table_type == "entity_desc":
            with_header = table_type_header_info.get("with_header", False)
            header_position = table_type_header_info.get("header_position", None)
            header_len = table_type_header_info.get("header_len", 0)
            headers, data = self._make_table_header_in_row(with_header, header_position, header_len)
            # 从这里开始，表格就已经是行表示的了，现在对于没有header的表格，让大模型猜一个；有header的表格，大模型校验一下这个header对不对
            headers = self._fix_headers(headers)
            # 这里有2个重要的输入了，一个是header，一个是data（前n行也是header)，现在开始对特殊表格做处理

        else:
            raise NotImplementedError(f"{table_type} table is not supported yet")

        return

    def _handle_symmetrical_header(self):
        # TODO header和数据一起处理
        pass

    def _handle_duplicate_header(self):
        # TODO 可能只处理header，重命名。注意，连续的header名称相同可能只是因为header跨列了，只有隔了列之后重名的，重命名为XX_2
        pass

    def _handle_header_span(self):
        # TODO
        pass

    def _handle_header_in_all_columns(self):
        pass

    def _transpose_table(self):
        pass

    def handle_header_in_multiple_lines(self):
        pass

    def get_table_type_and_header_meta(self, llm_client):
        # version 2.2
        """
你是一个表格分析专家，负责根据表格标题，表头和表格数据中分析表格结构，发现表格是哪种类型，表格中哪些列代表了主体，哪些列是对主体的补充说明，同时还可以分析主体之间的关系。
现在给你一张表格的数据，包括表格的标题(caption)，表格描述的顶层主体和顶层主体类型(top_entity,top_entity_type)和表格数据(data,以python二维数组表达）。请分析这张表的数据和表头，按步骤完成以下任务：

任务1: 表格类型分析。表格分为实体描述类表格和数据统计类表格。实体描述类表格主要是以表格的形式列举一些实体以及和实体相关的属性描述；数据统计类表格列出了很多数据，来详细描述主体某一方面的数据表现，常用于得分统计、营收统计，表达一些发展趋势和数据综合统计。如果是实体表现类表格，请输出{"table_type":"entity_desc"}，数据统计类输出{"table_type":"num_statistic"}

任务2: 如果任务1中判定是实体描述类表格，继续完成下列任务，否则直接返回结果。

任务3: 确认表格表头数据位置。请判断表格数据(data的二维数组中)中是否显式的写出了表头？如果数据中已经写出了表头信息，判断表头的位置(header_position)，以及表头占据了多少行，结果以json输出，例如: {"with_header":true, "header_position":"row","header_len":1}, header_position可选“row”，“column”，"unknown";如果表头不在表格数据中，with_header值为false，并且根据表格数据分析一下表头应该在row中还是column中，输出结果，header_len填写0。

表格信息在3个反引号中，请一步步推理,明确每一步的思考过程,逐步推导完成上述任务：
```
caption: 美国各州州名及首府（按州名首字母排序）
top_entity: 美国,
top_entity_type: 国家,
data:
[[ "1", "亚拉巴马州", "Alabama", "AL", "蒙哥马利", "Montgomery" ], [ "2", "阿拉斯加州", "Alaska", "AK", "朱诺", "Juneau" ], [ "3", "亚利桑那州", "Arizona", "AZ", "菲尼克斯", "Phoenix" ], [ "4", "阿肯色州", "Arkansas", "AR", "小石城", "Little rock" ], [ "5", "加利福尼亚州", "California", "CA", "萨克拉门托", "Sacramento" ], [ "6", "科罗拉多州", "Colorado", "CO", "丹佛", "Denver" ], [ "7", "康涅狄格州", "Connecticut", "CT", "哈特福德", "Hartford" ], [ "8", "特拉华州", "Delaware", "DE", "多佛", "Dover" ], [ "9", "佛罗里达州", "Florida", "FL", "塔拉哈西", "Tallahassee" ], [ "10", "佐治亚州", "Georgia", "GA", "亚特兰大", "Atlanta" ], [ "11", "夏威夷州", "Hawaii", "HI", "火奴鲁鲁", "Honolulu" ], [ "12", "爱达荷州", "Idaho", "ID", "博伊西", "Boise" ], [ "13", "伊利诺伊州", "Illinois", "IL", "斯普林菲尔德", "Springfield" ], [ "14", "印第安纳州", "Indiana", "IN", "印第安纳波利斯", "Indianapolis" ], [ "15", "艾奥瓦州", "Iowa", "IA", "得梅因", "Des Moines" ], [ "16", "堪萨斯州", "Kansas", "KS", "托皮卡", "Topeka" ], [ "17", "肯塔基州", "Kentucky", "KY", "法兰克福", "Frankfort" ], [ "18", "路易斯安那州", "Louisiana", "LA", "巴吞鲁日", "Baton Rouge" ], [ "19", "缅因州", "Maine", "ME", "奥古斯塔", "Augusta" ], [ "20", "马里兰州", "Maryland", "MD", "安纳波利斯", "Annapolis" ]]

```

        """
        return {
            "table_type": "entity_desc",
            "with_header": False,
            "header_position": "row",
            "header_len": 1
        }
        #
        #
        # return {
        #     "headers": ["序号", "姓名", "职务"],
        #     "header_position": "row",
        #     "header_len": 1
        # }

    def to_pure_text_table(self, data: List[List[Cell]]) -> List[List[str]]:
        # TODO: 大模型只需要纯文本, 去掉不必要的link
        pass

    def _need_infer_header(self):
        # TODO
        return True

    def sample_data(self, rows):
        # 选取n行数据做为sample
        pass

    def _make_table_header_in_row(self, with_header, header_position, header_len):
        if header_position == 'column':
            self.data = self._transpose_table()
        # TODO
        return ["headers"]

    def _fix_headers(self, headers):
        pass
"""
你是一个表格数据分析归纳专家，负责根据表格标题，表头和表格数据判断表头是否表述得当，如果没有表头，你可以准确的推断表格。

现在给你一张表格的数据，包括表格的标题(caption)，表格描述的顶层主体和顶层主体类型(top_entity,top_entity_type)和表格数据(data,以python二维数组表达）。请分析这张表的数据和表头，按步骤完成以下任务：

任务1: 判断这个表格是不是表述了一个可平铺的列表？平铺列表是指表格中所有的列都是同种类的实体，且彼此之间没有相互描述和补充的关系，这种表格其实是一个list，而不是传统意义的表格。如果是平铺列表则输出{"header_position":"list"},同时输出最可能的表头，例如{"header":["人物","人物"]}。由于表格其实描述了一个列表，所以这里的表头内容都是一致的。

任务2：如果不是平铺列表，则判断表格的开头n行是否准确的描述了表格？


表格信息在3个反引号中，请一步步推理,明确每一步的思考过程,逐步推导完成上述任务：

```
caption: 美国各州州名及首府（按州名首字母排序）
top_entity: 美国,
top_entity_type: 国家,
data:
[[ "1", "亚拉巴马州", "Alabama", "AL", "蒙哥马利", "Montgomery" ], [ "2", "阿拉斯加州", "Alaska", "AK", "朱诺", "Juneau" ], [ "3", "亚利桑那州", "Arizona", "AZ", "菲尼克斯", "Phoenix" ], [ "4", "阿肯色州", "Arkansas", "AR", "小石城", "Little rock" ], [ "5", "加利福尼亚州", "California", "CA", "萨克拉门托", "Sacramento" ], [ "6", "科罗拉多州", "Colorado", "CO", "丹佛", "Denver" ], [ "7", "康涅狄格州", "Connecticut", "CT", "哈特福德", "Hartford" ], [ "8", "特拉华州", "Delaware", "DE", "多佛", "Dover" ], [ "9", "佛罗里达州", "Florida", "FL", "塔拉哈西", "Tallahassee" ], [ "10", "佐治亚州", "Georgia", "GA", "亚特兰大", "Atlanta" ], [ "11", "夏威夷州", "Hawaii", "HI", "火奴鲁鲁", "Honolulu" ], [ "12", "爱达荷州", "Idaho", "ID", "博伊西", "Boise" ], [ "13", "伊利诺伊州", "Illinois", "IL", "斯普林菲尔德", "Springfield" ], [ "14", "印第安纳州", "Indiana", "IN", "印第安纳波利斯", "Indianapolis" ], [ "15", "艾奥瓦州", "Iowa", "IA", "得梅因", "Des Moines" ], [ "16", "堪萨斯州", "Kansas", "KS", "托皮卡", "Topeka" ], [ "17", "肯塔基州", "Kentucky", "KY", "法兰克福", "Frankfort" ], [ "18", "路易斯安那州", "Louisiana", "LA", "巴吞鲁日", "Baton Rouge" ], [ "19", "缅因州", "Maine", "ME", "奥古斯塔", "Augusta" ], [ "20", "马里兰州", "Maryland", "MD", "安纳波利斯", "Annapolis" ]]
```

```
caption: 著名人物-古代
top_entity: 河北省,
top_entity_type: 地区,
data:
[["尧", "伯夷", "叔齐", "扁鹊", "公孙龙", "赵武灵王", "毛遂", "赵云", "祖逖", "韩延徽"],
["怀丙", "赵奢", "赵姬", "徐福", "赵佗", "毛亨", "毛苌", "韩婴", "董仲舒", "吕端"],
["李夫人", "窦太后", "王政君", "甄宓", "李牧", "郭威", "刘秉忠", "魏征", "宋璟", "柴荣"],
["张角", "何伯策", "高适", "李春", "孙伏伽", "刘黑闼", "贾岛", "石勒", "高欢", "苏天爵"],
["崔浩", "纪晓岚", "曹鼐", "孟知祥", "关汉卿", "白朴", "王锡衮", "苏大", "梁梦龙", "高长恭"]]
```
"""


class TableExtractor(Extractor):
    project_id: int
    models: List[str]

    def __init__(self, project_id: int, **kwargs):
        super().__init__(project_id=project_id, **kwargs)
        # gpt_client = LLMClient.from_config(config=os.path.join(PWD, "../config/gpt3_5.json"))
        # gpt4_client = LLMClient.from_config(config=os.path.join(PWD, "../config/gpt4.json"))
        self.llm_client = qwen_client = LLMClient.from_config(
            config=os.path.join(PWD, "../config/deepseek.json"), use_pre=False
        )  # 110B
        # humming_client = LLMClient.from_config(config=os.path.join(PWD, "../config/humming.json"), use_pre=False)
        self.clients = {
            # "gpt-3.5-turbo": gpt_client,
            # "gpt-4": gpt4_client,
            # "humming": humming_client,
            "qwen": qwen_client,
            "deepseek": qwen_client,
        }
        # session = SchemaClient(project_id=self.project_id).create_session()
        # self.spg_types = session.spg_types
        self.max_retry_times = 3
        # self.debug = os.getenv("KNEXT_DEBUG_MODE") == "True"
        self.op = SPOPrompt(project_id=self.project_id)

    def invoke(self, input: Input) -> Sequence[Output]:
        """ """
        content = input[0].content
        chunk_header = input[0].header or ""

        if isinstance(content, str):
            content = json5.loads(content)

        top_entity_name = content.get("top_entity_name", None)
        top_entity_type = content.get("top_entity_type", None)
        context = content.get("context", "")
        table_caption = chunk_header + content.get("caption", "")
        headers = content.get("headers", None)
        header_position = content.get("header_position", None)
        header_len = content.get("header_len", None)
        table_data = content.get("data", None)

        assert table_data is not None
        try:
            spg_records = self.table_to_graph(
                table_data=table_data,
                top_entity_name=top_entity_name,
                top_entity_type=top_entity_type,
                table_context=context,
                caption=table_caption,
                headers=headers,
                header_position=header_position,
                header_len=header_len,
            )
            spo_list = self.op.aligner.parse_to_spo_list(spg_records)
            aligned_records = self.op.parse_response(spo_list)
            return aligned_records
        except Exception:
            errInfo = json.dumps(
                {
                    "traceback": traceback.format_exc(),
                }
            )
            print(errInfo)
            print("table analyze error, skip contents from table" + str(content))
            return []

    def batch(self, inputs: List[Input]) -> Sequence[Output]:
        records = []
        for input in inputs:
            records.extend(self.invoke(input))
        return records

    @retry
    def table_to_graph(
            self,
            table_data: List[list],
            top_entity_name=None,
            top_entity_type=None,
            table_context=None,
            caption=None,
            headers=None,
            header_position=None,
            header_len=None,
    ):
        """
        这里做表格成图的整体流程,https://yuque.antfin.com/knowledge-engine/ybn6uu/kbdgkzum4smzt2dg
        """
        table_type = self.analyze_table_type()

        if table_type == "entity_desc":
            header_info = self.analyze_table_header()
            standard_table = self.get_standard_table(header_info)
        elif table_type == "numeric_statistic":
            pass

        standard_table = table_data

        table_schema = self.analyze_table_schema(
            caption=caption,
            # headers: list,
            entity_name=top_entity_name,
            entity_type=top_entity_type,
            table_raw_data=standard_table,
        )

        # table_schema = {
        #     "entity": {
        #         "州名": {
        #             "type": "地区",
        #             "properties": [
        #                 {"header": "英文", "type": "NULL"},
        #                 {"header": "简称", "type": "NULL"},
        #             ],
        #         },
        #         "首府": {
        #             "type": "城市",
        #             "properties": [{"header": "英文_2", "type": "NULL"}],
        #         },
        #     },
        #     "relation": [
        #         {"subject_name": "州名", "relation": "首府是", "object_name": "首府"},
        #         {"subject_name": "top_entity", "relation": "包含", "object_name": "州名"},
        #     ],
        # }

        if isinstance(table_data, str):
            table_data = json5.loads(table_data)

        spg_records = self.build_spg_records(
            top_entity_name, top_entity_type, table_data, table_schema
        )

        return spg_records

    def analyze_table_type(self):
        return "entity_desc"

    def analyze_table_header(self):
        pass

    def get_standard_table(self, header_info):
        pass

    def analyze_table_schema(
            self,
            caption: str,
            # headers: list,
            entity_name,
            entity_type,
            table_raw_data: list,
    ):
        prompt = TableSchemaAnalyzePrompt()

        variables = dict(
            caption=caption,
            entity_name=entity_name,
            entity_type=entity_type,
            data=table_raw_data,
        )
        # TablePrompt.build_table_graph_schema_prompt()
        # response_json = self.llm_client.invoke(
        #     variables=dict(
        #         caption=caption,
        #         entity_name=entity_name,
        #         entity_type=entity_type,
        #         data=table_raw_data,
        #     ),
        #     prompt_op=prompt,
        # )
        response = self.llm_client(prompt.build_prompt(variables))
        # print("----table schema------ \n " + response + "--------")

        return prompt.parse_response(response)

    def build_spg_records(
            self, top_entity_name, top_entity_type, table_data, table_schema
    ):
        """
                table_schema:
        {
          "entity": {
            "州名": {
              "type": "地区",
              "properties": [
                { "header": "英文", "type": "NULL" },
                { "header": "简称", "type": "NULL" }
              ]
            },
            "首府": {
              "norm_type": "城市",
              "properties": [{ "header": "英文_2", "type": "NULL" }]
            }
          },
          "relation": [
            { "subject_name": "州名", "relation": "首府是", "object_name": "首府" },
            { "subject_name": "top_entity", "relation": "包含", "object_name": "州名" }
          ]
        }
        """
        spg_records_dict: Dict[str, SPGRecord] = {}
        schema_entities = table_schema.get("entity")
        schema_relations = table_schema.get("relation")
        table_header = table_data[0]

        # 单独处理词条名和类型
        if top_entity_name and top_entity_type:
            top_entity_spg_record = SPGRecord(top_entity_type, top_entity_name)
            spg_records_dict[
                f"{top_entity_name}#{top_entity_type}"
            ] = top_entity_spg_record

            # top_entity_relations = []
            for relation in schema_relations:
                if relation.get("subject_name") in ["top_entity", top_entity_name]:
                    object_name = relation.get("object_name")
                    object_schema = schema_entities.get(object_name)
                    relation_name = relation.get("relation")
                    spg_relation_name = (
                        f"{relation_name}#{object_schema.get('type', 'NULL')}"
                    )
                    spg_relation_values = set()  # 去重的目的
                    entity_header_idx = table_header.index(object_name)
                    for row in table_data[1:]:
                        spg_relation_values.add(row[entity_header_idx])

                    top_entity_spg_record.upsert_property(
                        spg_relation_name, ",".join(spg_relation_values)
                    )

        for entity_header, entity_props in schema_entities.items():
            entity_header_idx = table_header.index(entity_header)
            row_entity_type = entity_props.get("type")
            for row in table_data[1:]:
                row_entity_name = row[entity_header_idx]
                spg_entity_key = f"{row_entity_name}#{row_entity_type}"
                spg_record = spg_records_dict.get(spg_entity_key, None)
                if spg_record:
                    pass
                else:
                    spg_record = SPGRecord(row_entity_type, row_entity_name)
                    spg_records_dict[spg_entity_key] = spg_record

                # fill properties
                for props_header_schema in entity_props.get("properties", []):
                    props_header = props_header_schema.get("header")
                    if schema_entities.get(props_header):  # entity 中有这个属性,说明不是属性而是关系,这里不处理
                        continue
                    props_idx = table_header.index(props_header)
                    props_value = row[props_idx]
                    props_type = props_header_schema.get("type")
                    spg_prop_name = f"{props_header}#{props_type}"
                    spg_record.append_property(spg_prop_name, props_value)

                # fill relations
                for relation in schema_relations:
                    if relation.get("subject_name") == entity_header:
                        object_name = relation.get("object_name")
                        object_schema = schema_entities.get(object_name, None)
                        if object_schema:
                            object_type = object_schema.get('type', 'NULL')
                            entity_rel_idx = table_header.index(object_name)
                            object_name = row[entity_rel_idx]
                        elif object_schema is None and object_name == top_entity_name:
                            object_name = top_entity_name
                            object_type = top_entity_type
                        else:
                            continue

                        relation_name = relation.get("relation")
                        spg_rel_name = f"{relation_name}#{object_type}"

                        spg_record.append_property(spg_rel_name, object_name)

        return list(spg_records_dict.values())


if __name__ == "__main__":
    #     chunk_content = {
    #         "top_entity_name": "美国",
    #         "top_entity_type": "国家",
    #         "context": "",
    #         "caption": "美国各州州名及首府（按州名首字母排序）",
    #         "headers": ["序号", "州名", "英文", "简称", "首府", "英文_2"],
    #         "header_position": "row",
    #         "header_len": 1,
    #         "data": """
    # [["序号", "州名", "英文", "简称", "首府", "英文_2"], [ "1", "亚拉巴马州", "Alabama", "AL", "蒙哥马利", "Montgomery" ], [ "2", "阿拉斯加州", "Alaska", "AK", "朱诺", "Juneau" ], [ "3", "亚利桑那州", "Arizona", "AZ", "菲尼克斯", "Phoenix" ], [ "4", "阿肯色州", "Arkansas", "AR", "小石城", "Little rock" ], [ "5", "加利福尼亚州", "California", "CA", "萨克拉门托", "Sacramento" ], [ "6", "科罗拉多州", "Colorado", "CO", "丹佛", "Denver" ], [ "7", "康涅狄格州", "Connecticut", "CT", "哈特福德", "Hartford" ], [ "8", "特拉华州", "Delaware", "DE", "多佛", "Dover" ], [ "9", "佛罗里达州", "Florida", "FL", "塔拉哈西", "Tallahassee" ], [ "10", "佐治亚州", "Georgia", "GA", "亚特兰大", "Atlanta" ], [ "11", "夏威夷州", "Hawaii", "HI", "火奴鲁鲁", "Honolulu" ], [ "12", "爱达荷州", "Idaho", "ID", "博伊西", "Boise" ], [ "13", "伊利诺伊州", "Illinois", "IL", "斯普林菲尔德", "Springfield" ], [ "14", "印第安纳州", "Indiana", "IN", "印第安纳波利斯", "Indianapolis" ], [ "15", "艾奥瓦州", "Iowa", "IA", "得梅因", "Des Moines" ], [ "16", "堪萨斯州", "Kansas", "KS", "托皮卡", "Topeka" ], [ "17", "肯塔基州", "Kentucky", "KY", "法兰克福", "Frankfort" ], [ "18", "路易斯安那州", "Louisiana", "LA", "巴吞鲁日", "Baton Rouge" ], [ "19", "缅因州", "Maine", "ME", "奥古斯塔", "Augusta" ], [ "20", "马里兰州", "Maryland", "MD", "安纳波利斯", "Annapolis" ], [ "21", "马萨诸塞州", "Massachusetts", "MA", "波士顿", "Boston" ], [ "22", "密歇根州", "Michigan", "MI", "兰辛", "Lansing" ], [ "23", "明尼苏达州", "Minnesota", "MN", "圣保罗", "St.Paul" ], [ "24", "密西西比州", "Mississippi", "MS", "杰克逊", "Jackson" ], [ "25", "密苏里州", "Missouri", "MO", "杰斐逊城", "Jefferson City" ], [ "26", "蒙大拿州", "Montana", "MT", "海伦娜", "Helena" ], [ "27", "内布拉斯加州", "Nebraska", "NE", "林肯", "Lincoln" ], [ "28", "内华达州", "Nevada", "NV", "卡森城", "Carson City" ], [ "29", "新罕布什尔州", "New Hampshire", "NH", "康科德", "Concord" ], [ "30", "新泽西州", "New Jersey", "NJ", "特伦顿", "Trenton" ], [ "31", "新墨西哥州", "New Mexico", "NM", "圣菲", "Santa Fe" ], [ "32", "纽约州", "New York", "NY", "奥尔巴尼", "Albany" ], [ "33", "北卡罗来纳州", "North Carolina", "NC", "纳罗利", "Raleigh" ], [ "34", "北达科他州", "North Dakota", "ND", "俾斯麦", "Bismarck" ], [ "35", "俄亥俄州", "Ohio", "OH", "哥伦布", "Columbus" ], [ "36", "俄克拉何马州", "Oklahoma", "OK", "俄克拉何马城", "Oklahoma City" ], [ "37", "俄勒冈州", "Oregon", "OR", "塞勒姆", "Salem" ], [ "38", "宾夕法尼亚州", "Pennsylvania", "PA", "哈里斯堡", "Harrisburg" ], [ "39", "罗得岛州", "Rhode Island", "RI", "普罗维登斯", "Providence" ], [ "40", "南卡罗来纳州", "South Carolina", "SC", "哥伦比亚", "Columbia" ], [ "41", "南达科他州", "South Dakota", "SD", "皮尔", "Pierre" ], [ "42", "田纳西州", "Tennessee", "TN", "纳什维尔", "Nashville" ], [ "43", "得克萨斯州", "Texas", "TX", "奥斯汀", "Austin" ], [ "44", "犹他州", "Utah", "UT", "盐湖城", "Salt Lake City" ], [ "45", "佛蒙特州", "Vermont", "VT", "蒙彼利埃", "Montpelier" ], [ "46", "弗吉尼亚州", "Virginia", "VA", "里士满", "Richmond" ], [ "47", "华盛顿州", "Washington", "WA", "奥林匹亚", "Olympia" ], [ "48", "西弗吉尼亚州", "West Virginia", "WV", "查尔斯顿", "Charleston" ], [ "49", "威斯康星州", "Wisconsin", "WI", "麦迪逊", "Madison" ], [ "50", "怀俄明州", "Wyoming", "WY", "夏延", "Cheyenne"]]
    #             """,
    #     }

    #     chunk_content = {
    #         "top_entity_name": "俄罗斯",
    #         "top_entity_type": "国家",
    #         "context": "",
    #         "caption": "节日",
    #         "headers": [],
    #         "header_position": "row",
    #         "header_len": 1,
    #         "data": """
    # [ [ "日期", "节日名称" ], [ "1月1日", "新年" ], [ "1月7日", "圣诞节（东正教）" ], [ "1月25日", "圣达吉娅娜节（大学生节）" ], [ "2月23日", "卫国者节（军人节），或男人节" ], [ "2月底—3月初", "谢肉节（送冬节）" ], [ "3月8日", "国际妇女节" ], [ "3月底—4月初", "复活节" ], [ "4月的第三个星期天", "科学节" ], [ "5月1日", "国际劳动节" ], [ "5月5日", "报刊节" ], [ "5月9日", "胜利日" ], [ "6月1日", "国际儿童节" ], [ "6月12日", "俄罗斯日" ], [ "6月26日", "俄罗斯青年节" ], [ "7月的第二个星期天", "渔夫节" ], [ "8月的第二个星期六", "体育爱好者节" ], [ "8月27日", "俄罗斯电影节" ], [ "9月1日", "知识节" ], [ "10月的第一个星期天", "教师节" ], [ "11月4日", "人民团结日" ], [ "11月7日", "红场阅兵节" ], [ "11月10日", "警察节" ], [ "11月17日", "国际大学生节" ], [ "12月12日", "俄罗斯宪法节" ], [ "12月25日", "圣诞节" ] ]
    # """}
    # TODO 类似这种
    # "relation": [
    #         { "subject_name": "机构名称", "relation": "有", "object_name": "电话号码" },
    #         { "subject_name": "机构名称", "relation": "位于", "object_name": "俄罗斯" },
    #         { "subject_name": "top_entity", "relation": "包含", "object_name": "机构名称" }
    #     ]

    #     chunk_content = {
    #         "top_entity_name": "俄罗斯",
    #         "top_entity_type": "国家",
    #         "context": "",
    #         "caption": "求助",
    #         "headers": [],
    #         "header_position": "row",
    #         "header_len": 1,
    #         "data": """
    # [ ["机构名称", "电话号码"], ["医疗急救", "103"], ["中国驻俄使馆领事保护协助电话", "007-4999518661"], ["中国驻圣彼得堡总领馆领事保护协助电话", "007-812-7137605"], ["中国驻哈巴罗夫斯克总领馆领事保护协助电话", "007-4212340572"], ["中国驻叶卡捷琳堡总领馆领事保护协助电话", "007-9221509999"], ["中国驻伊尔库茨克总领馆领事保护协助电话", "007-9647301058"], ["中国驻符拉迪沃斯托克总领馆领事保护协助电话", "007-9020780873"], ["中国驻喀山总领馆领事保护协助电话", "007-9172734789"], ["中国中国游客24小时紧急医疗保险救助和投诉建议热线电话", "88007751869"] ]
    # """
    #     }

    #     chunk_content = {
    #         "top_entity_name": "法国",
    #         "top_entity_type": "国家",
    #         "context": "",
    #         "caption": "节日法国行政区划",
    #         "headers": [],
    #         "header_position": "row",
    #         "header_len": 1,
    #         "data": """
    # [ [ "大区", "省", "省编号" ], [ "上法兰西大区Hauts-de-France", "诺尔省Nord", "59" ], [ "上法兰西大区Hauts-de-France", "加来海峡省Pas-de-Calai", "62" ], [ "上法兰西大区Hauts-de-France", "索姆省Somme", "80" ], [ "上法兰西大区Hauts-de-France", "瓦兹省Oise", "60" ], [ "上法兰西大区Hauts-de-France", "埃纳省Aisne", "02" ], [ "法兰西岛大区Île-de-France", "巴黎Paris", "75" ], [ "法兰西岛大区Île-de-France", "上塞纳省Haute-Seine", "92" ], [ "法兰西岛大区Île-de-France", "瓦勒德马恩省Val-de-Marne", "94" ], [ "法兰西岛大区Île-de-France", "塞纳-圣但尼省Seine-Saint-Denis", "93" ], [ "法兰西岛大区Île-de-France", "伊夫林省Yvelines", "78" ], [ "法兰西岛大区Île-de-France", "瓦勒德瓦兹省Val-d'Oise", "95" ], [ "法兰西岛大区Île-de-France", "塞纳-马恩省Seine-et-Marne", "77" ], [ "法兰西岛大区Île-de-France", "埃松省Essonne", "91" ], [ "大东部大区Grand Est", "阿登省Ardennes", "08" ], [ "大东部大区Grand Est", "马恩省Marne", "51" ], [ "大东部大区Grand Est", "上马恩省Haute-Marne", "52" ], [ "大东部大区Grand Est", "奥布省Aube", "10" ], [ "大东部大区Grand Est", "默兹省Meuse", "55" ], [ "大东部大区Grand Est", "孚日省Vosges", "88" ], [ "大东部大区Grand Est", "摩泽尔省Moselle", "57" ], [ "大东部大区Grand Est", "默尔特-摩泽尔省Muerthe-Moselle", "54" ], [ "大东部大区Grand Est", "上莱茵省Haut-Rhin", "68" ], [ "大东部大区Grand Est", "下莱茵省Bas-Rhin", "67" ], [ "勃艮第-弗朗什-孔泰大区Bourgogne-Franche-Comté", "约讷省Yonne", "89" ], [ "勃艮第-弗朗什-孔泰大区Bourgogne-Franche-Comté", "涅夫勒省Niévre", "58" ], [ "勃艮第-弗朗什-孔泰大区Bourgogne-Franche-Comté", "索恩-卢瓦尔省Saône-et-Loire", "71" ], [ "勃艮第-弗朗什-孔泰大区Bourgogne-Franche-Comté", "科多尔省Côté-d’Or", "21" ], [ "勃艮第-弗朗什-孔泰大区Bourgogne-Franche-Comté", "上索恩省Haute-Saône", "70" ], [ "勃艮第-弗朗什-孔泰大区Bourgogne-Franche-Comté", "汝拉省Jura", "39" ], [ "勃艮第-弗朗什-孔泰大区Bourgogne-Franche-Comté", "杜省Doubs", "25" ], [ "勃艮第-弗朗什-孔泰大区Bourgogne-Franche-Comté", "贝尔福地区省Terr-de-Belfort", "90" ], [ "奥弗涅-罗讷-阿尔卑斯大区Auvergne-Rhône-Alpes", "安省Ain", "01" ], [ "奥弗涅-罗讷-阿尔卑斯大区Auvergne-Rhône-Alpes", "罗讷省Rhône", "69" ], [ "奥弗涅-罗讷-阿尔卑斯大区Auvergne-Rhône-Alpes", "卢瓦尔省Loire", "43" ], [ "奥弗涅-罗讷-阿尔卑斯大区Auvergne-Rhône-Alpes", "阿尔代什省Ardèche", "07" ], [ "奥弗涅-罗讷-阿尔卑斯大区Auvergne-Rhône-Alpes", "德龙省Drôme", "26" ], [ "奥弗涅-罗讷-阿尔卑斯大区Auvergne-Rhône-Alpes", "伊泽尔省Isère", "38" ], [ "奥弗涅-罗讷-阿尔卑斯大区Auvergne-Rhône-Alpes", "萨瓦省Savoie", "73" ], [ "奥弗涅-罗讷-阿尔卑斯大区Auvergne-Rhône-Alpes", "上萨瓦省Haute-Savoie", "74" ], [ "奥弗涅-罗讷-阿尔卑斯大区Auvergne-Rhône-Alpes", "阿列尔省Allier", "03" ], [ "奥弗涅-罗讷-阿尔卑斯大区Auvergne-Rhône-Alpes", "多姆山省Puy-de-Dôme", "63" ], [ "奥弗涅-罗讷-阿尔卑斯大区Auvergne-Rhône-Alpes", "康塔尔省Cantal", "15" ], [ "奥弗涅-罗讷-阿尔卑斯大区Auvergne-Rhône-Alpes", "上卢瓦尔省Haute-Loire", "42" ], [ "普罗旺斯-阿尔卑斯-蓝色海岸大区Provence-Alpes-Côté-d’Azur", "上阿尔卑斯省Haute-Alpes", "05" ], [ "普罗旺斯-阿尔卑斯-蓝色海岸大区Provence-Alpes-Côté-d’Azur", "上普罗旺斯阿尔卑斯省Alpes-de-Haute-Provence", "04" ], [ "普罗旺斯-阿尔卑斯-蓝色海岸大区Provence-Alpes-Côté-d’Azur", "滨海阿尔卑斯省Alpes-Maritimes", "06" ], [ "普罗旺斯-阿尔卑斯-蓝色海岸大区Provence-Alpes-Côté-d’Azur", "瓦尔省Var", "83" ], [ "普罗旺斯-阿尔卑斯-蓝色海岸大区Provence-Alpes-Côté-d’Azur", "罗讷河口省Bouches-du-Rhône", "13" ], [ "普罗旺斯-阿尔卑斯-蓝色海岸大区Provence-Alpes-Côté-d’Azur", "沃克吕兹省Vauclus", "84" ], [ "奥克西塔尼大区Occitanie", "洛泽尔省Lozèrre", "48" ], [ "奥克西塔尼大区Occitanie", "加尔省Gard", "30" ], [ "奥克西塔尼大区Occitanie", "埃罗省Hérault", "34" ], [ "奥克西塔尼大区Occitanie", "奥德省Aude", "11" ], [ "奥克西塔尼大区Occitanie", "东比利牛斯省Pyrénées-Orientales", "66" ], [ "奥克西塔尼大区Occitanie", "阿韦龙省Aveyron", "12" ], [ "奥克西塔尼大区Occitanie", "洛特省Lot", "46" ], [ "奥克西塔尼大区Occitanie", "塔恩省Tarn", "81" ], [ "奥克西塔尼大区Occitanie", "塔恩-加龙省Tarn-Garonne", "82" ], [ "奥克西塔尼大区Occitanie", "热尔省Gers", "32" ], [ "奥克西塔尼大区Occitanie", "上加龙省Haute Garonne", "31" ], [ "奥克西塔尼大区Occitanie", "阿列日省Ariège", "09" ], [ "奥克西塔尼大区Occitanie", "上比利牛斯省Hautes-Pyrénées", "65" ], [ "新阿基坦大区Nouvelle-Aquitaine", "比利牛斯-大西洋省Pyrénées-Atlantiques", "64" ], [ "新阿基坦大区Nouvelle-Aquitaine", "朗德省Landes", "40" ], [ "新阿基坦大区Nouvelle-Aquitaine", "洛特-加龙省Lot-et-Garonne", "47" ], [ "新阿基坦大区Nouvelle-Aquitaine", "吉伦特省Gironde", "33" ], [ "新阿基坦大区Nouvelle-Aquitaine", "多尔多涅省Dordogne", "24" ], [ "新阿基坦大区Nouvelle-Aquitaine", "滨海夏朗德省Charente-Maritime", "17" ], [ "新阿基坦大区Nouvelle-Aquitaine", "夏朗德省Charente", "16" ], [ "新阿基坦大区Nouvelle-Aquitaine", "德塞夫勒省Deux-Sevres", "79" ], [ "新阿基坦大区Nouvelle-Aquitaine", "维埃纳省Vienne", "86" ], [ "新阿基坦大区Nouvelle-Aquitaine", "上维埃纳省Haute-Vienne", "87" ], [ "新阿基坦大区Nouvelle-Aquitaine", "克勒兹省Creuse", "23" ], [ "新阿基坦大区Nouvelle-Aquitaine", "科雷兹省Corrèze", "19" ], [ "中央-卢瓦尔河谷大区Centre-Val de Loires", "厄尔-卢瓦尔省Eure-et-Loir", "28" ], [ "中央-卢瓦尔河谷大区Centre-Val de Loires", "卢瓦尔-谢尔省Loir-et-Cher", "41" ], [ "中央-卢瓦尔河谷大区Centre-Val de Loires", "安德尔-卢瓦尔省Indre-et-Loire", "37" ], [ "中央-卢瓦尔河谷大区Centre-Val de Loires", "安德尔省Indre", "36" ], [ "中央-卢瓦尔河谷大区Centre-Val de Loires", "谢尔省Cher", "18" ], [ "中央-卢瓦尔河谷大区Centre-Val de Loires", "卢瓦雷省Loiret", "45" ], [ "卢瓦尔河地区大区Pays de la Loire", "马耶讷省Mayenne", "53" ], [ "卢瓦尔河地区大区Pays de la Loire", "萨尔特省Sarthe", "72" ], [ "卢瓦尔河地区大区Pays de la Loire", "曼恩-卢瓦尔省Maine-et-Loire", "49" ], [ "卢瓦尔河地区大区Pays de la Loire", "大西洋岸卢瓦尔省Loire-Atlantique", "44" ], [ "卢瓦尔河地区大区Pays de la Loire", "旺代省Vendée", "85" ], [ "布列塔尼大区Bretagne", "伊勒-维莱讷省Ille-et-Vilaine", "35" ], [ "布列塔尼大区Bretagne", "阿摩尔滨海省Côtés-d'Armor", "22" ], [ "布列塔尼大区Bretagne", "莫尔比昂省Morbihan", "56" ], [ "布列塔尼大区Bretagne", "菲尼斯泰尔省Finistère", "29" ], [ "诺曼底大区Normandie", "奥恩省Orne", "61" ], [ "诺曼底大区Normandie", "卡尔瓦多斯省Calvados", "14" ], [ "诺曼底大区Normandie", "芒什省Manche", "50" ], [ "诺曼底大区Normandie", "滨海塞纳省Seine-Maritime", "76" ], [ "诺曼底大区Normandie", "厄尔省Eure", "27" ], [ "科西嘉大区Corse", "上科西嘉省Haute-Corse", "20B" ], [ "科西嘉大区Corse", "南科西嘉省Corse-du-Sud", "20A" ], [ "瓜德罗普大区", "瓜德罗普Guadeloupe", "971" ], [ "马提尼克大区", "马提尼克Martinique", "972" ], [ "法属圭亚那大区", "法属圭亚那French Guyane", "973" ], [ "留尼旺大区", "留尼旺La Réunion", "974" ], [ "马约特大区", "马约特Mayotte", "975" ], [ "", "圣皮埃尔和密克隆Saint-Pierre-et-Miquelon", "" ], [ "", "圣巴泰勒米Saint-Barthélemy", "" ], [ "", "法属圣马丁Saint-Martin", "" ], [ "", "瓦利斯和富图纳Wallis-et-Futuna", "" ], [ "", "法属波利尼西亚Polynésie française", "" ], [ "", "新喀里多尼亚Nouvelle-Calédonie", "" ], [ "", "法属南部和南极领地Terres australes et antarctiques", "" ], [ "", "克利珀顿岛Clipperton", "" ] ]
    # """
    #     }

    #     chunk_content = {
    #         "top_entity_name": "美国",
    #         "top_entity_type": "国家",
    #         "context": "",
    #         "caption": "美国各州州名及首府（按州名首字母排序）",
    #         "headers": ["序号", "州名", "英文", "简称", "首府", "英文_2"],
    #         "header_position": "row",
    #         "header_len": 1,
    #         "data": """
    # [["序号", "州名", "英文", "简称", "首府", "英文_2"], [ "1", "亚拉巴马州", "Alabama", "AL", "蒙哥马利", "Montgomery" ], [ "2", "阿拉斯加州", "Alaska", "AK", "朱诺", "Juneau" ], [ "3", "亚利桑那州", "Arizona", "AZ", "菲尼克斯", "Phoenix" ], [ "4", "阿肯色州", "Arkansas", "AR", "小石城", "Little rock" ], [ "5", "加利福尼亚州", "California", "CA", "萨克拉门托", "Sacramento" ], [ "6", "科罗拉多州", "Colorado", "CO", "丹佛", "Denver" ], [ "7", "康涅狄格州", "Connecticut", "CT", "哈特福德", "Hartford" ], [ "8", "特拉华州", "Delaware", "DE", "多佛", "Dover" ], [ "9", "佛罗里达州", "Florida", "FL", "塔拉哈西", "Tallahassee" ], [ "10", "佐治亚州", "Georgia", "GA", "亚特兰大", "Atlanta" ], [ "11", "夏威夷州", "Hawaii", "HI", "火奴鲁鲁", "Honolulu" ], [ "12", "爱达荷州", "Idaho", "ID", "博伊西", "Boise" ], [ "13", "伊利诺伊州", "Illinois", "IL", "斯普林菲尔德", "Springfield" ], [ "14", "印第安纳州", "Indiana", "IN", "印第安纳波利斯", "Indianapolis" ], [ "15", "艾奥瓦州", "Iowa", "IA", "得梅因", "Des Moines" ], [ "16", "堪萨斯州", "Kansas", "KS", "托皮卡", "Topeka" ], [ "17", "肯塔基州", "Kentucky", "KY", "法兰克福", "Frankfort" ], [ "18", "路易斯安那州", "Louisiana", "LA", "巴吞鲁日", "Baton Rouge" ], [ "19", "缅因州", "Maine", "ME", "奥古斯塔", "Augusta" ], [ "20", "马里兰州", "Maryland", "MD", "安纳波利斯", "Annapolis" ], [ "21", "马萨诸塞州", "Massachusetts", "MA", "波士顿", "Boston" ], [ "22", "密歇根州", "Michigan", "MI", "兰辛", "Lansing" ], [ "23", "明尼苏达州", "Minnesota", "MN", "圣保罗", "St.Paul" ], [ "24", "密西西比州", "Mississippi", "MS", "杰克逊", "Jackson" ], [ "25", "密苏里州", "Missouri", "MO", "杰斐逊城", "Jefferson City" ], [ "26", "蒙大拿州", "Montana", "MT", "海伦娜", "Helena" ], [ "27", "内布拉斯加州", "Nebraska", "NE", "林肯", "Lincoln" ], [ "28", "内华达州", "Nevada", "NV", "卡森城", "Carson City" ], [ "29", "新罕布什尔州", "New Hampshire", "NH", "康科德", "Concord" ], [ "30", "新泽西州", "New Jersey", "NJ", "特伦顿", "Trenton" ], [ "31", "新墨西哥州", "New Mexico", "NM", "圣菲", "Santa Fe" ], [ "32", "纽约州", "New York", "NY", "奥尔巴尼", "Albany" ], [ "33", "北卡罗来纳州", "North Carolina", "NC", "纳罗利", "Raleigh" ], [ "34", "北达科他州", "North Dakota", "ND", "俾斯麦", "Bismarck" ], [ "35", "俄亥俄州", "Ohio", "OH", "哥伦布", "Columbus" ], [ "36", "俄克拉何马州", "Oklahoma", "OK", "俄克拉何马城", "Oklahoma City" ], [ "37", "俄勒冈州", "Oregon", "OR", "塞勒姆", "Salem" ], [ "38", "宾夕法尼亚州", "Pennsylvania", "PA", "哈里斯堡", "Harrisburg" ], [ "39", "罗得岛州", "Rhode Island", "RI", "普罗维登斯", "Providence" ], [ "40", "南卡罗来纳州", "South Carolina", "SC", "哥伦比亚", "Columbia" ], [ "41", "南达科他州", "South Dakota", "SD", "皮尔", "Pierre" ], [ "42", "田纳西州", "Tennessee", "TN", "纳什维尔", "Nashville" ], [ "43", "得克萨斯州", "Texas", "TX", "奥斯汀", "Austin" ], [ "44", "犹他州", "Utah", "UT", "盐湖城", "Salt Lake City" ], [ "45", "佛蒙特州", "Vermont", "VT", "蒙彼利埃", "Montpelier" ], [ "46", "弗吉尼亚州", "Virginia", "VA", "里士满", "Richmond" ], [ "47", "华盛顿州", "Washington", "WA", "奥林匹亚", "Olympia" ], [ "48", "西弗吉尼亚州", "West Virginia", "WV", "查尔斯顿", "Charleston" ], [ "49", "威斯康星州", "Wisconsin", "WI", "麦迪逊", "Madison" ], [ "50", "怀俄明州", "Wyoming", "WY", "夏延", "Cheyenne"]]
    #             """,
    #     }
    # chunk = Chunk("america", "美国", "1", json.dumps(chunk_content))

    # caption = ""
    # entity_name = "美国"
    # entity_type = "国家"
    # table_raw_data = """
    #     [["序号", "州名", "英文", "简称", "首府", "英文_2"], [ "1", "亚拉巴马州", "Alabama", "AL", "蒙哥马利", "Montgomery" ], [ "2", "阿拉斯加州", "Alaska", "AK", "朱诺", "Juneau" ], [ "3", "亚利桑那州", "Arizona", "AZ", "菲尼克斯", "Phoenix" ], [ "4", "阿肯色州", "Arkansas", "AR", "小石城", "Little rock" ], [ "5", "加利福尼亚州", "California", "CA", "萨克拉门托", "Sacramento" ], [ "6", "科罗拉多州", "Colorado", "CO", "丹佛", "Denver" ], [ "7", "康涅狄格州", "Connecticut", "CT", "哈特福德", "Hartford" ], [ "8", "特拉华州", "Delaware", "DE", "多佛", "Dover" ], [ "9", "佛罗里达州", "Florida", "FL", "塔拉哈西", "Tallahassee" ], [ "10", "佐治亚州", "Georgia", "GA", "亚特兰大", "Atlanta" ], [ "11", "夏威夷州", "Hawaii", "HI", "火奴鲁鲁", "Honolulu" ], [ "12", "爱达荷州", "Idaho", "ID", "博伊西", "Boise" ], [ "13", "伊利诺伊州", "Illinois", "IL", "斯普林菲尔德", "Springfield" ], [ "14", "印第安纳州", "Indiana", "IN", "印第安纳波利斯", "Indianapolis" ], [ "15", "艾奥瓦州", "Iowa", "IA", "得梅因", "Des Moines" ], [ "16", "堪萨斯州", "Kansas", "KS", "托皮卡", "Topeka" ], [ "17", "肯塔基州", "Kentucky", "KY", "法兰克福", "Frankfort" ], [ "18", "路易斯安那州", "Louisiana", "LA", "巴吞鲁日", "Baton Rouge" ], [ "19", "缅因州", "Maine", "ME", "奥古斯塔", "Augusta" ], [ "20", "马里兰州", "Maryland", "MD", "安纳波利斯", "Annapolis" ], [ "21", "马萨诸塞州", "Massachusetts", "MA", "波士顿", "Boston" ], [ "22", "密歇根州", "Michigan", "MI", "兰辛", "Lansing" ], [ "23", "明尼苏达州", "Minnesota", "MN", "圣保罗", "St.Paul" ], [ "24", "密西西比州", "Mississippi", "MS", "杰克逊", "Jackson" ], [ "25", "密苏里州", "Missouri", "MO", "杰斐逊城", "Jefferson City" ], [ "26", "蒙大拿州", "Montana", "MT", "海伦娜", "Helena" ], [ "27", "内布拉斯加州", "Nebraska", "NE", "林肯", "Lincoln" ], [ "28", "内华达州", "Nevada", "NV", "卡森城", "Carson City" ], [ "29", "新罕布什尔州", "New Hampshire", "NH", "康科德", "Concord" ], [ "30", "新泽西州", "New Jersey", "NJ", "特伦顿", "Trenton" ], [ "31", "新墨西哥州", "New Mexico", "NM", "圣菲", "Santa Fe" ], [ "32", "纽约州", "New York", "NY", "奥尔巴尼", "Albany" ], [ "33", "北卡罗来纳州", "North Carolina", "NC", "纳罗利", "Raleigh" ], [ "34", "北达科他州", "North Dakota", "ND", "俾斯麦", "Bismarck" ], [ "35", "俄亥俄州", "Ohio", "OH", "哥伦布", "Columbus" ], [ "36", "俄克拉何马州", "Oklahoma", "OK", "俄克拉何马城", "Oklahoma City" ], [ "37", "俄勒冈州", "Oregon", "OR", "塞勒姆", "Salem" ], [ "38", "宾夕法尼亚州", "Pennsylvania", "PA", "哈里斯堡", "Harrisburg" ], [ "39", "罗得岛州", "Rhode Island", "RI", "普罗维登斯", "Providence" ], [ "40", "南卡罗来纳州", "South Carolina", "SC", "哥伦比亚", "Columbia" ], [ "41", "南达科他州", "South Dakota", "SD", "皮尔", "Pierre" ], [ "42", "田纳西州", "Tennessee", "TN", "纳什维尔", "Nashville" ], [ "43", "得克萨斯州", "Texas", "TX", "奥斯汀", "Austin" ], [ "44", "犹他州", "Utah", "UT", "盐湖城", "Salt Lake City" ], [ "45", "佛蒙特州", "Vermont", "VT", "蒙彼利埃", "Montpelier" ], [ "46", "弗吉尼亚州", "Virginia", "VA", "里士满", "Richmond" ], [ "47", "华盛顿州", "Washington", "WA", "奥林匹亚", "Olympia" ], [ "48", "西弗吉尼亚州", "West Virginia", "WV", "查尔斯顿", "Charleston" ], [ "49", "威斯康星州", "Wisconsin", "WI", "麦迪逊", "Madison" ], [ "50", "怀俄明州", "Wyoming", "WY", "夏延", "Cheyenne"]]
    #     """
    table_json_fire = "instruction_doc.json5"
    table_key = "知蛛"

    table_dir = "../data/table"
    with open(os.path.join(table_dir, table_json_fire), "r") as reader:
        chunk_dict = json5.loads(reader.read())

    chunk_params = chunk_dict.get(table_key, None)
    chunk_params.pop("llm_schema")

    assert chunk_params is not None

    chunk = Chunk(type=None,
                  chunk_id="fd65d8b09e3dd9da6814a6c97ed3f2d5e61ccd697d901532b6b3e0a60fbc0952",
                  chunk_name="400a6676814461868eb2eb2ed5aff0e683bd4cc41bd00c9506b9e30a6a52b4e7",
                  **chunk_params)

    spg_records = TableExtractor(123).invoke([chunk])
    print(spg_records)
