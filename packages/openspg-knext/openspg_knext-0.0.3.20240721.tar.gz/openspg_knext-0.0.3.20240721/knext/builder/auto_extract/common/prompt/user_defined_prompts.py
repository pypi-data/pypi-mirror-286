# -*- coding: utf-8 -*-
import copy
import json
from typing import Dict, List, Union

from pydantic import config
from knext.builder.operator.op import PromptOp
from knext.builder.operator.spg_record import SPGRecord
from knext.builder.auto_extract.model.chunk import Chunk, ChunkTypeEnum


def load_json(content):
    try:
        return json.loads(content)
    except json.JSONDecodeError as e:
        substr = content[: e.colno - 1]
        return json.loads(substr)


# wrapper of PromptOp
class Prompt(PromptOp):
    def __init__(self):
        self.prompt = {}

    def parse_result(self, line):
        return []

    def build_prompt(self, variables: Dict[str, str]) -> str:
        template = copy.deepcopy(self.prompt)

        if isinstance(variables, str):
            variables = {"input": variables}
        template.update(variables)
        self.variables = variables
        return json.dumps(template, ensure_ascii=False)

    def result_to_spgrecord(self, result: List):
        raise NotImplemented("result_to_spgrecord not implemented.")

    def parse_response(self, response: str, **kwargs) -> List[SPGRecord]:
        result = self.parse_result(response)
        if len(result) > 0:
            return self.result_to_spgrecord(result)
        return []


class SemanticSegPrompt(Prompt):
    def __init__(self):
        self.prompt = {
            "instruction": "\n请理解input字段中的文本内容，识别文本的结构和组成部分，并按照语义主题确定分割点，将其切分成互不重叠的若干小节。如果文章有章节等可识别的结构信息，请直接按照顶层结构进行切分。\n请按照schema定义的字段返回，包含小节摘要和小节起始点。须按照JSON字符串的格式回答。具体形式请遵从example字段中给出的若干例子。",
            "schema": {
                "小节摘要": "该小节文本的简单概括",
                "小节起始点": "该小节包含的原文的起点，控制在20个字左右。该分割点将被用于分割原文，因此必须可以在原文中找到！",
            },
            "input": "",
            "example": [
                {
                    "input": "周杰伦（Jay Chou），1979年1月18日出生于台湾省新北市，祖籍福建省永春县，华语流行乐男歌手、音乐人、演员、导演、编剧，毕业于淡江中学。\n2000年，在杨峻荣的推荐下，周杰伦开始演唱自己创作的歌曲。",
                    "output": [
                        {"小节摘要": "个人简介", "小节起始点": "周杰伦（Jay Chou），1979年1月18"},
                        {"小节摘要": "演艺经历", "小节起始点": "\n2000年，在杨峻荣的推荐下"},
                    ],
                },
                {
                    "input": "杭州市灵活就业人员缴存使用住房公积金管理办法（试行）\n为扩大住房公积金制度受益面，支持灵活就业人员解决住房问题，根据国务院《住房公积金管理条例》、《浙江省住房公积金条例》以及住房和城乡建设部、浙江省住房和城乡建设厅关于灵活就业人员参加住房公积金制度的有关规定和要求，结合杭州市实际，制订本办法。\n一、本办法适用于本市行政区域内灵活就业人员住房公积金的自愿缴存、使用和管理。\n二、本办法所称灵活就业人员是指在本市行政区域内，年满16周岁且男性未满60周岁、女性未满55周岁，具有完全民事行为能力，以非全日制、个体经营、新就业形态等灵活方式就业的人员。\n三、灵活就业人员申请缴存住房公积金，应向杭州住房公积金管理中心（以下称公积金中心）申请办理缴存登记手续，设立个人账户。\n ",
                    "output": [
                        {"小节摘要": "管理办法的制定背景和依据", "小节起始点": "为扩大住房公积金制度受益面"},
                        {"小节摘要": "管理办法的适用范围", "小节起始点": "一、本办法适用于本市行政区域内"},
                        {"小节摘要": "灵活就业人员的定义", "小节起始点": "二、本办法所称灵活就业人员是指"},
                        {
                            "小节摘要": "灵活就业人员缴存登记手续",
                            "小节起始点": "三、灵活就业人员申请缴存住房公积金",
                        },
                    ],
                },
            ],
        }

    def parse_result(self, result: Dict):
        llm_output = result["result"]
        content = result["content"]
        if isinstance(llm_output, str):
            llm_output = json.loads(llm_output)
        if isinstance(llm_output, dict) and "output" in llm_output:
            llm_output = llm_output["output"]
        print(f"llm_output[{type(llm_output)}] = {llm_output}")
        seg_info = []
        for seg_point in llm_output:
            print(f"seg_point = {seg_point}")
            if not isinstance(seg_point, dict):

                continue
            start = seg_point.get(
                "小节起始点",
            )
            if not isinstance(start, str):
                continue
            start = start.strip()
            # use first 10 charathers for split
            loc = content.find(start)
            if loc == -1:
                print(f"incorrect seg: {seg_point}")
                continue

            abstract = seg_point.get("小节摘要", None)
            seg_info.append((loc, abstract))

        seg_info.sort()
        print(f"seg_info = {seg_info}")
        locs = [x[0] for x in seg_info]
        abstracts = [x[1] for x in seg_info]
        locs.append(len(content))
        splitted = []
        for idx in range(len(abstracts)):
            start = locs[idx]
            end = locs[idx + 1]
            splitted.append(
                {
                    "name": abstracts[idx],
                    "content": content[start:end],
                    "length": end - start,
                }
            )

        return splitted

    def result_to_spgrecord(self, result: List):
        spg_records = []
        for item in result:
            tmp = SPGRecord("Chunk")
            tmp.upsert_properties(item)
            spg_records.append(tmp)
        return spg_records


