import os
import re
import asyncio
from collections import deque
import json
import logging
from knext.ca.base import Memory, Question, KagBaseModule

logger = logging.getLogger(__name__)


class FetchDomain(KagBaseModule):
    def __init__(self, llm_module, use_default_prompt_template=True):
        super().__init__(llm_module, use_default_prompt_template)

    def preprocess(self, question: Question):
        prompt = self.state_dict['prompt_template'].substitute(
            question=question.question
        )
        return prompt

    def postprocess(self, llm_output):
        parts = llm_output.split("llm_output:")
        result = parts[-1] if len(parts) > 1 else llm_output
        return result

    def get_module_name(self):
        return "FetchDomain"


class DivideQuestion(KagBaseModule):
    def __init__(self, llm_module, use_default_prompt_template=True):
        super().__init__(llm_module, use_default_prompt_template)

    def get_module_name(self):
        return "DivideQuestion"

    def preprocess(self, question: Question):
        prompt = self.state_dict['prompt_template'].substitute(
            question=question.question
        )
        self.question = question
        return prompt

    def postprocess(self, llm_output):
        def _output_parse(_output_string):
            # parse output
            parts = _output_string.split("llm_output:")  # 分割一次
            result = parts[-1] if len(parts) > 1 else _output_string
            # parse \n
            parts_2 = result.split('依赖关系是:')
            qustion = parts_2[0].strip().split('\n')
            dep = parts_2[1].strip().split('\n')
            return qustion, dep

        def _process_dep(_input_list):
            dep_dict = {}
            for dep in _input_list:
                res = dep.split("依赖")
                assert len(res) == 2
                key = res[0].strip()
                dep = res[1].strip('"').split(",") if "," in res[1] else res[1].strip().split("，")
                dep_real = [dep_i.strip() for dep_i in dep]
                dep_dict[key] = dep_real
            return dep_dict

        result_string = _output_parse(llm_output)
        sub_questions_list = []
        sub_logic_forms_list = []
        for org_question in result_string[0]:
            sub_questions_list.append(org_question)
        sub_dependencies = _process_dep(result_string[1])
        qk_Q_map = {}

        org_question_children = []
        for q_ind, sub_question in enumerate(sub_questions_list):
            q_key = f'问题{q_ind+1}'
            q_deps_Q_list = []
            for q_dep in sub_dependencies[q_key]:
                if q_dep == "None":
                    pass
                else:
                    q_deps_Q_list.append(qk_Q_map[q_dep])
            qk_Q_map[q_key] = Question(sub_question, q_deps_Q_list, [])
            org_question_children.append(qk_Q_map[q_key])
        self.question.children = org_question_children
        return list(qk_Q_map.values())


class RewriteQuestionBasedOnDeps(KagBaseModule):
    def __init__(self, llm_module, use_default_prompt_template=True):
        super().__init__(llm_module, use_default_prompt_template)

    def get_module_name(self):
        return "RewriteQuestionBasedOnDeps"

    def preprocess(self, question: Question):
        context_string = ''    
        if len(question.dependencies) > 0:
            for q in question.dependencies:
                context_string += f"问题：{q.question} \n 答案：{q.answer}"+'\n'
            prompt = self.state_dict['prompt_template'].substitute(
                question=question.question,
                context=context_string
            )
            return prompt
        else:
            return None

    def postprocess(self, llm_output):
        parts = llm_output.split("llm_output:")
        result = parts[-1] if len(parts) > 1 else llm_output
        return result


class MergeQuestionBasedOnChildren(KagBaseModule):
    def __init__(self, llm_module, use_default_prompt_template=True):
        super().__init__(llm_module, use_default_prompt_template)

    def get_module_name(self):
        return "MergeQuestionBasedOnChildren"

    def preprocess(self, question: Question):
        context_string = ''    
        if len(question.children) > 0:
            for q in question.children:
                context_string += f"问题：{q.question} \n 答案：{q.answer}"+'\n'
            prompt = self.state_dict['prompt_template'].substitute(
                question=question.question,
                context=context_string
            )
            return prompt
        else:
            return None

    def postprocess(self, llm_output):
        parts = llm_output.split("llm_output:")
        result = parts[-1] if len(parts) > 1 else llm_output
        return result


class DoesQuestionNeedExtraInfo(KagBaseModule):
    def __init__(self, llm_module, use_default_prompt_template=True):
        super().__init__(llm_module, use_default_prompt_template)

    def get_module_name(self):
        return "DoesQuestionNeedExtraInfo"

    def preprocess(self, question: Question):
        prompt = self.state_dict['prompt_template'].substitute(
            question=question.question
        )
        return prompt

    def postprocess(self, llm_output):
        if llm_output == '是':
            return True
        elif llm_output == '否':
            return False
        else:
            warning_reuslt = f'结果为:{llm_output}'
            logger.debug(f'{warning_reuslt}')
            return False


class DoesQuestionSolved(KagBaseModule):
    def __init__(self, llm_module, use_default_prompt_template=True):
        super().__init__(llm_module, use_default_prompt_template)

    def get_module_name(self):
        return "DoesQuestionSolved"

    def preprocess(self, question: Question):
        prompt = self.state_dict['prompt_template'].substitute(
            question=question.question,
            answer=question.answer
        )
        return prompt

    def postprocess(self, llm_output):
        if llm_output == '是':
            return True
        elif llm_output == '否':
            return result
        else:
            warning_reuslt = f'结果为:{llm_output}'
            logger.debug(f'{warning_reuslt}')
            return False


class AnswerQuestion(KagBaseModule):
    def __init__(self, llm_module, web_search=None, kbqa=None, use_default_prompt_template=True):
        super().__init__(llm_module, use_default_prompt_template)
        self.web_search = web_search
        self.kbqa = kbqa
        assert (web_search is not None) or (kbqa is not None)

    def get_module_name(self):
        return "AnswerQuestion"

    def preprocess(self, question: Question):
        kbqa_succeed = False
        kbqa_result = None
        context = ""
        if self.kbqa:
            kbqa_succeed, kbqa_result = self.kbqa.generate_answer(question.question)
            logger.info(f'kbqa_succeed: {kbqa_succeed}')
            kbqa_context = ""
            if kbqa_succeed:
                kbqa_abstract = json.loads(kbqa_result['answer'])['abstract']
                logger.info(f'kbqa_abstract: {kbqa_abstract}')
                kbqa_context = f'问题: {question.question}. 答案: {kbqa_abstract}'
                context += kbqa_context

        #if not self.kbqa_succeed and self.web_search: 
        if self.web_search:            
            web_search_results = ""
            kbqa_result = []
            for wb_ind, wb_result in enumerate(self.web_search.search(question.question, top_k=1)):
                for name, record in wb_result.items():
                    kbqa_result.append({name: record})
                web_search_results += f'问题: {question.question}. 答案: {wb_result}\n'
            logger.info(f'web_search_results\n{web_search_results}')
            context += web_search_results

        # add deps
        for d_q in question.dependencies:
            context += f'{d_q.question}: {d_q.answer}\n'

        # add children
        for c_q in question.children:
            context += f'{c_q.question}: {c_q.answer}\n'
        
        prompt = self.state_dict['prompt_template'].substitute(
            question=question.question,
            context=context,
        )
        return prompt, kbqa_result

    def forward(self, question: Question):
        prompt, kbqa_result = self.preprocess(question)
        llm_output = self.llm_module.generate(prompt)
        post_processed_output = self.postprocess(llm_output, kbqa_result)
        return post_processed_output

    def postprocess(self, llm_output, kbqa_result):
        return llm_output, kbqa_result
