import cohere

from domain.model.chat_history import ChatHistory

from env_config import EnvConfig

def to_chat_messages(chat_history: ChatHistory) -> list[dict]:
    """Convertit l'historique de chat en une liste de dictionnaires avec le format attendu par Cohere."""   
    return [{"role": msg.role, "content": msg.message} for msg in chat_history.messages]

class CohereTextGenerator():
    def __init__(self):
        self.client = cohere.ClientV2(EnvConfig.get_cohere_api_key())

    def generate_text(self, chat_history: ChatHistory) -> str:
        # system_prompt = self.system_prompt_service.get_system_prompt()
        
        response = self.client.chat(
            model="command-r",
            messages=to_chat_messages(chat_history)
        )
        return response.message.content[0].text # Retourne le texte généré par Cohere