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