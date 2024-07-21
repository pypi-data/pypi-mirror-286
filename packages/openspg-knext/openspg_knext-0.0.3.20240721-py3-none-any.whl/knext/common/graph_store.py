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
from typing import Any, Union, Dict


class GraphStore(ABC):


    @classmethod
    def from_config(cls, config: Union[str, Path, Dict[str, Any]]) -> "GraphStore":
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
                message += "can not load graph_store config from %r" % str(config_path)
                raise RuntimeError(message)
        elif isinstance(config, dict):
            pass
        else:
            message = "only str, Path and dict are supported; "
            message += "invalid graph_store config: %r" % (config,)
            raise RuntimeError(message)

        class_name = config.get("graph_store")
        if class_name is None:
            message = "graph_store class name is not specified"
            raise RuntimeError(message)
        graph_store_class = dynamic_import_class(class_name, "graph_store")
        if not issubclass(graph_store_class, GraphStore):
            message = "class %r is not a graph_store class" % (class_name,)
            raise RuntimeError(message)
        graph_store = graph_store_class._from_config(config)
        return graph_store

    @classmethod
    @abstractmethod
    def _from_config(cls, config: Dict[str, Any]) -> "GraphStore":
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


class TuGraphStore(GraphStore):
    """
    Invoke OpenAI embedding services to turn texts into embedding vectors.
    """

    def __init__(self, config: Dict[str, Any]):
        """Initialize the TuGraphStore with connection details."""
        self._host = config.get("host", "127.0.0.1")
        self._port = int(config.get("port", "7687"))
        self._username = config.get("username", "admin")
        self._password = config.get("password", "73@TuGraph")
        self._scheme = config.get("scheme", "bolt")
        self._namespace = config.get("namespace", "kag")
        self._node_label = "entity"
        self._edge_label = "relation"
        self._doc_label = "chunk"
        self._driver = self._create_conn()

        self.create_graph(self._namespace)
        try:
            self._create_default_schema()
        except:
            pass

    @classmethod
    def _from_config(cls, config: Dict[str, Any]) -> GraphStore:
        """
        Create vectorizer from `config`.

        :param config: vectorizer config
        :type config: Dict[str, Any]
        :return: vectorizer instance
        :rtype: Vectorizer
        """
        graph_store = cls(config)
        return graph_store

    def _create_conn(self):
        """Create a new TuGraphConnector from host, port, user, pwd, db_name."""
        try:
            from neo4j import GraphDatabase

            db_url = f"{self._scheme}://{self._host}:{str(self._port)}"
            driver = GraphDatabase.driver(db_url, auth=(self._username, self._password))
            driver.verify_connectivity()
            return driver

        except ImportError as err:
            raise ImportError(
                "neo4j package is not installed, please install it with "
                "`pip install neo4j`"
            ) from err

    def get_table_names(self):
        """Get all table names from the TuGraph by Neo4j driver."""
        # run the query to get vertex labels
        with self._driver.session(database="default") as session:
            v_result = session.run("CALL db.vertexLabels()").data()
            v_data = [table_name["label"] for table_name in v_result]

            # run the query to get edge labels
            e_result = session.run("CALL db.edgeLabels()").data()
            e_data = [table_name["label"] for table_name in e_result]
            return {"vertex_tables": v_data, "edge_tables": e_data}

    def _check_label(self, elem_type: str):
        result = self.get_table_names()
        if elem_type == "vertex":
            return self._node_label in result["vertex_tables"]
        if elem_type == "edge":
            return self._edge_label in result["edge_tables"]

    def _create_default_schema(self):
        if not self._check_label("vertex"):
            create_vertex_gql = (
                f"CALL db.createLabel("
                f"'vertex', '{self._node_label}', "
                f"'id', ['id',string,false])"
            )
            self.run(create_vertex_gql)
            create_vertex_gql = (
                f"CALL db.createLabel("
                f"'vertex', '{self._doc_label}', "
                f"'id', ['id',string,false], "
                f"['title',string,false], "
                f"['content',string,false])"
            )
            # "CALL db.createLabel('vertex', 'entity1', 'id', ['id',string,false]) "
            self.run(create_vertex_gql)
        if not self._check_label("edge"):
            create_edge_gql = f"""CALL db.createLabel(
                'edge', '{self._edge_label}', '[["{self._node_label}",
                "{self._node_label}"]]', ["id",STRING,false])"""
            self.run(create_edge_gql)
            create_edge_gql = f"""CALL db.createLabel(
                'edge', 'source', '[["{self._node_label}",
                "{self._doc_label}"]]', ["id",STRING,false])"""
            self.run(create_edge_gql)

    def _escape_quotes(self, value: str) -> str:
        """Escape single and double quotes in a string for queries."""
        return value.replace("'", "\\'").replace('"', '\\"')

    def insert_triplet(self, subject: str, predicate: str, object: str) -> None:
        """Add triplet."""

        subj_escaped = self._escape_quotes(subject)
        rel_escaped = self._escape_quotes(predicate)
        obj_escaped = self._escape_quotes(object)

        subj_query = f"MERGE (n1:{self._node_label} {{id:'{subj_escaped}'}})"
        obj_query = f"MERGE (n1:{self._node_label} {{id:'{obj_escaped}'}})"
        rel_query = (
            f"MERGE (n1:{self._node_label} {{id:'{subj_escaped}'}})"
            f"-[r:{self._edge_label} {{id:'{rel_escaped}'}}]->"
            f"(n2:{self._node_label} {{id:'{obj_escaped}'}})"
        )
        self.run(query=subj_query)
        self.run(query=obj_query)
        self.run(query=rel_query)

    def insert_doc(self, entity_id, doc_id, title, content):
        entity_id = self._escape_quotes(entity_id)
        title = self._escape_quotes(title)
        content = self._escape_quotes(content)

        doc_query = (
            f"MERGE (n1:{self._doc_label} {{id:'{doc_id}'}}) "
            f"ON CREATE SET n1.title='{title}', "
            f"n1.content='{content}'"
        )
        rel_query = (
            f"MERGE (n1:{self._node_label} {{id:'{entity_id}'}})"
            f"-[r:source {{id:'source'}}]->"
            f"(n2:{self._doc_label} {{id:'{doc_id}'}})"
        )
        self.run(query=doc_query)
        self.run(query=rel_query)

    def create_graph(self, graph_name: str) -> None:
        """Create a new graph."""
        # run the query to get vertex labels
        with self._driver.session(database="default") as session:
            graph_list = session.run("CALL dbms.graph.listGraphs()").data()
            exists = any(item["graph_name"] == graph_name for item in graph_list)
            if not exists:
                session.run(f"CALL dbms.graph.createGraph('{graph_name}', '', 2048)")

    def delete_graph(self, graph_name: str) -> None:
        """Delete a graph."""
        with self._driver.session(database="default") as session:
            graph_list = session.run("CALL dbms.graph.listGraphs()").data()
            exists = any(item["graph_name"] == graph_name for item in graph_list)
            if exists:
                session.run(f"Call dbms.graph.deleteGraph('{graph_name}')")

    def run(self, query: str):
        """Run GQL."""
        with self._driver.session(database=self._namespace) as session:
            result = session.run(query)
            return list(result)

    def close(self):
        self._driver.close()
