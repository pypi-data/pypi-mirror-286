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

import ast
import os
import re
import json
import time
import uuid
from binascii import b2a_hex
from datetime import datetime
from pathlib import Path
from typing import Union, Dict, List, Any
from urllib import request
from openai import OpenAI

import requests
import traceback
from Crypto.Cipher import AES

from knext.builder.auto_extract.common import arks_pb2
from knext.builder.operator import PromptOp


DEFAULT_CONFIG_PATH = os.path.join(os.path.dirname(__file__), "../", "config")


class LLMClient:
    model: str

    @classmethod
    def from_config(cls, config: Union[str, dict], use_pre: bool = False):
        if isinstance(config, str) and Path(config).is_file():
            with open(config, "r") as f:
                nn_config = json.load(f)
        else:
            nn_config = config

        model_name = nn_config.get("model")
        scene_name = nn_config.get("scene_name")
        if "gpt" in model_name:
            return AntGPTClient(nn_config)
        elif scene_name:
            if use_pre:
                return MayaHttpClient.from_config(nn_config)
            else:
                return MayaDnsFilterClient.from_config(nn_config)
        else:
            return OpenAIClient.from_config(nn_config)

    @staticmethod
    def from_config_name(config_name: str, use_pre: bool = False):
        return LLMClient.from_config(
            os.path.join(DEFAULT_CONFIG_PATH, f"{config_name}.json"), use_pre
        )

    def remote_inference(self, prompt):
        raise NotImplementedError

    def invoke(self, variables: Dict[str, Any], prompt_op: PromptOp):
        result = []
        prompt = prompt_op.build_prompt(variables)
        print("Prompt: " + prompt)
        try:
            response = self.remote_inference(prompt)
            print("Response: " + str(response))
            result = prompt_op.parse_response(response)
            print("Result: " + str(result))
        except:
            errInfo = json.dumps(
                {
                    "traceback": traceback.format_exc(),
                }
            )
            print(errInfo)
            pass
        return result

    def batch(self, variables: Dict[str, Any], prompt_op: PromptOp) -> List:
        results = []
        prompts = prompt_op.build_prompt(variables)
        if isinstance(prompts, str):
            return self.invoke(variables, prompt_op)
        for idx, prompt in enumerate(prompts):
            print("Prompt_" + str(idx + 1) + ": " + prompt)
            try:
                response = self.remote_inference(
                    prompt=prompt,
                )
                print("Response_" + str(idx + 1) + ": " + str(response))
                result = prompt_op.parse_response(response, idx=idx, **variables)
                print("Result_" + str(idx + 1) + ": " + str(result))
                results.extend(result)
            except:
                errInfo = json.dumps(
                    {
                        "traceback": traceback.format_exc(),
                    }
                )
                print(errInfo)
                continue
        return results

    def mock_ee_response(self):
        raise NotImplementedError

    def mock_kg_response(self):
        raise NotImplementedError

    def mock_spo_response(self):
        raise NotImplementedError