class QwenUserManualQuestionExtractPrompt(Prompt):
    def __init__(self, manual_name):
        self.prompt = {
            "instruction": f"input字段是{manual_name}说明书的一部分内容。请你阅读该文档，站在用户的角度，提出一些该文档可以回答的问题，问题尽量要发散，多角度。数量最好在10个以上。请将结果以json list格式返回，具体请遵从example字段中给出的示例。",
            "example": {
                "input": """
开启点火开关时，仪表盘上的SRS警告灯亮起。发动机启动后，警告灯会在几秒钟内熄灭。
                """,
                "output": [
                    "开启点火开关时，SRS警告灯应该有什么反应？",
                    "发动机启动后，SRS警告灯不熄灭是正常的吗？",
                    "SRS警告灯亮起代表了什么？",
                    "",
                ],
            },
            "input": "",
        }

    def parse_result(self, result: Dict):
        return []


class QwenUserManualEntityExtractPrompt(Prompt):
    def __init__(self, manual_name):
        self.prompt = {
            "instruction": f"input字段是{manual_name}说明书的一部分内容。我需要基于该内容构建一个知识图谱。请你抽取出该部分说明书内容中所包含的实体，schema字段给出了你抽取出的实体需要包含的字段名以及含义。请返回json格式输出结果，须严格遵从example字段中给出的示例。不要输出任何非json格式的内容，如额外的解释说明。",
            "schema": {
                "名称": "实体的名称",
                "类型": "实体的类型，不得出现字段entity_types列出的类型以外的类型",
                "简介": "对实体的简单介绍",
            },
            "example": {
                "input": """
                自检系统包含电量检测功能，当电池耗尽时，仪表盘上的SRS警告灯亮起，表示需更换电池
                """,
                "output": [
                    {"名称": "电池", "类型": "耗材", "简介": "为SRS提供电力"},
                    {"名称": "仪表盘", "类型": "设备", "简介": "车辆内部的一个面板"},
                    {"名称": "SRS警告灯", "类型": "设备", "简介": "仪表盘上的一个指示灯"},
                    {"名称": "自检系统", "类型": "系统", "简介": "车辆上对工作状态进行检测的系统。"},
                    {"名称": "电量检测功能", "类型": "功能", "简介": "检测电量的功能"},
                ],
            },
            "input": "",
        }

    def standardize_entity(self, entity: Dict):
        if not isinstance(entity, dict):
            return None
        name = entity.get("名称", "")
        type_ = entity.get("类型", "")
        desc = entity.get("简介", "")
        if len(name) == 0:
            return None
        entity_types = self.variables["entity_types"]
        if type_ not in entity_types:
            return None
        return {
            "名称": name,
            "类型": type_,
            "简介": desc,
        }

    def parse_result(self, result: Dict):
        content = result["content"]
        llm_output = result["result"]
        output = []
        for item in llm_output:
            try:
                if isinstance(item, dict) and "output" in item:
                    item = item["output"]
                for entity in item:
                    tmp = self.standardize_entity(entity)
                    if isinstance(tmp, dict):
                        output.append(tmp)
            except Exception as e:
                print(f"failed to parse llm output: {item}, info: {e}")
        return output

    def result_to_spgrecord(self, result: List):
        output = []
        type_mapping = {"设备": "Device", "系统": "System", "耗材": "Consumable"}
        for item in result:
            tmp = SPGRecord(type_mapping[item["类型"]])
            tmp.upsert_properties({"name": item["名称"], "description": item["简介"]})
            output.append(tmp)
        return output


