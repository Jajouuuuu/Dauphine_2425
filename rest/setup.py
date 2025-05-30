from env_config import EnvConfig

from domain.port.impl.generator_controller_adapter import GeneratorControllerAdapter
from domain.service.text_generation_service import TextGenerationService
from domain.service.system_prompt_service import SystemPromptService
from domain.service.chat_history_service import ChatHistoryService
from domain.service.historic_service import HistoricService

from infrastructure.adapter.infrastructure_adapter import InfrastructureAdapter
from infrastructure.history.json_history_repository import JsonHistoryRepository
from infrastructure.text_generator.cohere_text_generator import CohereTextGenerator

from rest.endpoint.generator_rest_adapter import GeneratorRestAdapter

def create_generator_rest_adapter():
    # Initialize persistence services
    cohere_text_generator = CohereTextGenerator()
    json_history_repository = JsonHistoryRepository(EnvConfig.get_json_history_repository())
    
    # Inject CohereTextGenerator into TextGeneratorAdapter
    infrastructure_adapter = InfrastructureAdapter(cohere_text_generator, json_history_repository)
    
    # Initialize services
    historic_service = HistoricService(json_history_repository)
    chat_history_service = ChatHistoryService(infrastructure_adapter)
    
    # Initialize text generation service with both required dependencies
    text_generation_service = TextGenerationService(
        text_generator=infrastructure_adapter,
        historic_service=historic_service
    )

    # Configure services and adapters
    generator_controller_adapter = GeneratorControllerAdapter(text_generation_service, chat_history_service)
    return GeneratorRestAdapter(generator_controller_adapter)



