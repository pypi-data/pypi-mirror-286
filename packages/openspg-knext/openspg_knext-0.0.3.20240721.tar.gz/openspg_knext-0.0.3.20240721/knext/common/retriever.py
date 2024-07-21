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

import io
import json
from pathlib import Path
from abc import ABC, abstractmethod
from typing import Any, Union, Iterable, Dict, Tuple
from knext.common.vectorizer import Vectorizer


Item = Dict[str, Any]
RetrievalResult = Iterable[Tuple[Item, float]]


class Retriever(ABC):
    """
    Retriever indexing a collection of items and supports fast retrieving of the
    desired items given a query.
    """

    @classmethod
    def from_config(cls, config: Union[str, Path, Dict[str, Any]]) -> "Retriever":
        """
        Create retriever from `config`.

        If `config` is a string or path, it will be loaded as a dictionary depending
        on its file extension. Currently, the following formats are supported:

        * .json: JSON
        * .json5: JSON with comments support
        * .yaml: YAML

        :param config: retriever config
        :type config: str, Path or Dict[str, Any]
        :return: retriever instance
        :rtype: Retriever
        """
        from nn4k.utils.class_importing import dynamic_import_class

        if isinstance(config, (str, Path)):
            config_path = config
            if not isinstance(config_path, Path):
                config_path = Path(config_path)
            if config_path.name.endswith(".yaml"):
                import yaml

                with io.open(config_path, "r", encoding="utf-8") as fin:
                    config = yaml.safe_load(fin)
            elif config_path.name.endswith(".json5"):
                import json5

                with io.open(config_path, "r", encoding="utf-8") as fin:
                    config = json5.load(fin)
            elif config_path.name.endswith(".json"):
                with io.open(config_path, "r", encoding="utf-8") as fin:
                    config = json.load(fin)
            else:
                message = "only .json, .json5 and .yaml are supported currently; "
                message += "can not load retriever config from %r" % str(config_path)
                raise RuntimeError(message)
        elif isinstance(config, dict):
            pass
        else:
            message = "only str, Path and dict are supported; "
            message += "invalid retriever config: %r" % (config,)
            raise RuntimeError(message)

        class_name = config.get("retriever")
        if class_name is None:
            message = "retriever class name is not specified"
            raise RuntimeError(message)
        retriever_class = dynamic_import_class(class_name, "retriever")
        if not issubclass(retriever_class, Retriever):
            message = "class %r is not a retriever class" % (class_name,)
            raise RuntimeError(message)
        retriever = retriever_class._from_config(config)
        return retriever

    @classmethod
    @abstractmethod
    def _from_config(cls, config: Dict[str, Any]) -> "Retriever":
        """
        Create retriever from `config`. This method is supposed to be implemented
        by derived classes.

        :param config: retriever config
        :type config: Dict[str, Any]
        :return: retriever instance
        :rtype: Retriever
        """
        message = "abstract method _from_config is not implemented"
        raise NotImplementedError(message)

    def index(self, items: Union[Item, Iterable[Item]]) -> None:
        """
        Add one or more items to the index of the retriever.

        NOTE: This method may not be supported by the retriever.

        :param items: items to index
        :type items: Item or Iterable[Item]
        """
        message = "method index is not supported by the retriever"
        raise RuntimeError(message)

    @abstractmethod
    def retrieve(
        self, queries: Union[str, Iterable[str]], topk: int = 10
    ) -> Union[RetrievalResult, Iterable[RetrievalResult]]:
        """
        Retrieve items for the given query or queries.

        :param queries: queries to retrieve
        :type queries: str or Iterable[str]
        :param int topk: how many most related items to return for each query, default to 10
        :return: retrieval results of the queries
        :rtype: RetrievalResult or Iterable[RetrievalResult]
        """
        message = "abstract method retrieve is not implemented"
        raise NotImplementedError(message)


