import time


from db import db_session
from db.message import Message



class OldsaratovService:
    def __init__(self, llm):
        self.llm = llm

    def ask(self, service: str, text: str, source: str, chat_id: str):
        result = self.llm.invoke(service, text, source, chat_id)
        self.__add_answer(result, service, text, source, chat_id)
        return {"answer": result}

    def __add_answer(self, result: str, service: str, text: str, source: str, chat_id: str) -> None:
        session = db_session.create_session()
        now_time = time.time()
        msg_1 = Message(source=source, chat_id=chat_id, entity="user", text=text, time=now_time, type_bot=service)
        msg_2 = Message(source=source, chat_id=chat_id, entity="ai", text=result, time=now_time + 10e-9,
                        type_bot=service)
        session.add(msg_1)
        session.add(msg_2)
        session.commit()
        session.close()
