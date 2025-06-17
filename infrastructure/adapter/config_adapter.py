import os
from typing import Any, Optional
from domain.port.config_provider import ConfigProviderPort

class ConfigAdapter(ConfigProviderPort):
    """Concrete implementation of configuration provider following hexagonal architecture"""
    
    def __init__(self):
        """Initialize the configuration adapter"""
        self._config_cache = {}
    
    def get_config(self, key: str) -> Optional[str]:
        """Get configuration value by key
        
        Args:
            key: Configuration key
            
        Returns:
            Configuration value or None if not found
        """
        # Check cache first
        if key in self._config_cache:
            return self._config_cache[key]
        
        # Try environment variable
        value = os.getenv(key)
        if value is not None:
            self._config_cache[key] = value
            
        return value
    
    def get_config_int(self, key: str, default: int = 0) -> int:
        """Get configuration value as integer
        
        Args:
            key: Configuration key
            default: Default value if not found or conversion fails
            
        Returns:
            Configuration value as integer
        """
        value = self.get_config(key)
        if value is None:
            return default
            
        try:
            return int(value)
        except (ValueError, TypeError):
            return default
    
    def get_config_bool(self, key: str, default: bool = False) -> bool:
        """Get configuration value as boolean
        
        Args:
            key: Configuration key
            default: Default value if not found or conversion fails
            
        Returns:
            Configuration value as boolean
        """
        value = self.get_config(key)
        if value is None:
            return default
            
        return value.lower() in ('true', '1', 'yes', 'on')
    
    def set_config(self, key: str, value: Any) -> None:
        """Set configuration value
        
        Args:
            key: Configuration key
            value: Configuration value
        """
        self._config_cache[key] = str(value) 