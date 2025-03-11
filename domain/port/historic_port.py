from abc import ABC, abstractmethod
from domain.model.historic import Historic

class HistoricRepository(ABC):
    @abstractmethod
    def save(self, historic: Historic):
        pass

    @abstractmethod
    def get(self, id: int) -> Historic:
        pass