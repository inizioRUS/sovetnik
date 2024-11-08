from typing import Type

from db import db_session
from db.message import Message
from .prompt import SYSTEM_PROMPTS
from llama_index.llms.ollama import Ollama
from openai import OpenAI
import json

SYSTEM_PROMPT_TEMPLATE = (
    "<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\n{}<|eot_id|>\n"
)
USER_PROMPT_TEMPLATE = "<|start_header_id|>user<|end_header_id|>\n\n{}<|eot_id|>\n"

ASSISTANT_PROMPT_TEMPLATE = "<|start_header_id|>assistant<|end_header_id|>\n\n{}<|eot_id|>\n"

ASSISTANT_PROMPT_TEMPLATE_END = "<|start_header_id|>assistant<|end_header_id|>\n\n"

MAX_PROMPT_TOKENS = 30000


class LLMAggregate:
    def __init__(self, llm: Ollama):
        self.client = OpenAI(
            api_key="sk-or-vv-3f0b8eb4592db2ae5a8d8f371b666de903a291f69f3f0acc45bdfc4df3dc0aff",
            base_url="https://api.vsegpt.ru/v1",
        )

        self.llm = llm

    def __get_data_of_chat(self, source: str, type: str, chat_id: str) -> list[Type[Message]]:
        session = db_session.create_session()
        messages = session.query(Message).filter(Message.chat_id == chat_id,
                                                 Message.source == source, Message.type_bot == type).all()
        messages = sorted(messages, key=lambda x: x.time)
        session.close()
        return messages

    def __build_model_prompt(self, prompts: list[Type[Message]], service: str) -> tuple[list[str], int]:
        final_prompt = [{"role": "system", "content": SYSTEM_PROMPTS[service]}]
        for prompt in prompts:
            if prompt.entity == 'user':
                final_prompt.append({"role": "user", "content": prompt.text})
            else:
                final_prompt.append({"role": "assistant", "content": prompt.text})
        return final_prompt

    def invoke(self, service: str, text: str, source: str, chat_id: str):
        prompts = self.__get_data_of_chat(source, service, chat_id)
        prompt = self.__build_model_prompt(prompts, service)
        prompt.append({"role": "user", "content": text})
        answer = self.flex(prompt)
        return answer

    def flex(self, messages):
        response_big = self.client.chat.completions.create(
            model="openai/gpt-4o-mini",
            messages=messages,
            temperature=0.1,
            n=1,
            max_tokens=3000
        )

        response = response_big.choices[0].message.content
        try:
            return json.loads(response)['tool_input']['text_answer']
        except Exception as e:
            try:
                return json.loads(response)['tool_input']['response']
            except Exception as e:
                return response
