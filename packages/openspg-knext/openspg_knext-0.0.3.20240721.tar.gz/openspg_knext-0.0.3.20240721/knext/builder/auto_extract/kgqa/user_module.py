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
import logging
import concurrent.futures
import concurrent.futures
# from agent_modules import Flash_extractor_pipe
from knext.builder.auto_extract.kgqa.agent_modules import AntKnowAgent, KGQA_pipe

from knext.builder.auto_extract.common.llm_client import LLMClient
from knext.ca.agent import DivideAndConquerAgent
from knext.ca.base import Question

logger = logging.getLogger()


class ControlGenModule(object):
    def __init__(self, project_id: int, load_model_info=None):
        # local_path = load_model_info["bailing_flash_extractor"]
        self.llm_core = LLMClient.from_config_name("deepseek")
        self.llm_gen = LLMClient.from_config_name("deepseek")
        self.kgqa_pipe = KGQA_pipe()
        self.project_id = project_id

    def _call_agent_answer(self, features: dict):
        if "top_k" in features.keys():
            top_k = features["top_k"]
        else:
            top_k = 8
        self.llm_extractor = LLMClient.from_config_name("deepseek")
        self.core_agent = AntKnowAgent(
            reason_llm=self.llm_core,
            memory_llm=self.llm_extractor,
            generate_llm=self.llm_gen,
            top_k=top_k,
            project_id=self.project_id
        )
        instruction = features["query"]
        response, p, d, m = self.core_agent.agent_process(instruction)
        evidence = d
        response = response.replace("\n", "")

        reason_dict = {}
        index = 0
        for item in p+m:
            index += 1
            reason_dict[index] = item
        return {
            "答案":[response],
            "推理过程":reason_dict,
            "图谱证据链":evidence,
        }

    def _call_kbqa_answer(self, features: dict):
        features["do_summery"] = True
        return self.kgqa_pipe.process(features)

    def _get_default_result(self):
        return {
            "msgtype": "markdown",
            "answer": "抱歉，数据增量建设中，暂未查到结果",
            "evidence": [],
            "source": "search/kbqa",
        }

    def _call_with_parall(self, features):
        # 注意，这里存在等待问题
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            # 启动两个子函数的并发执行
            kbqa_agent_future = executor.submit(self._call_kbqa_answer, features)
            search_agent_future = executor.submit(self._call_agent_answer, features)
            for future in concurrent.futures.as_completed(
                [kbqa_agent_future, search_agent_future]
            ):
                try:
                    f = future.result()
                    logger.info(f"{features}  __call__ result {f}")
                    if "answer" not in f.keys():
                        continue
                    if (
                        "not found" in f["answer"]
                        or "抱歉，图数据增量建设中，暂未查到结果" in f["answer"]
                        or f["answer"] == ""
                    ):
                        continue
                    return f
                except Exception as exc:
                    logger.error(
                        f"{features} run failed! err_info={str(exc)}", exc_info=True
                    )
        # 兜底策略
        return self._get_default_result()

    def _call_with_kbqa_first(self, features):
        f = self._call_kbqa_answer(features)[0]
        logger.info(f"{features}  __call__ kbqa result {f}")
        if (
            "answer" in f.keys()
            and ("not found" not in f["answer"])
            and "抱歉，图数据增量建设中，暂未查到结果" != f["answer"]
            and f["answer"] != ""
        ):
            return f
        f = self._call_agent_answer(features)
        logger.info(f"{features}  __call__ search result {f}")
        return f

    def __call__(self, features):
        if type(features) == list:
            features = features[0]
            return [self._call_with_parall(features)]
            # return [self._call_with_kbqa_first(features)]
        # return self._call_with_kbqa_first(features)
        return self._call_with_parall(features)


def create_user_module(load_model_info=None):
    return ControlGenModule(load_model_info)


class KGQA:

    def invoke(self, task_id: int, project_id: int, query: str):
        divide_and_conquer_agent = DivideAndConquerAgent(task_id=task_id, project_id=project_id, debug_mode=True, report_log=True)
        question = Question(question=query)
        divide_and_conquer_agent.forward(question)

        return None

    def invoke_2(self, project_id: int, query: str):
        pro = ControlGenModule(project_id=project_id)
        features = {"query": query, "top_k": 3}
        res = pro._call_agent_answer(features)
        import json
        return json.dumps(res, ensure_ascii=False, indent=4, separators=(',', ':'))



if __name__ == "__main__":
    # # text = '2024年北京半程马拉松吸引了空前的参赛热情，预报名人数达到97988人，创下了赛事历史新高。在3月12日启动报名后的3天内，来自42个国家和地区的跑者踊跃参与，其中北京本地选手占48%，而京外选手则占52%。比赛规模设定为2万人，包括男、女半程马拉松项目。这一数据充分展示了北京半马的广泛影响力和不断增长的吸引力。\n2024年4月14日的北京国际长跑节——北京半程马拉松赛事中，中国选手展现出色实力，成功包揽了男子和女子组别的冠军。在这场规模达2万人的比赛中，从天安门广场出发，终点位于奥林匹克公园中心区庆典广场。预报名人数高达97988人，男性选手占74%，女性选手占26%。这场盛事见证了中国选手的辉煌胜利。\n2024年4月14日，中国男子马拉松国家队成员何杰在北京半程马拉松中以1小时03分44秒的成绩首夺冠军，但比赛尾声时，三名外籍选手的可疑举动引发争议，他们似乎鼓励何杰超越并减速。这一事件在社交媒体上激起热议，北京市体育局随即介入调查。何杰作为杭州亚运会冠军及男子国家纪录保持者，其品牌赞助商特步也正对此事进行调查核实。\n2024年北京半程马拉松赛事中，男子组比赛成绩引发争议，尤其是中国选手何杰与三位非洲选手的表现。针对公众对比赛中某些情况的质疑，特别是关于三位非洲选手冲刺阶段的行为，北京半马组委会已成立专项调查组。调查组将对比赛结果进行全面、深入的审查，以确保公正性。组委会承诺将尽快公布调查结果，回应社会关切。\n2024年4月14日的北京半程马拉松比赛中，何杰在特步的支持下夺冠，但比赛直播中出现的场景引起争议，有人认为他受到了三名外籍选手的“保送”。作为赛事合作伙伴，特步在次日表示，公司正在与多方合作详细调查此事，并承诺将公布更多信息。北京市体育局也介入调查。何杰作为特步的签约运动员，其夺冠情况的争议使得特步的回应显得尤为重要。'
    # # query = '为新闻生成简要的标题，要求简洁清晰。【新闻】:{}'.format(text)
    # pro = ControlGenModule()
    # # features = {"query": query, "top_k": 1}
    # # res = pro.__call__(features)
    # # querys = ['吴京的国籍是哪里', '2024年唯一一次日全食是什么时候，在中国能看见吗', '2023年豆瓣评分最高的10部电影是什么']
    # querys = ["徐志摩和鹿鼎记的作者是什么关系"]
    # for query in querys:
    #     features = {"query": query, "top_k": 8}
    #     st = time.time()
    #     res = pro._call_agent_answer(features)
    #     ed = time.time()
    #     print(round(ed - st, 3) * 1000)
    agent = KGQA()
    query = "65岁能办理绍兴市-新昌县的道路危险货物运输装卸管理人员和押运人员从业资格证么？"
    print(agent.invoke(179, 3, query))
    # print(agent.invoke_2(3, query))
