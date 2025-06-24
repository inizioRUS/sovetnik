import requests as r



print(r.post("http://127.0.0.1:8000/query",
             json={
                 "service": "oldsaratov",
                 "text": "Расскажи про новые вагоны",
                 "source": "string",
                 "chat_id": "string1"
             }).json())

