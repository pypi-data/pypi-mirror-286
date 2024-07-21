import concurrent
import logging
import os
from concurrent.futures import ThreadPoolExecutor

from knext.builder.auto_extract.common.llm_client import LLMClient
from knext.builder.auto_extract.extractor.baike_extractor import BaikeExtractor
from knext.builder.auto_extract.post_processor.post_processor import DefaultPostProcessor
from knext.builder.auto_extract.splitter.doc_splitter import DocSplitter, MarkDownDocSplitter



# # 配置日志
# def configure_logging():
#     logging.basicConfig(level=logging.INFO,
#                         format='%(asctime)s - %(threadName)s - %(levelname)s - %(message)s')
#
# def t1():
#     splitter = DocSplitter()
#     extractor = BaikeExtractor(project_id=2, models="deepseek-chat")
#     post_processor = DefaultPostProcessor(project_id=2)
#     file_name = "zhou.txt"
#     chunks = splitter._handle(file_name, user_query="百科-人物-周杰伦")
#     print(chunks)
#
#     PWD = os.path.dirname(__file__)
#     spg_record_list = extractor._handle(chunks[0])
#     print(spg_record_list)
#     sub_graph = post_processor._handle(spg_record_list)
#     print(sub_graph)
#
# def t2():
#     configure_logging()
#     logger = logging.getLogger(__name__)
#     logger.info("主线程开始")
#     splitter = MarkDownDocSplitter()
#     extractor = BaikeExtractor(project_id=2, models="deepseek-chat")
#     post_processor = DefaultPostProcessor(project_id=2)
#     file_name = "../data/baike-person-zhoujielun-short.md"
#     chunks = splitter._handle(file_name, user_query="百科-人物-周杰伦")
#     print(chunks)
#
#     futures = []
#     spg_record_list = []
#     with ThreadPoolExecutor(max_workers=10) as executor:
#         for chunk in chunks:
#             futures.append(executor.submit(extractor._handle, chunk))
#
#         for i, future in enumerate(concurrent.futures.as_completed(futures)):
#             spg_records = future.result()
#             spg_record_list.extend(spg_records)
#
#     print(spg_record_list)
#     sub_graph = post_processor._handle(spg_record_list)
#     print(sub_graph)
#
#     logger.info("主线程结束")


if __name__ == '__main__':
    # t2()
    from knext.builder.auto_extract.common.llm_client import LLMClient
    client = LLMClient.from_config_name("qwen")
    print(client("你好"))
