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
import requests
from pathlib import Path
from abc import ABC, abstractmethod
from typing import Any, Union, Iterable, Dict


EmbeddingVector = Iterable[float]


class Vectorizer(ABC):
    """
    Vectorizer turns texts into embedding vectors.
    """

    @classmethod
    def from_config(cls, config: Union[str, Path, Dict[str, Any]]) -> "Vectorizer":
        """
        Create vectorizer from `config`.

        If `config` is a string or path, it will be loaded as a dictionary depending
        on its file extension. Currently, the following formats are supported:

        * .json: JSON
        * .json5: JSON with comments support
        * .yaml: YAML

        :param config: vectorizer config
        :type config: str, Path or Dict[str, Any]
        :return: vectorizer instance
        :rtype: Vectorizer
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
                message += "can not load vectorizer config from %r" % str(config_path)
                raise RuntimeError(message)
        elif isinstance(config, dict):
            pass
        else:
            message = "only str, Path and dict are supported; "
            message += "invalid vectorizer config: %r" % (config,)
            raise RuntimeError(message)

        class_name = config.get("vectorizer")
        if class_name is None:
            message = "vectorizer class name is not specified"
            raise RuntimeError(message)
        vectorizer_class = dynamic_import_class(class_name, "vectorizer")
        if not issubclass(vectorizer_class, Vectorizer):
            message = "class %r is not a vectorizer class" % (class_name,)
            raise RuntimeError(message)
        vectorizer = vectorizer_class._from_config(config)
        return vectorizer

    @classmethod
    @abstractmethod
    def _from_config(cls, config: Dict[str, Any]) -> "Vectorizer":
        """
        Create vectorizer from `config`. This method is supposed to be implemented
        by derived classes.

        :param config: vectorizer config
        :type config: Dict[str, Any]
        :return: vectorizer instance
        :rtype: Vectorizer
        """
        message = "abstract method _from_config is not implemented"
        raise NotImplementedError(message)

    @abstractmethod
    def vectorize(self, texts: Union[str, Iterable[str]]) -> Union[EmbeddingVector, Iterable[EmbeddingVector]]:
        """
        Vectorize a text string into an embedding vector or multiple text strings into
        multiple embedding vectors.

        :param texts: texts to vectorize
        :type texts: str or Iterable[str]
        :return: embedding vectors of the texts
        :rtype: EmbeddingVector or Iterable[EmbeddingVector]
        """
        message = "abstract method vectorize is not implemented"
        raise NotImplementedError(message)


class OpenAIVectorizer(Vectorizer):
    """
    Invoke OpenAI embedding services to turn texts into embedding vectors.
    """

    def __init__(self, config: Dict[str, Any]):
        from nn4k.invoker import NNInvoker

        self._invoker = NNInvoker.from_config(config)

    @classmethod
    def _from_config(cls, config: Dict[str, Any]) -> Vectorizer:
        """
        Create vectorizer from `config`.

        :param config: vectorizer config
        :type config: Dict[str, Any]
        :return: vectorizer instance
        :rtype: Vectorizer
        """
        vectorizer = cls(config)
        return vectorizer

    def vectorize(self, texts: Union[str, Iterable[str]]) -> Union[EmbeddingVector, Iterable[EmbeddingVector]]:
        """
        Vectorize a text string into an embedding vector or multiple text strings into
        multiple embedding vectors.

        :param texts: texts to vectorize
        :type texts: str or Iterable[str]
        :return: embedding vectors of the texts
        :rtype: EmbeddingVector or Iterable[EmbeddingVector]
        """
        results = self._invoker.remote_inference(texts, type="Embedding")
        if isinstance(texts, str):
            assert len(results) == 1
            return results[0]
        else:
            assert len(results) == len(texts)
            return results


class MayaVectorizer(Vectorizer):
    """
    Invoke Maya embedding services to turn texts into embedding vectors.
    """

    def __init__(self, config: Dict[str, Any]):
        url = config.get("url")
        if url is None:
            message = "Maya model url is required"
            raise RuntimeError(message)
        debug_mode = config.get("debug_mode", False)
        self._url = url
        self._debug_mode = debug_mode
        if not self._debug_mode:
            app_name = config.get("app_name")
            if app_name is None:
                message = "Maya app name is required"
                raise RuntimeError(message)
            app_token = config.get("app_token")
            if app_token is None:
                message = "Maya app token is required"
                raise RuntimeError(message)
            model_id = config.get("model_id")
            if model_id is None:
                message = "Maya model id is required"
                raise RuntimeError(message)
            model_version = config.get("model_version")
            if model_version is None:
                message = "Maya model version is required"
                raise RuntimeError(message)
            self._app_name = app_name
            self._app_token = app_token
            self._model_id = model_id
            self._model_version = model_version

    @classmethod
    def _from_config(cls, config: Dict[str, Any]) -> Vectorizer:
        """
        Create vectorizer from `config`.

        :param config: vectorizer config
        :type config: Dict[str, Any]
        :return: vectorizer instance
        :rtype: Vectorizer
        """
        vectorizer = cls(config)
        return vectorizer

    def vectorize(self, texts: Union[str, Iterable[str]]) -> Union[EmbeddingVector, Iterable[EmbeddingVector]]:
        """
        Vectorize a text string into an embedding vector or multiple text strings into
        multiple embedding vectors.

        :param texts: texts to vectorize
        :type texts: str or Iterable[str]
        :return: embedding vectors of the texts
        :rtype: EmbeddingVector or Iterable[EmbeddingVector]
        """
        sentence_list = texts
        if isinstance(sentence_list, str):
            sentence_list = [sentence_list]
        headers = {"Content-Type": "application/json"}
        if self._debug_mode:
            headers["MPS-app-name"] = "test"
            headers["MPS-http-version"] = "1.0"
        trace_id = "knext.common.vectorizer.MayaVectorizer"
        if self._debug_mode:
            data = {"inputs": sentence_list, "trace_id": trace_id}
            data = json.dumps(data, separators=(",", ":"), ensure_ascii=False)
            data = {"features": {"data": data}}
        else:
            data = {
                "appName": self._app_name,
                "appToken": self._app_token,
                "modelId": self._model_id,
                "modelVersion": self._model_version,
                "sentenceList": sentence_list,
                "traceId": trace_id,
                "invokeType": "embeddings",
            }
        data = json.dumps(data, separators=(",", ":"), ensure_ascii=False)
        data = data.encode("utf-8")
        res = requests.post(self._url, headers=headers, data=data)
        res.raise_for_status()
        body = res.json()
        success = body.get("success", False)
        if not success:
            message = "fail to invoke maya embedding model"
            if hasattr(self, "_model_id"):
                message += " %r" % self._model_id
            error_msg = body.get("errorMsg")
            if error_msg is not None:
                message += "; %s" % error_msg
            raise RuntimeError(message)
        if self._debug_mode:
            results = body["resultMap"]["result"]
            results = json.loads(results)
        else:
            results = body["embeddingList"]
        if isinstance(texts, str):
            assert len(results) == 1
            return results[0]
        else:
            assert len(results) == len(texts)
            return results
