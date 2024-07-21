import json
import os
#os.environ["KNEXT_HOST_ADDR"]="http://30.183.176.183:8887"
# from nscommon.maya.maya_service.maya_service_client import MayaServiceClient

# from antllm.api.completion import Completion
# import time

from knext.builder.auto_extract.common.llm_client import LLMClient
from knext.common import project as rest
from knext.common.search import SearchClient


def query_mobile_search(sceneCode, userId, query, searchSrc, paramsMap):
    request_query = {
        "sceneCode": sceneCode,
        "uid": userId,
        "query": query,
        "searchSrc": searchSrc,
        "paramsMap": paramsMap,
    }
    print(request_query)
    # url = os.path.join(None, 'open/search/mobileSearch')
    url = "https://automl.alipay.com/webapi/v1/open/search/mobileSearch"

    try:
        import requests

        response = requests.post(url, json=request_query)

        print(response.text)

        if response.status_code == 200:
            return response.text
        else:
            print(
                f"request fail, status code: {response.status_code}, content: {response.text}"
            )
    except Exception as e:
        print(e)


def mobile_search(query):
    # 构建搜索参数
    search_param = {
        "whole_search_strategy": "whole_network_search",  # 固定值，必填
        "source": "alps_rag",  # 检索请求源，必填
        # "domain_filter": "baike.baidu.com" # 过滤白名单，用于指定搜索源，可以不填
    }

    # 默认参数设置，以下参数均为必填
    paramsMap = {
        "actionSrc": "llmContent",
        "targetTabId": "",
        "requestType": "llmWholeSearch",
        "client_os": "android",
        "client_version": "10.5.26.5406",
        "bird_params": '{"tplVersion":"6.0.3", "platform":"android"}',
        "lbs": "121.4695052083333,31.22249484592014",
        "whole_search_param": str(search_param),
    }

    # 通过modelhub接口将参数透传进行查询
    # from alps.modelhub.api_client import modelhub

    response_str = query_mobile_search(
        sceneCode="llmWholeSearchFeedScene",  # 场景码，必填
        userId="2088312389916284",  # 用户id，必填
        query=query,  # 查询文本
        searchSrc="LLMweb",
        paramsMap=paramsMap,
    )

    response_dict = json.loads(response_str)
    return response_dict


# class Qwen_72B_chat_online_pipe:
#     def __init__(self):
#         self.client = MayaServiceClient(
#             scene_name="Qwen_Qwen_72B_Chat_int4", chain_name="v1"
#         )
#
#     def generate(self, prompt):
#         features = []
#         feature_0 = {
#             "message": prompt[:2000],
#             "max_input_len": 2000,
#             "max_output_len": 1024,
#         }
#         features.append(feature_0)
#         response = self.client.call_service(features, debug=False)
#         return response[0]


# class Qwen_1_5_72B_chat_online_pipe:
#     def __init__(self):
#         from nscommon.maya.maya_service.maya_service_client import MayaServiceClient
#
#         self.client = MayaServiceClient(
#             scene_name="Qwen1_5_110B_Chat_GPTQ_Int4", chain_name="v1"
#         )
#
#     def generate(self, prompt):
#         features = []
#         feature_0 = {
#             "message": prompt[:4000],
#             "max_input_len": 4000,
#             "max_output_len": 1024,
#         }
#         features.append(feature_0)
#         response = self.client.call_service(features, debug=False)
#         return response[0]


# class Qwen1_5_14B_chat_online_pipe:
#     def __init__(self):
#         self.client = Qwen15_14B_chat_vllm(top_p=0.8)

#     def generate(self, prompt):
#         return self.client.invoke(prompt)

# class bailing_65B_0315_online_pipe:
#     def __init__(self):
#         self.client = Bailing_65B_0315()

#     def generate(self, prompt):
#         return self.client.invoke(prompt)

# class Flash_extractor_pipe:
#     def __init__(self, local_path):
#         # path = os.path.join(local_path, 'flash_extractor')
#         self.completer = Completion(local_path)

#     def generate(self, prompt):
#         st = time.time()
#         response = self.completer.generate(prompt, max_tokens=1000).texts[0]
#         ed = time.time()
#         print(round(ed-st, 3) * 1000)
#         return response


# class Flash_extractor_pipe:
#     def __init__(self):
#         self.client = LLMClient.from_config_name("bailing")
#
#     def generate(self, prompt):
#         print(prompt)
#         st = time.time()
#         features = []
#         # maya2部署feature的字段
#         feature_0 = {
#             "message": prompt,
#             "max_input_len": 4096,
#             "max_output_len": 1024,
#             "lora_name": self.lora_name,  # 需要指定自己任务的lora_name, 没有时不填
#         }
#         features.append(feature_0)
#         response = self.client(features, debug=False)
#         ed = time.time()
#         print("摘要耗时：{}ms".format(round(ed - st, 3) * 1000))
#         print(response[0])
#         return response[0]