class AntGPTClient(LLMClient):
    def __init__(self, config: Union[str, dict]):
        if isinstance(config, str) and Path(config).is_file():
            with open(config, "r") as f:
                self.nn_config = json.load(f)
        else:
            self.nn_config = config

        self.param = {k: v for k, v in self.nn_config.items()}
        self.url = self.param.pop("url")
        self.api_key = self.param.pop("apiKey")
        self.key = self.param.pop("key")
        self.model = self.param.pop("model")
        self.temperature = self.param.pop("temperature")
        self.max_tokens = self.param.pop("maxToken")
        self.n = self.param.pop("n")

        self.service_names = {
            "sync": "chatgpt_prompts_completions_query_dataview",
            "async": "asyn_chatgpt_prompts_completions_query_dataview",
            "query": "chatgpt_response_query_dataview",
        }

    def aes_encrypt(self, data):
        """aes加密函数，如果data不是16的倍数【加密文本data必须为16的倍数！】，那就补足为16的倍数
        :param key:
        :param data:
        """
        iv = "1234567890123456"
        cipher = AES.new(
            self.key.encode("utf-8"), AES.MODE_CBC, iv.encode("utf-8")
        )  # 设置AES加密模式 此处设置为CBC模式
        block_size = AES.block_size

        # 判断data是不是16的倍数，如果不是用b'\0'补足
        if len(data) % block_size != 0:
            add = block_size - (len(data) % block_size)
        else:
            add = 0
        data = data.encode("utf-8") + b"\0" * add
        encrypted = cipher.encrypt(data)  # aes加密
        result = b2a_hex(encrypted)  # b2a_hex encode  将二进制转换成16进制
        return result.decode("utf-8")

    def sync_request(self, prompt):
        # import pdb; pdb.set_trace()
        encodeurl = "%s" % self.url.encode("utf8")

        self.param["serviceName"] = self.service_names["sync"]
        self.param["queryConditions"] = {
            "url": encodeurl,
            "model": self.model,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "n": self.n,
            "api_key": self.api_key,
            "messages": prompt,
        }
        data = json.dumps(self.param)
        post_data = {"encryptedParam": self.aes_encrypt(data)}
        response = requests.post(
            self.url,
            data=json.dumps(post_data),
            headers={"Content-Type": "application/json"},
        )
        print(response.json())
        x = response.json()["data"]["values"]["data"]
        ast_str = ast.literal_eval("'" + x + "'")
        js = ast_str.replace("&quot;", '"')
        js = js.replace("&#39;", "'")
        data = json.loads(js)
        content = data["choices"][0]["message"]["content"]
        content = content.replace("&rdquo;", "”").replace("&ldquo;", "“")
        content = content.replace("&middot;", "")
        print(content)
        return content

    def async_request(self, prompt, message_key):
        # import pdb; pdb.set_trace()
        encodeurl = "%s" % self.url.encode("utf8")
        self.param["serviceName"] = self.service_names["async"]
        self.param["queryConditions"] = {
            "url": encodeurl,
            "model": self.model,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "n": self.n,
            "api_key": self.api_key,
            "messages": prompt,
            "messageKey": message_key,
            "outputType": "PULL",
        }
        data = json.dumps(self.param)
        post_data = {"encryptedParam": self.aes_encrypt(data)}
        response = requests.post(
            self.url,
            data=json.dumps(post_data),
            headers={"Content-Type": "application/json"},
        )
        return response

    def query_async_response(self, message_key, interval=1, timeout=120):
        self.param["serviceName"] = self.service_names["query"]
        self.param["queryConditions"] = {
            "messageKey": message_key,
        }
        data = json.dumps(self.param)
        post_data = {"encryptedParam": self.aes_encrypt(data)}

        start_time = time.time()
        count = 1
        while True:
            print(f"{count} attempts to query asynchronous gpt_client response...")
            response = requests.post(
                self.url,
                data=json.dumps(post_data),
                headers={"Content-Type": "application/json"},
            )
            values = response.json()["data"]["values"]
            if values:
                print(response.json())
                x = response.json()["data"]["values"]["response"]
                ast_str = ast.literal_eval("'" + x + "'")
                js = ast_str.replace("&quot;", '"')
                js = js.replace("&#39;", "'")
                data = json.loads(js)
                content = data["choices"][0]["message"]["content"]
                content = content.replace("&rdquo;", "”").replace("&ldquo;", "“")
                return content

            if time.time() - start_time > timeout:
                raise TimeoutError(f"Polling timed out, exceeding {timeout} seconds.")
            time.sleep(interval)
            count += 1

    def __call__(self, prompt):
        return self.sync_request(prompt)

    def remote_inference(self, prompt):
        content = [{"role": "user", "content": prompt}]
        now = datetime.now()
        timestamp = datetime.timestamp(now)
        async_message_key = "KNEXT_" + str(timestamp * 1000).split(".")[0]
        _response = self.async_request(content, async_message_key)
        if _response:
            response = self.query_async_response(async_message_key)
        else:
            raise ValueError("Async request error.")
        return response


