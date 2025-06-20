from typing import List

from domain.model.chat_history import ChatHistory
from domain.port.driven.text_generator_port import TextGeneratorPort
from cohere import Client
from domain.model.role_message import RoleMessage
from config.env_config import EnvConfig

class CohereTextGenerator(TextGeneratorPort):
    """
    Adapter for Cohere API.
    """
    def __init__(self, api_key: str = None):
        """
        Initialize the Cohere client.
        If api_key is not provided, it will be fetched from environment variables.
        """
        self.api_key = api_key or EnvConfig.get_cohere_api_key()
        self.client = Client(self.api_key)
    
    def generate_text(self, prompt: str) -> str:
        """
        Generate text using Cohere's chat model.
        """
        response = self.client.chat(
            message=prompt,
        )
        return response.text
    
    def generate_text_with_history(self, prompt: str, history: list[RoleMessage]) -> str:
        """
        Generate text using Cohere's chat model with conversation history.
        """
        response = self.client.chat(
            message=prompt,
            chat_history=history
        )
        return response.text
    def get_generated_text(self, chat_history: ChatHistory) -> str:
        """
        Utilise l'historique de conversation pour générer une réponse via l'API Cohere.
        Le dernier message utilisateur est utilisé comme prompt, le reste est envoyé en contexte.
        """
        messages: List[RoleMessage] = chat_history.messages

        # On cherche le dernier message utilisateur comme prompt
        last_user_message = next(
            (m.message for m in reversed(messages) if m.role == "user"),
            ""
        )

        # Envoi de l'historique complet en contexte
        return self.generate_text_with_history(last_user_message, messages)

