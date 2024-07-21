import logging
import requests
import json
# from nscommon.maya.maya_service.maya_service_client import MayaServiceClient
# from ant_ha3_client.models import AreQrsStringQuery
# from ant_ha3_client.api.are_proxy_controller_api import AreProxyControllerApi

from knext.builder.auto_extract.common.llm_client import LLMClient
from knext.common import project as rest
from knext.common.search import SearchClient

logger = logging.getLogger(__name__)


class LLMModule(object):
    def __init__(self):
        # self.client = MayaServiceClient(
        #     #scene_name="Qwen1_5_110B_Chat_GPTQ_Int4",
        #     scene_name="Qwen1_5_110B",
        #     chain_name="v1",
        # )
        self.client = LLMClient.from_config_name("deepseek")
        self._llm_type = 'native_qwen_110B'

    def generate(self, prompt):
        return self.client(prompt)
        # message = prompt
        # features = []
        # feature_0 = {
        #     "message": prompt,
        #     "max_input_len":1024*10,
        #     "max_output_len":1024,
        # }
        # features.append(feature_0)
        # result = self.client(features)
        # result = result[0]
        # return result


class KBQAModule(object):
    def __init__(self):
        self.client = LLMClient.from_config_name("qwen")

    def generate_answer_path(self, query, return_content='answer'):
        assert return_content in ['native', 'logic_form', 'answer']
        try:
            features =  {
                'query': query,
                'do_executor': False,
                'req_id':'aaaaaa'
            }
            result = self.client(features)
            if return_content == 'native':
                return result
            elif return_content == 'logic_form':
                return result['logic_querys']
            elif return_content == 'answer':
                return result['answer_path'][0]['o']
        except Exception as err:
            return "KBQA查找失败"

    def generate_answer(self, query, return_content='answer'):
        assert return_content in ['native', 'logic_form', 'answer']
        try:
            logic_forms = self.generate_logic_form(query)
            logger.debug(f'BQA. query: {query}; logic_forms: {logic_forms}')
            url = "http://spgservice-standard-pre.alipay.com/v1/kgqa/task/execute"
            headers = {
                "Content-Type": "application/json"
            }
            data = {
                "query": query,
                "do_summary": True,
                "projectId": 641000302,
                "logicForms": logic_forms
            }

            response = requests.post(url, data=json.dumps(data), headers=headers).json()
            logger.debug(f'KBQA. query: {query}; response: {response}')
            if response['success'] and response['resultObject']['answer']:
                return True, response['resultObject']
            else:
                return False, "KBQA查找失败" 
        except Exception as err:
            print(f'kbqa exception: {err}')
            return False, "KBQA查找失败" 

    def generate_logic_form(self, query):
        features =  {
            'query': query,
            'do_executor': False
        }
        result = self.client.call_service(features)
        return result['logic_forms']

    def execute_logic_forms(self, query, logic_forms):
        features =  {
            'query': query,
            'do_executor': True,
            'logic_querys': logic_forms,
            #'do_get_detail': True,
            'logic_querys': logic_forms
        }
        result = self.client.call_service(features)
        return result['answer_path'][0]['o']


class WebSearch(object):
    def __init__(self):
        self.search_param = {
            "whole_search_strategy": "whole_network_search",  # 固定值，必填
            "source": "alps_rag",  # 检索请求源，必填
            # "domain_filter": "baike.baidu.com" # 过滤白名单，用于指定搜索源，可以不填
        }

        self.paramsMap = {
            "actionSrc": "llmContent",
            "targetTabId": "",
            "requestType": "llmWholeSearch",
            "client_os": "android",
            "client_version": "10.5.26.5406",
            "bird_params": '{"tplVersion":"6.0.3", "platform":"android"}',
            "lbs": "121.4695052083333,31.22249484592014",
            "whole_search_param": str(self.search_param),
        }

    def search(self, query, top_k=1):
        response_str = self.query_mobile_search(
            sceneCode="llmWholeSearchFeedScene",  # 场景码，必填
            userId="2088312389916284",  # 用户id，必填
            query=query,  # 查询文本
            searchSrc="LLMweb",
            paramsMap=self.paramsMap,
        )
        response_dict = json.loads(response_str)
        #return response_dict['feedInfo']['feeds'][0].keys()
        docs = []
        for r in response_dict["feedInfo"]["feeds"][:top_k]:
            feed = r["extInfo"]["title"] + "|" + r["extInfo"]["abstract_extract"]
            docs.append(feed)
        return docs

    def query_mobile_search(self, sceneCode, userId, query, searchSrc, paramsMap):
        request_query = {
            "sceneCode": sceneCode,
            "uid": userId,
            "query": query,
            "searchSrc": searchSrc,
            "paramsMap": paramsMap
        }
        url = 'https://automl.alipay.com/webapi/v1/open/search/mobileSearch'
        
        try:
            import requests
            response = requests.post(url, json=request_query)

            if response.status_code == 200:
                return response.text
            else:
                logger.info(f"request fail, status code: {response.status_code}, content: {response.text}")
        except Exception as e:
            logger.warning(e)


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



