from fastapi import FastAPI
from pydantic import BaseModel
from llama_index.llms.ollama import Ollama

from askservice import AskService
from llm.llm_aggregate import LLMAggregate
from pipelines.sibintek import SibintekService
from pipelines.vr import VRService
from pipelines.juridical import JuridicalService
from db import db_session


class QueryBody(BaseModel):
    service: str
    text: str
    source: str
    chat_id: str


class QueryBody_sib(BaseModel):
    text: str


llm = LLMAggregate(Ollama(
    base_url="http://localhost:11434",
    model="llama3.1:8b",
    temperature=0,
    context_window=100000,
    request_timeout=120,
    additional_kwargs={
        "num_predict": 1024,
        "repeat_penalty": 1.2
    }
))

app = FastAPI()
sib = SibintekService(llm)
sevises = {"vr": VRService(llm), "juridical": JuridicalService(llm)}
askservice = AskService(sevises)
db_session.global_init("db/data.sqlite")


@app.post("/query")
async def query(queryBody: QueryBody):
    return askservice.ask(queryBody.service, queryBody.text, queryBody.source, queryBody.chat_id)


@app.post("/query_sib")
async def query_sib(queryBody: QueryBody_sib):
    return sib.ask(queryBody.text)
