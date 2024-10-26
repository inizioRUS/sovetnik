from llama_index.embeddings.huggingface import HuggingFaceEmbedding

embed_model = HuggingFaceEmbedding(model_name="intfloat/multilingual-e5-large")


def make_emb(text: str) -> list[float]:
    return embed_model.get_text_embedding(text)