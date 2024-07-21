# -*- coding: utf-8 -*-

import re
import copy
import json
from typing import Dict, List, Union

from pydantic import config
from knext.builder.operator.op import PromptOp
from knext.builder.operator.spg_record import SPGRecord
from knext.builder.auto_extract.model.chunk import Chunk, ChunkTypeEnum


def find_json_strings(text):
    pattern = r"```json\n(.*?)\n```"
    matches = re.findall(pattern, text, re.DOTALL)
    return matches


def load_json(content):
    try:
        json_strings = find_json_strings(content)
        if len(json_strings) == 1:
            return json.loads(json_strings[0])
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
        if result is None:
            return result
        if len(result) > 0:
            return self.result_to_spgrecord(result)
        return []


class EntityExtractPrompt(Prompt):
    def __init__(self, name: str):
        self.prompt = {
            "instruction": f"input字段是{name}的一部分内容，我需要基于其构建一个知识图谱。请你尽可能多抽取出该部分内容中包含的实体，schema字段给出了你抽取出的实体需要包含的字段名以及含义。请返回json格式输出结果。不要输出任何非json格式的内容，如额外的解释说明。",
            "schema": {
                "名称": "实体的名称",
                "类型": "实体的类型",
            },
            "example": {
                "input": """
                周杰伦凭借专辑《范特西》获得第13届台湾金曲奖最佳专辑制作人奖，并举行The One世界巡回演唱会
                """,
                "output": [
                    {"名称": "周杰伦", "类型": "人物"},
                    {"名称": "《范特西》", "类型": "专辑"},
                    {"名称": "The One", "类型": "演出"},
                    {"名称": "台湾金曲奖", "类型": "奖项"},
                    {"名称": "最佳专辑制作人奖", "类型": "奖项"},
                    {"名称": "台湾", "类型": "地点"},
                ],
            },
            "input": "",
        }

    def standardize_entity(self, entity: Dict):
        if not isinstance(entity, dict):
            return None
        name = entity.get("名称", "").lower()
        type_ = entity.get("类型", "")
        desc = entity.get("描述", "")
        if len(name) == 0:
            return None
        entity_types = self.variables.get("entity_types", None)
        if entity_types and type_ not in entity_types:
            return None
        return {
            "名称": name,
            "类型": type_,
            "描述": desc,
        }

    def parse_result(self, result: Dict):
        content = result["content"]
        llm_output = result["result"]
        output = []
        for item in llm_output:
            try:
                if isinstance(item, str):
                    item = load_json(item)
                if isinstance(item, dict) and "output" in item:
                    item = item["output"]
                for entity in item:
                    tmp = self.standardize_entity(entity)
                    if isinstance(tmp, dict):
                        output.append(tmp)
            except Exception as e:
                print(f"failed to parse llm output: {item}, info: {e}")
                return None
        return output

    def result_to_spgrecord(self, result: List):
        output = []
        for item in result:
            tmp = SPGRecord(item["类型"])
            tmp.upsert_properties({"name": item["名称"], "description": item["描述"]})
            output.append(tmp)
        return output


