from domain.model.chat_history import ChatHistory
from domain.port.driven.text_generator_port import TextGeneratorPort
from domain.service.historic_service import HistoricService
from typing import Union

class TextGenerationService:
    def __init__(self, text_generator: TextGeneratorPort, historic_service: HistoricService):
        self.text_generator = text_generator
        self.historic_service = historic_service

    def get_generated_text(self, input_text: Union[str, ChatHistory]) -> str:
        """Generate text response for either a string prompt or ChatHistory"""
        try:
            # If input is ChatHistory, extract the last message
            if isinstance(input_text, ChatHistory):
                prompt = input_text.messages[-1].message if input_text.messages else ""
            else:
                prompt = input_text

            generated_text = self.text_generator.get_generated_text(prompt)
            self.historic_service.add_message(generated_text)
            return generated_text
        except Exception as e:
            print(f"Error in text generation or historic update: {e}")
            raise e