class MayaHttpClient(LLMClient):
    """
    通过http服务访问MAYA服务
    不支持Batch调用, features需为Dict
    """

    def __init__(
        self,
        scene_name,
        chain_name="v1",
        uid="123456",
        lora_name=None,
        use_pre=False,
        model="",
    ):
        """

        Args:
            scene_name: 所部署的服务的名字
            chain_name: 所部署的服务的版本
            use_pre: 是否调用预发环境服务
        """
        self.service_name = scene_name
        self.chain_name = chain_name
        self.uid = uid
        self.lora_name = lora_name
        self.model = model
        self.query_service_id_token = "d9d0dd30-2c86-4329-8317-33cb617c184d"
        self.query_service_id_url = (
            "https://aistudio.alipay.com/api/v1/mpsMayaService/queryModelService"
        )
        self.model_service_id = self.get_service_id_by_service_name()
        self.client_headers = {
            "Content-Type": "application/json;charset=utf-8",
            "MPS-app-name": "test",
            "MPS-http-version": "1.0",
            "MPS-debug": "true",
        }
        if use_pre:
            self.client_url = f"https://paiplusinferencepre.alipay.com/inference/{self.model_service_id}/{self.chain_name}"
        else:
            self.client_url = f"https://paiplusinference.alipay.com/inference/{self.model_service_id}/{self.chain_name}"

    @classmethod
    def from_config(cls, config: Union[str, dict], use_pre: bool = False):
        uid = config.get("uid", "123456")
        scene_name = config.get("scene_name")
        chain_name = config.get("chain_name", "v1")
        lora_name = config.get("lora_name", "v1")
        model = config.get("model", "")
        return cls(scene_name, chain_name, uid, lora_name, use_pre, model)

    def get_service_id_by_service_name(self):
        # 通过service name查询service id
        params = {"sceneName": self.service_name, "token": self.query_service_id_token}
        result = requests.post(self.query_service_id_url, json=params)
        if result.status_code == 200:
            model_service_id = result.json()["data"][0]["modelServiceId"]
            # logger.info(f'get_service_id_by_service_name succeed: {model_service_id}')
            return model_service_id
        else:
            raise RuntimeError(
                f"get_service_id_by_service_name Error: {json.dumps(result.json(), indent=4)}"
            )

    def call_service(self, prompt: Dict, debug=False, keep_origin_features=False):
        """
        args:
            features: 进行预测的特征, 应为一个Dict, 当传入List时仅使用features[0]进行预测服务
            debug: 是否打印日志
            keep_origin_features: 是否保留原始特质, 即不进行in_string/out_string封装
        """
        if isinstance(prompt, List):
            features = prompt[0]
            # logger.warning(f"MayaHttpClient.call_service 'features' should be a Dict, but get List. "
            #                "call_service use features[0]")
        elif isinstance(prompt, str):
            features = {"message": prompt, "lora_name": self.lora_name}
        else:
            features = prompt
        if self.model_service_id:
            if keep_origin_features:
                input_dict = {"features": features}
            else:
                in_string = json.dumps(features, ensure_ascii=False)
                input_dict = {"features": {"in_string": in_string}}
            # if debug:
            #     logger.info(
            #         f"================= request =================\n"
            #         f"{input_dict}\n"
            #         f"================= request end ================="
            #     )
            r = requests.post(
                self.client_url, json=input_dict, headers=self.client_headers
            )
            # if debug:
            #     logger.info(
            #         f'================= response =================\n'
            #         f'{json.dumps(r.json(), indent=4)}\n'
            #         f'================= response end ================='
            #     )
            if r.status_code == 200:
                if r.json()["success"]:
                    if keep_origin_features:
                        result = r.json()["resultMap"]
                    else:
                        result = r.json()["resultMap"]["out_string"]
                    return result
                else:
                    raise RuntimeError(
                        f"Call Service Failed. \n{json.dumps(r.json(), indent=4)}"
                    )
            else:
                raise RuntimeError(
                    f"Call {self.model_service_id} failed. Error: {json.dumps(r.json(), indent=4)}"
                )
        else:
            raise RuntimeError(
                f"Service {self.service_name} client create failed. Try to create maya client later"
            )

    def __call__(self, prompt):
        return self.call_service(prompt)

    def remote_inference(self, prompt):
        result = self.call_service(prompt)
        match = re.search(r"```json(.*?)```", result)
        if match:
            result = match.group(1)
        try:
            json_result = json.loads(result)
        except:
            return result
        return json_result


