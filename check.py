import requests as r

print(r.post("http://127.0.0.1:8000/query",
             json={
                 "service": "juridical",
                 "text": "Привет!",
                 "source": "string",
                 "chat_id": "string"
             }))
