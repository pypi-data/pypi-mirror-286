# -*- coding: utf-8 -*-


import copy
import re
import ipdb
import numpy as np
import pandas as pd
import os
import json
import pickle
import multiprocessing as mp
from glob import glob
from tqdm import tqdm
from typing import List, Union
from scipy.sparse import csr_array
from knext.builder.auto_extract.index.utils import EmbeddingService, knn

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"


def build_graph(
    openie_output_file: str,
    embedding_service: EmbeddingService,
    workdir: str,
    nns: int = 100,
    synonym_thresh: float = 0.8,
):

    inter_triple_weight = 0.3
    similarity_max = 1.0

    openie_output = json.load(
        open(
            openie_output_file,
            "r",
        )
    )

    docs = openie_output["docs"]

    entities = []
    articles = set()
    relations = {}  # (s,o)->p
    triple_tuples = []
    # full_neighborhoods = {}  # s->(s,p,o)

    for i, doc in tqdm(enumerate(docs), total=len(docs)):
        title = doc["title"]
        article_title = title.split("#")[0]
        articles.add(article_title)

        document = doc["passage"]
        ner_entities = doc["extracted_entities"]
        triples = doc["extracted_triples"]
        entities.extend(ner_entities)
        # Populate Triples from OpenIE
        for triple in triples:
            entities.extend(triple)

            s, p, o = triple
            relations[(s, o)] = p

            entities.append(s)
            entities.append(o)

        triple_tuples.append(triples)

    print("Creating Graph")
    unique_entities = list(set(entities))
    unique_entities.sort()
    entity_id_map = {p: i for i, p in enumerate(unique_entities)}  #  entity->id

    unique_articles = list(articles)
    unique_articles.sort()
    article_id_map = {p: i for i, p in enumerate(unique_articles)}  #  article->id

    facts = []
    for triples in triple_tuples:
        facts.extend([tuple(t) for t in triples])
    print(f"original num facts: {len(facts)}")
    facts = list(set(facts))
    print(f"dedupes num facts: {len(facts)}")
    facts.sort()
    triple_id_map = {f: i for i, f in enumerate(facts)}  # triple->id

    docs_to_facts = {}  # Num Docs x Num Facts
    articles_to_docs = {}  #  Num Articles x Num Docs
    facts_to_entities = {}  # Num Facts x Num Entities
    docs_to_entities = {}  # Num Docs x Num Entities

    graph = {}  # Num Entities x Num Entities

    # Creating Adjacency and Document to Entity Matrices
    for doc_id, triples in tqdm(enumerate(triple_tuples), total=len(triple_tuples)):
        doc = docs[doc_id]
        article_title = doc["title"].split("#")[0]
        print(doc_id, doc["title"], article_title)
        article_id = article_id_map[article_title]
        articles_to_docs[(article_id, doc_id)] = 1

        entities = doc["extracted_entities"]
        for entity in unique_entities:
            if entity in doc["text"]:
                entity_id = entity_id_map[entity]
                docs_to_entities[(doc_id, entity_id)] = 1
        fact_edges = []

        # Iterate over triples
        for triple in triples:
            triple = tuple(triple)
            fact_id = triple_id_map[triple]
            s, p, o = triple

            docs_to_facts[(doc_id, fact_id)] = 1

            s_id = entity_id_map[s]
            o_id = entity_id_map[o]

            facts_to_entities[(fact_id, s_id)] = 1
            facts_to_entities[(fact_id, o_id)] = 1
            fact_edge_r = (s_id, o_id)
            fact_edge_l = (o_id, s_id)
            fact_edges.append(fact_edge_r)
            fact_edges.append(fact_edge_l)

            graph[fact_edge_r] = graph.get(fact_edge_r, 0.0) + inter_triple_weight
            graph[fact_edge_l] = graph.get(fact_edge_l, 0.0) + inter_triple_weight

    print(articles_to_docs)
    docs_to_facts_mat = csr_array(
        (
            [int(v) for v in docs_to_facts.values()],
            (
                [int(e[0]) for e in docs_to_facts.keys()],
                [int(e[1]) for e in docs_to_facts.keys()],
            ),
        ),
        shape=(len(triple_tuples), len(facts)),
    )
    facts_to_entities_mat = csr_array(
        (
            [int(v) for v in facts_to_entities.values()],
            (
                [e[0] for e in facts_to_entities.keys()],
                [e[1] for e in facts_to_entities.keys()],
            ),
        ),
        shape=(len(facts), len(unique_entities)),
    )

    docs_to_entities_mat = csr_array(
        (
            [int(v) for v in docs_to_entities.values()],
            (
                [e[0] for e in docs_to_entities.keys()],
                [e[1] for e in docs_to_entities.keys()],
            ),
        ),
        shape=(len(docs), len(unique_entities)),
    )

    articles_to_docs_mat = csr_array(
        (
            [int(v) for v in articles_to_docs.values()],
            (
                [e[0] for e in articles_to_docs.keys()],
                [e[1] for e in articles_to_docs.keys()],
            ),
        ),
        shape=(len(unique_articles), len(docs)),
    )

    # Build entity and doc indices
    # Build the index in a new process to avoid potential deadlocks in colbert.

    doc_content = []
    for doc in docs:
        title = doc["title"]
        text = doc["text"]
        doc_content.append(
            json.dumps(f"{title}\n{text}".replace("\t", " "), ensure_ascii=False)
        )

    doc_index = embedding_service(doc_content, batch_size=4, normalize=True)
    entity_index = embedding_service(unique_entities, batch_size=8, normalize=True)
    entity_similarity = knn(entity_index, entity_index, nns)

    # print("Start to build index for documents...")
    # with mp.Pool(processes=1) as pool:
    #     pool.apply(
    #         build_colbert_index,
    #         args=("document", checkpoint_path, workdir, doc_content),
    #     )
    # print("Start to build index for entities...")
    # with mp.Pool(processes=1) as pool:
    #     pool.apply(
    #         build_colbert_index,
    #         args=("entity", checkpoint_path, workdir, unique_entities),
    #     )

    # # Expanding OpenIE triples with cosine similiarity-based synonymy edges
    # entity_similarity = colbertv2_knn(
    #     workdir, unique_entities, unique_entities, "entity", nns
    # )
    print("Augmenting Graph from Similarity")

    graph_plus = copy.deepcopy(graph)
    synonyms = []
    for entity_id in tqdm(entity_similarity.keys(), total=len(entity_similarity)):
        entity = unique_entities[entity_id]

        # filter out too short entities
        if len(entity) > 2:
            nearest_neighbor_ids, scores = entity_similarity[entity_id]

            num_nns = 0
            for nn_id, score in zip(nearest_neighbor_ids, scores):
                if score < synonym_thresh or num_nns > 100:
                    break
                if nn_id != entity_id:
                    nn = unique_entities[nn_id]
                    sim_edge = (entity_id, nn_id)
                    relations[(entity, nn)] = "equivalent"
                    graph_plus[sim_edge] = similarity_max * score
                    synonyms.append((entity, nn))
    return {
        # "docs": [{"title": x["title"], "text": x["text"]} for x in docs],
        "docs": docs,
        "doc_index": doc_index,  # indexed documents
        "entity_index": entity_index,  # indexed entities
        "entity_id_map": entity_id_map,
        "triple_id_map": triple_id_map,
        "article_id_map": article_id_map,
        "relations": relations,
        "docs_to_facts": docs_to_facts,
        "facts_to_entities": facts_to_entities,
        "docs_to_facts_mat": docs_to_facts_mat,
        "docs_to_entities_mat": docs_to_entities_mat,
        "facts_to_entities_mat": facts_to_entities_mat,
        "articles_to_docs_mat": articles_to_docs_mat,
        "graph_plus": graph_plus,
        "entity_similarity": entity_similarity,
    }


if __name__ == "__main__":
    workdir = os.path.expanduser("~/Src/libs/data/policy_files/")
    openie_output_file = os.path.join(workdir, "zhengce-deepseek-output-v2.json")
    embedding_service = EmbeddingService(use_pre=True, num_parallel=1)
    graph_data = build_graph(
        openie_output_file=openie_output_file,
        embedding_service=embedding_service,
        workdir=workdir,
        nns=100,
        synonym_thresh=0.7,
    )
    print(graph_data.keys())
    basename = os.path.splitext(openie_output_file)[0]

    pickle.dump(
        graph_data,
        open(
            os.path.join(workdir, f"{basename}-graph.pkl"),
            "wb",
        ),
    )
