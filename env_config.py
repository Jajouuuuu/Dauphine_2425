import os
from dotenv import load_dotenv

class EnvConfig:
    """Class to handle environment variables."""
    
    # Load environment variables once at the class level
    load_dotenv()
    _cohere_api_key = os.getenv("COHERE_API_KEY")
    _json_history_repository_path = os.getenv("JSON_HISTORY_REPOSITORY")
    _api_host = os.getenv("API_HOST", "127.0.0.1")
    _api_port = os.getenv("API_PORT", "8000")
    _api_url = f"http://{_api_host}:{_api_port}"

    @classmethod
    def get_cohere_api_key(cls) -> str:
        if not cls._cohere_api_key:
            raise ValueError("COHERE_API_KEY environment variable is not set.")
        return cls._cohere_api_key
    
    @classmethod
    def get_json_history_repository(cls) -> str:
        if not cls._json_history_repository_path:
            raise ValueError("JSON_HISTORY_REPOSITORY environment variable is not set.")
        return cls._json_history_repository_path
    
    @classmethod
    def get_api_host(cls) -> str:
        return cls._api_host

    @classmethod
    def get_api_port(cls) -> str:
        return cls._api_port
    
    @classmethod
    def get_api_port_int(cls) -> int:
        return int(cls._api_port)

    @classmethod
    def get_api_url(cls) -> str:
        return cls._api_url
    