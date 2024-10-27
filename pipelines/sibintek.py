from dbMilvus import DbMilvus
from support_fun import make_emb


class SibintekService:
    def __init__(self, db: DbMilvus):
        self.db = db
        self.db.load("sibintek")
        self.db.load("sibintek_guide")

    def ask(self, text: str):
        config = {
            "collection_name": "sibintek",
            "data": [make_emb("query: " + text)],
            "limit": 3,
            "search_params": {"metric_type": "COSINE", "params": {}},
            "output_fields": ["id", "type", "ask_solve"]
        }
        res = self.db.search(
            config
        )



        answer = ""
        services = {}

        if res[0]['distance'] > 0.9:
            count = 1
            services[res[0]['entity']["type"]] = 1
        else:
            count = 3
            for i in res:
                if i['entity']["type"] not in services:
                    services[i['entity']["type"]] = 0
                services[i['entity']["type"]] += 1



        answer += f"Ваш запрос: {text}\n"

        answer += "Cервис(ы):\n"
        for i in services.keys():
            answer += f"{i} с вероятностью - {str(services[i] / count)}\n"





        answer += "Наиболее похожие запросы:\n"
        answer += f"{res[0]['id']} с метрикой подобия - {res[0]['distance']}\n"
        for i in res[1:]:
            if i['distance'] > 0.9:
                answer += f"{i['id']} с метрикой подобия - {i['distance']}\n"



        config = {
            "collection_name": "sibintek_guide",
            "data": [make_emb("query: " + text)],
            "limit": 1,
            "search_params": {"metric_type": "COSINE", "params": {}},
            "output_fields": ["filename"]
        }
        res = self.db.search(
            config
        )

        if res[0]['distance'] > 0.8:
            answer += f"Самый релевантный документ: {res[0]['entity']['filename']}\n"
        return answer