class QwenUserManualEntityAttributesExtractPrompt(Prompt):
    def __init__(self, manual_name):
        self.prompt = {
            "instruction": f"input字段是{manual_name}说明书的一部分内容，entities字段是input字段中抽取的实体，包含实体名称和实体类型。我需要基于此构建一个知识图谱。请你进一步从input字段中抽取出entities字段中实体的属性。请将结果以json list格式返回，具体请遵从example字段中给出的示例。",
            "schema": {
                "名称": "实体名称，需要在entities字段中",
                "属性名": "实体的属性名称",
                "属性值": "实体的属性值",
                "简介": "介绍当前实体的属性，如该属性代表的含义。也可以为空。",
            },
            "example": {
                "input": """
                在以下部分将介绍关于下列驾驶安全系统的信息：儿童防护锁（第67页）
                """,
                "entities": [
                    {"名称": "防抱死制动系统（ABS ）", "类型": "系统"},
                    {"名称": "后排车门", "类型": "设备"},
                    {"名称": "儿童防护锁", "类型": "设备"},
                    {"名称": "驾驶安全系统", "类型": "系统"},
                ],
                "output": [
                    {"名称": "儿童防护锁", "属性名": "页码", "属性值": "第67页"},
                ],
            },
            "input": "",
            "entities": "",
        }

    def standardize_entity_property(self, property_info: Dict):
        if not isinstance(property_info, dict):
            return None
        entity_name = property_info.get("名称", "")
        property_name = property_info.get("属性名", "")
        property_value = property_info.get("属性值", "")
        if len(entity_name) == 0 or len(property_name) == 0 or len(property_value) == 0:
            return None
        standard_entity = None
        for entity in self.variables["entities"]:
            if entity["名称"] == entity_name:
                standard_entity = entity
                break
        if standard_entity is None:
            return None

        desc = property_info.get("简介", "")
        return {
            "名称": standard_entity["名称"],
            "类型": standard_entity["类型"],
            "属性名": property_name,
            "属性值": property_value,
            "简介": desc,
        }

    def parse_result(self, result: Dict):
        content = result["content"]
        llm_output = result["result"]
        output = []
        for item in llm_output:
            try:

                if isinstance(item, dict) and "output" in item:
                    item = item["output"]
                for entity in item:
                    tmp = self.standardize_entity_property(entity)
                    if isinstance(tmp, dict):
                        output.append(tmp)
            except Exception as e:
                print(f"failed to parse llm output: {item}, info: {e}")

        return output

    def result_to_spgrecord(self, result: List):
        entities = {}
        for item in result:
            entity_name = item["名称"]
            entity_type = item["类型"]
            key = f"{entity_name}$${entity_type}"
            entity = entities.get(key, SPGRecord(entity_type))

            entity.upsert_properties({"name": entity_name, item["属性名"]: item["属性值"]})
            entities[key] = entity
        return list(entities.values())


class QwenUserManualEntityStateExtractPrompt(Prompt):
    def __init__(self, manual_name):
        self.prompt = {
            "instruction": f"input字段是{manual_name}说明书的一部分内容，entities字段是input字段中抽取的实体。我需要基于此构建一个知识图谱。请你进一步从input字段中抽取出entities字段中实体的状态。请将结果以json list格式返回，具体请遵从example字段中给出的示例。",
            "schema": {
                "名称": "实体名称，需要在entities字段中",
                "状态": "实体当前的状态",
                "简介": "介绍当前实体的状态，如导致该状态的原因，或者该状态代表的含义。也可以为空",
            },
            "example": {
                "input": """
                如果系统出现故障，SRS警告灯会在几秒钟内亮起。
                """,
                "entities": [{"名称": "SRS告警灯", "类型": "设备"}],
                "output": [
                    {"名称": "SRS告警灯", "状态": "亮起", "简介": "SRS警告灯亮起表示系统有故障"},
                    {
                        "名称": "SRS告警灯",
                        "状态": "熄灭",
                        "简介": "发动机启动后警告灯在几秒钟内熄灭",
                    },
                ],
            },
            "input": "",
            "entities": "",
        }

    def standardize_entity_state(self, property_info: Dict):
        if not isinstance(property_info, dict):
            return None
        entity_name = property_info.get("名称", "")
        state = property_info.get("状态", "")
        if len(entity_name) == 0 or len(state) == 0:
            return None
        standard_entity = None
        for entity in self.variables["entities"]:
            if entity["名称"] == entity_name:
                standard_entity = entity
                break
        if standard_entity is None:
            return None

        desc = property_info.get("简介", "")
        return {
            "名称": standard_entity["名称"],
            "类型": standard_entity["类型"],
            "状态": state,
            "简介": desc,
        }

    def parse_result(self, result: Dict):
        content = result["content"]
        llm_output = result["result"]
        output = []
        for item in llm_output:
            try:

                if isinstance(item, dict) and "output" in item:
                    item = item["output"]
                for entity_state in item:
                    tmp = self.standardize_entity_state(entity_state)
                    if isinstance(tmp, dict):
                        output.append(tmp)
            except Exception as e:
                print(f"failed to parse llm output: {item}, info: {e}")

        return output

    def result_to_spgrecord(self, result: List):
        entities = {}
        for item in result:
            entity_name = item["名称"]
            entity_type = item["类型"]
            key = f"{entity_name}$${entity_type}"
            entity = entities.get(key, SPGRecord(entity_type))
            entity.upsert_properties({"name": entity_name, "state": item["状态"]})
            entities[key] = entity
        return list(entities.values())


