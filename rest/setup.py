from config.env_config import EnvConfig

from domain.port.impl.generator_controller_adapter import GeneratorControllerAdapter
from domain.service.text_generation_service import TextGenerationService
from domain.service.system_prompt_service import SystemPromptService
from domain.service.chat_history_service import ChatHistoryService
from domain.service.historic_service import HistoricService

from infrastructure.text_generator.cohere_text_generator import CohereTextGenerator
from infrastructure.history.json_history_repository import JsonHistoryRepository

from rest.endpoint.generator_rest_adapter import GeneratorRestAdapter

def setup_generator_dependencies() -> GeneratorRestAdapter:
    """
    Sets up the dependencies for the generator endpoint.
    """
    cohere_api_key = EnvConfig.get_cohere_api_key()
    json_history_repository_path = EnvConfig.get_json_history_repository()
    
    text_generator = CohereTextGenerator(cohere_api_key)
    chat_history_repository = JsonHistoryRepository(json_history_repository_path)
    
    system_prompt_service = SystemPromptService(text_generator)
    
    historic_service = HistoricService(chat_history_repository)
    
    chat_history_service = ChatHistoryService(chat_history_repository)
    
    text_generation_service = TextGenerationService(
        text_generator,
        historic_service
    )
    
    generator_controller_adapter = GeneratorControllerAdapter(text_generation_service, chat_history_service)
    return GeneratorRestAdapter(generator_controller_adapter)

# Alias to maintain backward compatibility with rest.api import
create_generator_rest_adapter = setup_generator_dependencies