class Retriever:
    def __init__(self, project_id=1):
        self.project_id = project_id

    def retrieve(self, query, top_k):
        docs = []
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
        print(query_dict)
        records = search_client.search(query=query_dict, size=top_k)
        print(records)
        for r in records:
            feed = {}
            feed[r.properties.get("name")] = r.properties.get("content")
            if feed not in docs:
                docs.append(feed)
        return docs

    def search(self, query, top_k):
        return self.retrieve(query, top_k)



class HotEventModule(object):
    def __init__(self):
        # from ant_ha3_client.models import AreQrsStringQuery
        self.embedding_service_url = 'http://cv.gateway.alipay.com/ua/invoke'
        self.serviceCode = 'datacube-16631'
        self.request_type = 'embedding'
        self.cluster = 'kg_hot_event_offline'

    def apply_aidesk_3(self, text):
        if not isinstance(text,str):
            query = str(text)
        if len(text) == 0:
            return None
        headers = {
            'Content-Type': 'application/json',
        }
        data = {
            "params": {"type": self.request_type, "text":text}, 
            "serviceCode": self.serviceCode, 
            "appId": "f5bda3e2884a1075",
            "appName": "sentence_embedding",
            "attributes": {"_ROUTE_":"UA"}
        }
        json_str = json.dumps(data)
        response = requests.post(self.embedding_service_url, headers=headers, data=json_str)
        result_dict = response.json()
        try:
            prob = eval(result_dict['resultMap']['algo_result'])['result']
        except:
            prob = None
        return prob

    def get_embedding(self, text):
        retry = 0
        embedding = None
        while retry < 3 and not embedding:
            retry += 1
            embedding = self.apply_aidesk_3(text)[0]
        emb_str = str(embedding ).replace("[","").replace("]","").replace(" ","")
        return embedding, emb_str 


# query= name:"莫斯科" &&config=trace:TRACE3,format:xml,timeout:30000,hit:100,start:0,result_compress:no_compress,qrs_chain:embedding_768_chain,cluster:kg_hot_event_offline
    def search(self, query, hit_k=100, index_name='name', rank_profile=None, timestamp=None,time_opera = ">"):
        qrs_query = AreQrsStringQuery()
        cluster = self.cluster
        qrs_query.cluster = cluster

        if index_name != "embedding":
            if isinstance(query,str): 
                query_str = "query=" + index_name + ":'" + query + "' && config=format:protobuf,timeout:30000,hit:" + str(hit_k) + ",start:0,result_compress:no_compress,cluster:" + cluster
            elif isinstance(query,list):
                sub =' OR '.join([index_name+":'"+q+"' " for q in query])
                query_str = "query=" + sub + " &&config=format:protobuf,timeout:30000,hit:"+ str(hit_k) + ",start:0,result_compress:no_compress,qrs_chain:embedding_768_chain,cluster:" + cluster  
        else:
            query_str = "query=" + index_name + ":'" + query + "' &&config=format:protobuf,timeout:30000,hit:" + str(hit_k) + ",start:0,result_compress:no_compress,qrs_chain:embedding_768_chain,cluster:" + cluster  
    
        if rank_profile:
            query_str += " && rank=rank_profile:" + rank_profile   
        if timestamp:
            if cluster == "kg_hot_event_offline":
                query_str += " && filter=firstReportTime" + time_opera + str(timestamp)
            elif cluster == "kg_forum_hotevent":
                query_str += " && filter=occurTime" + time_opera + str(timestamp)
            else:
                query_str += ' && filter= ( mediaName="新浪新闻" OR mediaName="今日头条" OR mediaName="搜狐新闻客户端")'
    
        qrs_query.query_string =  query_str 
        qrs_query.biz_group="CTO_AIE"
        qrs_query.source="aistudio"
        are_proxy_api = AreProxyControllerApi()

        rst = []
        retry = 0
        while (not  rst and retry <10):
            qrs_result = are_proxy_api.qrs_search_using_post(body=qrs_query)
            rst = qrs_result.to_dict()
            retry +=1

        result = []
        try:
            for hit in rst['result_obj'][ 'hits']['hit']:
                summary = hit['summary'] 
                if "name" not in  summary:
                    continue
                
                if cluster == "kg_idx_news_offline" :
                    if 'publishTime' not in  summary :

                        print(" summary : no publishTime")
                    # print( summary["name"],int(summary['publishTime']),timestamp )
                    
                    if  time_opera==">" and timestamp and  int(summary['publishTime']) <  timestamp :
                    #print("时间过滤")
                        continue
                    elif time_opera=="<" and timestamp and  int(summary['publishTime']) > timestamp :
                        continue
                summary["index_name"]  = index_name
                if index_name !="embedding":
                    #print(summary)
                    summary["name"] =  summary["name"]#.replace("<font color=red>","").replace("</font>","").strip()
                    summary["description"] =  summary["description"][:1024]#.replace("<font color=red>","").replace("</font>","").strip()
                    _, summary["embedding"] = self.get_embedding(summary["name"])
                result.append(summary)
        except:
            print("召回报错：",rst)
        return  result