class QwenUserManualEventExtractPrompt(Prompt):
    def __init__(self, manual_name):
        self.prompt = {
            "instruction": f"input字段是{manual_name}说明书的一部分内容，entities字段是input字段中抽取的实体，events字段是我关注的事项列表。我需要基于此构建一个知识图谱。请帮我从input字段中抽取出其中包含在events列表中的所有事项，以及事项中涉及的所有实体。请将结果以json list格式返回，具体请遵从example字段中给出的示例。",
            "schema": {
                "名称": "事项名称",
                "事项类型": "事项所属的类型，需要在events字段中",
                "实体": "事项涉及的实体列表，实体需要出现在entities字段中",
                "事项简介": "事项内容的简短介绍",
            },
            "example": {
                "input": """
'当点火开关开启且发动机运转时， SRS功能将定时执行自测试。因此，可以及时探测到故障。开启点火开关时， 仪表盘上的SRS警告灯亮起。发动机启动后，警告灯会在几秒钟内熄灭。'
                """,
                "entities": [
                    {"名称": "SRS告警灯", "类型": "设备"},
                    {"名称": "发动机", "类型": "设备"},
                    {"名称": "点火开关", "类型": "设备"},
                ],
                "output": [
                    {
                        "名称": "SRS功能自测试",
                        "事项类型": "功能描述",
                        "实体": ["安全气囊(SRS)", "点火开关"],
                        "事项简介": "在点火开关开启且发动机运转时，SRS功能将执行自测试以及时探测故障。",
                    },
                ],
            },
            "input": "",
            "entities": "",
            "events": ["功能描述", "使用前的准备", "操作步骤", "维护和保养", "故障排除", "安全警告", "问题与解答"],
        }

    def standardize_event(self, event: Dict):
        if not isinstance(event, dict):
            return None
        event_name = event.get("名称", "")
        event_type = event.get("事项类型", "")
        entities = event.get("实体", [])
        standard_entities = []

        for entity in self.variables["entities"]:
            if entity["名称"] in entities:
                standard_entities.append(entity)

        desc = event.get("事项简介", "")
        if len(event_name) == 0 or len(event_type) == 0:
            return None
        if isinstance(entities, str):
            entities = [entities]
        if not isinstance(entities, list):
            return None
        return {
            "name": event_name,
            "type": event_type,
            "entities": [x["名称"] for x in standard_entities],
            "description": desc,
        }

    def parse_result(self, result: Dict):
        content = result["content"]
        llm_output = result["result"]
        output = []
        for item in llm_output:
            try:

                if isinstance(item, dict) and "output" in item:
                    item = item["output"]
                for entity in item:
                    tmp = self.standardize_event(entity)
                    # make sure entity exists in content
                    if isinstance(tmp, dict):
                        output.append(tmp)
            except Exception as e:
                print(f"failed to parse llm output: {item}, info: {e}")

        return output

    def result_to_spgrecord(self, result: List):
        output = []
        for item in result:
            tmp = SPGRecord("Event")
            tmp.upsert_properties(item)
            output.append(tmp)
        return output


class QwenUserManualEntityRelationExtractPrompt(Prompt):
    def __init__(self, manual_name):
        self.prompt = {
            "instruction": f"input字段是{manual_name}说明书的一部分内容，entities字段是input字段中抽取的实体。我需要基于此构建一个知识图谱。请帮我从input字段中抽取出entities中实体两两之间存在的关系，关系以[主体,客体,谓词,简介]四元组表示，其含义参见schema字段。请将结果以json格式返回，具体请遵从example字段中给出的示例。",
            "schema": {
                "主体": "主体名称，需要包含在entities字段中",
                "客体": "客体名称，需要包含在entities字段中",
                "谓词": "表示主体和客体之间的关系",
                "简介": "该关系的简短介绍",
            },
            "example": {
                "input": """
                儿童防护锁属于车辆安全系统的一部分，后排车门上的儿童防护锁可以单独锁止后排车门。
                """,
                "entities": ["儿童防护锁", "后排车门", "车辆安全系统"],
                "output": [
                    {
                        "主体": "儿童防护锁",
                        "客体": "后排车门",
                        "谓词": "锁止",
                        "简介": "儿童防护锁可单独锁止后排车门",
                    },
                    {
                        "主体": "儿童防护锁",
                        "客体": "车辆安全系统",
                        "谓词": "包含于",
                        "简介": "儿童防护锁属于车辆安全系统的一部分",
                    },
                ],
            },
            "input": "",
            "entities": "",
        }

    def standardize_relation(self, relation: Dict):
        if not isinstance(relation, dict):
            return None
        subject = relation.get("主体", "")
        predicate = relation.get("谓词", "")
        object_ = relation.get("客体", [])
        desc = relation.get("简介", "")
        if len(subject) == 0 or len(predicate) == 0 or len(object_) == 0:
            return None

        standard_subject = None
        for entity in self.variables["entities"]:
            if entity["名称"] == subject:
                standard_subject = entity
                break

        standard_object = None
        for entity in self.variables["entities"]:
            if entity["名称"] == object_:
                standard_object = entity
                break

        if standard_subject is None or standard_object is None:
            return None

        return {
            "subject": standard_subject,
            "predicate": predicate,
            "object": standard_object,
            "description": desc,
        }

    def parse_result(self, result: Dict):
        content = result["content"]
        llm_output = result["result"]
        output = []
        for item in llm_output:
            try:

                if isinstance(item, dict) and "output" in item:
                    item = item["output"]
                for relation in item:
                    tmp = self.standardize_relation(relation)
                    if isinstance(tmp, dict):
                        output.append(tmp)
            except Exception as e:
                print(f"failed to parse llm output: {item}")

        return output

    def result_to_spgrecord(self, result: List):
        output = []
        for item in result:

            object_ = item["object"]
            tmp = SPGRecord(object_["类型"])
            tmp.upsert_property("name", object_["名称"])
            output.append(tmp)

            subject = item["subject"]
            tmp = SPGRecord(subject["类型"])
            tmp.upsert_property("name", subject["名称"])
            tmp.upsert_property(item["predicate"], object_["名称"])
            output.append(tmp)
        return output


