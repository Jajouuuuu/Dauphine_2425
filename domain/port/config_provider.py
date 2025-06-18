from abc import ABC, abstractmethod
from typing import Any, Optional

class ConfigProviderPort(ABC):
    """Port for configuration management following hexagonal architecture"""
    
    @abstractmethod
    def get_config(self, key: str) -> Optional[str]:
        """Get configuration value by key"""
        pass
    
    @abstractmethod
    def get_config_int(self, key: str, default: int = 0) -> int:
        """Get configuration value as integer"""
        pass
    
    @abstractmethod
    def get_config_bool(self, key: str, default: bool = False) -> bool:
        """Get configuration value as boolean"""
        pass
    
    @abstractmethod
    def set_config(self, key: str, value: Any) -> None:
        """Set configuration value"""
        pass 