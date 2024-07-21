# -*- coding: utf-8 -*-
import os
import pickle
import json
from sklearn.utils.sparsefuncs import min_max_axis
import torch
import jieba
import pandas as pd
import igraph as ig
import numpy as np
import requests
from tqdm import tqdm
from typing import List
from scipy.special import expit
from collections import defaultdict
from tenacity import retry, stop_after_attempt, wait_random_exponential
from knext.builder.auto_extract.index.utils import EmbeddingService, knn
from knext.builder.auto_extract.common.llm_client import LLMClient
from knext.builder.auto_extract.index.openie_extractor import (
    EntityExtractPrompt,
    KeywordsExtractPrompt,
)
from knext.builder.auto_extract.index.utils import (
    NodeType,
    EdgeType,
)

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"


def min_max_normalize(x):
    return (x - np.min(x)) / (np.max(x) - np.min(x))


def sigmoid(x):
    return expit(2 * min_max_normalize(x) - 1)


class HippoRAG:
    def __init__(
        self,
        index_data_path,
        embedding_service: EmbeddingService,
        task_name="",
        extraction_model_name="deepseek",
        node_specificity=True,
        dpr_only=False,
        graph_alg="ppr",
        damping=0.1,
        similarity_threshold=0.7,
        recognition_threshold=0.7,
        weighted_graph: bool = True,
        edge_weights: dict = {},
        debug: bool = True,
    ):
        self.embedding_service = embedding_service
        self.index_data_path = index_data_path
        self.task_name = task_name
        self.extraction_model_name = extraction_model_name
        self.extraction_model_name_processed = extraction_model_name.replace("/", "_")

        self.llm_client = LLMClient.from_config_name(extraction_model_name)
        self.entity_type = "ents_only_lower_preprocess"
        self.node_specificity = node_specificity

        self.graph_alg = graph_alg
        self.damping = damping
        self.similarity_threshold = similarity_threshold
        self.recognition_threshold = recognition_threshold
        self.weighted_graph = weighted_graph
        self.edge_weights = edge_weights
        self.debug = debug
        # Loading Important Corpus Files
        self.load_important_files()

        # Construct Graph
        self.build_graph()

        self.dpr_only = dpr_only

        self.statistics = {}
        self.ensembling_debug = []

    def extract_neighbors(self, node, node_type):
        node_id = self.node_id_map[(node, node_type)]
        edges = []
        for k, v in self.graph_plus.items():
            if node_id in k:
                s, o = k
                s_name = self.id_node_map[s]
                o_name = self.id_node_map[o]
                edges.append([s, o, s_name, o_name, v])
        return edges

    def rank_docs(self, query: str, top_k=5):
        """
        Rank documents based on the query
        :param query: the input entity
        :param top_k: the number of documents to return
        :return: the ranked document ids and their scores
        """

        rank_info = {}

        entity_start, entity_end = self.node_type_index[NodeType.ENTITY.name]
        chunk_start, chunk_end = self.node_type_index[NodeType.CHUNK.name]
        document_start, document_end = self.node_type_index[NodeType.DOCUMENT.name]

        if self.dpr_only:
            query_ner_list = []
        else:
            # Extract Entities
            try:
                print("Query NER...")
                query_ner_list = self.named_entity_recognition(query)
            except:
                print("Error in Query NER")
                query_ner_list = []

        query_chunk_scores = defaultdict(int)
        query_index = self.embedding_service([query])
        ranking = knn(query_index, self.chunk_index, k=len(self.docs))
        doc_ids, scores = ranking[0]
        for doc_id, score in zip(doc_ids, scores):
            query_chunk_scores[doc_id] = score

        if self.debug:
            chunk_titles = []
            chunk_scores = []
            for k, v in query_chunk_scores.items():
                chunk_titles.append(self.id_node_map[k])
                chunk_scores.append(v)
            chunk_scores = np.array(chunk_scores)
            indices = np.argsort(-chunk_scores)

            rank_info["dpr_chunks"] = [chunk_titles[x] for x in indices[:top_k]]
            rank_info["dpr_chunk_indices"] = indices[:top_k].tolist()
            rank_info["dpr_chunk_scores"] = chunk_scores[indices[:top_k]]

        ppr_chunk_scores = defaultdict(int)
        if len(query_ner_list) > 0:
            top_entity_vectors, top_entity_scores = self.get_top_entity_vec(
                query_ner_list
            )
            for chunk_id, chunk_score in query_chunk_scores.items():
                if chunk_score > self.recognition_threshold:
                    top_entity_vectors[chunk_id] = chunk_score * 0.1
            if self.debug:
                entity_weights = {}
                for idx in range(len(top_entity_vectors)):
                    if top_entity_vectors[idx] > 0:
                        entity_weights[self.id_node_map[idx][0]] = top_entity_vectors[
                            idx
                        ]

                rank_info["sim_entities"] = top_entity_scores
                rank_info["sim_entity_weights"] = entity_weights

            if len(top_entity_scores) > 0:
                # Run Personalized PageRank (PPR) or other Graph Alg Doc Scores
                combined_vector = np.max([top_entity_vectors], axis=0)

                if self.graph_alg == "ppr":
                    ppr_scores = self.run_pagerank_igraph_chunk([top_entity_vectors])[0]
                elif self.graph_alg == "none":
                    ppr_scores = combined_vector
                elif self.graph_alg == "neighbor_2":
                    ppr_scores = self.get_neighbors(combined_vector, 2)
                elif self.graph_alg == "neighbor_3":
                    ppr_scores = self.get_neighbors(combined_vector, 3)
                elif self.graph_alg == "paths":
                    ppr_scores = self.get_neighbors(combined_vector, 3)
                else:
                    assert False, f"Graph Algorithm {self.graph_alg} Not Implemented"

                for chunk_id in range(chunk_start, chunk_end):
                    ppr_chunk_scores[chunk_id] = ppr_scores[chunk_id]

                if self.debug:
                    scores = ppr_scores[entity_start:entity_end]
                    scores = min_max_normalize(scores)
                    indices = np.argsort(-scores)
                    rank_info["ppr_entities"] = [
                        self.entities[x] for x in indices[:top_k]
                    ]
                    rank_info["ppr_entity_scores"] = scores[indices[:top_k]]

                    scores = ppr_scores[chunk_start:chunk_end]
                    scores = min_max_normalize(scores)
                    indices = np.argsort(-scores)
                    rank_info["ppr_chunks"] = [self.chunks[x] for x in indices[:top_k]]
                    rank_info["ppr_chunk_scores"] = scores[indices[:top_k]]
                    rank_info["ppr_chunk_indices"] = indices[:top_k]
                    scores = ppr_scores[document_start:document_end]
                    scores = min_max_normalize(scores)
                    indices = np.argsort(-scores)
                    rank_info["ppr_documents"] = [
                        self.documents[x] for x in indices[:top_k]
                    ]
                    rank_info["ppr_document_scores"] = scores[indices[:top_k]]
                    rank_info["ppr_document_indices"] = indices[:top_k]
        query_chunk_scores = min_max_normalize(
            np.array([query_chunk_scores[x] for x in range(chunk_start, chunk_end)])
        )
        ppr_chunk_scores = min_max_normalize(
            np.array([ppr_chunk_scores[x] for x in range(chunk_start, chunk_end)])
        )

        if len(query_ner_list) == 0 or len(top_entity_scores) == 0:
            chunk_score = query_chunk_scores
        elif (
            np.min(list(top_entity_scores.values())) > self.recognition_threshold
        ):  # high confidence in named entities
            chunk_score = ppr_chunk_scores
        else:  # relatively low confidence in named entities, combine the two scores
            # the higher threshold, the higher chance to use the chunk ensemble
            alpha = 1.0
            chunk_score = ppr_chunk_scores * alpha + query_chunk_scores * (1 - alpha)

        # Return ranked chunks and ranked scores
        sorted_chunk_ids = np.argsort(chunk_score, kind="mergesort")[::-1]
        sorted_scores = chunk_score[sorted_chunk_ids]

        output_chunk_ids = sorted_chunk_ids.tolist()[:top_k]
        output_chunk_scores = sorted_scores.tolist()[:top_k]

        rank_info["output_chunks"] = [self.chunks[x] for x in output_chunk_ids]
        rank_info["output_scores"] = output_chunk_scores

        print("*" * 80)
        for k, v in rank_info.items():
            print(f"{k}: {v}")
        print("*" * 80)

        return output_chunk_ids, output_chunk_scores, rank_info

    def get_docs(self, doc_ids: List):
        output = []
        for doc_id in doc_ids:
            doc = self.docs[doc_id]
            output.append({"title": doc["title"], "text": doc["text"]})
        return output

    def get_neighbors(self, score_vector, max_depth=4):

        initial_nodes = score_vector.nonzero()[0]
        min_score = np.min(score_vector[initial_nodes])

        for initial_node in initial_nodes:
            all_neighborhood = []

            current_nodes = [initial_node]

            for depth in range(max_depth):
                next_nodes = []

                for node in current_nodes:
                    next_nodes.extend(self.g.neighbors(node))
                    all_neighborhood.extend(self.g.neighbors(node))

                current_nodes = list(set(next_nodes))

            for i in set(all_neighborhood):
                score_vector[i] += 0.5 * min_score

        return score_vector

    def load_important_files(self):
        self.index_data = pickle.load(open(self.index_data_path, "rb"))

        self.graph_plus = self.index_data["graph_plus"]
        self.docs = self.index_data["docs"]
        self.entities = self.index_data["entities"]
        self.num_entities = len(self.entities)
        self.chunks = self.index_data["chunks"]
        self.num_chunks = len(self.chunks)
        self.documents = self.index_data["documents"]
        self.num_documents = len(self.documents)
        self.node_type_index = self.index_data["node_type_index"]
        # self.synonym_entities = self.index_data["synonym_entities"]
        self.entity_weight = self.index_data["entity_weight"]

        # entity_start = self.node_type_index[NodeType.ENTITY.name][0]
        # weights = [0] * self.num_entities
        # for entity_id, entity_weight in self.entity_weight.items():
        #     weights[entity_id - entity_start] = entity_weight

        # weights = sigmoid(np.array(weights))

        # for entity_id in self.entity_weight.keys():
        #     weight = weights[entity_id - entity_start]
        #     self.entity_weight[entity_id] = weight

        for chunk, doc in zip(self.chunks, self.docs):
            if chunk != doc["title"]:
                raise ValueError("chunk order mismiatch with doc order.")

        entity_start, entity_end = self.node_type_index[NodeType.ENTITY.name]
        if entity_end - entity_start != self.num_entities:
            raise ValueError("entity size incorrect")

        chunk_start, chunk_end = self.node_type_index[NodeType.CHUNK.name]
        if chunk_end - chunk_start != self.num_chunks:
            raise ValueError("chunk size incorrect")

        document_start, document_end = self.node_type_index[NodeType.DOCUMENT.name]
        if document_end - document_start != self.num_documents:
            raise ValueError("document size incorrect")

        self.chunk_index = self.index_data["chunk_index"]
        for chunk_id in self.chunk_index[0]:
            if chunk_id < chunk_start or chunk_id >= chunk_end:
                raise ValueError("chunk index incorrect")

        self.entity_index = self.index_data["entity_index"]
        for entity_id in self.entity_index[0]:
            if entity_id < entity_start or entity_id >= entity_end:
                raise ValueError("entity index incorrect")

        # node->id
        self.node_id_map = self.index_data["node_id_map"]
        # id->node
        self.id_node_map = {}
        for k, v in self.node_id_map.items():
            self.id_node_map[v] = k

    def build_graph(self):

        edges = set()

        new_graph_plus = {}
        self.kg_adj_list = defaultdict(dict)
        self.kg_inverse_adj_list = defaultdict(dict)

        document_to_chunks = {}
        chunk_to_entities = {}
        for edge, meta in tqdm(
            self.graph_plus.items(), total=len(self.graph_plus), desc="Building Graph"
        ):
            s, o = edge
            weight, edge_type = meta
            weight *= self.edge_weights.get(edge_type, 1)

            if (s, o) not in edges and s != o:
                new_graph_plus[edge] = weight
                edges.add(edge)
                self.kg_adj_list[s][o] = weight
                self.kg_inverse_adj_list[o][s] = weight

            if edge_type == EdgeType.DOCUMENT_CONTAINS_CHUNK.name:
                if s not in document_to_chunks:
                    document_to_chunks[s] = [o]
                else:
                    document_to_chunks[s].append(o)
            elif edge_type == EdgeType.ENTITY_IN_CHUNK.name:
                # s: entity, o: chunk
                if o not in chunk_to_entities:
                    chunk_to_entities[o] = [s]
                else:
                    chunk_to_entities[o].append(s)

        chunk_concurrency_weight = self.edge_weights.get(
            EdgeType.CHUNK_CONCURRENT_CHUNK.name, None
        )
        if chunk_concurrency_weight is not None:
            print(f"Add chunk concurrency edges with weight {chunk_concurrency_weight}")
            for chunks_in_document in document_to_chunks.values():
                for i in range(len(chunks_in_document)):
                    for j in range(i + 1, len(chunks_in_document)):
                        new_graph_plus[
                            (chunks_in_document[i], chunks_in_document[j])
                        ] = chunk_concurrency_weight
                        new_graph_plus[
                            (chunks_in_document[j], chunks_in_document[i])
                        ] = chunk_concurrency_weight

        entity_concurrency_in_doc_weight = self.edge_weights.get(
            EdgeType.ENTITY_CONCURRENTINDOC_ENTITY.name, None
        )
        if entity_concurrency_in_doc_weight is not None:
            print(
                f"Add entity concurrency edges with weight {entity_concurrency_in_doc_weight}"
            )
            for entities_in_chunk in chunk_to_entities.values():
                for i in range(len(entities_in_chunk)):
                    for j in range(i + 1, len(entities_in_chunk)):
                        new_graph_plus[
                            (entities_in_chunk[i], entities_in_chunk[j])
                        ] = entity_concurrency_in_doc_weight
                        new_graph_plus[
                            (entities_in_chunk[j], entities_in_chunk[i])
                        ] = entity_concurrency_in_doc_weight

        self.graph_plus = new_graph_plus

        edges = list(self.graph_plus.keys())
        n_vertices = len(self.node_id_map)
        self.g = ig.Graph(n_vertices, edges)
        if self.weighted_graph:
            self.g.es["weight"] = [self.graph_plus[edge] for edge in edges]
        else:
            self.g.es["weight"] = [1] * len(edges)
        print("Graph built: num vertices:", n_vertices, "num edges:", len(edges))

    def run_pagerank_igraph_chunk(self, reset_score_chunk):
        """
        Run pagerank on the graph
        :param reset_score_chunk:
        :return: PageRank scores
        """
        pageranked_scores = []

        for reset_score in tqdm(reset_score_chunk, desc="pagerank chunk"):
            scores = self.g.personalized_pagerank(
                vertices=range(len(self.node_id_map)),
                damping=self.damping,
                directed=False,
                weights="weight",
                reset=reset_score,
                implementation="prpack",
            )

            pageranked_scores.append(np.array(scores))

        return np.array(pageranked_scores)

    def get_top_entity_vec(self, query_ner_list: list, k: int = 2):
        """
        Get the most similar entities (as vector) in the KG given the named entities
        :param query_ner_list:
        :return:
        """

        query_ner_index = self.embedding_service(query_ner_list)
        ranking = knn(query_ner_index, self.entity_index, k=k)
        entity_ids = []
        max_scores = []
        query_entity_ids = []
        for i in range(len(query_ner_list)):
            nn_info = ranking.get(i)
            if nn_info is None:
                raise ValueError(f"nearest neighbors of {query_ner_list[i]} not found")
            nn_ids, nn_scores = nn_info
            for nn_id, nn_score in zip(*nn_info):
                if nn_score >= self.similarity_threshold:
                    entity_ids.append(nn_id)
                    max_scores.append(nn_score)
                    query_entity_ids.append(i)

        top_entity_vec = np.zeros(len(self.node_id_map))

        for max_score, entity_id in zip(max_scores, entity_ids):
            if self.node_specificity:
                if (
                    self.entity_weight[entity_id] == 0
                ):  # just in case the entity is not recorded in any documents
                    weight = 1
                else:  # the more frequent the entity, the less weight it gets
                    weight = self.entity_weight[entity_id]

                # punish long entity
                if len(self.entities[entity_id]) > 10:
                    weight = weight * (max_score**2)

                top_entity_vec[entity_id] = weight
            else:
                top_entity_vec[entity_id] = 1.0

        top_entity_scores = {}
        for entity_id, score, query_entity_id in zip(
            entity_ids, max_scores, query_entity_ids
        ):
            top_entity_scores[
                (query_ner_list[query_entity_id], self.id_node_map[entity_id])
            ] = score

        return top_entity_vec, top_entity_scores

    @retry(stop=stop_after_attempt(3))
    def named_entity_recognition(self, text: str):

        prompt_op = EntityExtractPrompt(self.task_name)
        prompt_args = {"input": text}
        prompt = prompt_op.build_prompt(prompt_args)
        llm_output = self.llm_client.remote_inference(prompt)
        entities = prompt_op.parse_result(
            {"result": [llm_output], "content": prompt_args["input"]}
        )

        # print(f"entity extract prompt: \n{prompt}")
        # print(f"entity extract output: \n{entities}")

        if entities is None:
            raise ValueError(f"failed to run extraction, input: {prompt}")
        prompt_op = KeywordsExtractPrompt(self.task_name)
        prompt_args = {"input": text}
        prompt = prompt_op.build_prompt(prompt_args)
        llm_output = self.llm_client.remote_inference(prompt)
        keywords = prompt_op.parse_result(
            {"result": [llm_output], "content": prompt_args["input"]}
        )
        # print(f"keyword extract prompt: \n{prompt}")
        # print(f"keyword extract output: \n{keywords}")

        if keywords is None:
            raise ValueError(f"failed to run extraction, input: {prompt}")

        # TODO: link semantic graph
        extra_words = []
        for word in jieba.cut(text):
            if word in self.entities:
                extra_words.append(word)

        print(f"entities={entities}")
        print(f"keywords={keywords}")
        print(f"extra_words={extra_words}")

        extracted_entities = list(set(entities + keywords + extra_words))
        return extracted_entities

    def answer(self, query: str, top_k: int = 5):
        ranks, scores, logs = self.rank_docs(query, top_k)
        docs = self.get_docs(ranks)
        content = []
        total_len = 0
        for doc, score in zip(docs, scores):
            # if score < 0.4:
            #     break
            title = doc["title"]
            text = doc["text"]
            tmp = f"标题:{title}\n正文:{text}"
            content.append(tmp)
            total_len += len(tmp)
            # if total_len >= 3000:
            #     break
        if len(content) == 0:
            return f"您未提供任何可以回答问题“{query}”的资料，因此我无法提供答案。"
        template = {
            "instruction": "请阅读documents字段中给出的材料，然后基于该材料内容，回答question字段的问题。注意，请严格基于documents字段中的材料回答问题，如果发现documents字段中的材料与问题无关，请直接拒答。",
            "documents": content,
            "question": query,
        }
        print("question============================================")
        print(template)
        prompt = json.dumps(template, ensure_ascii=False)
        rsp = self.llm_client.remote_inference(prompt)
        print("answer==============================================")
        print(rsp)

        return rsp