class QwenFileReqPrompt(Prompt):
    def __init__(self):
        self.prompt = {
            "instruction": "input字段给出了办理各种政务业务所需材料的文档内容，里面包含受理特定业务时所需要提供的材料文件。请首先分析文本中包含的各种业务办理的前提条件。如果有前提条件，则对每个前提条件逐个抽取出所需文件的信息；如果没有前提条件，那么直接整体抽取出所需文件的信息。结果照schema字段中定义的格式进行结构化，每个字段的含义参见schema字段的介绍。请按照JSON字符串的格式回答。返回格式也是json，请遵从example1和example2字段中给出的例子。",
            "schema": [
                {
                    "前提条件(字符串形式，表示办理业务的前提条件。对同一个业务事项，不同前提条件可能需要的材料也不同。如果只有一个前提条件，直接填无": [
                        {
                            "文件名(表示材料的名称，如本人身份证明, 农业银行有效一类借记卡)": "",
                            "文件要求(所需文件的形式，一定要在候选集[无,原件, 复印件, 原件与复印件, 原件或复印件,电子凭证]中四选一)": "",
                            "复印件份数(表示复印件的份数，如1,2,3，如果不需要复印件，则填0)": "",
                        }
                    ],
                }
            ],
            "example": {
                "input": """
贷款合同和银行出具的还款流水及利息还款凭证原件一份；（个人创业担保贷款贴息申领需提供）|_|《个人创业“一件事”联办申请表》|_|吸纳人员社保缴纳凭证原件一份（创业带动就业补贴申领需提供）|_|申请人（重点人群）身份印证材料原件和复印件各一份（一次性创业补贴申领、一次性创业社保补贴申领、创业带动就业补贴申领需提供）
                """,
                "output": [
                    {
                        "无": [
                            {"文件名": "个人创业“一件事”联办申请表", "文件要求": "原件", "复印件份数": 0},
                        ],
                        "个人创业担保贷款贴息申领": [
                            {"文件名": "贷款合同和银行出具的还款流水", "文件要求": "原件", "复印件份数": 0},
                            {"文件名": "贷款合同和银行出具的利息还款凭证", "文件要求": "原件", "复印件份数": 0},
                        ],
                        "创业带动就业补贴申领": [{"文件名": "吸纳人员社保缴纳凭证", "文件要求": "原件", "复印件份数": 0}],
                        "一次性创业补贴申领": [
                            {"文件名": "申请人（重点人群）身份印证材料", "文件要求": "原件和复印件", "复印件份数": 1}
                        ],
                        "一次性创业社保补贴申领": [
                            {"文件名": "申请人（重点人群）身份印证材料", "文件要求": "原件和复印件", "复印件份数": 1}
                        ],
                        "创业带动就业补贴申领需提供": [
                            {"文件名": "申请人（重点人群）身份印证材料", "文件要求": "原件和复印件", "复印件份数": 1}
                        ],
                    }
                ],
            },
            "input": "",
        }

    def check_terminate(self, file_info):
        for key in file_info.keys():
            if key.endswith("文件名") or key.endswith("文件要求") or key.endswith("复印件份数"):
                return True
        return False

    def format_prerequisites(self, prerequisites, prefix=""):
        output = {}
        if not isinstance(prerequisites, dict):
            return output
        for prerequest, files in prerequisites.items():

            if not isinstance(files, list):
                files = [files]
            if self.check_terminate(files[0]):
                output[prerequest] = files
            else:
                tmp = []
                for file_info in files:
                    file_info = self.format_prerequisites(file_info, prefix=prerequest)
                    for k, v in file_info.items():
                        output[prerequest + "->" + k] = v
        return output

    def postprocess(self, output):
        processed_item = copy.deepcopy(output)
        prerequisites = processed_item.pop("prerequisites", {})
        if len(prerequisites) == 0:
            return output
        if isinstance(prerequisites, list):
            prerequisites = prerequisites[0]
        if isinstance(prerequisites, str):
            try:
                prerequisites = json.loads(prerequisites.replace("'", '"'))
            except Exception as e:
                return output
        try:
            prerequisites = self.format_prerequisites(prerequisites)
            tmp = {}
            for k, v in prerequisites.items():
                if len(v) == 0:
                    continue
                if k.endswith("->无"):
                    k = "无"
                tmp[k] = v
            prerequisites = tmp
        except Exception as e:
            print(f"failed to format prerequisites, info: {e}")

        # nos = prerequisites.pop("无", [])
        nos = []
        processed_prerequisites = {}
        for prerequest, files in prerequisites.items():
            tmp = []
            if not isinstance(files, list):
                files = [files]
            for file_info in files:
                file_name = file_info.get("文件名", "").strip()
                file_req = file_info.get("文件要求", None).strip()
                if file_req in [
                    "无",
                    "",
                    "免提交",
                    "不需要提供",
                    "不提交",
                    "无需",
                    "无需提供",
                    "无需提交",
                    "由经办机构自行获取",
                    "填写",
                    "登记",
                    "提交或者核验",
                    "缴回",
                ]:
                    file_req = "无"
                elif file_req in ["电子凭证", "电子版", "上传到在线文件夹中", "上传"]:
                    file_req = "电子版"
                elif "原件" not in file_req and "复印件" not in file_req:
                    print(f"invalid file_req {file_info}, fix to 原件")
                    file_req = "原件"

                try:
                    num_copies = int(file_info.get("复印件份数", 0))
                except:
                    num_copies = 0
                if num_copies == 0 and "复印" in file_req:
                    num_copies = 1
                if "复印" not in file_req:
                    num_copies = 0
                    # print(f"invalid num_copies, {file_info} fix to 1")
                if prerequest == "无":
                    nos.append(
                        {"文件名": file_name, "文件要求": file_req, "复印件份数": num_copies}
                    )
                else:
                    if file_name.strip() == prerequest.strip():
                        nos.append(
                            {
                                "文件名": file_name,
                                "文件要求": file_req,
                                "复印件份数": num_copies,
                            }
                        )
                    else:
                        tmp.append(
                            {
                                "文件名": file_name,
                                "文件要求": file_req,
                                "复印件份数": num_copies,
                            }
                        )
            if len(tmp) > 0:
                processed_prerequisites[prerequest] = tmp
        processed_prerequisites["无"] = nos
        processed_item["prerequisites"] = processed_prerequisites
        return processed_item

    def parse_result(self, result: Dict):
        content = result["content"]
        llm_output = result["result"]

        parsed = []
        for item in llm_output:
            if isinstance(item, dict) and "output" in item:
                item = item["output"]
            if isinstance(item, list):
                parsed += item
            else:
                parsed.append(item)

        entry_name = result["GovernmentService"]
        location = result["AdministrativeArea"]
        tmp = {}
        tmp["prerequisites"] = parsed
        tmp["GovernmentService"] = entry_name
        tmp["AdministrativeArea"] = location
        tmp = [self.postprocess(tmp)]
        return tmp

    def result_to_spgrecord(self, result):
        records = []

        for item in result:
            entry_name = item["GovernmentService"]
            location = item["AdministrativeArea"]
            prerequisites = item["prerequisites"]
            events = {}
            for sub_event, files in prerequisites.items():
                required_files = []
                if sub_event == "无":
                    cur_event_name = entry_name
                else:
                    cur_event_name = f"{entry_name}-{sub_event}"
                event = events.get(cur_event_name, SPGRecord("GovernmentService"))
                event.upsert_property("name", cur_event_name)
                event.upsert_property("location", location)
                for file_ in files:
                    tmp = SPGRecord("Material")
                    tmp.upsert_properties(
                        {
                            "name": file_["文件名"],
                            "requires": file_.get("文件要求"),
                            "numberOfCopies": file_.get("复印件份数", 0),
                            "prerequisite": cur_event_name,
                        }
                    )
                    records.append(tmp)
                    required_files.append(file_["文件名"])
                event.upsert_property("requiredMaterial", ",".join(required_files))
                events[cur_event_name] = event

            main_event = None
            sub_events = []
            for k, v in events.items():
                if k == "无":
                    main_event = v
                else:
                    sub_events.append(v)
                    records.append(v)
            if main_event is None:
                main_event = SPGRecord("GovernmentService")
                main_event.upsert_property("name", entry_name)
            if len(sub_events) > 0:
                sub_service_names = []
                for sub_event in sub_events:
                    service_name = sub_event.get_property("name")
                    if service_name != entry_name:
                        sub_service_names.append(service_name)
                main_event.upsert_property("subService", sub_service_names)

            records.append(main_event)
        return records


