import requests as r

print(r.post("http://127.0.0.1:8007/query",
             json={
                 "service": "vr",
                 "text": "На выходных, будут играть все члены семьи",
                 "source": "string",
                 "chat_id": "string"
             }).json())
