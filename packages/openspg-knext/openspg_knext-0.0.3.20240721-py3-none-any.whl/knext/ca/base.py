import os
from string import Template

import logging

logger = logging.getLogger(__name__)


# class Memory(object):
#     def __init__(self):
#         self.storage = {}
#
#     def store(self, question, answer):
#         self.storage[question] = answer
#
#     def retrieve(self, question):
#         return self.storage.get(question, "Answer not found")
#
#     def fetch_all_answers(self):
#         result = []
#         for k, v in self.storage.items():
#             result.append(v)
#         return result


class Memory:
    def __init__(self, pipe):
        self.llm = pipe
        self.evidence_memory = []

    def extractor(self, docs, instruction):
        prompt = "根据以下文段，总结与指令“{}”相关的关键信息，并明确解释为何与指令相关。如果没有相关信息，直接返回空字符串。\n“{}”\n请确保所提供的信息准确反映了文段的内容。".format(
            instruction, str(docs)
        )
        evidence = self.llm(prompt)
        if evidence not in self.evidence_memory:
            self.evidence_memory.append(evidence)

    def serialize_memory(self):
        serialize_memory = "[证据记忆]:{}\n".format(str(self.evidence_memory))
        return serialize_memory


class Question(object):
    '''
        问题和问题之间可能存在两种关系：
        1. 一个问题的问题内容，依赖于另一个问题的答案
        2. 一个问题的
    '''
    def __init__(self, question, dependencies=[], children=[]):
        self.question = question
        self.dependencies = dependencies
        self.children = children
        self.answer = None

    def is_solved(self):
        return self.answer is not None

    def __str__(self):
        repr_str = f'''question: {self.question}\ndeps:\n'''
        # dependies
        for ind, dep in enumerate(self.dependencies):
            repr_str += f'  dep_question {ind}: {dep.question}\n'
        return repr_str


class KagBaseModule(object):
    def __init__(self, llm_module, use_default_prompt_template=True):
        self.llm_module = llm_module
        self.state_dict = self.init_state_dict(use_default_prompt_template)
        
    def get_module_name(self):
        raise NotImplementedError

    def forward(self, question: Question):
        prompt = self.preprocess(question)
        # print("--------------------prompt--------------------")
        # print(prompt)
        llm_output = self.llm_module.generate(prompt)
        # print("--------------------llm_output--------------------")
        # print(llm_output)
        post_processed_output = self.postprocess(llm_output)
        # print("--------------------post_processed_output--------------------")
        # print(post_processed_output)
        return post_processed_output

    def preprocess(self, question: Question):
        return question.question

    def postprocess(self, llm_output):
        return llm_output

    def get_ca_default_prompt_template_dir(self):
        directory = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(directory, 'default_prompt_template')

    def load_prompt_template(self, prompt_dir):
        prompt_file_path = os.path.join(
            prompt_dir, 
            f'{self.get_module_name()}.txt'
        )
        with open(prompt_file_path, 'r') as f:
            template_string = f.read()
        return Template(template_string)

    def save_prompt_template(self, prompt_dir, prompt_template):
        prompt_file_path = os.path.join(
            prompt_dir, f'{self.get_module_name()}.txt')
        with open(prompt_file_path, 'w') as f:
            f.write(prompt_template)

    def create_default_state_dict(self):
        default_prompt_template = self.load_prompt_template(
            self.get_ca_default_prompt_template_dir())
        state_dict = {
            'prompt_template': default_prompt_template,
        }
        return state_dict

    def save_state_dict(self, save_dir, state_dict):
        prompt_dir = os.path.join(save_dir, 'prompt_template')
        os.makedirs(prompt_dir, exist_ok=True)
        self.save_prompt_template(prompt_dir, state_dict['prompt_template'].template)

    def load_state_dict(self, save_dir):
        prompt_dir = os.path.join(save_dir, 'prompt_template')
        prompt_template = self.load_prompt_template(prompt_dir)
        state_dict = {
            'prompt_template': prompt_template,
        }
        return state_dict

    def does_state_dict_exists(self, save_dir):
        prompt_file_path = os.path.join(
            save_dir, 'prompt_template', f'{self.get_module_name()}.txt')
        print(f'prompt_file_path: {prompt_file_path}')
        return os.path.exists(prompt_file_path)

    def init_state_dict(self, use_default_prompt_template):
        # load a fetch domain config from local dir
        if use_default_prompt_template:
            return self.create_default_state_dict()
        else:
            working_dir = os.getcwd()
            if self.does_state_dict_exists(working_dir):
                state_dict = self.load_state_dict(working_dir)
            else:
                state_dict = self.create_default_state_dict()
                self.save_state_dict(working_dir, state_dict)
            return state_dict
