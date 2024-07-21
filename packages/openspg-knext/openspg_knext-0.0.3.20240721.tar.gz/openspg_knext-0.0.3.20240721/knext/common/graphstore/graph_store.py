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

from abc import ABC, abstractmethod


class GraphStore(ABC):

    @abstractmethod
    def close(self):
        pass

    @abstractmethod
    def initialize_schema(self, schema):
        pass

    @abstractmethod
    def upsert_node(self, label, properties, id_key="id"):
        pass

    @abstractmethod
    def upsert_nodes(self, label, properties_list, id_key="id"):
        pass

    @abstractmethod
    def get_node(self, label, id_value, id_key="id"):
        pass

    @abstractmethod
    def delete_node(self, label, id_value, id_key="id"):
        pass

    @abstractmethod
    def delete_nodes(self, label, id_values, id_key="id"):
        pass

    @abstractmethod
    def upsert_relationship(self, start_node_label, start_node_id_value,
                            end_node_label, end_node_id_value,
                            rel_type, properties, upsert_nodes=True,
                            start_node_id_key="id", end_node_id_key="id"):
        pass

    @abstractmethod
    def upsert_relationships(self, start_node_label, end_node_label, rel_type,
                             relationships, upsert_nodes=True, start_node_id_key="id",
                             end_node_id_key="id"):
        pass

    @abstractmethod
    def delete_relationship(self, start_node_label, start_node_id_value,
                            end_node_label, end_node_id_value,
                            rel_type, start_node_id_key="id", end_node_id_key="id"):
        pass

    @abstractmethod
    def delete_relationships(self, start_node_label, start_node_id_values,
                             end_node_label, end_node_id_values, rel_type,
                             start_node_id_key="id", end_node_id_key="id"):
        pass

    @abstractmethod
    def create_index(self, label, property_key, index_name=None):
        pass

    @abstractmethod
    def create_vector_index(self, label, property_key, index_name=None,
                            vector_dimensions=1536, metric_type="cosine"):
        pass

    @abstractmethod
    def delete_index(self, index_name):
        pass

    @abstractmethod
    def execute_pagerank(self, iterations=20, damping_factor=0.85):
        pass