class QwenApplyReqPrompt(Prompt):
    def __init__(self):
        self.prompt = {
            "instruction": "input字段给出了各种政务业务受理条件的文档内容，里面包含受理特定业务所需要满足的必要条件和可选条件。请从文本中逐个拆分并抽取出这些条件，并结构化成schema字段中定义的[subject, predicate, object, status]四元组格式，每个字段的含义参见schema字段的介绍。请按照JSON字符串的格式回答。返回格式请遵从example字段中给出的例子。",
            "schema": {
                "subject": "表示某个业务的受理条件，一定要以以“受理条件”结尾",
                "predicate": "表示某个业务的其中一个受理条件，如生产经营原种注册资本, 年龄条件等",
                "object": "表示predicate必须满足的限制",
                "status": "表示该条件是否一定要满足，一定是“必须满足”或“满足其一”两者之一",
            },
            "example": {
                "input": "长沙居住证申领的受理条件如下：公民离开常住户口所在地，到其他城市居住半年以上，符合有合法稳定就业、合法稳定住所、连续就读条件之一的，可以按照《居住证暂行条例》的规定申领居住证。",
                "output": [
                    ["长沙居住证申领受理条件", "居住时长", ["半年以上"], "必须满足"],
                    ["长沙居住证申领受理条件", "符合条件", ["合法稳定就业", "合法稳定住所", "连续就读"], "满足其一"],
                ],
            },
            "input": "",
        }

    def standardize_result(self, condition: List[str]):
        if len(condition) != 4:
            return None
        subject, predicate, object, status = condition

        if status.strip() not in ["必须满足", "满足其一"]:
            return None
        if isinstance(object, str):
            object = [object]
        if len(object) == 1:
            status = "必须满足"

        return {"事项名称": subject, "条件名称": predicate, "条件值": object, "约束": status}

    def parse_result(self, result: Dict):
        content = result["content"]
        llm_output = result["result"]
        output = []
        for item in llm_output:
            try:
                if isinstance(item, dict):
                    item = item["output"]
                if isinstance(item, list):
                    for cond in item:
                        tmp = self.standardize_result(cond)
                        if tmp is not None:
                            output.append(tmp)
                else:
                    tmp = self.standardize_result(item)
                    if tmp is not None:
                        output.append(item)
            except Exception as e:
                print(f"failed to parse llm output: {item}, info: {e}")

        for item in output:
            item["GovernmentService"] = result["GovernmentService"]
        return output

    def result_to_spgrecord(self, result):
        records = []

        for item in result:
            entry_name = item["事项名称"]
            cond_name = item["条件名称"]
            value = item["条件值"]
            constraint = item["约束"]
            tmp = SPGRecord("ApplyCondition")
            tmp.upsert_properties(
                {
                    "name": f"{entry_name}-{cond_name}",
                    "value": ",".join(value) if isinstance(value, list) else value,
                    "constraint": constraint,
                }
            )
            records.append(tmp)

        entry_name = result[0]["GovernmentService"]
        event_record = SPGRecord("GovernmentService")
        event_record.upsert_property("name", entry_name)
        event_record.upsert_property(
            "conditions", ",".join([x.get_property("name") for x in records])
        )

        records.append(event_record)
        return records


