from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from askservice import AskService
from llm.llm_aggregate_api import LLMAggregate
from pipelines.oldsaratov import OldsaratovService
from db import db_session

class QueryBody(BaseModel):
    service: str
    text: str
    source: str
    chat_id: str


class QueryBody_sib(BaseModel):
    text: str


llm = LLMAggregate(None)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)
sevises = { "oldsaratov": OldsaratovService(llm)}
askservice = AskService(sevises)
db_session.global_init("db/data.sqlite")


@app.post("/query")
async def query(queryBody: QueryBody):
    return askservice.ask(queryBody.service, queryBody.text, queryBody.source, queryBody.chat_id)
