import docx
import os

from pymilvus import MilvusClient
from tqdm import tqdm

from support_fun import token_count_emb, make_emb


def getText(filename):
    doc = docx.Document(filename)
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    return '\n'.join(fullText)


client = MilvusClient(uri="http://localhost:19530")
data = []
index = 0
for i in tqdm(os.listdir("docx_doc")):
    data.append(
        {"id": index, "filename": i, "guide_vector": make_emb("passage: " + getText("docx_doc/" + i))})
    index += 1
res = client.insert(
    collection_name="sibintek_guide",
    data=data)
