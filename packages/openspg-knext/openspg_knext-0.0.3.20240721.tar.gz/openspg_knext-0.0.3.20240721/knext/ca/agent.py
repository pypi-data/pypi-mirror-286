import os
import re
import asyncio
from collections import deque
import json
import requests
import traceback
import copy
from datetime import datetime
import logging
from knext.ca.tools import LLMModule, WebSearch, KBQAModule, HotEventModule, Retriever
from knext.ca.base import Memory, Question
from knext.ca.logic_module import FetchDomain, DivideQuestion
from knext.ca.logic_module import RewriteQuestionBasedOnDeps
from knext.ca.logic_module import DoesQuestionSolved
from knext.ca.logic_module import DoesQuestionNeedExtraInfo
from knext.ca.logic_module import MergeQuestionBasedOnChildren
from knext.ca.logic_module import AnswerQuestion

logger = logging.getLogger(__name__)


class DivideAndConquerAgent(object):
    def __init__(self, task_id: int, project_id: int, debug_mode=False, report_log=False, use_default_prompt_template=True):
        self.llm = LLMModule()
        self.fetch_domain = FetchDomain(self.llm, use_default_prompt_template)
        self.divide_question = DivideQuestion(self.llm, use_default_prompt_template)
        self.rewrite_question = RewriteQuestionBasedOnDeps(self.llm, use_default_prompt_template)
        self.does_question_need_info = DoesQuestionNeedExtraInfo(self.llm, use_default_prompt_template)
        self.merge_question = MergeQuestionBasedOnChildren(self.llm, use_default_prompt_template)
        self.answer_question = AnswerQuestion(self.llm, Retriever(project_id=project_id), None, use_default_prompt_template)
        self.memory = Memory(self.llm)
        self.hot_event_module = HotEventModule()

        self.debug_mode = debug_mode
        self.queue = None
        self.queue_tasks = []
        self.task_id = task_id
        self._java_service_url = "akg-pre.alipay.com"
        self.query_code = None
        self.report_log = report_log
        self.result_collector = {
            "答案":[],
            "推理过程":{},
            "图谱证据链":[],
        }

    async def is_question_deps_ready(self, question: Question):
        while True:
            all_solved = True
            for dep in question.dependencies:
                if not dep.is_solved():
                    all_solved = False
            if all_solved:
                break
            await asyncio.sleep(0.5)
        return

    async def is_question_children_ready(self, question: Question):
        while True:
            all_solved = True
            for child in question.children:
                if not child.is_solved():
                    all_solved = False
            if all_solved:
                break
            await asyncio.sleep(0.5)
        return

    async def merge_problem_impl(self, question: Question):
        await asyncio.create_task(self.is_question_children_ready(question))
        answer = self.merge_question.forward(question)
        info_dict = {
            'title': f'回答合并问题',
            'content': f'问题: {question.question}\n答案: {answer}',
        }
        self.store_into_intermediate_queue(info_dict)
        question.answer = answer
        return answer

    async def solve_problem_impl(self, question: Question):
        await asyncio.create_task(self.is_question_deps_ready(question))
        org_question_str = question.question

        rewrited_question = None
        if len(question.dependencies) > 0:
            rewrited_question = self.rewrite_question.forward(question)
            info_dict = {
                'title': f'重写问题',
                'content': f'原问题: {org_question_str}. 重写后的问题: {rewrited_question}',
            }
            self.store_into_intermediate_queue(info_dict)

            new_question = Question(rewrited_question, question.dependencies, question.children)
        else:
            new_question = question
        answer, kbqa_result = self.answer_question.forward(new_question)

        info_dict = {
            'title': f'回答问题',
            'content': f'问题: {org_question_str}. 答案: {answer}',
        }
        if kbqa_result:
            self.result_collector["图谱证据链"] = kbqa_result
            if kbqa_result != 'KBQA查找失败':
                self.kbqa_result_list.append(kbqa_result)
            # info_dict['kbqa'] = kbqa_result

        self.store_into_intermediate_queue(info_dict)
        question.answer = answer
        return question

    async def async_store_into_queue(self, info_str):
        await self.queue.put(info_str)

    def store_into_intermediate_queue(self, info_dict):
        if not isinstance(info_dict, StopAsyncIteration):
            if self.debug_mode:
                title = info_dict['title']
                content = info_dict['content']
                debug_str = f'{title}: {content}'
                print(debug_str)
                logger.info(debug_str)

            if self.report_log:
                title = info_dict['title']
                content = info_dict['content']
                task_id = self.task_id
                self._insert_query_log(task_id=task_id, title=title, log_content=content)

            self.queue_tasks.append(
                asyncio.create_task(
                    self.async_store_into_queue(info_dict)
                )
            )

    async def solve_problem_mainloop(self, question: Question, max_loop_time, query_code):
        self.query_code = query_code
        self.kbqa_result_list = []
        self.store_into_intermediate_queue(
            {
                'title': '开始处理问题',
                'content': f'{question.question}',
            }
        )

        current_domain = self.fetch_domain.forward(question)
        if current_domain == '其他':
            answer = f'用户问题: {question.question}不属于可回答领域，结束问答'
            self.store_into_intermediate_queue(
                {
                    'title': '领域判断',
                    'content': answer,
                }
            )
            self.store_into_intermediate_queue(StopAsyncIteration())
            return {
                'answer': answer,
                'kbqa_list': self.kbqa_result_list,
            }
        elif current_domain == '热点事件':
            try:
                hot_event_result = self.hot_event_module.search(question.question)
                self.store_into_intermediate_queue(StopAsyncIteration())
            except Exception as err:
                logger.info(f'通过热点事件查询失败。原因: {err}')
        else:
            pass

        self.store_into_intermediate_queue(
            {
                'title': '领域判断',
                'content': f'属于领域: {current_domain}',
            }
        )

        for i in range(max_loop_time):
            # divide and answer children question
            current_question = Question(question.question, question.dependencies, question.children)
            self.store_into_intermediate_queue(
                {
                    'title': '问题拆解',
                    'content': '开始按照逻辑进行问题拆解',
                }
            )
            children_questions = self.divide_question.forward(current_question)
            # print(current_question.question, [q.question for q in children_questions])
            for q_i, q in enumerate(children_questions):
                self.store_into_intermediate_queue(
                    {
                        'title': f'子问题{q_i}',
                        'content': q.question,
                    }
                )

            if len(children_questions) > 0:
                children_tasks = []
                for child_question in children_questions:
                    children_tasks.append(asyncio.create_task(self.solve_problem_impl(child_question)))

                children_answers = []
                for c_task in children_tasks:
                    child_answer = await c_task
                    self.result_collector["推理过程"][child_answer.question] = child_answer.answer
                    child_answer = child_answer.answer

            # answer parent question
            parent_task = asyncio.create_task(self.merge_problem_impl(current_question))
            answer = await parent_task
            if i + 1 == max_loop_time:
                # self.store_into_intermediate_queue(f'问题{question.question}解决完成，答案：{answer}')
                self.store_into_intermediate_queue(
                    {
                        'title': f'解决完成',
                        'content': f'答案: {answer}',
                    }
                )
            else:
                verify_result = self.verify_problem_solved(question)
                if verify_result == '是':
                    self.store_into_intermediate_queue(f'答案：{answer}')
                    break
                else:
                    now_question = Question(verify_result, question.dependencies, question.children)
                    self.store_into_intermediate_queue(
                        f'问题{question.question}未能解决完成，继续回答问题：{now_question.question}')

        self.store_into_intermediate_queue(StopAsyncIteration())
        return {
            'answer': answer,
            'kbqa_list': self.kbqa_result_list,
        }

    def _insert_query_log(self, task_id, title=None, log_content=None):
        url = f"http://127.0.0.1:8887/public/v1/reasoner/dialog/report"
        data = {
            "taskId": task_id,
            "executeStatus": title,
            "content": log_content,
            "gmtCreate": self._gmt_create(),
        }
        print(data)
        try:
            r = requests.get(url, params=data)
            if r.status_code == 200:
                logger.info(f"insert query log success")
            else:
                logger.warning(f"insert query log failed: {r.text}")
        except Exception:
            err_msg = traceback.format_exc()
            logger.warning(f"insert query log error: {err_msg}")

    def _gmt_create(self):
        current_time = datetime.now()
        formatted_time = current_time.strftime('%Y-%m-%d %H:%M:%S')
        return formatted_time

    def reset_context(self):
        self.remaining_question_set = set()
        self.ready_question_set = set()
        self.solved_question_set = set()
        self.ready_question_count = 0
        self.queue = asyncio.Queue()
        self.queue_tasks = []

    def forward(self, question: Question, query_code="test"):
        loop = asyncio.new_event_loop()  # 创建新的事件循环
        asyncio.set_event_loop(loop)  # 设置当前线程的事件循环为新创建的
        self.reset_context()
        self.query_code = query_code
        # self.queue = asyncio.Queue()
        max_loop_time = 1
        # if loop.is_running():
        #     result = asyncio.ensure_future(self.solve_problem_mainloop(question, max_loop_time))
        # else:
        result = loop.run_until_complete(self.solve_problem_mainloop(question, max_loop_time, query_code))
        self.result_collector["答案"].append(result['answer'])
        return self.result_collector


if __name__ == '__main__':
    query = "周杰伦的孩子分别叫什么"
    divide_and_conquer_agent = DivideAndConquerAgent(project_id=2, debug_mode=True)
    question = Question(question=query)
    result = divide_and_conquer_agent.forward(question)
    print(divide_and_conquer_agent.result_collector)