class QwenPersonRelationPrompt(Prompt):
    def __init__(self):
        self.prompt = {
            "instruction": "你是专门进行人物关系提取的专家。请从中抽取出符合schema定义的人物关系，不存在的事件返回空列表，不存在的论元返回null。请按照JSON字符串的格式回答。具体形式请遵从example字段中给出的例子。",
            "schema": [
                "主体人物",
                "人物关系",
                "客体人物",
                "时间",
            ],
            "input": "",
            "example": {
                "input": "金钹法王原型是蜈蚣精，手拿武器金钹，称号是凤凰山大寨主，是电视剧《新白娘子传奇》中的人物。为报二十年前白素贞杀死自己的儿子蜈蚣精之仇，千方百计陷害白白素贞之子许仕林，最后被观音击杀。",
                "output": [
                    {
                        "主体人物": "金钹法王",
                        "人物关系": "仇人",
                        "客体人物": "白素贞",
                        "时间": "null",
                    },
                    {
                        "主体人物": "金钹法王",
                        "人物关系": "仇人",
                        "客体人物": "许仕林",
                        "时间": "null",
                    },
                    {
                        "主体人物": "白素贞",
                        "人物关系": "儿子",
                        "客体人物": "许仕林",
                        "时间": "null",
                    },
                    {
                        "主体人物": "观音",
                        "人物关系": "击杀",
                        "客体人物": "金钹法王",
                        "时间": "null",
                    },
                ],
            },
        }

    def parse_result(self, line):
        content = json.loads(line)
        result = content["result"]
        output = []
        for item in result:
            if isinstance(item, dict):
                item = item["output"]
            elif isinstance(item, list):
                output += item
            else:
                output.append(item)
        paragraph_id = content["paragraph_id"]
        entity_id = content["entity_id"]
        entry_name = content["entry_name"]
        for item in output:
            item["paragraph_id"] = paragraph_id
            item["entity_id"] = entity_id
            item["entry_name"] = entry_name
        return output


class QwenSpoPrompt(Prompt):
    def __init__(self):
        self.prompt = {
            "instruction": "你是专门进行知识图谱三元组的专家。请从中抽取出所有以[subject, subject_type, predicate, object, object_type, time]六元组表示的人物或物品属性。注意：1. subject_type和object_type只能是[人物,地点,物品,属性]之一, 2. predicate不能是动词（如占领，攻克，召集等），因为动词不表示属性。请按照JSON字符串的格式回答。具体形式请遵从example字段中给出的例子。",
            "input": "",
            "example": {
                "input": "金钹法王原型是蜈蚣精，手拿武器金钹，称号是凤凰山大寨主，是电视剧《新白娘子传奇》中的人物。为报二十年前青白二蛇杀死自己的儿子蜈蚣精之仇，千方百计陷害白蛇之子许仕林，最后被观音击杀。",
                "output": [
                    ["金钹法王", "人物", "原型", "蜈蚣精", "人物", "null"],
                    ["金钹法王", "人物", "武器", "金钹", "物品", "null"],
                    ["金钹法王", "人物", "出自", "新白娘子传奇", "物品", "null"],
                    ["金钹法王", "人物", "住所", "凤凰山", "地点", "null"],
                    ["金钹法王", "人物", "称号", "凤凰山大寨主", "属性", "null"],
                ],
            },
        }

    def parse_result(self, line):
        content = json.loads(line)
        result = content["result"]
        spos = []
        for item in result:
            if isinstance(item, dict):
                item = item["output"]
            elif isinstance(item, list):
                spos += item
            else:
                spos.append(item)
        paragraph_id = content["paragraph_id"]
        entity_id = content["entity_id"]
        entry_name = content["entry_name"]
        output = []
        for item in spos:
            if len(item) == 6 and None not in item[:5]:
                output.append(
                    {
                        "paragraph_id": paragraph_id,
                        "entity_id": entity_id,
                        "entry_name": entry_name,
                        "spo": item,
                    }
                )
        return output