class EntityExtractPromptV2(Prompt):
    def __init__(self, name: str):
        self.prompt = {
            "instruction": f"input字段是{name}的一部分内容，我需要基于其构建一个知识图谱。entities字段是已经抽取出的实体，请你尽可能多抽取出该部分内容中包含的entities之外的所有实体，schema字段给出了你抽取出的实体需要包含的字段名以及含义。请返回json格式输出结果，须严格遵从example字段中给出的示例。不要输出任何非json格式的内容，如额外的解释说明。",
            "schema": {
                "名称": "实体的名称",
                "类型": "实体的类型，不得出现字段entity_types列出的类型以外的类型",
                "描述": "对实体的简单介绍",
            },
            "example": {
                "input": """
                周杰伦凭借专辑《范特西》获得第13届台湾金曲奖最佳专辑制作人奖，并举行The One世界巡回演唱会
                """,
                "entity_types": {
                    "人物": "具有特定身份、角色或特征的个人",
                    "地点": "特定的地理位置或场所",
                    "机构": "人或团体的集合，如政府机构、公司、学校、社团、俱乐部、杂志社等",
                    "作品": "文学、艺术、科学或其他领域的创作",
                    "演出": "在观众面前进行的现场表演活动，如演唱会等",
                    "场馆": "用于举行活动的地点",
                    "奖项": "对个人或团体在某一领域或活动中表现卓越的认可和奖励",
                },
                "entities": [
                    {"名称": "周杰伦", "类型": "人物"},
                    {"名称": "《范特西》", "类型": "设备"},
                    {"名称": "The One", "类型": "演出"},
                ],
                "output": [
                    {"名称": "台湾金曲奖", "类型": "奖项", "描述": "音乐类奖项"},
                    {"名称": "台湾", "类型": "地点", "描述": "中国的一个省份"},
                ],
            },
            "input": "",
        }

    def standardize_entity(self, entity: Dict):
        if not isinstance(entity, dict):
            return None
        name = entity.get("名称", "").lower()
        type_ = entity.get("类型", "")
        desc = entity.get("描述", "")
        if len(name) == 0:
            return None
        entity_types = self.variables["entity_types"]
        if type_ not in entity_types:
            return None
        return {
            "名称": name,
            "类型": type_,
            "描述": desc,
        }

    def parse_result(self, result: Dict):
        content = result["content"]
        llm_output = result["result"]
        output = []
        for item in llm_output:
            try:
                if isinstance(item, str):
                    item = load_json(item)
                if isinstance(item, dict) and "output" in item:
                    item = item["output"]
                for entity in item:
                    tmp = self.standardize_entity(entity)
                    if isinstance(tmp, dict):
                        output.append(tmp)
            except Exception as e:
                print(f"failed to parse llm output: {item}, info: {e}")
                return None
        return output

    def result_to_spgrecord(self, result: List):
        output = []
        for item in result:
            tmp = SPGRecord(item["类型"])
            tmp.upsert_properties({"name": item["名称"], "description": item["描述"]})
            output.append(tmp)
        return output


