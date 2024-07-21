# -*- coding: utf-8 -*-
import os
import pickle
import json
import torch
import jieba
import pandas as pd
import igraph as ig
import numpy as np
import requests
from tqdm import tqdm
from typing import List
from scipy.special import softmax
from collections import defaultdict
from tenacity import retry, stop_after_attempt, wait_random_exponential
from knext.builder.auto_extract.index.utils import EmbeddingService, knn
from knext.builder.auto_extract.common.llm_client import LLMClient
from knext.builder.auto_extract.index.openie_extractor import (
    EntityExtractPrompt,
    KeywordsExtractPrompt,
)

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"


def min_max_normalize(x):
    return (x - np.min(x)) / (np.max(x) - np.min(x))


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

        # Loading Important Corpus Files
        self.load_important_files()

        # Construct Graph
        self.build_graph()

        self.dpr_only = dpr_only

        self.statistics = {}
        self.ensembling_debug = []

    def rank_docs(self, query: str, top_k=5):
        """
        Rank documents based on the query
        :param query: the input entity
        :param top_k: the number of documents to return
        :return: the ranked document ids and their scores
        """

        rank_info = {}

        if self.dpr_only:
            query_ner_list = []
        else:
            # Extract Entities
            try:
                query_ner_list = self.named_entity_recognition(query)
            except:
                print("Error in Query NER")
                query_ner_list = []

        query_doc_scores = np.zeros(self.docs_to_entities_mat.shape[0])
        query_index = self.embedding_service([query])
        ranking = knn(query_index, self.doc_index, k=len(self.docs))
        doc_ids, scores = ranking[0]
        for doc_id, score in zip(doc_ids, scores):
            query_doc_scores[doc_id] = score
        indices = np.argsort(-query_doc_scores)
        # print(f"top dpr docs: {[self.docs[x]['title'] for x in indices[:top_k]]}")
        # print(f"top dpr doc scores: {query_doc_scores[indices[:top_k]]}")

        rank_info["dpr_docs"] = [self.docs[x]["title"] for x in indices[:top_k]]
        rank_info["dpr_scores"] = query_doc_scores[indices[:top_k]]

        ppr_doc_scores = np.zeros(len(self.docs))
        if len(query_ner_list) > 0:
            top_entity_vectors, top_entity_scores = self.get_top_entity_vec(
                query_ner_list
            )
            entity_weights = {}
            for idx in range(len(self.entities)):
                if top_entity_vectors[idx] > 0:
                    entity_weights[self.entities[idx]] = top_entity_vectors[idx]

            rank_info["sim_entities"] = top_entity_scores
            rank_info["sim_entity_weights"] = entity_weights

            if len(top_entity_scores) > 0:
                # Run Personalized PageRank (PPR) or other Graph Alg Doc Scores
                combined_vector = np.max([top_entity_vectors], axis=0)

                if self.graph_alg == "ppr":
                    ppr_entity_scores = self.run_pagerank_igraph_chunk(
                        [top_entity_vectors]
                    )[0]
                elif self.graph_alg == "none":
                    ppr_entity_scores = combined_vector
                elif self.graph_alg == "neighbor_2":
                    ppr_entity_scores = self.get_neighbors(combined_vector, 2)
                elif self.graph_alg == "neighbor_3":
                    ppr_entity_scores = self.get_neighbors(combined_vector, 3)
                elif self.graph_alg == "paths":
                    ppr_entity_scores = self.get_neighbors(combined_vector, 3)
                else:
                    assert False, f"Graph Algorithm {self.graph_alg} Not Implemented"

                indices = np.argsort(-ppr_entity_scores)
                # print(
                #     f"top ppr entities: {self.entities[indices[:top_k]]}, {ppr_entity_scores[indices[:top_k]]}"
                # )
                rank_info["ppr_entities"] = self.entities[indices[:top_k]]
                rank_info["ppr_entity_scores"] = ppr_entity_scores[indices[:top_k]]

                # s_score+o_score
                # fact_score = self.facts_to_entities_mat.dot(ppr_entity_scores)
                # indices = np.argsort(-fact_score)
                # print(
                #     f"top facts entity: {[self.facts[x] for x in indices[:10]]}, {fact_score[indices[:10]]}"
                # )

                # ppr_doc_scores = self.docs_to_facts_mat.dot(fact_score)

                ppr_doc_scores = self.docs_to_entities_mat.dot(ppr_entity_scores)
                ppr_doc_scores = min_max_normalize(
                    ppr_doc_scores
                )  # convert to similarity
                indices = np.argsort(-ppr_doc_scores)

                # score_info = []
                # tmp = self.docs_to_entities_mat.todense()
                # for index in indices[:top_k]:
                #     entity_vec = tmp[index,:]
                #     entities = []
                #     for idx in range(len(entity_vec)):
                #         if entity_vec[idx]>0:
                #             entities.append((self.entities[idx],  entity_vec[idx]*ppr_entity_scores[idx]))
                #     score_info.append(entities)
                rank_info["ppr_docs"] = [self.docs[x]["title"] for x in indices[:top_k]]
                rank_info["ppr_scores"] = ppr_doc_scores[indices[:top_k]]

                ppr_article_scores = self.articles_to_docs_mat.dot(ppr_doc_scores)
                indices = np.argsort(-ppr_article_scores)
                rank_info["ppr_article"] = self.articles[indices[:top_k]]
                rank_info["ppr_article_score"] = ppr_article_scores[indices[:top_k]]

                for idx, doc in enumerate(self.docs):
                    article_title = doc["title"].split("#")[0]
                    article_idx = self.article_id_map[article_title]
                    ppr_doc_scores[idx] += ppr_article_scores[article_idx]

        if len(query_ner_list) == 0 or len(top_entity_scores) == 0:
            doc_score = query_doc_scores
            self.statistics["doc"] = self.statistics.get("doc", 0) + 1
        elif (
            np.min(list(top_entity_scores.values())) > self.recognition_threshold
        ):  # high confidence in named entities
            doc_score = ppr_doc_scores
            self.statistics["ppr"] = self.statistics.get("ppr", 0) + 1
        else:  # relatively low confidence in named entities, combine the two scores
            # the higher threshold, the higher chance to use the doc ensemble
            doc_score = ppr_doc_scores * 0.5 + query_doc_scores * 0.5

            top_ppr = np.argsort(ppr_doc_scores)[::-1][:10]
            top_ppr = [(top, ppr_doc_scores[top]) for top in top_ppr]

            top_doc = np.argsort(query_doc_scores)[::-1][:10]
            top_doc = [(top, query_doc_scores[top]) for top in top_doc]

            top_hybrid = np.argsort(doc_score)[::-1][:10]
            top_hybrid = [(top, doc_score[top]) for top in top_hybrid]

            self.ensembling_debug.append((top_ppr, top_doc, top_hybrid))
            self.statistics["ppr_doc_ensemble"] = (
                self.statistics.get("ppr_doc_ensemble", 0) + 1
            )

        # Return ranked docs and ranked scores
        sorted_doc_ids = np.argsort(doc_score, kind="mergesort")[::-1]
        sorted_scores = doc_score[sorted_doc_ids]
        print(f"sorted_scores = {sorted_scores}")
        if not (self.dpr_only) and len(query_ner_list) > 0:
            # logs
            entity_one_hop_triples = []
            for entity_id in np.where(top_entity_vectors > 0)[0]:
                # get all the triples that contain the entity from self.graph_plus
                for t in list(self.kg_adj_list[entity_id].items())[:20]:
                    entity_one_hop_triples.append([self.entities[t[0]], t[1]])
                for t in list(self.kg_inverse_adj_list[entity_id].items())[:20]:
                    entity_one_hop_triples.append([self.entities[t[0]], t[1], "inv"])

            # get top ranked nodes from doc_score and self.docs_to_entities_mat
            nodes_in_retrieved_doc = []
            for doc_id in sorted_doc_ids[:5]:
                node_id_in_doc = list(
                    np.where(self.docs_to_entities_mat[[doc_id], :].toarray()[0] > 0)[0]
                )
                nodes_in_retrieved_doc.append(
                    [self.entities[node_id] for node_id in node_id_in_doc]
                )

            # get top ppr_entity_scores
            if len(top_entity_scores) > 0:
                top_pagerank_entity_ids = np.argsort(
                    ppr_entity_scores, kind="mergesort"
                )[::-1][:20]
            else:
                top_pagerank_entity_ids = []
            # get entities for top_pagerank_entity_ids
            top_ranked_nodes = [
                self.entities[entity_id] for entity_id in top_pagerank_entity_ids
            ]
            logs = {
                "named_entities": query_ner_list,
                "linked_node_scores": [
                    list(k) + [float(v)] for k, v in top_entity_scores.items()
                ],
                "1-hop_graph_for_linked_nodes": entity_one_hop_triples,
                "top_ranked_nodes": top_ranked_nodes,
                "nodes_in_retrieved_doc": nodes_in_retrieved_doc,
            }
        else:
            logs = {}

        output_doc_ids = sorted_doc_ids.tolist()[:top_k]
        output_doc_scores = sorted_scores.tolist()[:top_k]

        rank_info["output_docs"] = [self.docs[x]["title"] for x in output_doc_ids]
        rank_info["output_scores"] = output_doc_scores

        print("*" * 80)
        for k, v in rank_info.items():
            print(f"{k}: {v}")
        print("*" * 80)

        return output_doc_ids, output_doc_scores, logs

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

        self.docs = self.index_data["docs"]
        self.doc_index = self.index_data["doc_index"]
        self.entity_index = self.index_data["entity_index"]

        # entity->id
        self.kb_entity_dict = self.index_data["entity_id_map"]
        # triple->id
        self.triple_id_map = self.index_data["triple_id_map"]
        # article->id
        self.article_id_map = self.index_data["article_id_map"]

        # (s,o)->p
        self.relations_dict = self.index_data["relations"]
        # triples
        self.facts = list(self.triple_id_map.keys())
        self.facts = [
            self.facts[i] for i in np.argsort(list(self.triple_id_map.values()))
        ]
        # entities
        self.entities = np.array(list(self.kb_entity_dict.keys()))[
            np.argsort(list(self.kb_entity_dict.values()))
        ]
        # articles
        self.articles = np.array(list(self.article_id_map.keys()))[
            np.argsort(list(self.article_id_map.values()))
        ]

        # entities contained in doc
        self.docs_to_facts = self.index_data["docs_to_facts"]
        # entities contained in triple
        self.facts_to_entities = self.index_data["facts_to_entities"]

        self.docs_to_facts_mat = self.index_data[
            "docs_to_facts_mat"
        ]  # (num docs, num facts)
        self.facts_to_entities_mat = self.index_data[
            "facts_to_entities_mat"
        ]  # (num facts, num entities)
        self.docs_to_entities_mat = self.index_data[
            "docs_to_entities_mat"
        ]  # (num docs, num entities)

        row_norm = self.docs_to_entities_mat.sum(axis=1)
        self.docs_to_entities_mat = self.docs_to_entities_mat / row_norm[:, np.newaxis]
        self.docs_to_entities_mat = self.docs_to_entities_mat.tocsr()

        self.entity_to_num_doc = self.docs_to_entities_mat.sum(
            0
        ).T  # higher value means less important

        self.articles_to_docs_mat = self.index_data["articles_to_docs_mat"]

        self.graph_plus = self.index_data[
            "graph_plus"
        ]  # (entity1 id, entity2 id) -> the number of occurrences

    def build_graph(self):

        edges = set()

        new_graph_plus = {}
        self.kg_adj_list = defaultdict(dict)
        self.kg_inverse_adj_list = defaultdict(dict)

        for edge, weight in tqdm(
            self.graph_plus.items(), total=len(self.graph_plus), desc="Building Graph"
        ):
            edge1 = edge[0]
            edge2 = edge[1]

            if (edge1, edge2) not in edges and edge1 != edge2:
                new_graph_plus[(edge1, edge2)] = self.graph_plus[(edge[0], edge[1])]
                edges.add((edge1, edge2))
                self.kg_adj_list[edge1][edge2] = self.graph_plus[(edge[0], edge[1])]
                self.kg_inverse_adj_list[edge2][edge1] = self.graph_plus[
                    (edge[0], edge[1])
                ]

        self.graph_plus = new_graph_plus

        edges = list(edges)

        n_vertices = len(self.kb_entity_dict)
        self.g = ig.Graph(n_vertices, edges)

        self.g.es["weight"] = [self.graph_plus[(v1, v3)] for v1, v3 in edges]
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
                vertices=range(len(self.kb_entity_dict)),
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

        top_entity_vec = np.zeros(len(self.entities))

        for max_score, entity_id in zip(max_scores, entity_ids):
            if self.node_specificity:
                if (
                    self.entity_to_num_doc[entity_id] == 0
                ):  # just in case the entity is not recorded in any documents
                    weight = 1
                else:  # the more frequent the entity, the less weight it gets
                    weight = 1 / self.entity_to_num_doc[entity_id]

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
                (query_ner_list[query_entity_id], self.entities[entity_id])
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
        damping=0.1,
        similarity_threshold=0.7,
        recognition_threshold=0.9,
    )

    queries = [
        # "公积金可以抵个税不",
        # "公积金贷款首付多少，能贷多少",
        # "两孩家庭的公积金贷款有优待吗",
        "我在建德，疫情管控期间能不能多提一些公积金交房租",
        # "社保基数怎么规定的",
        # "海水为什么看上去是蓝色的",
    ]
    output = []
    for query in queries:
        output.append(hipporag.answer(query, 10))
    for q, a in zip(queries, output):
        print("-" * 80)
        print(f"问题: \n{q}")
        print(f"答案: \n{a}")