class QwenExperiencePrompt(Prompt):
    def __init__(self):
        self.prompt = {
            "instruction": "你是专门进行事件提取的专家。请从中抽取出符合schema定义的事件，不存在的事件返回空列表，不存在的论元返回null。请按照JSON字符串的格式回答。具体形式请遵从example字段中给出的例子。注意，事件摘要控制在20字以内！！",
            "schema": [
                "时间",
                "地点",
                "事件类型",
                "主体人物",
                "摘要",
                "相关人物",
                "相关物品",
            ],
            "input": "",
            "example": {
                "input": "主体人物：张无忌。张无忌被布袋和尚用乾坤一气袋掳上明教总坛光明顶，却在袋中把《九阳真经》最后一关冲破，神功遂得以大成。又因追赶成昆而与小昭走进秘道获得《乾坤大挪移》。",
                "output": [
                    {
                        "时间": "null",
                        "地点": "明教总坛光明顶",
                        "事件类型": "习得技能",
                        "主体人物": "张无忌",
                        "摘要": " 神功大成",
                        "相关人物": ["布袋和尚"],
                        "相关物品": ["乾坤一气袋", "九阴真经"],
                    },
                    {
                        "时间": "null",
                        "地点": "密道",
                        "事件类型": "习得技能",
                        "主体人物": "张无忌",
                        "摘要": " 获得乾坤大挪移",
                        "相关人物": ["成昆", "小昭"],
                        "相关物品": ["乾坤大挪移"],
                    },
                ],
            },
        }

    def parse_result(self, line):
        content = json.loads(line)
        result = content["result"]
        output = []
        for item in result:
            if isinstance(item, dict):
                item = item["output"]
            elif isinstance(item, list):
                output += item
            else:
                output.append(item)
        paragraph_id = content["paragraph_id"]
        entity_id = content["entity_id"]
        entry_name = content["entry_name"]
        for item in output:
            item["paragraph_id"] = paragraph_id
            item["entity_id"] = entity_id
            item["entry_name"] = entry_name
        return output


class HummingPrompt(Prompt):
    def __init__(self):
        self.prompt = {
            "instruction": "你是专门进行事件提取的专家。请从input中抽取出符合schema定义的事件，不存在的事件返回空列表，不存在的论元返回null。请按照JSON字符串的格式回答。",
            "schema": [
                {
                    "事业履历事件": "人物的学习、工作、职务、事业相关的经历",
                    "trigger": True,
                    "arguments": {
                        "行为": "描述事件中人物入学、入职、出道、参演作品、学习技能、达成成就等的短语",
                        "主体人物": "事件的主体",
                        "职位": "描述主体人物担任的职位",
                        "时间": "事件发生的时间，包括年份、季节、完整的年月日等",
                        "地点": "事件发生的地点（包括地名、地标名称、景点名称等）、组织机构（公司、学校、帮派等）",
                        "事件摘要": "整个事件经历的简要描述，最好10个字以内",
                    },
                },
                {
                    "人生经历事件": "人物的出生、结婚、怀孕、生子、死亡等关于个人生活经历的事件",
                    "trigger": True,
                    "arguments": {
                        "行为": "描述事件中行为的动词或动词短语",
                        "主体人物": "事件的主体",
                        "时间": "描述事件发生的具体时间，可以是具体日期或相对时间，也可以包含地点信息和具体的日子和星期。",
                        "地点": "事件发生的具体地点，比如城市、行政区划。",
                        "事件摘要": "整个事件经历的简要描述，最好10个字以内",
                        "客体人物": "事件中除了主体之外的其他人物",
                    },
                },
            ],
            "input": "",
        }

    def parse_result(self, line):
        content = json.loads(line)
        result = content["result"]
        output = []
        for item in result:
            item = load_json(item)
            item = item.get("事业履历事件", []) + item.get("人生经历事件", [])
            for event in item:
                output.append(event["arguments"])
        paragraph_id = content["paragraph_id"]
        entity_id = content["entity_id"]
        entry_name = content["entry_name"]
        for item in output:
            item["paragraph_id"] = paragraph_id
            item["entity_id"] = entity_id
            item["entry_name"] = entry_name
        return output