class ESBaseRetriever(Retriever):
    """
    Retrieve items with Elasticsearch.
    """

    def __init__(self, config: Dict[str, Any]):
        from elasticsearch import Elasticsearch

        url = config.get("url")
        if url is None:
            message = "Elasticsearch url is required"
            raise RuntimeError(message)
        index_name = config.get("index_name")
        if index_name is None:
            message = "Elasticsearch index name is required"
            raise RuntimeError(message)
        delete_index_if_exists = config.get("delete_index_if_exists", False)
        self._es_client = Elasticsearch(url)
        self._index_name = index_name
        self._delete_index_if_exists = delete_index_if_exists
        self._ensure_index_created()

    @classmethod
    def _from_config(cls, config: Dict[str, Any]) -> Retriever:
        """
        Create retriever from `config`.

        :param config: retriever config
        :type config: Dict[str, Any]
        :return: retriever instance
        :rtype: Retriever
        """
        retriever = cls(config)
        return retriever

    @abstractmethod
    def _ensure_index_created(self):
        message = "method _ensure_index_created is not implemented"
        raise NotImplementedError(message)

    def _preprocess_items(self, items: Iterable[Item]) -> None:
        pass

    def index(self, items: Union[Item, Iterable[Item]]) -> None:
        """
        Add one or more items to the index of the retriever.

        :param items: items to index
        :type items: Item or Iterable[Item]
        """
        if isinstance(items, dict):
            items = [items]
        self._preprocess_items(items)
        operations = []
        for item in items:
            operations.append({"index": {"_index": self._index_name}})
            operations.append(item)
        results = self._es_client.bulk(
            index=self._index_name, operations=operations, refresh=True
        )
        errors = results.get("errors", False)
        if errors:
            message = "fail to index %d items" % len(items)
            for item in results.get("items", []):
                node = item.get("index", {})
                node = node.get("error", {})
                node = node.get("caused_by", {})
                msg = node.get("reason")
                if isinstance(msg, str):
                    message += "; %s" % msg
                    break
            raise RuntimeError(message)

    @abstractmethod
    def _make_search_queries(
        self, texts: Iterable[str], topk: int
    ) -> Iterable[Dict[str, Any]]:
        message = "method _make_search_queries is not implemented"
        raise NotImplementedError(message)

    def retrieve(
        self, queries: Union[str, Iterable[str]], topk: int = 10
    ) -> Union[RetrievalResult, Iterable[RetrievalResult]]:
        """
        Retrieve items for the given query or queries.

        :param queries: queries to retrieve
        :type queries: str or Iterable[str]
        :param int topk: how many most related items to return for each query, default to 10
        :return: retrieval results of the queries
        :rtype: RetrievalResult or Iterable[RetrievalResult]
        """
        texts = queries
        if isinstance(texts, str):
            texts = [texts]
        searches = self._make_search_queries(texts, topk=topk)
        results = self._es_client.msearch(index=self._index_name, searches=searches)
        responses = results.get("responses", [])
        answers = []
        for response in responses:
            if "error" in response:
                node = response.get("error", {})
                node = node.get("root_cause", [])
                node = node[0] if node else {}
                msg = node.get("reason")
                message = "fail to retrieve for %d queries" % len(texts)
                if isinstance(msg, str):
                    message += "; %s" % msg
                raise RuntimeError(message)
            node = response.get("hits", {})
            node = node.get("hits", [])
            answer = []
            for item in node:
                source = item.get("_source")
                score = item.get("_score")
                answer.append((source, score))
            answers.append(answer)
        if isinstance(queries, str):
            assert len(answers) == 1
            return answers[0]
        else:
            assert len(answers) == len(queries)
            return answers


