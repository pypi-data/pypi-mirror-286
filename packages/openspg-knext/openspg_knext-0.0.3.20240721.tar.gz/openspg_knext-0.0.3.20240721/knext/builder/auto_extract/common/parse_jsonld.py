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


import json

from pypinyin import pinyin, Style

filename = 'cns-core.jsonId'
with open(filename, 'r') as file:
    data = file.read()
    jsonld_data = json.loads(data)

root_types = ["Person",
              # "Organization", "Place", "Product"
              ]

def generate_english_name(original_str, category):
    pinyin_list = pinyin(original_str, style=Style.NORMAL)
    pinyin_str = ''.join([item[0].capitalize() for item in pinyin_list])
    result_str = pinyin_str[0].lower() + pinyin_str[1:] if category == "property" else pinyin_str
    return result_str


def get_type_from_url(url: str):
    if not url:
        return ""
    if url[-1] == '/':
        _type = url.split('/')[-2].strip()
    else:
        _type = url.split('/')[-1].strip()
    return _type


def find_by_name_zh(name_zh: str, category: str):
    for item in jsonld_data.get("@graph", []):
        if item.get("nameZh", "") == name_zh and item.get("category") == category:
            return item
    return None


def parse_sub_types():
    lines = """"""
    for _root in root_types:
        # 处理属性
        properties = []
        type_line = ""
        type_desc = ""
        for item in jsonld_data.get("@graph", []):
            if item.get("name", "") == _root:
                type_line = f"{_root}({item.get('nameZh')}): EntityType\n"
                type_desc = item.get("descriptionZh", "")
                _properties = item.get("properties", "")
                for prop_url in _properties.split(','):
                    prop_name = get_type_from_url(prop_url)
                    properties.append(prop_name)
                break
        property_lines = []
        relation_lines = []
        for _prop in properties:
            for item in jsonld_data.get("@graph", []):
                if item.get("nameZh", "") == _prop and item.get("category") == "property":
                    p_name = item.get("name", "") or generate_english_name(_prop, "property")
                    if not item.get("rangeIncludes", ""):
                        o_type = "Text"
                        p_desc = item.get("descriptionZh", "")
                        p_desc = "" if "https:" in p_desc else p_desc
                        property_lines.append((f"{p_name}({_prop}): {o_type}", p_desc))
                        break
                    for _range_include_url in item.get("rangeIncludes", "").split(','):
                        o_type_zh = get_type_from_url(_range_include_url)
                        _item = find_by_name_zh(o_type_zh, "type")
                        o_type = _item.get('name', "") or generate_english_name(o_type_zh, "type")
                        p_desc = item.get("descriptionZh", "")
                        p_desc = "" if "https:" in p_desc else p_desc
                        relation_lines.append((f"{p_name}({_prop}): {o_type}", p_desc))
                    break
        property_lines, relation_lines = list(set(property_lines)), list(set(relation_lines))
        lines += type_line
        lines += "    desc: " + type_desc + '\n' if type_desc else ""
        lines += "    properties:\n"
        for _line, _desc in property_lines:
            lines += "        " + _line + '\n' + ("            desc: " + _desc + '\n' if _desc else "")
        lines += "    relations:\n"
        for _line, _desc in relation_lines:
            lines += "        " + _line + '\n' + ("            desc: " + _desc + '\n' if _desc else "")
    print(lines)


def parse_type_to_top():
    data = jsonld_data.get("@graph", [])
    sub_type_mapping = {item["nameZh"]: get_type_from_url(item["subTypeOf"]) for item in data if item["category"] == "type"}
    for k, v in sub_type_mapping.items():
        if k == v:
            print(k)
    print(sub_type_mapping)
    def find_top_type(nameZh, mapping):
        """
        递归查找最顶层的类型
        """
        # 终止条件：当子类型为空，表示已到达顶层
        if mapping[nameZh] == "":
            return nameZh
        return find_top_type(mapping[nameZh], mapping)

    # 根据每个条目的nameZh，找到其顶层的subTypeOf
    result = {name: find_top_type(name, sub_type_mapping) for name in sub_type_mapping}

    print(result)


if __name__ == '__main__':
    # parse_sub_types()
    parse_type_to_top()
