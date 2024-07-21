import base64
import json
from multiprocessing import Pool

import numpy as np

from knext.builder.auto_extract.kag.extractor import OpenIEExtractor
from knext.common.graph_store import TuGraphStore
from knext.common.retriever import ESBaseRetriever
from knext.schema.marklang.schema_ml import SPGSchemaMarkLang

LOCAL_GRAPH_STORE_CONFIG = {
    "graph_store": "knext.common.graph_store.TuGraphStore",
    "host": "127.0.0.1",
    "port": "7687",
    "username": "admin",
    "password": "73@TuGraph",
    "scheme": "bolt",
    "namespace": "kag",
}

host = base64.b64decode("cGFpcGx1c2luZmVyZW5jZS5hbGlwYXkuY29t").decode("utf-8")
model = base64.b64decode(
    "MWVmYzliZDY5ZjZkYTNhNV9iZ2VfbGFyZ2Vfa2didWlsZGVyX29mZmxpbmU="
).decode("utf-8")
LOCAL_ENTITY_RETRIEVER_CONFIG = {
    "retriever": "knext.common.retriever.ESSemanticRetriever",
    "url": "elasticsearch://127.0.0.1:9200?scheme=http",
    "index_name": "entity",
    # "delete_index_if_exists": True,
    "vectorized_field_name": "id",
    "vector_dimensions": 768,
    "vectorizer": {
        "vectorizer": "knext.common.vectorizer.MayaVectorizer",
        "url": "https://%s/inference/%s/v1" % (host, model),
        "debug_mode": True,
    },
}

LOCAL_CHUNK_RETRIEVER_CONFIG = {
    "retriever": "knext.common.retriever.ESSemanticRetriever",
    "url": "elasticsearch://127.0.0.1:9200?scheme=http",
    "index_name": "chunk",
    # "delete_index_if_exists": True,
    "vectorized_field_name": "content",
    "vector_dimensions": 768,
    "vectorizer": {
        "vectorizer": "knext.common.vectorizer.MayaVectorizer",
        "url": "https://%s/inference/%s/v1" % (host, model),
        "debug_mode": True,
    },
}


class KAGIndexer:

    def __init__(self, file_path, extract_num_processes=1):
        self.extractor = OpenIEExtractor()
        self.extract_num_processes = extract_num_processes
        self.file_path = file_path

        self.graph_store = TuGraphStore.from_config(LOCAL_GRAPH_STORE_CONFIG)
        self.entity_retriever = ESBaseRetriever.from_config(LOCAL_ENTITY_RETRIEVER_CONFIG)
        self.doc_retriever = ESBaseRetriever.from_config(LOCAL_CHUNK_RETRIEVER_CONFIG)

    def load_json_file(self):
        corpus = json.load(open(self.file_path, 'r'))

        if 'hotpotqa' in self.file_path:
            keys = list(corpus.keys())
            retrieval_corpus = [{'idx': i, 'title': key, 'passage': key + '\n' + ''.join(corpus[key])} for i, key in enumerate(keys)]
        else:
            retrieval_corpus = corpus
            for idx, document in enumerate(retrieval_corpus):
                document['idx'] = idx
                document['passage'] = document['title'] + '\n' + document['text']

        return retrieval_corpus

    def invoke(self):
        retrieval_corpus = self.load_json_file()

        splits = np.array_split(range(len(retrieval_corpus)), self.extract_num_processes)
        splitted_documents = []

        for split in splits:
            splitted_documents.append([retrieval_corpus[i] for i in split])

        if self.extract_num_processes > 1:
            with Pool(processes=self.extract_num_processes) as pool:
                outputs = pool.map(self.extractor.batch, splitted_documents)
        else:
            outputs = [self.extractor.batch(documents) for documents in splitted_documents]

        for idx, output in outputs:
            title = retrieval_corpus[idx]['title']
            passage = retrieval_corpus[idx]['passage']
            for triplet in output:
                if not isinstance(triplet, list) or len(triplet) != 3:
                    continue
                self.graph_store.insert_triplet(triplet[0], triplet[1], triplet[2])
                self.graph_store.insert_doc(triplet[0], idx, title, passage)
                self.graph_store.insert_doc(triplet[2], idx, title, passage)
                self.entity_retriever.index({"id": triplet[0]})
                self.entity_retriever.index({"id": triplet[2]})
            self.doc_retriever.index({"id": title, "title": title, "content": passage})


if __name__ == '__main__':
    # indexer = KAGIndexer("hotpotqa_corpus.json", extract_num_processes=10)
    # # indexer.invoke()
    # print(indexer.entity_retriever.retrieve("Manny Machado"))
    # print(indexer.doc_retriever.retrieve("Manny Machado"))
    # # indexer.entity_retriever._es_client.delete_by_query(index="chunk", body={"query": {"match_all": {}}})
    # result = indexer.entity_retriever._es_client.search(index="entity", body={"query": {"match": {"id": "Manny Machado"}}})
    # print([(hit['_id'], hit['_source']['id']) for hit in result['hits']['hits']])
    # print(result['hits']['hits'][0])
    ml = SPGSchemaMarkLang("default.schema", with_server=False)
    print(ml.types)