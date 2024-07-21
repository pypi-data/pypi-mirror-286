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
import re
import os
import time
import functools
import traceback
import concurrent.futures
import numpy as np
import multiprocessing as mp
from typing import List, Dict
from knext.builder.auto_extract.base import Extractor
from knext.builder.auto_extract.model.chunk import Chunk, ChunkTypeEnum
from knext.builder.auto_extract.model.sub_graph import SubGraph
from knext.builder.auto_extract.splitter import (
    PDFDocSplitter,
    CSVDocSplitter,
    MarkDownDocSplitter,
)
from knext.builder.auto_extract.post_processor.post_processor import PostProcessor
from knext.builder.auto_extract.common.llm_client import LLMClient

# from knext.builder.auto_extract.llm_client import MayaHttpClient
# from nscommon.maya.maya_service.maya_service_client import MayaServiceClient
from knext.builder.auto_extract.common.prompt.exp_prompt import *
from knext.builder.operator import SPGRecord


def get_features(message: str, lora_name: str = None):
    feature = {
        "message": message,
        "max_input_len": 10240,
        "max_output_len": 10240,
        "lora_name": lora_name,
    }
    return [feature]


def extract_json_content(text):
    # 正则表达式匹配 json 和之间的内容
    pattern = r"```json\s+(.*?)\s+```"
    # 使用re.search找到第一个匹配的内容
    match = re.search(pattern, text, re.DOTALL)
    if match:
        # 返回匹配的内容
        return match.group(1)
    else:
        return text


def retry(tries=10, wait=1, backoff=2, exceptions=(Exception,)):
    """Configurable retry decorator, Useage:

    @retry(tries=3)
    def func():
       pass

    This is equivalent to:  func = retry(retries=3)(func)
    """

    def dec(function):
        @functools.wraps(function)
        def function_with_retry(*args, **kwargs):
            current_wait = wait
            count = 1
            while True:
                try:
                    return function(*args, **kwargs)
                except exceptions as e:
                    if wait == 0:
                        msg = f"failed to call {function.__name__}, info: {e}"
                        print(msg)
                        traceback.print_exc()
                        raise
                    else:
                        if count < tries or tries < 0:
                            if tries < 0:
                                msg = f"failed to call {function.__name__} [{count}/Inf], info: {e}"
                            else:
                                msg = f"failed to call {function.__name__} [{count}/{tries}], info: {e}"
                            print(msg)
                            time.sleep(current_wait)
                            current_wait *= backoff
                            if kwargs is None:
                                kwargs = {}
                            kwargs["retry"] = tries - count
                            count += 1
                        elif count == tries:
                            msg = f"failed to call {function.__name__} [{count}/{tries}], info: {e}"
                            print(msg)
                            raise e

        return function_with_retry

    return dec


