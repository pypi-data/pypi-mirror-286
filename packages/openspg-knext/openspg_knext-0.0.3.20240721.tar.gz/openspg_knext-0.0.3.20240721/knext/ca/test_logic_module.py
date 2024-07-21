import os
import json
import sys
sys.path.append('/mnt/new_nas/users/kongfa/Codes/kag_agent')
from string import Template


import inspect
from knext import ca
from knext.ca.logic_module import FetchDomain, DivideQuestion, Question
from knext.ca.logic_module import RewriteQuestionBasedOnDeps
from knext.ca.logic_module import DoesQuestionNeedExtraInfo
from knext.ca.logic_module import MergeQuestionBasedOnChildren
from knext.ca.logic_module import AnswerQuestion
from knext.ca.tools import LLMModule, WebSearch, KBQAModule


def get_ca_default_prompt_template_dir():
    directory = os.path.dirname(ca.__file__)
    return os.path.join(directory, 'default_prompt_template')


def fetch_domain_lab():
    llm = LLMModule(domain='常识')
    fetch_domain_module = FetchDomain(llm)
    result = fetch_domain_module.forward(Question("周杰伦的老婆是谁", [], []))
    print(result)


def test_divide_question_lab():
    llm = LLMModule()
    fetch_domain_module = DivideQuestion(llm)
    result = fetch_domain_module.forward(
        #Question("请问同时出演过《猎冰》和《狂飙》的演员是谁？", [], [])
        #Question("没有营业执照可以办理宁波市-宁海县的公章刻制业特种行业许可证么?", [], [])
        Question("65岁能办理绍兴市-新昌县的道路危险货物运输装卸管理人员和押运人员从业资格证么?", [], [])

    )
    for q in result:
        print(q.question)


def rewrite_question_lab():
    llm = LLMModule(domain='常识')
    rewrite_question_module = RewriteQuestionBasedOnDeps(llm)
    dep = Question('钱学森的妻子是谁？')
    dep.answer = '钱学森的妻子是蒋英'
    result = rewrite_question_module.forward(
        Question("钱学森的妻子的父亲是谁？", [dep])
    )
    print(result)


def question_need_info_lab():
    llm = LLMModule(domain='常识')
    does_q_need_info = DoesQuestionNeedExtraInfo(llm)
    result = does_q_need_info.forward(
        Question("钱学森的妻子的父亲是谁？")
    )
    print(result)


def merge_question_lab():
    llm = LLMModule(domain='常识')
    merge_q = MergeQuestionBasedOnChildren(llm)
    q1 = Question("钱学森的妻子是谁？")
    q1.answer = "蒋英"
    q2 = Question("蒋英的父亲是谁？")
    q2.answer = "蒋百里"
    children=[q1, q2]
    result = merge_q.forward(
        Question("钱学森的妻子的父亲是谁？", children=children)
    )
    print(result)

def answer_question_lab():
    llm = LLMModule(domain='常识')
    answer_question = AnswerQuestion(llm, WebSearch(), KBQAModule())
    result = answer_question.forward(
        Question("金庸和徐志摩的关系是什么")
    )
    print(result)


if __name__ == '__main__':
    #fetch_domain_lab()
    divide_question_lab()
    #rewrite_question_lab()
    #question_need_info_lab()
    #merge_question_lab()
    #answer_question_lab()

