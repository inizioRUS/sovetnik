class AskService:
    def __init__(self, services):
        self.list_of_service = services

    def ask(self, service: str, text: str, source: str, chat_id: str) -> str:
        return self.list_of_service[service].ask(service, text, source, chat_id)
