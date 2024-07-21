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
import hashlib
import json
from typing import Dict, List, Type

from knext.builder.operator.spg_record import SPGRecord
from knext.schema.model.base import BaseSpgType, ConstraintTypeEnum, SpgTypeEnum


class Node(object):
    id: str
    name: str
    label: str
    properties: Dict[str, str]
    hash_map: Dict[int, str] = dict()

    def __init__(self, _id: str, name: str, label: str, properties: Dict[str, str]):
        self.name = name
        self.label = label
        self.properties = properties
        self.id = _id

    @classmethod
    def from_spg_record(cls, idx, spg_record: SPGRecord):
        return cls(
            _id=idx,
            name=spg_record.get_property("name"),
            label=spg_record.spg_type_name,
            properties=spg_record.properties,
        )

    @staticmethod
    def unique_key(spg_record):
        return spg_record.spg_type_name + '_' + spg_record.get_property("name", "")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "label": self.label,
            "properties": self.properties,
        }


class Edge(object):
    id: str
    from_id: str
    from_type: str
    to_id: str
    to_type: str
    label: str
    properties: Dict[str, str]

    def __init__(
            self, _id: str, from_node: Node, to_node: Node, label: str, properties: Dict[str, str]
    ):
        self.from_id = from_node.id
        self.from_type = from_node.label
        self.to_id = to_node.id
        self.to_type = to_node.label
        self.label = label
        self.properties = properties
        if not _id:
            _id = id(self)
        self.id = _id

    @classmethod
    def from_spg_record(
            cls, s_idx, subject_record: SPGRecord, o_idx, object_record: SPGRecord, label: str
    ):
        from_node = Node.from_spg_record(s_idx, subject_record)
        to_node = Node.from_spg_record(o_idx, object_record)

        return cls(_id="", from_node=from_node, to_node=to_node, label=label, properties={})

    def to_dict(self):
        return {
            "id": self.id,
            "from": self.from_id,
            "to": self.to_id,
            "fromType": self.from_type,
            "toType": self.to_type,
            "label": self.label,
            "properties": self.properties,
        }


class SubGraph(object):
    nodes: List[Node] = list()
    edges: List[Edge] = list()

    def __init__(self, nodes: List[Node], edges: List[Edge]):
        self.nodes = nodes
        self.edges = edges

    def to_dict(self):
        return {
            "resultNodes": [n.to_dict() for n in self.nodes],
            "resultEdges": [e.to_dict() for e in self.edges],
        }

    def update(self, sub_graph: Type['SubGraph']):
        self.nodes.extend(sub_graph.nodes)
        self.edges.extend(sub_graph.edges)

    @staticmethod
    def filter_record(spg_record: SPGRecord, spg_type: BaseSpgType):

        filtered_properties, filtered_relations = {}, {}
        for prop_name, prop_value in spg_record.properties.items():
            if prop_value != 'NAN':
                filtered_properties[prop_name] = prop_value
        for rel_name, rel_value in spg_record.relations.items():
            if rel_value != 'NAN':
                filtered_relations[rel_name] = rel_value
        spg_record.properties = filtered_properties
        spg_record.relations = filtered_relations

        # if len(spg_record.properties) == 1 and spg_record.get_property("name"):
        #     print("filtered_entity: ")
        #     print(spg_record)
        #     return None
        if spg_type.spg_type_enum == SpgTypeEnum.Event and \
                (spg_type.properties.get('subject') and not spg_record.properties.get('subject')) and \
                (spg_type.properties.get('object') and not spg_record.properties.get('object')) and \
                (spg_type.properties.get('eventTime') and not spg_record.properties.get('eventTime')):
            print("filtered_event: ")
            print(spg_record)
            return None
        else:
            return spg_record

    @staticmethod
    def filter_node(nodes: List[Node], edges: List[Edge]):
        ids = []
        filtered_nodes = []
        for edge in edges:
            ids.extend([edge.from_id, edge.to_id])
        for node in nodes:
            if len(node.properties) == 1 and node.properties.get("name"):
                if node.id not in ids:
                    print("filtered_node: ")
                    print(node)
                    continue
            filtered_nodes.append(node)
        return filtered_nodes

    @staticmethod
    def generate_hash_id(value):
        m = hashlib.md5()
        m.update(value.encode('utf-8'))
        md5_hex = m.hexdigest()
        decimal_value = int(md5_hex, 16)
        return int(str(decimal_value)[:10])

    @classmethod
    def from_spg_record(
            cls, spg_types: Dict[str, BaseSpgType], spg_records: List[SPGRecord]
    ):
        #TODO, 此处硬编码需要更改
        spg_types_zh = {}
        for key, value in spg_types.items():
            spg_types_zh[value.name_zh] = value
        nodes, edges = set(), set()
        filtered_records = []
        for subject_record in spg_records:
            spg_type_name = subject_record.spg_type_name
            spg_type = spg_types.get(spg_type_name)
            # TODO, 此处硬编码需要更改
            if not spg_type:
                spg_type = spg_types_zh.get(spg_type_name)
                if spg_type is None:
                    print("-"*80)
                    print(subject_record)
            filtered_record = cls.filter_record(subject_record, spg_type)
            if filtered_record:
                filtered_records.append(filtered_record)
        for subject_record in filtered_records:
            idx = cls.generate_hash_id(f"{subject_record.spg_type_name}#{subject_record.get_property('name')}")
            from_node = Node.from_spg_record(idx, subject_record)
            spg_type_name = subject_record.spg_type_name
            spg_type = spg_types.get(spg_type_name)
            # TODO, 此处硬编码需要更改
            if not spg_type:
                spg_type = spg_types_zh.get(spg_type_name)
            removed_props = []
            for prop_name, prop_value in subject_record.properties.items():
                prop = spg_type.properties.get(prop_name)
                if not prop:
                    continue
                object_type_name = prop.object_type_name
                prop_value_list, info_dict = [], {}
                if object_type_name not in ["Text", "Integer", "Float"] or prop.constraint.get(ConstraintTypeEnum.MultiValue):
                    prop_value_list = prop_value.split(",")
                elif prop_name == "basicInfo":
                    info_dict.update(json.loads(prop_value))
                elif prop_name == "otherInfo":
                    info_dict.update(json.loads(prop_value))
                else:
                    prop_value_list = [prop_value]
                removed_values = []
                for value in prop_value_list:
                    for object_record in filtered_records:
                        o_idx = cls.generate_hash_id(f"{object_record.spg_type_name}#{object_record.get_property('name')}")
                        if (
                                object_record.spg_type_name == object_type_name
                                and (object_record.get_property("name") == value or value in object_record.get_property("additionalName", "").split(','))
                        ):
                            removed_values.append(value)
                            edge = Edge.from_spg_record(
                                idx, subject_record, o_idx, object_record, prop_name
                            )
                            edges.add(edge)
                if removed_values == prop_value_list:
                    removed_props.append(prop_name)
            for prop in removed_props:
                from_node.properties.pop(prop)
            nodes.add(from_node)

        nodes = cls.filter_node(list(nodes), list(edges))

        return cls(nodes=list(nodes), edges=list(edges))
