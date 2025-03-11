from domain.port.historic_port import HistoricRepository
from domain.model.historic import Historic

class HistoricService:
    def __init__(self, historic_repository: HistoricRepository):
        self.historic_repository = historic_repository

    def add_message(self, message: str):
        historic = self.historic_repository.get(1) 
        historic.add_message(message)
        self.historic_repository.save(historic)

    def get_historic(self) -> list:
        historic = self.historic_repository.get(1) 
        return historic.list_message
