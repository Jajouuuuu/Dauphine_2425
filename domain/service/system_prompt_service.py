from domain.model.system_prompt import SystemPrompt
from domain.port.driven.text_generator_port import TextGeneratorPort


class SystemPromptService:
    def __init__(self,text_generator: TextGeneratorPort):
        # Initialisez le prompt par défaut
        self.system_prompt = SystemPrompt(
            content="You are an assistant, helping a user answering his questions"
        )
        self.text_generator = text_generator

    def get_system_prompt(self) -> str:
        return self.system_prompt.content

    def set_system_prompt(self, content: str):
        self.system_prompt.content = content