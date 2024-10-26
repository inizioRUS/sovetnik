import json
from pymilvus import MilvusClient, Collection, connections

from llm.llm_aggregate import LLMAggregate
from support_fun import make_emb


class SibintekService:
    def __init__(self, llm: LLMAggregate):
        self.llm = llm
        connections.connect(
            alias="default",
            host='localhost',
            port='19530'
        )
        self.collection = Collection(name="sibintek")
        self.collection.load()
        self.client = MilvusClient(uri="http://localhost:19530")

    def ask(self, service: str, text: str, source: str, chat_id: str):
        res = self.client.search(
            collection_name="sibintek",
            data=[make_emb("query: " + text)],
            limit=5,
            search_params={"metric_type": "COSINE", "params": {}},
            output_fields=["id", "type", "ask_solve"]

        )
        result = json.dumps(res)
        return result
