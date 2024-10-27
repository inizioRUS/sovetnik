from typing import List, Any, Type

from db import db_session
from db.message import Message
from .prompt import SYSTEM_PROMPTS
from llama_index.llms.ollama import Ollama
from llama_index.core import PromptTemplate
from transformers import LlamaTokenizerFast

SYSTEM_PROMPT_TEMPLATE = (
    "<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\n{}<|eot_id|>\n"
)
USER_PROMPT_TEMPLATE = "<|start_header_id|>user<|end_header_id|>\n\n{}<|eot_id|>\n"

ASSISTANT_PROMPT_TEMPLATE = "<|start_header_id|>assistant<|end_header_id|>\n\n{}<|eot_id|>\n"

ASSISTANT_PROMPT_TEMPLATE_END = "<|start_header_id|>assistant<|end_header_id|>\n\n"

MAX_PROMPT_TOKENS = 30000


class LLMAggregate:
    def __init__(self, llm: Ollama):
        self.llm = llm
        self._tokenizer = LlamaTokenizerFast.from_pretrained("hf-internal-testing/llama-tokenizer")

    def __get_data_of_chat(self, source: str, chat_id: str) -> list[Type[Message]]:
        session = db_session.create_session()
        messages = session.query(Message).filter(Message.chat_id == chat_id,
                                                 Message.source == source).all()
        messages = sorted(messages, key=lambda x: x.time)
        session.close()
        return messages

    def __build_model_prompt(self, prompts: list[Type[Message]], service: str) -> tuple[list[str], int]:
        final_prompt = [SYSTEM_PROMPT_TEMPLATE.format(SYSTEM_PROMPTS[service])]
        size = len(final_prompt[0])
        for prompt in prompts:
            if prompt.entity == 'user':
                final_prompt.append(USER_PROMPT_TEMPLATE.format(prompt.text))
            else:
                final_prompt.append(ASSISTANT_PROMPT_TEMPLATE.format(prompt.text))
            cur = len(self._tokenizer.encode(final_prompt[-1]))
            while size + cur > MAX_PROMPT_TOKENS:
                size -= len(self._tokenizer.encode(final_prompt.pop(1)))
            size += cur
        return final_prompt, size

    def invoke(self, service: str, text: str, source: str, chat_id: str):
        end = USER_PROMPT_TEMPLATE.format(text) + ASSISTANT_PROMPT_TEMPLATE_END
        cur = len(self._tokenizer.encode(end))
        prompts = self.__get_data_of_chat(source, chat_id)
        prompt, size = self.__build_model_prompt(prompts, service)
        while size + cur > MAX_PROMPT_TOKENS:
            size -= len(self._tokenizer.encode(prompt.pop(1)))
        prompt = "".join(prompt) + end
        answer = self.llm.predict(PromptTemplate(prompt))
        split_position = answer.rfind(ASSISTANT_PROMPT_TEMPLATE_END)
        if split_position >= 0:
            answer = answer[split_position + len(ASSISTANT_PROMPT_TEMPLATE_END):]
        return answer