class EntityAttributesExtractPrompt(Prompt):
    def __init__(self, name):
        self.prompt = {
            "instruction": f"input字段是{name}的一部分内容，entities字段是input字段中抽取的实体，包含实体名称和实体类型。我需要基于此构建一个知识图谱。请你进一步从input字段中抽取出entities字段中实体的属性。请将结果以json list格式返回，具体请遵从example字段中给出的示例。",
            "schema": {
                "名称": "实体名称，需要在entities字段中",
                "属性名": "实体的属性名称。注意属性名不能是动词如结婚,发表，需要改成对应的名词表述：结婚->配偶, 发表->发表作品！",
                "属性值": "实体的属性值",
                "描述": "介绍当前实体的属性，如该属性代表的含义。也可以为空。",
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

        desc = property_info.get("描述", "")
        return {
            "名称": standard_entity["名称"].lower(),
            "类型": standard_entity["类型"],
            "属性名": property_name,
            "属性值": property_value,
            "描述": desc,
        }

    def parse_result(self, result: Dict):
        content = result["content"]
        llm_output = result["result"]
        output = []
        for item in llm_output:
            try:
                if isinstance(item, str):
                    item = load_json(item)

                if isinstance(item, dict) and "output" in item:
                    item = item["output"]
                for entity in item:
                    tmp = self.standardize_entity_property(entity)
                    if isinstance(tmp, dict):
                        output.append(tmp)
            except Exception as e:
                print(f"failed to parse llm output: {item}, info: {e}")
                return None
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


class EntityAttributeFilterExtractPrompt(Prompt):
    def __init__(self, name):
        self.prompt = {
            "instruction": f"input字段是{name}的一部分内容，attributes字段是input字段中抽取的实体的属性。请你基于文本内容对这些属性过滤，删除不适合作为知识图谱构建的属性值，并返回剩余结果。判断原则：1. 属性名不能是动词；2. 属性描述的不能是一个事件，如主演电影， 请将结果以json list格式返回，具体请遵从example字段中给出的示例。",
            "example": {
                "input": """
                在以下部分将介绍关于下列驾驶安全系统的信息：儿童防护锁（第67页），用于锁止车门。
                """,
                "attributes": [
                    {"名称": "儿童防护锁", "属性名": "页码", "属性值": "第67页"},
                    {"名称": "儿童防护锁", "属性名": "锁止", "属性值": "车门"},
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

        desc = property_info.get("描述", "")
        return {
            "名称": standard_entity["名称"],
            "类型": standard_entity["类型"],
            "属性名": property_name,
            "属性值": property_value,
            "描述": desc,
        }

    def parse_result(self, result: Dict):
        content = result["content"]
        llm_output = result["result"]
        output = []
        for item in llm_output:
            try:
                if isinstance(item, str):
                    item = load_json(item)

                if isinstance(item, dict) and "output" in item:
                    item = item["output"]
                for entity in item:
                    tmp = self.standardize_entity_property(entity)
                    if isinstance(tmp, dict):
                        output.append(tmp)
            except Exception as e:
                print(f"failed to parse llm output: {item}, info: {e}")
                return None
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


class EntityRelationExtractPrompt(Prompt):
    def __init__(self, name):
        self.prompt = {
            "instruction": f"input字段是{name}的一部分内容，entities字段是input字段中抽取的实体。我需要基于此构建一个知识图谱。请帮我从input字段中尽可能多地抽取出entities中实体两两之间存在的关系，越多越好。关系以[主体,客体,谓词,属性,简介]五元组表示，其含义参见schema字段。请将结果以json格式返回，具体请遵从example字段中给出的示例。",
            "schema": {
                "主体": "主体，需要包含在entities字段中",
                "客体": "客体名称，需要包含在entities字段中",
                "谓词": "表示主体和客体之间的关系，以主体-谓词-客体构成的一句话需要与原文含义相同",
                "关系属性": "属于该条关系的属性，以{属性名:属性值}的形式表示，多个属性使用list表示，没有属性用空list表示",
                "客体属性": "属于客体的属性，以{属性名:属性值}的形式表示，多个属性使用list表示，没有属性用空list表示",
                "简介": "该关系的简短介绍",
            },
            "example": {
                "input": """
                王雪纯是87版《红楼梦》中晴雯的配音者，她在1993年成为《正大综艺》的主持人。
                """,
                "entities": ["王雪纯", "《红楼梦》", "晴雯" "《正大综艺》"],
                "output": [
                    {
                        "主体": "王雪纯",
                        "客体": "晴雯",
                        "谓词": "配音",
                        "简介": "王雪纯是87版《红楼梦》中晴雯的配音者",
                        "关系属性": [],
                        "客体属性": [{"作品": "《红楼梦》"}, {"版本": "87版"}],
                    },
                    {
                        "主体": "王雪纯",
                        "客体": "《正大综艺》",
                        "谓词": "主持人",
                        "简介": "王雪纯在1993年成为《正大综艺》的主持人",
                        "关系属性": [{"时间": "1993年"}],
                        "客体属性": [],
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
        relation_properties = relation.get("关系属性", [])
        object_properties = relation.get("客体属性", [])
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
            "relation_properties": relation_properties,
            "object_properties": object_properties,
            "description": desc,
        }

    def parse_result(self, result: Dict):
        content = result["content"]
        llm_output = result["result"]
        output = []
        for item in llm_output:
            try:
                if isinstance(item, str):
                    item = load_json(item)

                if isinstance(item, dict) and "output" in item:
                    item = item["output"]
                for relation in item:
                    tmp = self.standardize_relation(relation)
                    if isinstance(tmp, dict):
                        output.append(tmp)
            except Exception as e:
                print(f"failed to parse llm output: {item}, info: {e}")
                return None
        return output

    # def result_to_spgrecord(self, result: List):
    #     output = []
    #     for item in result:

    #         object_ = item["object"]
    #         tmp = SPGRecord(object_["类型"])
    #         tmp.upsert_property("name", object_["名称"])
    #         output.append(tmp)

    #         subject = item["subject"]
    #         tmp = SPGRecord(subject["类型"])
    #         tmp.upsert_property("name", subject["名称"])
    #         tmp.upsert_property(item["predicate"], object_["名称"])
    #         tmp.upsert_property("extra_properties", item["properties"])
    #         output.append(tmp)
    #     return output

    def result_to_spgrecord(self, result: List):
        output = []
        for item in result:

            object_ = item["object"]
            tmp = SPGRecord(object_["类型"])
            tmp.upsert_property("name", object_["名称"])
            for p in item["object_properties"]:
                for k, v in p.items():
                    tmp.upsert_property(k, v)
            output.append(tmp)

            subject = item["subject"]
            tmp = SPGRecord(subject["类型"])
            tmp.upsert_property("name", subject["名称"])
            tmp.upsert_relation(
                item["predicate"],
                object_["类型"],
                [object_["名称"], {"relation_properties": item["relation_properties"]}],
            )

            # tmp.upsert_property("name", subject["名称"])
            # tmp.upsert_property(item["predicate"], object_["名称"])
            # tmp.upsert_property("extra_properties", item["properties"])
            output.append(tmp)
        return output


class EventExtractPrompt(Prompt):
    def __init__(self, name):
        self.prompt = {
            "instruction": f"input字段是{name}的一部分内容，entities字段是input字段中抽取的实体，events字段是我关注的事项列表。我需要基于此构建一个知识图谱。请帮我从input字段中抽取出其中包含在events列表中的所有事件，以及事件的时间、地点、主客体等基础信息。请将结果以json list格式返回，具体请遵从example字段中给出的示例。注意，example只是给出了较少的示例，并未涵盖所有需要抽取的事项；由于你很可能会遗漏事件，所以请尽可能多的抽取事件。",
            "schema": {
                "名称": "事件名称",
                "类型": "事件所属的类型，需要在events字段中",
                "主体": "事件主体，需要出现在entities字段中，如果有多个主体，则使用list表示，如果没有主体，则为空list",
                "客体": "事件客体，需要出现在entities字段中，如果有多个客体，则使用list表示，如果没有客体，则为空list",
                "时间": "事件发生的时间，如果没有时间信息，则为空字符串",
                "地点": "事件发生的地点，如果没有地点信息，则为空字符串",
                "属性": "事件包含的其他属性，需要与该事件紧密相关，以{属性名:属性值}的形式表示，多个属性使用list表示，没有属性用空list表示",
                "描述": "事件内容的描述",
            },
            "example": {
                "input": """
                2000年11月7日，在杨峻荣的推荐下，周杰伦发行个人首张音乐专辑《Jay》。
                2008年5月13日， 周杰伦与昆凌在广州向汶川地震灾区捐款50万元，其中用30万在重庆梁平援建一所希望小学。
                2002年，周杰伦凭借专辑《范特西》中的歌曲《爱在西元前》获得第12届台湾金曲奖最佳作曲人奖。
                """,
                "entities": [
                    {"名称": "杨峻荣", "类型": "人物"},
                    {"名称": "周杰伦", "类型": "人物"},
                    {"名称": "昆凌", "类型": "人物"},
                    {"名称": "《Jay》", "类型": "作品"},
                    {"名称": "《范特西》", "类型": "作品"},
                    {"名称": "《爱在西元前》", "类型": "作品"},
                    {"名称": "台湾金曲奖", "类型": "奖项"},
                    {"名称": "昆凌", "类型": "人物"},
                    {"名称": "英国", "类型": "地点"},
                    {"名称": "台湾", "类型": "地点"},
                    {"名称": "汶川", "类型": "地点"},
                    {"名称": "广州", "类型": "地点"},
                    {"名称": "重庆梁平", "类型": "地点"},
                ],
                "events": ["早年经历", "演艺经历", "个人生活", "社会活动", "获奖记录"],
                "output": [
                    {
                        "名称": "周杰伦发行首张音乐专辑",
                        "类型": "演艺经历",
                        "主体": ["周杰伦"],
                        "客体": ["《Jay》"],
                        "时间": "2000年11月7日",
                        "地点": "",
                        "属性": [{"推荐人": "杨峻荣"}],
                        "描述": "2000年11月7日，在杨峻荣的推荐下，周杰伦发行个人首张音乐专辑《Jay》",
                    },
                    {
                        "名称": "周杰伦获得第12届台湾金曲奖最佳作曲人奖与最佳专辑奖",
                        "类型": "获奖记录",
                        "主体": ["周杰伦"],
                        "客体": ["台湾金曲奖"],
                        "时间": "2008年5月13日",
                        "地点": "台湾",
                        "属性": [
                            {"届数": "第12届"},
                            {"奖项": ["最佳作曲人奖", "最佳专辑奖"]},
                            {"获奖专辑": "《范特西》"},
                            {"获奖作品": "《爱在西元前》"},
                        ],
                        "描述": "2002年，周杰伦凭借专辑《范特西》中的歌曲《爱在西元前》获得第12届台湾金曲奖最佳作曲人奖。",
                    },
                    {
                        "名称": "周杰伦捐款",
                        "类型": "社会活动",
                        "主体": ["周杰伦", "昆凌"],
                        "客体": ["汶川地震灾区"],
                        "时间": "2008年5月13日",
                        "地点": "广州",
                        "属性": [
                            {"捐款金额": "50万元"},
                            {"捐款用途": "用30万在重庆梁平援建一所希望小学"},
                        ],
                        "描述": "周杰伦向汶川地震灾区捐款",
                    },
                ],
            },
            "input": "",
            "entities": "",
            "events": ["早年经历", "演艺经历", "个人生活", "社会活动", "获奖记录"],
        }

    def standardize_event(self, event: Dict):
        if not isinstance(event, dict):
            return None
        event_name = event.get("名称", "")
        event_type = event.get("类型", "")
        event_subjects = event.get("主体", [])
        if isinstance(event_subjects, str):
            event_subjects = [event_subjects]
        event_objects = event.get("客体", [])
        if isinstance(event_objects, str):
            event_objects = [event_objects]

        event_time = event.get("时间", "")
        event_location = event.get("地点", "")
        event_properties = event.get("属性", [])
        event_desc = event.get("描述", "")

        standard_subjects = []

        for entity in self.variables["entities"]:
            if entity["名称"] in event_subjects:
                standard_subjects.append(entity)

        standard_objects = []

        for entity in self.variables["entities"]:
            if entity["名称"] in event_objects:
                standard_objects.append(entity)

        if len(event_name) == 0 or len(event_type) == 0 or len(standard_subjects) == 0:
            return None

        return {
            "name": event_name,
            "type": event_type,
            "subjects": [x["名称"] for x in standard_subjects],
            "objects": [x["名称"] for x in standard_objects],
            "time": event_time,
            "location": event_location,
            "event_properties": event_properties,
            "description": event_desc,
        }

    def parse_result(self, result: Dict):
        content = result["content"]
        llm_output = result["result"]
        output = []
        for item in llm_output:
            try:
                if isinstance(item, str):
                    item = load_json(item)

                if isinstance(item, dict) and "output" in item:
                    item = item["output"]
                for entity in item:
                    tmp = self.standardize_event(entity)
                    # make sure entity exists in content
                    if isinstance(tmp, dict):
                        output.append(tmp)
            except Exception as e:
                print(f"failed to parse llm output: {item}, info: {e}")
                return None
        return output

    def result_to_spgrecord(self, result: List):
        output = []
        for item in result:
            tmp = SPGRecord("Event")
            tmp.upsert_properties(item)
            output.append(tmp)
        return output


class FinClassifyPrompt(Prompt):
    def __init__(self):
        self.prompt = {
            "instruction": "input字段是一篇金融新闻，events字段是我关注的金融事件列表。请阅读input字段的内容，然后判断events字段中提供的金融事件列表是否在input字段中实际发生。请返回事件名称，以及其是否发生（须为 [未发生, 已发生] 二者之一）。请以json格式输出结果，须严格遵从example字段中给出的若干示例。不要输出任何非json格式的内容，如额外的解释说明。",
            "events": [
                "质押",
                "股份回购",
                "解除质押",
                "被约谈",
                "企业收购",
                "股东增持",
                "高管变动",
                "中标",
                "公司上市",
                "企业融资",
                "亏损",
                "股东减持",
                "企业破产",
            ],
            "example": [
                {
                    "input": "\n经中国证券监督管理委员会出具的《关于核准甘肃国芳工贸集团股份有限公司首次公开发行股票的批复》文件核准，甘肃国芳工贸（集团）股份有限公司（以下简称“公司”或“国芳集团(5.030,-0.10,-1.95%)”）向社会公众首次公开发行人民币普通股（A股）股票160,000,000股。经上海证券交易所批准，公司股票于2017年9月29日在上海证券交易所上市。\n公司控股股东、实际控制人、董事长张国芳承诺：（1）国芳集团经中国证券监督管理委员会核准首次公开发行股票后，自本公司股票在证券交易所上市交易之日起三十六个月内，不减持或者委托他人管理本人持有的公司公开发行股票前已发行的股份，也不由公司回购本人持有的公司公开发行股票前已发行的股票。（2）本人所持公司股票在锁定期满后2年内不进行质押。\n                ",
                    "output": {
                        "质押": "未发生",
                        "股份回购": "未发生",
                        "解除质押": "未发生",
                        "被约谈": "未发生",
                        "企业收购": "未发生",
                        "股东增持": "未发生",
                        "高管变动": "未发生",
                        "中标": "未发生",
                        "公司上市": "已发生",
                        "企业融资": "未发生",
                        "亏损": "未发生",
                        "股东减持": "未发生",
                        "企业破产": "未发生",
                    },
                },
                {
                    "input": "\n西王食品（SZ 000639，收盘价：5.52元）5月22日晚间发布公告称，西王食品股份有限公司证券事务代表王亚珂先生因工作调整原因，不再担任公司证券事务代表职务。结合公司的实际工作需要，聘任张婷女士担任公司证券事务代表职务。\n                ",
                    "output": {
                        "质押": "未发生",
                        "股份回购": "未发生",
                        "解除质押": "未发生",
                        "被约谈": "未发生",
                        "企业收购": "未发生",
                        "股东增持": "未发生",
                        "高管变动": "已发生",
                        "中标": "未发生",
                        "公司上市": "未发生",
                        "企业融资": "未发生",
                        "亏损": "未发生",
                        "股东减持": "未发生",
                        "企业破产": "未发生",
                    },
                },
            ],
            "input": "",
        }

    def parse_result(self, result: Dict):
        llm_output = result["result"]
        output = []
        for item in llm_output:
            try:
                if isinstance(item, str):
                    item = load_json(item)
                if isinstance(item, dict) and "output" in item:
                    item = item["output"]
                for event_type, happened in item.items():
                    if event_type not in self.variables["events"]:
                        continue
                    if happened.strip() == "已发生":
                        output.append(event_type)
            except Exception as e:
                print(f"failed to parse llm output: {item}, info: {e}")
                return None
        return output

    def result_to_spgrecord(self, result: List):
        return []


class FinEventExtractPrompt(Prompt):
    def __init__(self):
        self.prompt = {
            "instruction": "我需要完成一个金融事件要素抽取任务，input字段是一篇金融新闻，schema中定义了我关注的金融事件以及其包含的要素名称。请阅读该的内容，然后抽取出文章中包含的金融事件名称以及相关要素，对于子事件或者事件细节同样要当做事件返回，如多次股东增持/减持/质押/解除质押，或者收购/回购等的具体细节，以及任何文中提及的相关事件，都要抽取事件要素！！。其中，事件要素以{role:role_name, argument:argument_name}的形式表示，其中role为要素名, argument为要素值，如果要素值未提及，则填null，如果要素是多值，则使用list表示。请以json格式输出结果，须严格遵从example字段中给出的若干示例。重要提示：1. 请严格区分要素中的完成时间和披露时间，完成时间指事件的结束时间，披露时间则是该事件公布的时间。2. 直接返回json数据，不要加任何解释说明。",
            "input": "",
            "schema": "",
            "example": "",
        }

    def standardize_argument(self, event_argument):

        if isinstance(event_argument, list):
            event_argument = event_argument[0]
        if isinstance(event_argument, str):
            event_argument = event_argument.strip()
            if event_argument.lower() in ["null", "none", "", "无"]:
                return None
            return event_argument
        else:
            return None

    def parse_result(self, result: Dict):
        schema = result["args"]["schema"]
        llm_output = result["result"][0]
        if isinstance(llm_output, str):
            llm_output = json.loads(llm_output)
        if isinstance(llm_output, dict) and "output" in llm_output:
            llm_output = llm_output["output"]
        if not isinstance(llm_output, list):
            llm_output = [llm_output]
        formatted = {}
        for event in llm_output:
            for event_type, event_arguments in event.items():
                if not isinstance(event_arguments, list):
                    event_arguments = [event_arguments]
                formatted_event_arguments = []
                for event_argument in event_arguments:
                    if not isinstance(event_argument, dict):
                        continue
                    role = event_argument.get("role")
                    argument = event_argument.get("argument")
                    if role is None or argument is None:
                        continue
                    formatted_event_arguments.append(
                        {"role": role, "argument": self.standardize_argument(argument)}
                    )
                if event_type in formatted:
                    formatted[event_type].append(formatted_event_arguments)
                else:
                    formatted[event_type] = [formatted_event_arguments]

        return {"data": formatted, "raw": result["result"][0]}

    def result_to_spgrecord(self, result: List):
        return []


class FinEventMergePrompt(Prompt):
    def __init__(self):
        self.prompt = {
            "instruction": "我需要完成一个金融事件要素抽取与融合任务，input字段是一篇金融新闻，schema中定义了我关注的金融事件以及其包含的要素名称。base定义了我已经抽取出来的事件，但是可能有遗漏的事件要素或者其他事件。请阅读上述字段的内容，然后input原文中哪些可以正确补充到base数据对应的字段中的信息，并返回补全后的base字段内容。其中，事件要素以{role:role_name, argument:argument_name}的形式表示，其中role为要素名, argument为要素值，如果要素值未提及，则填null，如果要素是多值，则使用list表示。example是一个示例，请你参考。请以json格式输出结果，须严格遵从base字段中的格式。特别提示：1. 不要增删改base数据里的披露时间/披露日期等字段; 2. 直接返回json格式的输出结果，不得添加任何说明和解释。",
            "input": "",
            "base": "",
            "example": {
                "input": "原标题：仁东控股股份有限公司关于控股股东增持计划实施结果的公告\n股东北京仁东信息技术有限公司保证向本公司提供的信息内容真实、准确、完整，没有虚假记载、误导性陈述或重大遗漏。\n本公司及董事会全体成员保证公告内容与信息披露义务人提供的信息一致。\n重要内容提示：\n仁东控股股份有限公司（以下简称“公司”）于2019年5月16日披露控股股东北京仁东信息技术有限公司（以下简称“仁东信息”）增持计划：仁东信息拟在未来3个月内，通过包括但不限于集中竞价、大宗交易等方式，增持公司股份不低于总股本的1.5%。\n截止本公告披露日，本次增持计划已实施完毕，仁东信息发来告知函，其具体增持情况如下：\n一、计划增持主体的基本情况\n1、计划增持主体：北京仁东信息技术有限公司\n2、持股数量及比例：本次增持计划实施前，仁东信息持有公司股份128,613,358股，占公司总股本的22.97%。本次增持计划实施后，仁东信息已通过大宗交易方式累计增持公司股份9,478,133股，占公司总股本的1.69%。\n3、计划增持主体在本次公告前6个月未减持过本公司股份。\n二、增持计划的主要内容\n1、增持股份的目的：基于对公司的内在价值和未来发展前景的信心，确保公司股价稳定和保障广大中小投资者利益。\n2、拟增持股份的数量：拟增持公司股份不低于总股本的1.5%。\n3、拟增持股份的价格前提：本次拟增持的股份不设置固定价格、价格区间及累计跌幅比例。\n4、增持计划的实施期限：自增持计划公告之日起3个月内。\n5、增持股份的方式：包括但不限于集中竞价交易、大宗交易等。\n6、本次增持不是基于其主体的特定身份，如丧失相关身份时将继续实施本增持计划。\n7、增持股份不存在锁定安排，仁东信息及其一致行动人承诺在增持计划实施期间及法定期限内不减持其所持有的公司股份。\n三、增持计划实施情况\n2019年5月16日至2019年6月28日，仁东信息通过大宗交易方式增持仁东控股股份3,974,802股（占公司总股本的比例为0.71%），平均成交价格为12.43元/股。\n2019年6月29日至2019年8月9日，仁东信息通过大宗交易方式增持仁东控股股份2,000,000股（占公司总股本的比例为0.36%），平均成交价格为15.15元/股。\n2019年8月10日至2019年8月16日，仁东信息通过大宗交易方式增持仁东控股股份3,503,331股（占公司总股本的比例为0.63%），平均成交价格为15.45元/股。\n截至本公告披露日，仁东信息通过大宗交易方式累计增持公司股份9,478,133股，占公司总股本的1.69%，已超过此次增持计划的下限；累计增持金额133,844,693元。增持计划实施前，仁东信息持有公司股份128,613,358股，占公司总股本的22.97%。增持计划实施后，仁东信息持有公司股份138,091,491股，占公司总股本的24.66%。\n四、其他相关说明\n1、仁东信息及其一致行动人承诺，在增持计划实施期间及法定期限内不减持其所持有的公司股份。\n2、本次增持公司股份不会导致公司股份分布不具备上市条件，不会导致公司控制权发生变化。\n五、备查文件\n1、北京仁东信息技术有限公司的告知函。\n仁东控股股份有限公司\n董事会\n二〇一九年八月十六日",
                "base": [
                    {
                        "股东增持": [
                            [
                                {"role": "股票简称", "argument": "仁东控股"},
                                {"role": "披露时间", "argument": "2019年5月16日"},
                                {"role": "交易股票/股份数量", "argument": "不低于总股本的1.5%"},
                                {"role": "交易金额", "argument": "133,844,693元"},
                                {"role": "交易完成时间", "argument": "自增持计划公告之日起3个月内"},
                                {"role": "增持方", "argument": "北京仁东信息技术有限公司"},
                                {"role": "增持部分占总股本比例", "argument": "不低于总股本的1.5%"},
                            ]
                        ]
                    }
                ],
                "output": {
                    "股东增持": [
                        {"role": "股票简称", "argument": "仁东控股"},
                        {"role": "增持方", "argument": "北京仁东信息技术有限公司"},
                        {
                            "role": "交易股票/股份数量",
                            "argument": [
                                "3,974,802",
                                "2,000,000",
                                "3,503,331",
                                "9,478,133",
                            ],
                        },
                        {
                            "role": "增持部分占总股本比例",
                            "argument": ["0.71%", "0.36%", "0.63%", "1.69%"],
                        },
                        {
                            "role": "每股交易价格",
                            "argument": ["12.43元", "15.15元", "15.45元", "133,844,693元"],
                        },
                        {"role": "披露时间", "argument": "2019年5月16日"},
                        {
                            "role": "交易完成时间",
                            "argument": [
                                "2019年5月16日至2019年6月28日",
                                "2019年6月29日至2019年8月9日",
                                "2019年8月10日至2019年8月16日",
                                "截至本公告披露日",
                            ],
                        },
                    ]
                },
            },
        }

    def parse_result(self, result: Dict):
        llm_output = result["result"][0]
        if isinstance(llm_output, str):
            llm_output = json.loads(llm_output)
        if isinstance(llm_output, dict) and "output" in llm_output:
            llm_output = llm_output["output"]
        if isinstance(llm_output, dict) and "base" in llm_output:
            llm_output = llm_output["base"]
        if not isinstance(llm_output, list):
            llm_output = [llm_output]

        formatted = {}
        print(f"llm_output = {llm_output}")
        for item in llm_output:
            for event_type, events in item.items():
                if not isinstance(events, list):
                    events = [events]
                formatted_event_arguments = []
                for event_arguments in events:
                    if not isinstance(event_arguments, list):
                        event_arguments = [event_arguments]

                    event_argument = event_arguments[0]
                    if not isinstance(event_argument, dict):
                        raise TypeError(
                            f"unsupported event_argument type {type(event_argument)}"
                        )
                    role = event_argument.get("role")
                    argument = event_argument.get("argument")
                    if role is None or argument is None:
                        # role: argument format
                        tmp = []
                        for role, argument in event_argument.items():
                            tmp.append({"role": role, "argument": argument})
                        formatted_event_arguments.append(tmp)
                    else:
                        # {role:role_name, argument:argument_name} format
                        for event_argument in event_arguments:
                            role = event_argument.get("role")
                            argument = event_argument.get("argument")
                            if role is None or argument is None:
                                continue
                            formatted_event_arguments.append(
                                {"role": role, "argument": argument}
                            )

                if event_type in formatted:
                    formatted[event_type].extend(formatted_event_arguments)
                else:
                    formatted[event_type] = formatted_event_arguments

        return {"data": formatted, "raw": result["result"][0]}

    def result_to_spgrecord(self, result: List):
        return []