class FinExtractor(Extractor):
    def __init__(self, project_id, **kwargs):

        self.job_conf = kwargs["job_conf"]
        self.llm_clients = [
            LLMClient.from_config_name(
                x["model_name"],
                use_pre=x["use_pre"],
            )
            for x in self.job_conf["model_conf"]
        ]
        self.prompts = {
            "classify": FinClassifyPrompt,
            "extract": FinEventExtractPrompt,
        }
        self.load_data(self.job_conf["data_dir"])
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=8)

    def load_data(self, data_dir):
        schema_file = os.path.join(data_dir, "duee_fin_event_schema.json")
        self.schema = {}
        with open(schema_file, "r") as reader:
            for line in reader:

                schema = json.loads(line)
                event_type = schema["event_type"]
                role_names = []
                for role in schema["role_list"]:
                    role_name = role["role"]
                    enum_items = role.get("enum_items", None)
                    if enum_items is not None:
                        role_name = f"{role_name}(须是{enum_items}之一)"
                    role_names.append(role_name)
                self.schema[event_type] = role_names
        # load examples
        self.examples = {}
        self.training_data = []
        with open(
            os.path.join(data_dir, "duee_fin_dev.json/duee_fin_dev.json"), "r"
        ) as reader:
            for line in reader:
                item = json.loads(line)
                self.training_data.append(self.data2chunk(item))
                text = item["text"]
                event_list = item.get("event_list", None)
                if event_list is None:
                    continue

                event_dict = {}
                for event in event_list:
                    event_type = event["event_type"]
                    arguments = event["arguments"]
                    if event_type not in event_dict:
                        event_dict[event_type] = [arguments]
                    else:
                        event_dict[event_type].append(arguments)
                for event_type, event_arguments in event_dict.items():
                    example = {
                        "input": text,
                        "output": [{event_type: x} for x in event_arguments],
                    }
                    if event_type in self.examples:
                        self.examples[event_type].append(example)
                    else:
                        self.examples[event_type] = [example]
        for event_type in self.examples.keys():
            self.examples[event_type].sort(key=lambda x: -len(x["output"]))

    def data2chunk(self, item):
        text = item["text"]
        title = item["title"]
        id_ = item["id"]
        return Chunk(ChunkTypeEnum.Text, "", title, id_, text)

    def get_schema_and_example(self, event_type):
        schema = self.schema.get(event_type)
        examples = self.examples.get(event_type)
        if examples is not None:
            examples = examples[:10]
            total = len(examples)
            indices = np.random.choice(total, 2, replace=False)
            example = [examples[x] for x in indices]
            return schema, example
        return schema, None

    def get_prompt(self, prompt_name):
        return self.prompts[prompt_name]()

    @retry(tries=3)
    def _extract(self, llm_client, prompt_name, prompt_args, **kwargs):

        prompt_op = self.get_prompt(prompt_name)
        prompt = prompt_op.build_prompt(prompt_args)
        llm_output = llm_client.remote_inference(prompt)
        print(f"extract input: \n{prompt}\nextract output:\n {llm_output}")
        raw_result = prompt_op.parse_result(
            {"result": [llm_output], "args": prompt_args}
        )
        if raw_result is None:
            raise ValueError(f"failed to run extraction, input: {prompt}")
        spg_records = prompt_op.result_to_spgrecord(raw_result)
        return raw_result, spg_records

    def pextract(self, args: List[List]):
        all_futs = []
        for prompt_info in args:
            prompt_name, prompt_args = prompt_info
            futs = []
            for llm_client in self.llm_clients:
                fut = self.executor.submit(
                    self._extract,
                    llm_client=llm_client,
                    prompt_name=prompt_name,
                    prompt_args=prompt_args,
                )
                futs.append(fut)
            all_futs.append(futs)
        return [[x.result() for x in futs] for futs in all_futs]

    def invoke(self, chunks: List[Chunk]):
        output = []
        for chunk in chunks:
            if len(chunk.content) < 50:
                continue
            try:
                content = chunk.content
                # classify
                prompt_name = "classify"
                prompt_args = {
                    "input": content.lower(),
                    "events": list(self.schema.keys()),
                }
                classify_output = self.pextract([[prompt_name, prompt_args]])[0]

                dedup = set()
                for classes, _ in classify_output:
                    for class_ in classes:
                        if class_ not in dedup:
                            dedup.add(class_)

                events = list(dedup)
                args = []
                for event in events:
                    schema, examples = self.get_schema_and_example(event)
                    prompt_args = {
                        "input": content,
                        "schema": {event: schema},
                        "event_type": event,
                        "examples": examples,
                    }
                    args.append(["extract", prompt_args])
                all_extract_output = self.pextract(args)
                tmp = []
                for event, extract_output in zip(events, all_extract_output):
                    for model_extract_output in extract_output:
                        model_extract_output = model_extract_output[0]
                        tmp.append(model_extract_output)
                output.append({chunk.id: {"success": True, "data": tmp}})
            except Exception as e:
                output.append({chunk.id: {"success": False, "info": str(e)}})
        return output


def mp_run(job_conf, worker_id, worker_count, output_file):
    extractor = FinExtractor(0, job_conf=job_conf)
    count = len(extractor.training_data)
    shard_count = count // worker_count
    start = min(count, worker_id * shard_count)
    end = min(count, start + shard_count)

    with open(output_file, "w") as writer:
        for chunk in extractor.training_data[start:end]:
            output = extractor.invoke([chunk])
            if isinstance(output, list) and len(output) > 0:
                writer.write(json.dumps(output[0], ensure_ascii=False))
                writer.write("\n")
                writer.flush()
            else:
                print(f"incorrect output {output}")


if __name__ == "__main__":

    job_conf = {
        "model_conf": [
            {
                "model_name": "deepseek",
                "lora_name": None,
                "use_pre": False,
            },
        ],
        # "data_dir": "/ossfs/workspace/data/DuEE",
        "data_dir": "/Users/simplex/tmp2/DuEE-fin/",
    }

    # extractor = FinExtractor(0, job_conf=job_conf)

    # out = extractor.invoke(extractor.training_data[4388:4389])

    # multi process extract
    num_processes = 16

    ps = []
    file_names = []
    for worker_id in range(num_processes):
        process_out_file_name = f"DuEE-extracted-{worker_id}-{num_processes}.jsonl"
        process_out_file_name = os.path.join(
            job_conf["data_dir"], "deepseek_output_dev", process_out_file_name
        )
        file_names.append(process_out_file_name)
        p = mp.Process(
            target=mp_run,
            args=(
                job_conf,
                worker_id,
                num_processes,
                process_out_file_name,
            ),
        )
        p.start()
        ps.append(p)
    for p in ps:
        p.join()
