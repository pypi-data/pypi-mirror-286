import json
from typing import Dict

from knext.builder.auto_extract.base import Extractor
from knext.builder.auto_extract.common.llm_client import LLMClient
from knext.builder.operator import PromptOp


class OpenIENERPrompt(PromptOp):
    template_query = """
    Please extract all named entities that are important for solving the questions below.
    Place the named entities in json format.
    """
    template_paragraph = """
    Your task is to extract named entities from the given paragraph. 
    Respond with a JSON list of entities.
    """
    example_query = """
    Input: Which magazine was started first Arthur's Magazine or First for Women?
    Output: {"named_entities": ["First for Women", "Arthur's Magazine"]}
    """
    example_paragraph = """
    Input: Radio City
    Radio City is India's first private FM radio station and was started on 3 July 2001.
    It plays Hindi, English and regional songs.
    Radio City recently forayed into New Media in May 2008 with the launch of a music portal - PlanetRadiocity.com that offers music related news, videos, songs, and other music-related features.

    Output: {"named_entities": ["Radio City", "India", "3 July 2001", "Hindi", "English", "May 2008", "PlanetRadiocity.com"]}
    """


    def __init__(self, **kwargs):
        super().__init__()
        input_type = kwargs.get("input_type", "query")
        with_example = kwargs.get("with_example", True)
        self.template = self.template_query if input_type == "query" else self.template_paragraph
        if with_example:
            self.example = self.example_query if input_type == "query" else self.example_paragraph

    def build_prompt(self, variables: Dict[str, str]) -> str:
        instruction = json.dumps(
            {
                "instruction": self.template,
                "example": self.example,
                "input": variables.get("input"),
            },
            ensure_ascii=False,
        )
        return instruction

    def parse_response(self, response: str, **kwargs):
        if isinstance(response, str):
            response = json.loads(response)
        if isinstance(response, dict):
            assert 'named_entities' in response
            return response['named_entities']
        elif isinstance(response, list):
            return response
        else:
            return []


class OpenIETriplePrompt(PromptOp):
    template = """
    Your task is to construct an RDF (Resource Description Framework) graph from the given passages and named entity lists. 
    Respond with a JSON list of triples, with each triple representing a relationship in the RDF graph. 
    
    Pay attention to the following requirements:
    - Each triple should contain at least one, but preferably two, of the named entities in the list for each passage.
    - Clearly resolve pronouns to their specific names to maintain clarity.
    """
    example = """
    Convert the paragraph into a JSON dict, it has a named entity list and a triple list.
    input:
    ```
    Radio City
    Radio City is India's first private FM radio station and was started on 3 July 2001.
    It plays Hindi, English and regional songs.
    Radio City recently forayed into New Media in May 2008 with the launch of a music portal - PlanetRadiocity.com that offers music related news, videos, songs, and other music-related features.
    ```
    
    named_entity_json: {"named_entities":
        ["Radio City", "India", "3 July 2001", "Hindi", "English", "May 2008", "PlanetRadiocity.com"]
    }
    output: {"triples": [
                ["Radio City", "located in", "India"],
                ["Radio City", "is", "private FM radio station"],
                ["Radio City", "started on", "3 July 2001"],
                ["Radio City", "plays songs in", "Hindi"],
                ["Radio City", "plays songs in", "English"]
                ["Radio City", "forayed into", "New Media"],
                ["Radio City", "launched", "PlanetRadiocity.com"],
                ["PlanetRadiocity.com", "launched in", "May 2008"],
                ["PlanetRadiocity.com", "is", "music portal"],
                ["PlanetRadiocity.com", "offers", "news"],
                ["PlanetRadiocity.com", "offers", "videos"],
                ["PlanetRadiocity.com", "offers", "songs"]
        ]
    }
    """

    def __init__(self, **kwargs):
        super().__init__()
        language = kwargs.get("language", "zh")
        with_example = kwargs.get("with_example", True)

    def build_prompt(self, variables: Dict[str, str]) -> str:
        instruction = json.dumps(
            {
                "instruction": self.template,
                "named_entity_json": variables.get("named_entity_json"),
                "example": self.example,
                "input": variables.get("input"),
            },
            ensure_ascii=False,
        )
        return instruction

    def parse_response(self, response: str, **kwargs):
        if isinstance(response, str):
            response = json.loads(response)
        if isinstance(response, dict):
            assert 'triples' in response
            return response['triples']
        elif isinstance(response, list):
            return response
        else:
            return []


class OpenIEExtractor(Extractor):

    def __init__(self, model="gpt3_5"):
        self.client = LLMClient.from_config_name(model)
        self.ner_op = OpenIENERPrompt(input_type="paragraph", with_example=True)
        self.triple_op = OpenIETriplePrompt()

    def named_entity_recognition(self, passage: str):
        doc_entities = self.client.invoke({"input": passage}, self.ner_op)
        return doc_entities

    def openie_post_ner_extract(self, passage: str, entities: list):
        named_entity_json = {"named_entities": entities}
        triples = self.client.invoke({"input": passage, "named_entity_json": json.dumps(named_entity_json)}, self.triple_op)
        return triples

    def invoke(self, document):
        idx = document["idx"]
        passage = document["passage"]
        entities = self.named_entity_recognition(passage)
        triples = self.openie_post_ner_extract(passage, entities)
        return idx, triples

    def batch(self, texts):
        triples = []
        for text in texts:
            triples.extend(self.invoke(text))
        return triples
