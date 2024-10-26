from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from transformers import LlamaTokenizerFast

embed_model = HuggingFaceEmbedding(model_name="intfloat/multilingual-e5-large")
tokenizer = LlamaTokenizerFast.from_pretrained("hf-internal-testing/llama-tokenizer")


def make_emb(text: str) -> list[float]:
    return embed_model.get_text_embedding(text)

def token_count(text:str) -> int:
    return len(tokenizer.encode(text))