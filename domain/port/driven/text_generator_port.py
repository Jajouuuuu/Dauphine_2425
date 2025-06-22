from abc import ABC, abstractmethod

from domain.model.chat_history import ChatHistory

class TextGeneratorPort(ABC):
    @abstractmethod
    def get_generated_text(self, chat_history: ChatHistory) -> str:
        pass

    @abstractmethod
    def generate_text(self, prompt: str) -> str:
        """
        Génère une réponse directement à partir d'un prompt texte.
        """
        pass