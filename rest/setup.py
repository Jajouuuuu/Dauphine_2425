from domain.adapter.generator_controller_adapter import GeneratorControllerAdapter
from domain.service.text_generation_service import TextGenerationService

from infrastructure.adapter.text_generator_adapter import TextGeneratorAdapter

from rest.endpoint.generator_rest_adapter import GeneratorRestAdapter

from infrastructure.historic.historic_repository import JsonHistoricRepository
from domain.service.historic_service import HistoricService

def create_generator_rest_adapter():
    text_generator_adapter = TextGeneratorAdapter()
    historic_repository = JsonHistoricRepository("historic.json")
    historic_service = HistoricService(historic_repository)
    text_generation_service = TextGenerationService(text_generator_adapter, historic_service)
    generator_controller_adapter = GeneratorControllerAdapter(text_generation_service)
    return GeneratorRestAdapter(generator_controller_adapter)
