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
from knext.builder.auto_extract.index.utils import (
    EmbeddingService,
    knn,
    NodeType,
    EdgeType,
)
from tqdm.std import defaultdict

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"


def build_graph(
    openie_output_file: str,
    embedding_service: EmbeddingService,
    workdir: str,
    nns: int = 100,
    synonym_thresh: float = 0.8,
):

    similarity_max = 1.0

    openie_output = json.load(
        open(
            openie_output_file,
            "r",
        )
    )

    docs = openie_output["docs"]
    chunk_map = {}
    entity_set = set()
    document_set = set()
    relations = {}  # (s,o)->p
    triple_tuples = []
    # full_neighborhoods = {}  # s->(s,p,o)

    for i, doc in tqdm(enumerate(docs), total=len(docs)):
        title = doc["title"]

        chunk_map[title] = doc
        document_title = title.split("#")[0]
        document_set.add(document_title)
        document = doc["passage"]
        extracted_entities = doc["extracted_entities"]
        extracted_triples = doc["extracted_triples"]
        for entity in extracted_entities:
            entity_set.add(entity)
        # Populate Triples from OpenIE
        for triple in extracted_triples:
            s, p, o = triple
            relations[(s, o)] = p

            entity_set.add(s)
            entity_set.add(o)

        triple_tuples.append(extracted_triples)

    print("Creating Graph")

    # create_node
    unique_entities = list(set(entity_set))
    unique_entities.sort()
    # entity_id_map = {p: i for i, p in enumerate(unique_entities)}  #  entity->id

    unique_chunks = list(chunk_map.keys())
    unique_chunks.sort()
    docs = [chunk_map[x] for x in unique_chunks]

    unique_documents = list(document_set)
    unique_documents.sort()
    # document_id_map = {p: i for i, p in enumerate(unique_documents)}  #  document->id

    node_id_map = {}
    idx = 0
    node_type_index = {}

    for node_type, nodes in zip(
        [NodeType.ENTITY, NodeType.CHUNK, NodeType.DOCUMENT],
        [unique_entities, unique_chunks, unique_documents],
    ):
        node_type_index[node_type.name] = [idx, idx + len(nodes)]
        for node in nodes:
            key = (node, node_type.name)
            if key not in node_id_map:
                node_id_map[key] = idx
                idx += 1

    num_nodes = len(node_id_map)

    # facts = []
    # for triples in triple_tuples:
    #     facts.extend([tuple(t) for t in triples])
    # print(f"original num facts: {len(facts)}")
    # facts = list(set(facts))
    # print(f"dedupes num facts: {len(facts)}")
    # facts.sort()
    # triple_id_map = {f: i for i, f in enumerate(facts)}  # triple->id

    # docs_to_facts = {}
    documents_to_chunks = {}
    # facts_to_entities = {}
    entities_to_chunks = {}
    entities_to_entities = {}

    for i, doc in tqdm(enumerate(docs), total=len(docs), desc="Create Graph"):
        chunk_title = doc["title"]
        content = chunk_title + doc["passage"]
        document_title = chunk_title.split("#")[0]

        chunk_id = node_id_map[(chunk_title, NodeType.CHUNK.name)]
        document_id = node_id_map[(document_title, NodeType.DOCUMENT.name)]

        documents_to_chunks[(document_id, chunk_id)] = (
            documents_to_chunks.get((document_id, chunk_id), 0) + 1
        )

        for entity in unique_entities:
            if entity in content:
                entity_id = node_id_map[(entity, NodeType.ENTITY.name)]
                entities_to_chunks[(entity_id, chunk_id)] = (
                    entities_to_chunks.get((entity_id, chunk_id), 0) + 1
                )

        extracted_triples = doc["extracted_triples"]
        for triple in extracted_triples:
            s, p, o = triple
            s_id = node_id_map[(s, NodeType.ENTITY.name)]
            o_id = node_id_map[(o, NodeType.ENTITY.name)]
            entities_to_entities[(s_id, o_id)] = (
                entities_to_entities.get((s_id, o_id), 0) + 1
            )

    graph = {}

    for k, v in documents_to_chunks.items():
        graph[k] = (v, EdgeType.DOCUMENT_CONTAINS_CHUNK.name)

    for k, v in entities_to_chunks.items():
        graph[k] = (v, EdgeType.ENTITY_IN_CHUNK.name)

    for k, v in entities_to_entities.items():
        graph[k] = (v, EdgeType.ENTITY_CONCURRENT_ENTITY.name)

    # Build entity and doc indices
    # Build the index in a new process to avoid potential deadlocks in colbert.

    chunk_content = []
    for doc in docs:
        title = doc["title"]
        text = doc["text"]
        chunk_content.append(
            json.dumps(f"{title}\n{text}".replace("\t", " "), ensure_ascii=False)
        )

    # build vector index for chunks
    chunk_local_ids, chunk_emb = embedding_service(
        chunk_content, batch_size=2, normalize=True
    )

    chunk_global_ids = []
    for chunk_local_id in chunk_local_ids:
        chunk = docs[chunk_local_id]["title"]
        chunk_id = node_id_map[(chunk, NodeType.CHUNK.name)]
        chunk_global_ids.append(chunk_id)

    chunk_index = (chunk_global_ids, chunk_emb)

    # build vector index for entities
    entity_local_ids, entity_emb = embedding_service(
        unique_entities, batch_size=8, normalize=True
    )
    entity_global_ids = []
    for entity_local_id in entity_local_ids:
        entity = unique_entities[entity_local_id]
        entity_id = node_id_map[(entity, NodeType.ENTITY.name)]
        entity_global_ids.append(entity_id)

    entity_index = (entity_global_ids, entity_emb)

    entity_similarity = knn(entity_index, entity_index, nns)

    print("Augmenting Graph from Similarity")

    synonym_entities = defaultdict(list)

    graph_plus = copy.deepcopy(graph)
    entity_id_start = node_type_index[NodeType.ENTITY.name][0]
    for entity_id in tqdm(entity_similarity.keys(), total=len(entity_similarity)):
        entity = unique_entities[entity_id - entity_id_start]
        nearest_neighbor_ids, scores = entity_similarity[entity_id]

        num_nns = 0
        for nn_id, score in zip(nearest_neighbor_ids, scores):
            if score < synonym_thresh or num_nns > 100:
                break
            if nn_id != entity_id:
                graph_plus[(entity_id, nn_id)] = (
                    score,
                    EdgeType.ENTITY_SYNONYM_ENTITY.name,
                )
                graph_plus[(nn_id, entity_id)] = (
                    score,
                    EdgeType.ENTITY_SYNONYM_ENTITY.name,
                )
                synonym_entities[entity_id].append((nn_id, score))
                # nn = unique_entities[nn_id-entity_id_start]
                # synonym_entities[entity].append((nn, score))

    entity_tc = {}
    for entity in unique_entities:
        entity_id = node_id_map[(entity, NodeType.ENTITY.name)]
        count = 0
        for doc in docs:
            passage = doc["text"]
            count += passage.count(entity)
        entity_tc[entity_id] = count

    entity_in_chunks = {}
    for k, v in graph_plus.items():
        if v[1] == EdgeType.ENTITY_IN_CHUNK.name:
            entity_id, chunk_id = k
            entity_in_chunks[entity_id] = entity_in_chunks.get(entity_id, 0) + 1

    entity_weight = {}
    for entity in unique_entities:
        entity_id = node_id_map[(entity, NodeType.ENTITY.name)]
        tc = entity_tc.get(entity_id, 1)
        cc = entity_in_chunks.get(entity_id, 1)

        synonyms = synonym_entities.get(entity_id, [])
        for synonym in synonyms:
            sid, score = synonym
            tc += entity_tc.get(sid, 0) * score
            cc += entity_in_chunks.get(sid, 0) * score
        weight = np.log(1 + tc) / cc
        entity_weight[entity_id] = weight

    # for entity_id, count in entity_to_num_chunk.items():
    #     val = count
    #     synonym_entities = self.synonym_entities.get(entity_id, [])
    #     for synonym_entity in synonym_entities:
    #         sid, score = synonym_entity
    #         val += entity_to_num_chunk.get(sid, 0) * score
    #     self.entity_freq[entity_id] = val

    return {
        "docs": docs,
        "chunk_index": chunk_index,  # indexed document chunks
        "entity_index": entity_index,  # indexed entities
        "entities": unique_entities,
        "chunks": unique_chunks,
        "documents": unique_documents,
        "node_id_map": node_id_map,
        "node_type_index": node_type_index,
        "synonym_entities": synonym_entities,
        "entity_weight": entity_weight,
        "graph_plus": graph_plus,
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
        synonym_thresh=0.8,
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