class KGQA_pipe:
    def __init__(self):
        self.client = LLMClient.from_config_name("kbqa")

    def process(self, features):
        return self.client(features)


class Reasoner:
    def __init__(self, pipe):
        self.llm = pipe
        self.update_reason_path = []

    def judge(self, instruction, memory):
        prompt = "判断在完全依据当前已知信息且不允许推断的情况下，你是否能够完整准确地回复或完成指令“{}”。已知信息：“{}”。如果能，请回复“是”，之后给出对指令{}准确的回复，不要复述指令；如果不能，请回复“否”，并给出理由。".format(
            instruction, memory, instruction
        )
        print(prompt)
        response = self.llm(prompt)
        if response[0] == "是":
            if_finished = True
        else:
            if_finished = False
        return if_finished, response

    def plan(self, instruction, memory):
        prompt = (
            "基于当前的已知信息：“{}”\n如果需要完整准确地回复或完成指令“{}”，你还需要什么步骤，每一步以问题的形式提出，并分行列出。".format(
                memory, instruction
            )
        )
        response = self.llm(prompt)
        update_reason_path = self.format_reason_path(response)
        return update_reason_path

    def format_reason_path(self, response):
        update_reason_path = response.split("\n")
        return update_reason_path


class Retriever:
    def __init__(self, route="web-search", project_id=1):
        self.route = route
        self.project_id = project_id

    def retrieve(self, query, top_k):
        docs = []
        if self.route == "web-search":
            response_list = mobile_search(query)
            for r in response_list["feedInfo"]["feeds"][:top_k]:
                feed = r["extInfo"]["title"] + "|" + r["extInfo"]["abstract_extract"]
                if feed not in docs:
                    docs.append(feed)
        elif self.route == "esearch":
            client = rest.ProjectApi()
            projects = client.project_get()
            namespace = "DEFAULT"
            for project in projects:
                item = project.to_dict()
                if str(item["id"]) == str(self.project_id):
                    namespace = item["namespace"]
                    break
            search_client = SearchClient(spg_type_name=f"{namespace}.Chunk")
            query_dict = {"match": {"content": query}}
            records = search_client.search(query=query_dict, size=top_k)
            for r in records:
                feed = {}
                feed[r.properties.get("name")] = r.properties.get("content")
                if feed not in docs:
                    docs.append(feed)
        return docs


class Memory:
    def __init__(self, pipe):
        self.llm = pipe
        self.evidence_memory = []

    def extractor(self, docs, instruction):
        prompt = "根据以下文段，总结与指令“{}”相关的关键信息，并明确解释为何与指令相关。如果没有相关信息，直接返回空字符串。\n“{}”\n请确保所提供的信息准确反映了文段的内容。".format(
            instruction, str(docs)
        )
        print(prompt)
        evidence = self.llm(prompt)
        if evidence not in self.evidence_memory:
            self.evidence_memory.append(evidence)

    def serialize_memory(self):
        serialize_memory = "[证据记忆]:{}\n".format(str(self.evidence_memory))
        return serialize_memory


class Generator:
    def __init__(self, pipe):
        self.llm = pipe

    def generate(self, instruction, memory):
        prompt = "请根据已知信息：“{}”\n准确地回复指令“{}”，并给出解释。".format(memory, instruction)
        response = self.llm(prompt)
        return response


class AntKnowAgent:
    def __init__(self, reason_llm, memory_llm, generate_llm, top_k, project_id):
        self.reasoner = Reasoner(reason_llm)
        self.retriever = Retriever("esearch", project_id=project_id)
        self.memory = Memory(memory_llm)
        self.generator = Generator(generate_llm)
        self.top_k = top_k

    def agent_process(self, instruction):
        if_finished = False
        present_instruction = instruction
        present_memory = ""
        run_cnt = 0
        response = ""
        planning_path = [instruction]
        doc_path = []
        while not if_finished and run_cnt < 3:
            print("RUN[{}]\n".format(str(run_cnt)))
            run_cnt += 1
            docs = self.retriever.retrieve(present_instruction, self.top_k)
            for doc in docs:
                if doc not in doc_path:
                    doc_path.append(doc)
            self.memory.extractor(docs, instruction)
            present_memory = self.memory.serialize_memory()
            if_finished, response = self.reasoner.judge(instruction, present_memory)
            if not if_finished:
                update_reason_path = self.reasoner.plan(instruction, present_memory)
                planning_path.append(str(update_reason_path))
                print("当前推理路径为：", update_reason_path)
                present_instruction = update_reason_path[0]
        if if_finished:
            response = response.replace("是\n", "").replace("是。", "")
        else:
            response = self.generator.generate(instruction, present_memory)
            print("当前记忆:{}".format(present_memory))
        return response, planning_path, doc_path, self.memory.evidence_memory

# if __name__ == '__main__':
#     agent = AntKnowAgent()