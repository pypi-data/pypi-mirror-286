import concurrent
import logging
from concurrent.futures import ThreadPoolExecutor
from typing import List

from knext.builder.auto_extract.base import Extractor
from knext.builder.auto_extract.common.llm_client import LLMClient
from knext.builder.auto_extract.common.prompt.constraint_prompt import ConstraintKGPrompt, ConstraintEEPrompt
from knext.builder.auto_extract.common.prompt.free_prompt import SPOPrompt
from knext.builder.auto_extract.model.chunk import Chunk
from knext.builder.operator import SPGRecord, OneKE_KGPrompt, OneKE_EEPrompt
from knext.common import project as rest
from knext.schema.client import SchemaClient
from knext.schema.model.base import SpgTypeEnum


logger = logging.getLogger(__name__)


class TextExtractor(Extractor):
    def __init__(self, project_id: int, llm_clients: List[LLMClient], top_entity_type: str, **kwargs):
        super().__init__(project_id, **kwargs)
        self.llm_clients = llm_clients
        self.top_entity_type = top_entity_type
        session = SchemaClient(project_id=project_id).create_session()
        self.spg_types = session.spg_types
        self.logger = logging.getLogger(__name__)
        client = rest.ProjectApi()
        projects = client.project_get()
        self.namespace = "DEFAULT"
        for project in projects:
            item = project.to_dict()
            if str(item["id"]) == str(self.project_id):
                self.namespace = item["namespace"]
                break

    def invoke(self, input: List[Chunk]) -> List[SPGRecord]:
        spg_records = [self.chunk_extract(input[0])]
        content = input[0].content
        futures = []

        entity_types, event_types = [], []
        for spg_type in self.spg_types.values():
            if (
                spg_type.spg_type_enum == SpgTypeEnum.Entity
                and spg_type.name_zh == self.top_entity_type
            ):
                entity_types.append(spg_type.name)
                for k, v in spg_type.properties.items():
                    if v.object_type_name_zh == self.top_entity_type and spg_type.name not in entity_types:
                        entity_types.append(spg_type.name)
                        continue
            if spg_type.spg_type_enum == SpgTypeEnum.Event:
                for k, v in spg_type.properties.items():
                    if v.object_type_name_zh == self.top_entity_type and spg_type.name not in event_types:
                        event_types.append(spg_type.name)
                        continue
        with ThreadPoolExecutor(max_workers=3*len(self.llm_clients)) as executor:
            for idx, llm_client in enumerate(self.llm_clients):
                futures.append(executor.submit(self.entity_free_extract, llm_client, content, idx=idx*3+1))
                futures.append(executor.submit(self.entity_constraint_extract, llm_client, content, entity_types, idx=idx*3+2))
                futures.append(executor.submit(self.event_constraint_extract, llm_client, content, event_types, idx=idx*3+3))

            for i, future in enumerate(concurrent.futures.as_completed(futures)):
                spg_records.extend(future.result())
        return spg_records

    def batch(self, inputs: List[Chunk]) -> List[SPGRecord]:
        pass

    def chunk_extract(self, chunk):
        chunk_record = SPGRecord(spg_type_name=f"{self.namespace}.Chunk").upsert_properties({
            "name": chunk.name,
            "info": chunk.name,
            "content": chunk.content
        })
        return chunk_record

    def entity_free_extract(self, client: LLMClient, input_str: str, **kwargs):
        """
        Schema约束的抽取：
        1. 若上游有分类结果（例如["导演", "编剧"]），则先对齐到顶层类型（["人物"]），抽取该实体类型，并抽取所有带有该实体类型属性的事件类型。
        # 2. 若上游无分类结果，则抽取所有实体和事件类型。
        """
        thread_id = kwargs.get('idx')
        self.logger.info(f"执行任务 {thread_id}")
        print(f"\n[Thread {kwargs.get('idx')}]-{client.model}]Free extracting...\n")
        op = SPOPrompt(project_id=self.project_id)
        entity_records = client.invoke({"input": input_str}, op)
        print(f"\n[Thread {kwargs.get('idx')}]-{client.model}]Free extract finished.\n")
        return entity_records

    def print_logs(self, title, content):
        print(f"---------------------{title}---------------------")
        print(content)
        print(f"---------------------{title}---------------------")

    def entity_constraint_extract(
        self, client: LLMClient, input_str: str, entity_types: List[str], **kwargs
    ):
        """
        Schema约束的实体抽取：
        1. 若使用humming模型进行抽取，则使用OneKEPrompt，其他模型则使用AutoPrompt
        """
        if client.model in ["humming"]:
            op = OneKE_KGPrompt(entity_types, split_num=1, project_id=self.project_id)
        else:
            op = ConstraintKGPrompt(entity_types, project_id=self.project_id)

        print(f"\n[Thread {kwargs.get('idx')}]-{client.model}]Entity extracting...\n")
        entity_records = client.batch({"input": input_str, "types": entity_types}, op)
        self.print_logs(f"[Thread {kwargs.get('idx')}]-{client.model}]Entity Extract Response", entity_records)
        print(f"\n[Thread {kwargs.get('idx')}]-{client.model}]Entity extract finished.\n")
        return entity_records

    def event_constraint_extract(
        self, client: LLMClient, input_str: str, event_types: List[str], **kwargs
    ):
        """
        Schema约束的事件抽取：
        1. 若使用humming模型进行抽取，则使用OneKEPrompt，其他模型则使用AutoPrompt
        """
        if client.model in ["humming"]:
            op = OneKE_EEPrompt(event_types, split_num=1, project_id=self.project_id)
        else:
            op = ConstraintEEPrompt(event_types, project_id=self.project_id)

        print(f"\n[Thread {kwargs.get('idx')}]-{client.model}]Event extracting...\n")
        event_records = client.batch({"input": input_str, "types": event_types}, op)
        self.print_logs(f"[Thread {kwargs.get('idx')}]-{client.model}]Event Extract Response", event_records)
        print(f"\n[Thread {kwargs.get('idx')}]-{client.model}]Event extract finished.\n")
        return event_records
