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
import os
import re
from typing import List, Dict

from knext.builder.auto_extract.common.spg_aligner import SPGAligner
from knext.builder.operator import SPGRecord
from knext.builder.operator.builtin.auto_prompt import AutoPrompt

PWD = os.path.dirname(__file__)


class SPOPrompt(AutoPrompt):
    template_zh: str = "你是一个图谱知识抽取的专家，从input 中尽量多的抽取出所有[subject, subject_type, predicate, object, object_type]五元组，其中predicate不允许为动词，以标准json 格式输出，结果返回list"
    template_en: str = ""

    def __init__(self, **kwargs):
        types_list = kwargs.get("types_list", [])
        language = kwargs.get("language", "zh")
        with_description = kwargs.get("with_description", False)
        split_num = kwargs.get("split_num", 4)
        project_id = kwargs.get("project_id", None)
        super().__init__(types_list, project_id=project_id)
        if language == "zh":
            self.template = self.template_zh
        else:
            self.template = self.template_en
        self.with_description = with_description
        self.split_num = split_num
        self.aligner = SPGAligner(project_id=project_id)

        self._init_render_variables()

        self.params = kwargs

    def build_prompt(self, variables: Dict[str, str]) -> str:
        instruction = json.dumps(
            {
                "instruction": self.template,
                "input": variables.get("input"),
            },
            ensure_ascii=False,
        )
        return instruction

    def parse_response(self, response: str, **kwargs) -> List[SPGRecord]:
        spo_aligned_list = self.aligner.spo_align(spo_list=response)
        print(spo_aligned_list)
        # spo_aligned_list = [['美国', '区域地点', '所属区域', '亚拉巴马州,阿拉斯加州,亚利桑那州,阿肯色州,加利福尼亚州,科罗拉多州,康涅狄格州,特拉华州,佛罗里达州,佐治亚州,夏威夷州,爱达荷州,伊利诺伊州,印第安纳州,艾奥瓦州,堪萨斯州,肯塔基州,路易斯安那州,缅因州,马里兰州,马萨诸塞州,密歇根州,明尼苏达州,密西西比州,密苏里州,蒙大拿州,内布拉斯加州,内华达州,新罕布什尔州,新泽西州,新墨西哥州,纽约州,北卡罗来纳州,北达科他州,俄亥俄州,俄克拉何马州,俄勒冈州,宾夕法尼亚州,罗得岛州,南卡罗来纳州,南达科他州,田纳西州,得克萨斯州,犹他州,佛蒙特州,弗吉尼亚州,华盛顿州,西弗吉尼亚州,威斯康星州,怀俄明州', '区域地点'], ['亚拉巴马州', '区域地点', '简称', 'AL', 'NAN'], ['亚拉巴马州', '区域地点', '英文', 'Alabama', 'NAN'], ['亚拉巴马州', '区域地点', '首府是', '蒙哥马利', '区域地点'], ['阿拉斯加州', '区域地点', '简称', 'AK', 'NAN'], ['阿拉斯加州', '区域地点', '英文', 'Alaska', 'NAN'], ['阿拉斯加州', '区域地点', '首府是', '朱诺', '区域地点'], ['亚利桑那州', '区域地点', '简称', 'AZ', 'NAN'], ['亚利桑那州', '区域地点', '英文', 'Arizona', 'NAN'], ['亚利桑那州', '区域地点', '首府是', '菲尼克斯', '区域地点'], ['阿肯色州', '区域地点', '简称', 'AR', 'NAN'], ['阿肯色州', '区域地点', '英文', 'Arkansas', 'NAN'], ['阿肯色州', '区域地点', '首府是', '小石城', '区域地点'], ['加利福尼亚州', '区域地点', '简称', 'CA', 'NAN'], ['加利福尼亚州', '区域地点', '英文', 'California', 'NAN'], ['加利福尼亚州', '区域地点', '首府是', '萨克拉门托', '区域地点'], ['科罗拉多州', '区域地点', '简称', 'CO', 'NAN'], ['科罗拉多州', '区域地点', '英文', 'Colorado', 'NAN'], ['科罗拉多州', '区域地点', '首府是', '丹佛', '区域地点'], ['康涅狄格州', '区域地点', '简称', 'CT', 'NAN'], ['康涅狄格州', '区域地点', '英文', 'Connecticut', 'NAN'], ['康涅狄格州', '区域地点', '首府是', '哈特福德', '区域地点'], ['特拉华州', '区域地点', '简称', 'DE', 'NAN'], ['特拉华州', '区域地点', '英文', 'Delaware', 'NAN'], ['特拉华州', '区域地点', '首府是', '多佛', '区域地点'], ['佛罗里达州', '区域地点', '简称', 'FL', 'NAN'], ['佛罗里达州', '区域地点', '英文', 'Florida', 'NAN'], ['佛罗里达州', '区域地点', '首府是', '塔拉哈西', '区域地点'], ['佐治亚州', '区域地点', '简称', 'GA', 'NAN'], ['佐治亚州', '区域地点', '英文', 'Georgia', 'NAN'], ['佐治亚州', '区域地点', '首府是', '亚特兰大', '区域地点'], ['夏威夷州', '区域地点', '简称', 'HI', 'NAN'], ['夏威夷州', '区域地点', '英文', 'Hawaii', 'NAN'], ['夏威夷州', '区域地点', '首府是', '火奴鲁鲁', '区域地点'], ['爱达荷州', '区域地点', '简称', 'ID', 'NAN'], ['爱达荷州', '区域地点', '英文', 'Idaho', 'NAN'], ['爱达荷州', '区域地点', '首府是', '博伊西', '区域地点'], ['伊利诺伊州', '区域地点', '简称', 'IL', 'NAN'], ['伊利诺伊州', '区域地点', '英文', 'Illinois', 'NAN'], ['伊利诺伊州', '区域地点', '首府是', '斯普林菲尔德', '区域地点'], ['印第安纳州', '区域地点', '简称', 'IN', 'NAN'], ['印第安纳州', '区域地点', '英文', 'Indiana', 'NAN'], ['印第安纳州', '区域地点', '首府是', '印第安纳波利斯', '区域地点'], ['艾奥瓦州', '区域地点', '简称', 'IA', 'NAN'], ['艾奥瓦州', '区域地点', '英文', 'Iowa', 'NAN'], ['艾奥瓦州', '区域地点', '首府是', '得梅因', '区域地点'], ['堪萨斯州', '区域地点', '简称', 'KS', 'NAN'], ['堪萨斯州', '区域地点', '英文', 'Kansas', 'NAN'], ['堪萨斯州', '区域地点', '首府是', '托皮卡', '区域地点'], ['肯塔基州', '区域地点', '简称', 'KY', 'NAN'], ['肯塔基州', '区域地点', '英文', 'Kentucky', 'NAN'], ['肯塔基州', '区域地点', '首府是', '法兰克福', '区域地点'], ['路易斯安那州', '区域地点', '简称', 'LA', 'NAN'], ['路易斯安那州', '区域地点', '英文', 'Louisiana', 'NAN'], ['路易斯安那州', '区域地点', '首府是', '巴吞鲁日', '区域地点'], ['缅因州', '区域地点', '简称', 'ME', 'NAN'], ['缅因州', '区域地点', '英文', 'Maine', 'NAN'], ['缅因州', '区域地点', '首府是', '奥古斯塔', '区域地点'], ['马里兰州', '区域地点', '简称', 'MD', 'NAN'], ['马里兰州', '区域地点', '英文', 'Maryland', 'NAN'], ['马里兰州', '区域地点', '首府是', '安纳波利斯', '区域地点'], ['马萨诸塞州', '区域地点', '简称', 'MA', 'NAN'], ['马萨诸塞州', '区域地点', '英文', 'Massachusetts', 'NAN'], ['马萨诸塞州', '区域地点', '首府是', '波士顿', '区域地点'], ['密歇根州', '区域地点', '简称', 'MI', 'NAN'], ['密歇根州', '区域地点', '英文', 'Michigan', 'NAN'], ['密歇根州', '区域地点', '首府是', '兰辛', '区域地点'], ['明尼苏达州', '区域地点', '简称', 'MN', 'NAN'], ['明尼苏达州', '区域地点', '英文', 'Minnesota', 'NAN'], ['明尼苏达州', '区域地点', '首府是', '圣保罗', '区域地点'], ['密西西比州', '区域地点', '简称', 'MS', 'NAN'], ['密西西比州', '区域地点', '英文', 'Mississippi', 'NAN'], ['密西西比州', '区域地点', '首府是', '杰克逊', '区域地点'], ['密苏里州', '区域地点', '简称', 'MO', 'NAN'], ['密苏里州', '区域地点', '英文', 'Missouri', 'NAN'], ['密苏里州', '区域地点', '首府是', '杰斐逊城', '区域地点'], ['蒙大拿州', '区域地点', '简称', 'MT', 'NAN'], ['蒙大拿州', '区域地点', '英文', 'Montana', 'NAN'], ['蒙大拿州', '区域地点', '首府是', '海伦娜', '区域地点'], ['内布拉斯加州', '区域地点', '简称', 'NE', 'NAN'], ['内布拉斯加州', '区域地点', '英文', 'Nebraska', 'NAN'], ['内布拉斯加州', '区域地点', '首府是', '林肯', '区域地点'], ['内华达州', '区域地点', '简称', 'NV', 'NAN'], ['内华达州', '区域地点', '英文', 'Nevada', 'NAN'], ['内华达州', '区域地点', '首府是', '卡森城', '区域地点'], ['新罕布什尔州', '区域地点', '简称', 'NH', 'NAN'], ['新罕布什尔州', '区域地点', '英文', 'New Hampshire', 'NAN'], ['新罕布什尔州', '区域地点', '首府是', '康科德', '区域地点'], ['新泽西州', '区域地点', '简称', 'NJ', 'NAN'], ['新泽西州', '区域地点', '英文', 'New Jersey', 'NAN'], ['新泽西州', '区域地点', '首府是', '特伦顿', '区域地点'], ['新墨西哥州', '区域地点', '简称', 'NM', 'NAN'], ['新墨西哥州', '区域地点', '英文', 'New Mexico', 'NAN'], ['新墨西哥州', '区域地点', '首府是', '圣菲', '区域地点'], ['纽约州', '区域地点', '简称', 'NY', 'NAN'], ['纽约州', '区域地点', '英文', 'New York', 'NAN'], ['纽约州', '区域地点', '首府是', '奥尔巴尼', '区域地点'], ['北卡罗来纳州', '区域地点', '简称', 'NC', 'NAN'], ['北卡罗来纳州', '区域地点', '英文', 'North Carolina', 'NAN'], ['北卡罗来纳州', '区域地点', '首府是', '纳罗利', '区域地点'], ['北达科他州', '区域地点', '简称', 'ND', 'NAN'], ['北达科他州', '区域地点', '英文', 'North Dakota', 'NAN'], ['北达科他州', '区域地点', '首府是', '俾斯麦', '区域地点'], ['俄亥俄州', '区域地点', '简称', 'OH', 'NAN'], ['俄亥俄州', '区域地点', '英文', 'Ohio', 'NAN'], ['俄亥俄州', '区域地点', '首府是', '哥伦布', '区域地点'], ['俄克拉何马州', '区域地点', '简称', 'OK', 'NAN'], ['俄克拉何马州', '区域地点', '英文', 'Oklahoma', 'NAN'], ['俄克拉何马州', '区域地点', '首府是', '俄克拉何马城', '区域地点'], ['俄勒冈州', '区域地点', '简称', 'OR', 'NAN'], ['俄勒冈州', '区域地点', '英文', 'Oregon', 'NAN'], ['俄勒冈州', '区域地点', '首府是', '塞勒姆', '区域地点'], ['宾夕法尼亚州', '区域地点', '简称', 'PA', 'NAN'], ['宾夕法尼亚州', '区域地点', '英文', 'Pennsylvania', 'NAN'], ['宾夕法尼亚州', '区域地点', '首府是', '哈里斯堡', '区域地点'], ['罗得岛州', '区域地点', '简称', 'RI', 'NAN'], ['罗得岛州', '区域地点', '英文', 'Rhode Island', 'NAN'], ['罗得岛州', '区域地点', '首府是', '普罗维登斯', '区域地点'], ['南卡罗来纳州', '区域地点', '简称', 'SC', 'NAN'], ['南卡罗来纳州', '区域地点', '英文', 'South Carolina', 'NAN'], ['南卡罗来纳州', '区域地点', '首府是', '哥伦比亚', '区域地点'], ['南达科他州', '区域地点', '简称', 'SD', 'NAN'], ['南达科他州', '区域地点', '英文', 'South Dakota', 'NAN'], ['南达科他州', '区域地点', '首府是', '皮尔', '区域地点'], ['田纳西州', '区域地点', '简称', 'TN', 'NAN'], ['田纳西州', '区域地点', '英文', 'Tennessee', 'NAN'], ['田纳西州', '区域地点', '首府是', '纳什维尔', '区域地点'], ['得克萨斯州', '区域地点', '简称', 'TX', 'NAN'], ['得克萨斯州', '区域地点', '英文', 'Texas', 'NAN'], ['得克萨斯州', '区域地点', '首府是', '奥斯汀', '区域地点'], ['犹他州', '区域地点', '简称', 'UT', 'NAN'], ['犹他州', '区域地点', '英文', 'Utah', 'NAN'], ['犹他州', '区域地点', '首府是', '盐湖城', '区域地点'], ['佛蒙特州', '区域地点', '简称', 'VT', 'NAN'], ['佛蒙特州', '区域地点', '英文', 'Vermont', 'NAN'], ['佛蒙特州', '区域地点', '首府是', '蒙彼利埃', '区域地点'], ['弗吉尼亚州', '区域地点', '简称', 'VA', 'NAN'], ['弗吉尼亚州', '区域地点', '英文', 'Virginia', 'NAN'], ['弗吉尼亚州', '区域地点', '首府是', '里士满', '区域地点'], ['华盛顿州', '区域地点', '简称', 'WA', 'NAN'], ['华盛顿州', '区域地点', '英文', 'Washington', 'NAN'], ['华盛顿州', '区域地点', '首府是', '奥林匹亚', '区域地点'], ['西弗吉尼亚州', '区域地点', '简称', 'WV', 'NAN'], ['西弗吉尼亚州', '区域地点', '英文', 'West Virginia', 'NAN'], ['西弗吉尼亚州', '区域地点', '首府是', '查尔斯顿', '区域地点'], ['威斯康星州', '区域地点', '简称', 'WI', 'NAN'], ['威斯康星州', '区域地点', '英文', 'Wisconsin', 'NAN'], ['威斯康星州', '区域地点', '首府是', '麦迪逊', '区域地点'], ['怀俄明州', '区域地点', '简称', 'WY', 'NAN'], ['怀俄明州', '区域地点', '英文', 'Wyoming', 'NAN'], ['怀俄明州', '区域地点', '首府是', '夏延', '区域地点'], ['蒙哥马利', '区域地点', '英文_2', 'Montgomery', 'NAN'], ['朱诺', '区域地点', '英文_2', 'Juneau', 'NAN'], ['菲尼克斯', '区域地点', '英文_2', 'Phoenix', 'NAN'], ['小石城', '区域地点', '英文_2', 'Little rock', 'NAN'], ['萨克拉门托', '区域地点', '英文_2', 'Sacramento', 'NAN'], ['丹佛', '区域地点', '英文_2', 'Denver', 'NAN'], ['哈特福德', '区域地点', '英文_2', 'Hartford', 'NAN'], ['多佛', '区域地点', '英文_2', 'Dover', 'NAN'], ['塔拉哈西', '区域地点', '英文_2', 'Tallahassee', 'NAN'], ['亚特兰大', '区域地点', '英文_2', 'Atlanta', 'NAN'], ['火奴鲁鲁', '区域地点', '英文_2', 'Honolulu', 'NAN'], ['博伊西', '区域地点', '英文_2', 'Boise', 'NAN'], ['斯普林菲尔德', '区域地点', '英文_2', 'Springfield', 'NAN'], ['印第安纳波利斯', '区域地点', '英文_2', 'Indianapolis', 'NAN'], ['得梅因', '区域地点', '英文_2', 'Des Moines', 'NAN'], ['托皮卡', '区域地点', '英文_2', 'Topeka', 'NAN'], ['法兰克福', '区域地点', '英文_2', 'Frankfort', 'NAN'], ['巴吞鲁日', '区域地点', '英文_2', 'Baton Rouge', 'NAN'], ['奥古斯塔', '区域地点', '英文_2', 'Augusta', 'NAN'], ['安纳波利斯', '区域地点', '英文_2', 'Annapolis', 'NAN'], ['波士顿', '区域地点', '英文_2', 'Boston', 'NAN'], ['兰辛', '区域地点', '英文_2', 'Lansing', 'NAN'], ['圣保罗', '区域地点', '英文_2', 'St.Paul', 'NAN'], ['杰克逊', '区域地点', '英文_2', 'Jackson', 'NAN'], ['杰斐逊城', '区域地点', '英文_2', 'Jefferson City', 'NAN'], ['海伦娜', '区域地点', '英文_2', 'Helena', 'NAN'], ['林肯', '区域地点', '英文_2', 'Lincoln', 'NAN'], ['卡森城', '区域地点', '英文_2', 'Carson City', 'NAN'], ['康科德', '区域地点', '英文_2', 'Concord', 'NAN'], ['特伦顿', '区域地点', '英文_2', 'Trenton', 'NAN'], ['圣菲', '区域地点', '英文_2', 'Santa Fe', 'NAN'], ['奥尔巴尼', '区域地点', '英文_2', 'Albany', 'NAN'], ['纳罗利', '区域地点', '英文_2', 'Raleigh', 'NAN'], ['俾斯麦', '区域地点', '英文_2', 'Bismarck', 'NAN'], ['哥伦布', '区域地点', '英文_2', 'Columbus', 'NAN'], ['俄克拉何马城', '区域地点', '英文_2', 'Oklahoma City', 'NAN'], ['塞勒姆', '区域地点', '英文_2', 'Salem', 'NAN'], ['哈里斯堡', '区域地点', '英文_2', 'Harrisburg', 'NAN'], ['普罗维登斯', '区域地点', '英文_2', 'Providence', 'NAN'], ['哥伦比亚', '区域地点', '英文_2', 'Columbia', 'NAN'], ['皮尔', '区域地点', '英文_2', 'Pierre', 'NAN'], ['纳什维尔', '区域地点', '英文_2', 'Nashville', 'NAN'], ['奥斯汀', '区域地点', '英文_2', 'Austin', 'NAN'], ['盐湖城', '区域地点', '英文_2', 'Salt Lake City', 'NAN'], ['蒙彼利埃', '区域地点', '英文_2', 'Montpelier', 'NAN'], ['里士满', '区域地点', '英文_2', 'Richmond', 'NAN'], ['奥林匹亚', '区域地点', '英文_2', 'Olympia', 'NAN'], ['查尔斯顿', '区域地点', '英文_2', 'Charleston', 'NAN'], ['麦迪逊', '区域地点', '英文_2', 'Madison', 'NAN'], ['夏延', '区域地点', '英文_2', 'Cheyenne', 'NAN']]
        subject_records = {}
        basic_infos = {}
        other_infos = {}
        result = []
        for spo in spo_aligned_list:
            is_relation, is_property = False, False
            s, s_type_zh, p_zh, o, o_type_zh = spo[0], spo[1], spo[2], spo[3], spo[4]
            s = s.replace("《", '').replace("》", '').replace("'", "`")
            if s not in subject_records:
                subject_records[s] = (
                    SPGRecord(spg_type_name=self.aligner.type_zh_to_en(s_type_zh))
                    # .upsert_property("id", s)
                    .upsert_property("name", s)
                )
            if p_zh in self.property_info_zh[s_type_zh]:
                p, _, o_type = self.property_info_zh[s_type_zh][p_zh]
                is_property = True
            elif p_zh in self.relation_info_zh[s_type_zh]:
                p, _, o_type = self.relation_info_zh[s_type_zh][p_zh]
                is_relation = True
            elif p_zh in self.aligner.entity_has.get(s_type_zh, []) or p_zh in self.aligner.property_has.get(s_type_zh, []):
                p, _, o_type = p_zh, "", self.aligner.type_zh_to_en(o_type_zh)
                if s not in basic_infos:
                    basic_infos[s] = {p_zh: o}
                else:
                    basic_infos[s].update({p_zh: o})
            else:
                p, _, o_type = p_zh, "", self.aligner.type_zh_to_en(o_type_zh)
                if s not in other_infos:
                    other_infos[s] = {p_zh: o}
                else:
                    other_infos[s].update({p_zh: o})

            if is_relation:
                if "." not in o_type or "STD." in o_type:
                    continue
                o = o.replace("《", '').replace("》", '').replace("'", "`")
                old_o = subject_records[s].get_relation(p, o_type, "")
                o = o + ',' + old_o if old_o else o
                o_list = re.split("[,，、;；]", o)
                o = ','.join(o_list)
                result.extend(
                    [
                        SPGRecord(o_type)
                        # .upsert_property("id", _o)
                        .upsert_property("name", _o)
                        for _o in o_list
                    ]
                )
                subject_records[s].upsert_relation(p, o_type, o)
            elif is_property:
                o = o.replace("《", '').replace("》", '').replace("'", "`")
                old_o = subject_records[s].get_property(p, "")
                o = o + ',' + old_o if old_o else o
                o_list = re.split("[,，、;；]", o)
                o = ','.join(o_list)
                result.extend(
                    [
                        SPGRecord(o_type)
                        # .upsert_property("id", _o)
                        .upsert_property("name", _o)
                        for _o in o_list
                    ]
                )
                subject_records[s].upsert_property(p, o)
            else:
                pass
        for s, v in basic_infos.items():
            subject_records[s].upsert_property("basicInfo", json.dumps(basic_infos[s], ensure_ascii=False))
        for s, v in other_infos.items():
            subject_records[s].upsert_property("otherInfo", json.dumps(other_infos[s], ensure_ascii=False))

        for subject_record in subject_records.values():
            result.append(subject_record)
        return result
