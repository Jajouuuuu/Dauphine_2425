from domain.model.chat_history import ChatHistory
from domain.port.driven.text_generator_port import TextGeneratorPort

class TextGenerationService:
    def __init__(self, text_generator: TextGeneratorPort, historic_service: HistoricService):
        self.text_generator = text_generator
        self.historic_service = historic_service

    def get_generated_text(self, prompt: str) -> str:
        try:
            generated_text = self.text_generator.get_generated_text(prompt)
          
            self.historic_service.add_message(generated_text)
            return generated_text
        except Exception as e:
            print(f"Error in text generation or historic update: {e}")
            raise e

