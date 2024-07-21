# -*- coding: utf-8 -*-
import os
import json
import requests
import numpy as np
import concurrent.futures
import faiss
import gc
import time
from enum import Enum
from tqdm import tqdm
from typing import List, Union, Dict, Tuple
from tenacity import retry, stop_after_attempt, wait_exponential
from sklearn.metrics.pairwise import cosine_similarity

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"


class NodeType(str, Enum):
    DOCUMENT = 0
    CHUNK = 1
    ENTITY = 2


class EdgeType(str, Enum):
    DOCUMENT_CONTAINS_CHUNK = 0
    ENTITY_IN_CHUNK = 1
    CHUNK_CONCURRENT_CHUNK = 2
    ENTITY_CONCURRENT_ENTITY = 3
    ENTITY_CONCURRENTINDOC_ENTITY = 4
    ENTITY_SYNONYM_ENTITY = 5


class EmbeddingService:
    def __init__(self, use_pre: bool = True, num_parallel: int = 4):
        self.use_pre = use_pre
        self.num_parallel = num_parallel
        if self.use_pre:
            self.url = (
                "http://antassistant-735.gz00b.dev.alipay.net:8001/embedding/query"
            )
        else:
            self.url = f"http://antassistant-pool.gz99s.alipay.com:8001/embedding/query"

        self.executor = concurrent.futures.ThreadPoolExecutor(
            max_workers=self.num_parallel
        )

    @retry(
        stop=stop_after_attempt(5), wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    def call_embedding_service(self, req):
        result = requests.post(
            self.url,
            data=json.dumps(req),
            headers={"Content-Type": "application/json"},
        )

        output = result.json()
        if "embeddingList" not in output:
            print("incorrect input:", req["sentenceList"])
            print(output)
            raise ValueError(f"failed to call embedding service.")
        emb = output["embeddingList"]
        emb = np.array(emb)
        return emb

    def get_embedding(self, data: Union[List[str], str]):
        batched = False
        if isinstance(data, list):
            batched = True
            batch = [[x[:499]] for x in data]
        else:
            batch = [data[:499]]
        params = {
            "appName": "kgbuilder",
            "appToken": "90da00259d3cf77c",
            "modelId": "bge_kgbuilder",
            "modelVersion": "v1.5",
            "sentenceList": batch,
            "traceId": "123",
            "invokeType": "embeddings",
        }
        # if self.use_pre:
        #     params["modelId"] = "bge_kgbuilder_offline"
        # else:
        #     params["modelId"] = "bge_kgbuilder"
        try:
            emb = self.call_embedding_service(params)
        except Exception as e:
            print(f"failed to call embedding service for data {data}, info: {e}")
            return None
        if not batched:
            return emb.reshape(-1)
        return emb

    def __call__(self, data: List[str], batch_size: int = 4, normalize: bool = True):
        group = []
        tmp = []
        for input_str in data:
            tmp.append(input_str)
            if len(tmp) == batch_size:
                group.append(tmp)
                tmp = []
        if len(tmp) > 0:
            group.append(tmp)

        if self.use_pre:
            print("Switch to serial execution for pre environment.")
            embs = []
            for chunk in tqdm(group, total=len(group)):
                emb = self.get_embedding(data=chunk)
                time.sleep(1)
                embs.append(emb)
        else:
            futs = []
            for chunk in group:
                fut = self.executor.submit(self.get_embedding, data=chunk)
                futs.append(fut)
            embs = [x.result() for x in futs]
        id_list = []
        emb_list = []
        id_ = 0
        for chunk, emb in zip(group, embs):
            # skip failed strings
            if emb is None:
                id_ += len(chunk)
                continue
            for idx, input_str in enumerate(chunk):
                id_list.append(id_)
                emb_list.append(emb[idx, :])
                id_ += 1
        emb_list = np.vstack(emb_list, dtype=np.float32)
        if normalize:
            faiss.normalize_L2(emb_list)
        return id_list, emb_list


def knn(queries: Tuple, knowledge_base: Tuple, k=128, use_faiss: bool = False):
    if k > len(knowledge_base[0]):
        print(f"change k from {k} to {len(knowledge_base[0])}")
        k = len(knowledge_base[0])
    query_ids, query_vecs = queries
    knowledge_base_ids, knowledge_base_vecs = knowledge_base

    query_vecs = query_vecs.astype(np.float32)
    knowledge_base_vecs = knowledge_base_vecs.astype(np.float32)

    if use_faiss:
        if hasattr(faiss, "StandardGpuResources"):
            similarities, indices = knn_gpu(query_vecs, knowledge_base_vecs, k)
        else:
            similarities, indices = knn_cpu(query_vecs, knowledge_base_vecs, k)
    else:
        similarities, indices = knn_simple(query_vecs, knowledge_base_vecs, k)
    sorted_candidates = {}

    for new_index, nn_info in tqdm(enumerate(zip(similarities, indices))):
        nn_sim, nn_inds = nn_info
        nns = [knowledge_base_ids[i] for i in nn_inds.tolist()]

        sorted_candidates[query_ids[new_index]] = (nns, nn_sim)

    return sorted_candidates


def knn_simple(query_vecs, knowledge_base_vecs, k):
    distances = 1 - cosine_similarity(query_vecs, knowledge_base_vecs)
    ranks = np.argsort(distances, axis=1)
    indices = ranks[:, :k]
    distances = distances[np.arange(indices.shape[0]).reshape(-1, 1), indices]
    return 1 - distances, indices


def knn_cpu(query_vecs, knowledge_base_vecs, k):
    dim = query_vecs.shape[1]
    index = faiss.IndexFlat(dim, faiss.METRIC_INNER_PRODUCT)  # build the index
    index.add(knowledge_base_vecs)
    similarities, indices = index.search(query_vecs, k)  # 执行搜索
    return similarities, indices


def knn_gpu(query_vecs, knowledge_base_vecs, k):

    # Preparing Data for k-NN Algorithm
    print("Chunking")

    dim = len(knowledge_base_vecs[0])
    index_split = 4
    index_chunks = np.array_split(knowledge_base_vecs, index_split)
    query_chunks = np.array_split(query_vecs, 100)

    # Building and Querying FAISS Index by parts to keep memory usage manageable.
    print("Building Index")

    index_chunk_D = []
    index_chunk_I = []

    current_zero_index = 0

    for num, index_chunk in enumerate(index_chunks):

        print("Running Index Part {}".format(num))
        index = faiss.IndexFlat(dim, faiss.METRIC_INNER_PRODUCT)  # build the index

        if faiss.get_num_gpus() > 1:
            gpu_resources = []

            for i in range(faiss.get_num_gpus()):
                res = faiss.StandardGpuResources()
                gpu_resources.append(res)

            gpu_index = faiss.index_cpu_to_gpu_multiple_py(gpu_resources, index)
        else:
            gpu_resources = faiss.StandardGpuResources()
            gpu_index = faiss.index_cpu_to_gpu(gpu_resources, 0, index)

        print()
        gpu_index.add(index_chunk)

        D, I = [], []

        for q in tqdm(query_chunks):
            d, i = gpu_index.search(q, k)

            i += current_zero_index

            D.append(d)
            I.append(i)

        index_chunk_D.append(D)
        index_chunk_I.append(I)

        current_zero_index += len(index_chunk)

        #             print(subprocess.check_output(['nvidia-smi']))

        del gpu_index
        del gpu_resources
        gc.collect()

    print("Combining Index Chunks")

    stacked_D = []
    stacked_I = []

    for D, I in zip(index_chunk_D, index_chunk_I):
        D = np.vstack(D)
        I = np.vstack(I)

        stacked_D.append(D)
        stacked_I.append(I)

    del index_chunk_D
    del index_chunk_I
    gc.collect()

    stacked_D = np.hstack(stacked_D)
    stacked_I = np.hstack(stacked_I)

    full_sort_I = []
    full_sort_D = []

    for d, i in tqdm(zip(stacked_D, stacked_I)):
        sort_indices = np.argsort(d, kind="stable")

        sort_indices = sort_indices[::-1]

        i = i[sort_indices][:k]
        d = d[sort_indices][:k]

        full_sort_I.append(i)
        full_sort_D.append(d)

    del stacked_D
    del stacked_I
    gc.collect()

    return full_sort_D, full_sort_I


if __name__ == "__main__":
    strs = ["疫情影响", "疫情原因", "三胎家庭", "公积金"]
    emb_service = EmbeddingService(use_pre=True)
    emb = emb_service(strs)
    res1 = knn(emb, emb, use_faiss=True)
    res2 = knn(emb, emb, use_faiss=False)