class MayaDnsFilterClient(LLMClient):
    """
    通过Dns Filter的方式，在蚂蚁线上环境，进行服务调用
        - 只能线上环境，不能在mac端
        - 支持Batch调用, features需为List[Dict]格式
    """

    def __init__(
        self,
        scene_name,
        chain_name="v1",
        uid="123456",
        timeout=60000,
        max_input_len=1800,
        max_output_len=18000,
        ip_address=None,
        lora_name=None,
        model="",
    ):
        """
        args:
            scene_name: 所部署的服务的名字
            chain_name: 所部署的服务的版本
            client_request_timeout: 客户端请求超时时间
            connect_time_out: 连接超时时间
            port: java client agent启动时对应的端口号

        """
        self.scene_name = scene_name
        self.chain_name = chain_name
        self.uid = uid
        self.timeout = timeout
        self.max_input_len = max_input_len
        self.max_output_len = max_output_len
        self.ip_address = ip_address
        self.lora_name = lora_name
        self.model = model
        url_name = self.scene_name.lower().replace("_", "-")
        if ip_address:
            self.url = f"http://{self.ip_address}:10000/maya/pb/{self.scene_name}-{self.chain_name}"
        else:
            self.url = f"http://raymy.{url_name}.prod.global.alipay.com:10000/maya/pb/{self.scene_name}-{self.chain_name}"

    @classmethod
    def from_config(cls, config: Union[str, dict]):
        uid = config.get("uid", "123456")
        scene_name = config.get("scene_name")
        chain_name = config.get("chain_name", "v1")
        timeout = config.get("timeout", 60000)
        max_input_len = config.get("max_input_len", 1800)
        max_output_len = config.get("max_output_len", 18000)
        ip_address = config.get("ip_address", None)
        lora_name = config.get("lora_name", None)
        model = config.get("model", "")
        return cls(
            scene_name, chain_name, uid, timeout, max_input_len, max_output_len, ip_address, lora_name, model
        )

    def http_request(self, url: str, body: bytes, data_type: str = "binary"):
        headers = {"Content-Length": "%d" % len(body)}

        if data_type == "text":
            headers["Content-Type"] = "text/plain; charset=utf-8"
        else:
            headers["Content-Type"] = "binary/octet-stream"
        req = request.Request(url, data=body, headers=headers)
        return request.urlopen(req).read()

    def make_request(self, query: str):
        arks_request = arks_pb2.ArksRequest()
        arks_request.session_id = str(uuid.uuid1())
        arks_request.uid = self.uid

        arks_request.out_format = 1

        # scene and chain
        arks_request.scene_name = self.scene_name
        arks_request.chain_name = self.chain_name

        item1 = arks_request.items.add()
        item1.item_id = "item_id_001"
        item1_feature4 = item1.features.add()
        item1_feature4.contents.type = arks_pb2.ContentType.TYPE_STRING
        item1_feature4.key = "in_string"

        content = json.dumps(
            [
                {
                    "message": query,
                    "max_input_len": self.max_input_len,
                    "max_output_len": self.max_output_len,
                    "lora_name": self.lora_name,
                }
            ],
            ensure_ascii=False,
        )

        item1_feature4.contents.string_value.append(content)
        # 超时时间，单位ms
        arks_request.req_timeout_ms = self.timeout
        return arks_request

    def send_request(self, arks_request: arks_pb2.ArksRequest):
        binary = arks_request.SerializeToString()
        arks_response = arks_pb2.ArksResponse()

        try:
            server_response = self.http_request(self.url, binary, "binary")
            arks_response.ParseFromString(server_response)
            content = json.loads(arks_response.items[0].attributes[0].value)
            return content
        except Exception as err:
            print(f"send arks request to {self.url} failed: {err}")
            return []

    def __call__(self, query: str):
        req = self.make_request(query)
        rsp = self.send_request(req)
        if isinstance(rsp, list) and len(rsp) > 0:
            rsp = rsp[0]
        else:
            return None
        _end = rsp.rfind("```")
        _start = rsp.find("```json")
        if _end != -1 and _start != -1:
            json_str = rsp[_start + len("```json") : _end].strip()
        else:
            json_str = rsp
        try:
            json_result = json.loads(json_str)
        except:
            return rsp
        return json_result

    def remote_inference(self, prompt):
        return self(prompt)


class OpenAIClient(LLMClient):
    def __init__(
            self,
            api_key,
            base_url,
            stream: bool = False,
            temperature: int = 0.7,
            model="",
    ):
        self.api_key = api_key
        self.base_url = base_url
        self.model = model
        self.stream = stream
        self.temperature = temperature
        self.client = OpenAI(api_key=api_key, base_url=base_url)

    @classmethod
    def from_config(cls, config: Union[str, dict]):
        api_key = config.get("api_key")
        base_url = config.get("base_url")
        model = config.get("model", "")
        stream = config.get("stream", False)
        temperature = config.get("temperature", 0.7)
        return cls(
            api_key=api_key, base_url=base_url, stream=stream, temperature=temperature, model=model
        )

    def __call__(self, prompt):
        message = [
            {"role": "system", "content": "you are a helpful assistant"},
            {"role": "user", "content": prompt},
        ]
        response = self.client.chat.completions.create(
            model=self.model,
            messages=message,
            stream=self.stream,
            temperature=self.temperature
        )
        rsp = response.choices[0].message.content
        return rsp

    def call_service(self, prompt):
        return self(prompt)

    def remote_inference(self, prompt):
        rsp = self(prompt)
        _end = rsp.rfind("```")
        _start = rsp.find("```json")
        if _end != -1 and _start != -1:
            json_str = rsp[_start + len("```json") : _end].strip()
        else:
            json_str = rsp
        try:
            json_result = json.loads(json_str)
        except:
            return rsp
            # raise RuntimeError(f'JSON Parse Failed. \n{json.dumps(json_str, indent=4)}')
        return json_result