if __name__ == "__main__":

    embedding_service = EmbeddingService(use_pre=True, num_parallel=1)
    edge_weights = {
        EdgeType.CHUNK_CONCURRENT_CHUNK.name: 5,
        EdgeType.ENTITY_CONCURRENT_ENTITY.name: 0.3,
        EdgeType.ENTITY_CONCURRENTINDOC_ENTITY.name: 0.7,
        EdgeType.ENTITY_SYNONYM_ENTITY.name: 1,
    }
    hipporag = HippoRAG(
        index_data_path=os.path.expanduser(
            "~/Src/libs/data/policy_files/zhengce-deepseek-output-v2-graph.pkl"
        ),
        embedding_service=embedding_service,
        task_name="政策文件",
        extraction_model_name="deepseek",
        node_specificity=True,
        dpr_only=False,
        graph_alg="ppr",
        damping=0.5,
        similarity_threshold=0.8,
        recognition_threshold=0.85,
        edge_weights=edge_weights,
        weighted_graph=True,
    )

    queries = [
        # "公积金可以抵个税不",
        # "公积金贷款首付多少，能贷多少",
        # "两孩家庭的公积金贷款有优待吗",
        "我在建德，疫情管控期间能不能多提一些公积金交房租",
        # "社保基数怎么规定的",
        # "海水为什么看上去是蓝色的",
    ]
    info = []
    for query in queries:
        chunk_id, chunk_score, rank_info = hipporag.rank_docs(query, 10)
        info.append(rank_info)

    # output = []
    # for query in queries:
    #     output.append(hipporag.answer(query, 10))
    # for q, a in zip(queries, output):
    #     print("-" * 80)
    #     print(f"问题: \n{q}")
    #     print(f"答案: \n{a}")
