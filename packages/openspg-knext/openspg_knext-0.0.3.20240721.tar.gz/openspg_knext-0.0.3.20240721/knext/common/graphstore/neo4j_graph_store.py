# -*- coding: utf-8 -*-
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

from neo4j import GraphDatabase
import threading

from abc import ABCMeta
from knext.common.graphstore.graph_store import GraphStore


class SingletonMeta(ABCMeta):
    """
    Thread-safe Singleton metaclass
    """
    _instances = {}
    _lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class Neo4jClient(GraphStore, metaclass=SingletonMeta):

    def __init__(self, uri, user, password, database="neo4j"):
        self._driver = GraphDatabase.driver(uri, auth=(user, password))
        self._database = database
        self._vec_meta = dict()
        self._vec_meta_ts = 0.0
        self._vec_meta_timeout = 60.0

    def close(self):
        self._driver.close()

    def initialize_schema(self, schema):
        pass

    def upsert_node(self, label, properties, id_key="id"):
        with self._driver.session(database=self._database) as session:
            return session.execute_write(self._upsert_node, label, id_key, properties)

    @staticmethod
    def _upsert_node(tx, label, id_key, properties):
        query = f"MERGE (n:{label} {{{id_key}: $properties.{id_key}}}) SET n += $properties RETURN n"
        result = tx.run(query, properties=properties)
        return result.single()[0]

    def upsert_nodes(self, label, properties_list, id_key="id"):
        with self._driver.session(database=self._database) as session:
            return session.execute_write(self._upsert_nodes, label, properties_list, id_key)

    @staticmethod
    def _upsert_nodes(tx, label, properties_list, id_key):
        query = f"UNWIND $properties_list AS properties MERGE (n:{label} {{{id_key}: properties.{id_key}}}) SET n += properties RETURN n"
        result = tx.run(query, properties_list=properties_list)
        return [record['n'] for record in result]

    def get_node(self, label, id_value, id_key="id"):
        with self._driver.session(database=self._database) as session:
            return session.execute_read(self._get_node, label, id_key, id_value)

    @staticmethod
    def _get_node(tx, label, id_key, id_value):
        query = f"MATCH (n:{label} {{{id_key}: $id_value}}) RETURN n"
        result = tx.run(query, id_value=id_value)
        single_result = result.single()
        print(f"single_result: {single_result}")
        if single_result is not None:
            return single_result[0]
        else:
            return None

    def delete_node(self, label, id_value, id_key="id"):
        with self._driver.session(database=self._database) as session:
            session.execute_write(self._delete_node, label, id_key, id_value)

    @staticmethod
    def _delete_node(tx, label, id_key, id_value):
        query = f"MATCH (n:{label} {{{id_key}: $id_value}}) DETACH DELETE n"
        tx.run(query, id_value=id_value)

    def delete_nodes(self, label, id_values, id_key="id"):
        with self._driver.session(database=self._database) as session:
            session.execute_write(self._delete_nodes, label, id_key, id_values)

    @staticmethod
    def _delete_nodes(tx, label, id_key, id_values):
        query = f"UNWIND $id_values AS id_value MATCH (n:{label} {{{id_key}: id_value}}) DETACH DELETE n"
        tx.run(query, id_values=id_values)

    def upsert_relationship(self, start_node_label, start_node_id_value,
                            end_node_label, end_node_id_value, rel_type,
                            properties, upsert_nodes=True, start_node_id_key="id", end_node_id_key="id"):
        with self._driver.session(database=self._database) as session:
            return session.execute_write(self._upsert_relationship, start_node_label, start_node_id_key,
                                         start_node_id_value, end_node_label, end_node_id_key,
                                         end_node_id_value, rel_type, properties, upsert_nodes)

    @staticmethod
    def _upsert_relationship(tx, start_node_label, start_node_id_key, start_node_id_value,
                             end_node_label, end_node_id_key, end_node_id_value,
                             rel_type, properties, upsert_nodes):
        if upsert_nodes:
            query = (
                f"MERGE (a:{start_node_label} {{{start_node_id_key}: $start_node_id_value}}) "
                f"MERGE (b:{end_node_label} {{{end_node_id_key}: $end_node_id_value}}) "
                f"MERGE (a)-[r:{rel_type}]->(b) SET r += $properties RETURN r"
            )
        else:
            query = (
                f"MATCH (a:{start_node_label} {{{start_node_id_key}: $start_node_id_value}}), "
                f"(b:{end_node_label} {{{end_node_id_key}: $end_node_id_value}}) "
                f"MERGE (a)-[r:{rel_type}]->(b) SET r += $properties RETURN r"
            )
        result = tx.run(query, start_node_id_value=start_node_id_value,
                        end_node_id_value=end_node_id_value, properties=properties)
        return result.single()[0]

    def upsert_relationships(self, start_node_label, end_node_label, rel_type, relations,
                             upsert_nodes=True, start_node_id_key="id", end_node_id_key="id"):
        with self._driver.session(database=self._database) as session:
            return session.execute_write(self._upsert_relationships, relations, start_node_label,
                                         start_node_id_key, end_node_label, end_node_id_key, rel_type, upsert_nodes)

    @staticmethod
    def _upsert_relationships(tx, relations, start_node_label, start_node_id_key,
                              end_node_label, end_node_id_key, rel_type, upsert_nodes):

        if upsert_nodes:
            query = (
                "UNWIND $relations AS relationship "
                f"MERGE (a:{start_node_label} {{{start_node_id_key}: relationship.start_node_id}}) "
                f"MERGE (b:{end_node_label} {{{end_node_id_key}: relationship.end_node_id}}) "
                f"MERGE (a)-[r:{rel_type}]->(b) SET r += relationship.properties RETURN r"
            )
        else:
            query = (
                "UNWIND $relations AS relationship "
                f"MATCH (a:{start_node_label} {{{start_node_id_key}: relationship.start_node_id}}) "
                f"MATCH (b:{end_node_label} {{{end_node_id_key}: relationship.end_node_id}}) "
                f"MERGE (a)-[r:{rel_type}]->(b) SET r += relationship.properties RETURN r"
            )

        result = tx.run(query, relations=relations,
                        start_node_label=start_node_label, start_node_id_key=start_node_id_key,
                        end_node_label=end_node_label, end_node_id_key=end_node_id_key,
                        rel_type=rel_type)
        return [record['r'] for record in result]

    def delete_relationship(self, start_node_label, start_node_id_value,
                            end_node_label, end_node_id_value, rel_type,
                            start_node_id_key="id", end_node_id_key="id"):
        with self._driver.session(database=self._database) as session:
            session.execute_write(self._delete_relationship, start_node_label, start_node_id_key,
                                  start_node_id_value, end_node_label, end_node_id_key,
                                  end_node_id_value, rel_type)

    @staticmethod
    def _delete_relationship(tx, start_node_label, start_node_id_key, start_node_id_value,
                             end_node_label, end_node_id_key, end_node_id_value, rel_type):
        query = (
            f"MATCH (a:{start_node_label} {{{start_node_id_key}: $start_node_id_value}})-[r:{rel_type}]->"
            f"(b:{end_node_label} {{{end_node_id_key}: $end_node_id_value}}) DELETE r"
        )
        tx.run(query, start_node_id_value=start_node_id_value, end_node_id_value=end_node_id_value)

    def delete_relationships(self, start_node_label, start_node_id_values,
                             end_node_label, end_node_id_values, rel_type,
                             start_node_id_key="id", end_node_id_key="id"):
        with self._driver.session(database=self._database) as session:
            session.execute_write(self._delete_relationships,
                                  start_node_label, start_node_id_key, start_node_id_values,
                                  end_node_label, end_node_id_key, end_node_id_values, rel_type)

    @staticmethod
    def _delete_relationships(tx, start_node_label, start_node_id_key, start_node_id_values,
                              end_node_label, end_node_id_key, end_node_id_values, rel_type):
        query = (
            "UNWIND $start_node_id_values AS start_node_id_value "
            "UNWIND $end_node_id_values AS end_node_id_value "
            f"MATCH (a:{start_node_label} {{{start_node_id_key}: start_node_id_value}})-[r:{rel_type}]->"
            f"(b:{end_node_label} {{{end_node_id_key}: end_node_id_value}}) DELETE r"
        )
        tx.run(query, start_node_id_values=start_node_id_values, end_node_id_values=end_node_id_values)

    def _to_snake_case(self, name):
        import re
        words = re.findall("[A-Za-z][a-z0-9]*", name)
        result = "_".join(words).lower()
        return result

    def _create_vector_index_name(self, label, property_key):
        name = f"{label}_{property_key}_vector_index"
        name = self._to_snake_case(name)
        return "_" + name

    def _create_vector_field_name(self, property_key):
        name = f"{property_key}_vector"
        name = self._to_snake_case(name)
        return "_" + name

    def create_index(self, label, property_key, index_name=None):
        with self._driver.session(database=self._database) as session:
            session.execute_write(self._create_index, label, property_key, index_name)

    @staticmethod
    def _create_index(tx, label, property_key, index_name):
        if index_name is None:
            query = f"CREATE INDEX IF NOT EXISTS FOR (n:{label}) ON (n.{property_key})"
        else:
            query = f"CREATE INDEX {index_name} IF NOT EXISTS FOR (n:{label}) ON (n.{property_key})"
        tx.run(query)

    def create_vector_index(self, label, property_key, index_name=None,
                            vector_dimensions=1536, metric_type="cosine"):
        if index_name is None:
            index_name = self._create_vector_index_name(label, property_key)
        if not property_key.lower().endswith("vector"):
            property_key = self._create_vector_field_name(property_key)
        with self._driver.session(database=self._database) as session:
            session.execute_write(self._create_vector_index, label, property_key, index_name,
                                  vector_dimensions, metric_type)

    @staticmethod
    def _create_vector_index(tx, label, property_key, index_name, vector_dimensions, metric_type):
        query = (
            f"CREATE VECTOR INDEX $index_name IF NOT EXISTS FOR (n:{label}) ON (n.{property_key})"
            "OPTIONS { indexConfig: {"
            "  `vector.dimensions`: $vector_dimensions,"
            "  `vector.similarity_function`: $metric_type"
            "}}"
        )
        tx.run(query, index_name=index_name, vector_dimensions=vector_dimensions, metric_type=metric_type)

    def refresh_vector_index_meta(self, force=False):
        import time
        if not force and time.time() - self._vec_meta_ts < self._vec_meta_timeout:
            return
        def do_refresh_vector_index_meta(tx):
            query = "SHOW VECTOR INDEX"
            res = tx.run(query)
            data = res.data()
            meta = dict()
            for record in data:
                if record["entityType"] == "NODE":
                    label, = record["labelsOrTypes"]
                    vector_field, = record["properties"]
                    if label not in meta:
                        meta[label] = []
                    meta[label].append(vector_field)
            self._vec_meta = meta
            self._vec_meta_ts = time.time()
        with self._driver.session(database=self._database) as session:
            return session.execute_read(do_refresh_vector_index_meta)

    def delete_index(self, index_name):
        with self._driver.session(database=self._database) as session:
            session.execute_write(self._delete_index, index_name)

    @staticmethod
    def _delete_index(tx, index_name):
        query = f"DROP INDEX {index_name} IF EXISTS"
        tx.run(query)

    def execute_pagerank(self, iterations=20, damping_factor=0.85):
        with self._driver.session(database=self._database) as session:
            return session.execute_write(self._execute_pagerank, iterations, damping_factor)

    @staticmethod
    def _execute_pagerank(tx, iterations, damping_factor):
        query = (
            "CALL algo.pageRank.stream("
            "{iterations: $iterations, dampingFactor: $damping_factor}) "
            "YIELD nodeId, score "
            "RETURN algo.getNodeById(nodeId) AS node, score "
            "ORDER BY score DESC"
        )
        result = tx.run(query, iterations=iterations, damping_factor=damping_factor)
        return [{"node": record["node"], "score": record["score"]} for record in result]