class ESTextRetriever(ESBaseRetriever):
    """
    Retrieve items with Elasticsearch via text searching.
    """

    def __init__(self, config: Dict[str, Any]):
        searched_field_name = config.get("searched_field_name")
        if searched_field_name is None:
            message = "searched field name is required"
            raise RuntimeError(message)
        self._searched_field_name = searched_field_name
        super().__init__(config)

    def _ensure_index_created(self):
        if self._delete_index_if_exists:
            self._es_client.indices.delete(
                index=self._index_name, ignore_unavailable=True
            )
        if self._es_client.indices.exists(index=self._index_name):
            return
        self._es_client.indices.create(index=self._index_name)

    def _make_search_queries(
        self, texts: Iterable[str], topk: int
    ) -> Iterable[Dict[str, Any]]:
        searches = []
        for text in texts:
            searches.append({})
            searches.append(
                {
                    "_source": True,
                    "query": {"match": {self._searched_field_name: {"query": text}}},
                    "size": topk,
                }
            )
        return searches


class ESSemanticRetriever(ESBaseRetriever):
    """
    Retrieve items with Elasticsearch via embedding vectors.
    """

    def __init__(self, config: Dict[str, Any]):
        vectorized_field_name = config.get("vectorized_field_name")
        if vectorized_field_name is None:
            message = "vectorized field name is required"
            raise RuntimeError(message)
        vector_field_name = config.get("vector_field_name")
        if vector_field_name is None:
            vector_field_name = vectorized_field_name + "_vector"
        vector_dimensions = config.get("vector_dimensions")
        if vector_dimensions is None:
            message = "vector dimensions is required"
            raise RuntimeError(message)
        if not isinstance(vector_dimensions, int) or vector_dimensions <= 0:
            message = "vector dimensions must be positive integer"
            raise ValueError(message)
        if vector_dimensions > 1024:
            message = (
                "Elasticsearch cannot index vectors with dimension greater than 1024"
            )
            raise RuntimeError(message)
        metric_type = config.get("metric_type")
        if metric_type is None:
            metric_type = "IP"
        elif metric_type == "IP":
            pass
        else:
            message = "only IP metric_type is supported for the moment"
            raise RuntimeError(message)
        vec_config = config.get("vectorizer")
        if vec_config is None:
            message = "vectorizer config is required"
            raise RuntimeError(message)
        self._vectorized_field_name = vectorized_field_name
        self._vector_field_name = vector_field_name
        self._vector_dimensions = vector_dimensions
        self._metric_type = metric_type
        self._vectorizer = Vectorizer.from_config(vec_config)
        super().__init__(config)

    def _ensure_index_created(self):
        if self._delete_index_if_exists:
            self._es_client.indices.delete(
                index=self._index_name, ignore_unavailable=True
            )
        if self._es_client.indices.exists(index=self._index_name):
            return
        mappings = {
            "properties": {
                self._vector_field_name: {
                    "type": "dense_vector",
                    "dims": self._vector_dimensions,
                    "index": "true",
                    # Only IP (Inner Product) is supported for the moment and
                    # we assume the embedding vectors are normalized.
                    "similarity": "cosine",
                }
            }
        }
        self._es_client.indices.create(index=self._index_name, mappings=mappings)

    def _preprocess_items(self, items: Iterable[Item]) -> None:
        texts = []
        for item in items:
            text = item.get(self._vectorized_field_name)
            if text is None:
                message = "item has no field %r" % (self._vectorized_field_name,)
                raise RuntimeError(message)
            if not isinstance(text, str):
                message = "item has non-string field %r" % (
                    self._vectorized_field_name,
                )
                raise RuntimeError(message)
            texts.append(text)
        embeddings = self._vectorizer.vectorize(texts)
        for item, embedding in zip(items, embeddings):
            item[self._vector_field_name] = embedding

    def _make_search_queries(
        self, texts: Iterable[str], topk: int
    ) -> Iterable[Dict[str, Any]]:
        embeddings = self._vectorizer.vectorize(texts)
        searches = []
        for embedding in embeddings:
            searches.append({})
            searches.append(
                {
                    "_source": {"excludes": [self._vector_field_name]},
                    "knn": {
                        "field": self._vector_field_name,
                        "query_vector": embedding,
                        "k": topk,
                        "num_candidates": (topk * 3 + 1) // 2,
                    },
                    "size": topk,
                }
            )
        return searches
