from abc import ABC
from typing import Dict, List

import re
from knext.builder.operator.op import PromptOp
from knext.builder.operator.spg_record import SPGRecord
from knext.schema.client import SchemaClient
from knext.schema.model.base import BaseSpgType
from knext.schema.model.schema_helper import SPGTypeName, PropertyName, RelationName
import json5


class TableSchemaAnalyzePrompt(PromptOp):
    template = '''
你是一个表格分析专家，负责根据表格标题，表头和数据中分析表格结构，发现表格中哪些列代表了主体，哪些列是对主体的补充说明，同时还可以分析主体之间的关系。最终主体、属性、关系以图形式表示，即s-p-o
现在给你一张表格的数据，包括表格的标题(caption)，表格描述的顶层主体和顶层主体类型(top_entity,top_entity_type)和表格数据(data,以python二维数组表达）。请分析这张表的数据和表头，按步骤完成以下任务：

任务1:主体识别: 请尽可能多的识别表格中所有能构成独立实体的列，这些实体不仅包括明显的核心主体，也涵盖那些能够携带自身属性或与其它实体建立特定关系的列。编号,数字,日期,标识符等都不视为实体,而做为属性在任务2中处理。结果以json形式表达，格式例如："entity":["表列名1":{{"type":"主体类型1"}},"表列名2":{{"type":"主体类型2"}}]。

任务2:属性补充: 遍历任务1中识别出的每个主体，分析表格中哪些列是主体的属性？属性包括主体列的辅助信息、标识符、描述信息和补充信息等，但是不包括任务1中识别出来的主体列。请补充任务1中产出的entity json，列出主体的所有属性列,附加在主体dict中,key是properties。注意，一个属性列需要检查3个点：1）需要确保属性名称与表头严格一致 2）不应该是任务1中已经识别出来的主体 3）一个属性列应该归属到改列描述的主体，不被多个主体共享。4) type暂时留空，固定写"NULL"
举个例子，表头是["序号", "州名", "英文", "简称", "首府", "英文_2"],数据是:[[ "1", "亚拉巴马州", "Alabama", "AL", "蒙哥马利", "Montgomery" ], [ "2", "阿拉斯加州", "Alaska", "AK", "朱诺", "Juneau" ]]这里我们识别出的主体是“州名”和“首府”。”简称“和”英文“是描述”州名“的，因此补充主体属性{{"州名":{{"type":"地区","properties":[{{"header":"简称", "type":"NULL"}},{{"header":"英文", "type":"NULL"}}]}}, 列"英文_2"是描述主体“首府”的，因此补充主体属性{{"首府":{{"type":"地区","properties":[{{"header_2":"英文", "type":"NULL"}}]}}}}。由于首府是一个实体，因此不出现在州名的属性中。

任务3:识别主体之间的关系，以json形式表达spo关系，key是"relation",value是list of dict，value的dict是subject_name,relation,object_name。subject_name和object_name的值必须和主体名称严格对应。relation避免使用'属于','是','拥有','包含'这样的宽泛关系，而用诸如'首府是','包含州'这样的具体关系名称。输出格式例如："relation":[{{ "subject_name": "主体1", "relation": "首府是", "object_name": "主体2"}}]

任务4:分析第1步中识别出的主体和顶层主体的关系，这里可以参考表头和表标题的信息。添加到relation列表中。subject_name固定写"top_entity", object_name严格从entity的key中取。

任务5:合并上面的json后输出，key是entity和relation. 只输出schema信息，不输出具体的实例信息。 

表格信息在3个反引号中，请一步步推理,明确每一步的思考过程,逐步推导完成上述任务：
```
caption: {caption}
top_entity: {entity_name},
top_entity_type: {entity_type},
data:{data}
```
    '''

    def build_prompt(self, variables: Dict[str, str]) -> str:
        return self.template.format(caption=variables.get("caption"),
                                    entity_name=variables.get("entity_name"),
                                    entity_type=variables.get("entity_type"),
                                    data=variables.get("data"))

    def parse_response(self, response: str, **kwargs):
        pattern = r'\`\`\`json\n(.*?)\n\`\`\`'

        # 查找所有匹配项
        possible_json = re.findall(pattern, response, re.DOTALL)

        if possible_json:
            rsp = possible_json[-1]
        else:
            raise ValueError("doesn't find json structure from table schema analyze llm response")

        rsp = json5.loads(rsp)
        return rsp
