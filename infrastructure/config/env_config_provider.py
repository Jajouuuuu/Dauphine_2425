from typing import Any, Optional
import os
from dotenv import load_dotenv

from domain.port.config_provider import ConfigProviderPort


class EnvConfigProvider(ConfigProviderPort):
    """Environment-variable based configuration provider.

    Keeps infra code independent of the concrete .env loader; other providers
    (vault, AWS SSM, etc.) can implement the same port later without changing
    domain/application layers.
    """

    def __init__(self) -> None:
        # Ensure .env is loaded once
        load_dotenv()

    # ---------------------------------------------------------------------
    # Port implementation
    # ---------------------------------------------------------------------
    def get_config(self, key: str) -> Optional[str]:
        return os.getenv(key)

    def get_config_int(self, key: str, default: int = 0) -> int:
        value = os.getenv(key)
        try:
            return int(value) if value is not None else default
        except ValueError:
            return default

    def get_config_bool(self, key: str, default: bool = False) -> bool:
        value = os.getenv(key)
        if value is None:
            return default
        return value.lower() in {"1", "true", "yes", "on"}

    def set_config(self, key: str, value: Any) -> None:
        os.environ[key] = str(value) 