"""

{
  "@context": {
    "@vocab": "http://cnschema.org/"
  },
  "@graph": [
    {
      "SchemaorgV13": "SchemaorgV13",
      "category": "type",
      "name": "Person",
      "description": "A person (alive, dead, undead, or fictional).",
      "nameZh": "人物",
      "descriptionZh校验": "一个人（可以是活着的，死去的，不死的或者虚构的）",
      "properties": "https://cnschema.openkg.cn/别名, https://cnschema.openkg.cn/附加类型, https://cnschema.openkg.cn/地址, https://cnschema.openkg.cn/所属机构, https://cnschema.openkg.cn/别名, https://cnschema.openkg.cn/所获奖项, https://cnschema.openkg.cn/所获奖项, https://cnschema.openkg.cn/出生日期, https://cnschema.openkg.cn/出生地点, https://cnschema.openkg.cn/品牌, https://cnschema.openkg.cn/呼号, https://cnschema.openkg.cn/子女, https://cnschema.openkg.cn/同事, https://cnschema.openkg.cn/同事, https://cnschema.openkg.cn/联络点, https://cnschema.openkg.cn/联络点, https://cnschema.openkg.cn/逝世日期, https://cnschema.openkg.cn/逝世地点, https://cnschema.openkg.cn/描述, https://cnschema.openkg.cn/消歧描述, https://cnschema.openkg.cn/邓白氏编码, https://cnschema.openkg.cn/电子邮箱, https://cnschema.openkg.cn/脂肪含量, https://cnschema.openkg.cn/功能列表, https://cnschema.openkg.cn/跟进, https://cnschema.openkg.cn/游戏, https://cnschema.openkg.cn/风格, https://cnschema.openkg.cn/全球位置码, https://cnschema.openkg.cn/政府福利信息, https://cnschema.openkg.cn/有定义的术语, https://cnschema.openkg.cn/清单, https://cnschema.openkg.cn/销售点, https://cnschema.openkg.cn/作品组件, https://cnschema.openkg.cn/最高价, https://cnschema.openkg.cn/主队, https://cnschema.openkg.cn/姓名后面的敬语, https://cnschema.openkg.cn/医院隶属关系, https://cnschema.openkg.cn/鉴别检查, https://cnschema.openkg.cn/成像技术, https://cnschema.openkg.cn/交互类型, https://cnschema.openkg.cn/国际标准音像制品代码, https://cnschema.openkg.cn/管辖权, https://cnschema.openkg.cn/知道关于, https://cnschema.openkg.cn/知道语言, https://cnschema.openkg.cn/标签详情, https://cnschema.openkg.cn/维护者, https://cnschema.openkg.cn/制造商, https://cnschema.openkg.cn/会员, https://cnschema.openkg.cn/名称, https://cnschema.openkg.cn/角色职位, https://cnschema.openkg.cn/自然进展, https://cnschema.openkg.cn/新闻更新和指南, https://cnschema.openkg.cn/结束页码, https://cnschema.openkg.cn/上级条目, https://cnschema.openkg.cn/所属剧集, https://cnschema.openkg.cn/表演活动, https://cnschema.openkg.cn/预期的行动, https://cnschema.openkg.cn/出版准则, https://cnschema.openkg.cn/亲属, https://cnschema.openkg.cn/等同, https://cnschema.openkg.cn/用户需求, https://cnschema.openkg.cn/兄弟姐妹, https://cnschema.openkg.cn/兄弟姐妹, https://cnschema.openkg.cn/赞助者, https://cnschema.openkg.cn/配偶, https://cnschema.openkg.cn/主题, https://cnschema.openkg.cn/纳税识别号码, https://cnschema.openkg.cn/电话号码, https://cnschema.openkg.cn/链接, https://cnschema.openkg.cn/欧盟税号, https://cnschema.openkg.cn/重量, https://cnschema.openkg.cn/工作地点, https://cnschema.openkg.cn/受雇于/",
      "equivalentClass": "http://xmlns.com/foaf/0.1/人物/",
      "subTypeOf": "",
      "subTypes": "https://cnschema.openkg.cn/文艺界的人,https://cnschema.openkg.cn/体育界的人,https://cnschema.openkg.cn/学术界的人,https://cnschema.openkg.cn/公司的人,https://cnschema.openkg.cn/医院的人,https://cnschema.openkg.cn/家庭角色,https://cnschema.openkg.cn/历史人物/",
      "wikidataUrl": "https://www.wikidata.org/wiki/Q5",
      "schemaorgUrl": "https://schema.org/Person"
    },
  ]
}
"""