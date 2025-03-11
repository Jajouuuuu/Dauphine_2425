from abc import ABC, abstractmethod

class GeneratorControllerPort(ABC):
    @abstractmethod
    def generate_message(self, prompt: str) -> str:
        pass

    def display_historic(int: id):
        pass