# Usage example:
if __name__ == "__main__":
    neo4j_client = Neo4jClient(uri="neo4j://localhost:7687", user="neo4j", password="andy_test", database="neo4j")

    # Add or update single node
    node = neo4j_client.upsert_node("Person", {"id": 1, "name": "Alice", "age": 30})
    print(f"Upserted Node: {node}")

    # Add multiple nodes
    nodes = neo4j_client.upsert_nodes("Person", [
        {"id": 2, "name": "Bob", "age": 24},
        {"id": 3, "name": "Charlie", "age": 28}
    ])
    print(f"Added Nodes: {nodes}")

    # Add or update single relationship
    relationship = neo4j_client.upsert_relationship("Person", 1, "Person", 2, "KNOWS", {"since": 2020})
    print(f"Upserted Relationship: {relationship}")

    # Add multiple relationships
    relationships = neo4j_client.upsert_relationships("Person", "Person", "FRIEND", [
        {"start_node_id": 1, "end_node_id": 3, "properties": {"since": 2021}},
        {"start_node_id": 2, "end_node_id": 3, "properties": {"since": 2019}}
    ])
    print(f"Added Relationships: {relationships}")

    # Get node
    node_fetched = neo4j_client.get_node("Person", 1)
    print(f"Fetched Node: {node_fetched}")

    # Create vector index
    neo4j_client.create_vector_index("Person", "name")
    neo4j_client.refresh_vector_index_meta(force=True)
    print(neo4j_client._vec_meta)

    # Delete node
    neo4j_client.delete_node("Person", 1)
    print(f"Deleted Node with id: 1")

    # Delete relationship
    neo4j_client.delete_relationship("Person", 2, "Person", 3, "FRIEND")
    print(f"Deleted Relationship between ids 2 and 3")

    # Create index
    # neo4j_client.create_index("Person", "name")

    # Execute PageRank
    # pagerank_results = neo4j_client.execute_pagerank()
    # print(f"PageRank Results: {pagerank_results}")

    # Close the connection
    neo4j_client.close()
