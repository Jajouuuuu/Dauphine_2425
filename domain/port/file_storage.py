from abc import ABC, abstractmethod
from typing import Any, Optional

class FileStoragePort(ABC):
    """Port for file storage operations following hexagonal architecture"""
    
    @abstractmethod
    def save_file(self, file_path: str, content: Any) -> bool:
        """Save content to a file"""
        pass
    
    @abstractmethod
    def load_file(self, file_path: str) -> Optional[Any]:
        """Load content from a file"""
        pass
    
    @abstractmethod
    def delete_file(self, file_path: str) -> bool:
        """Delete a file"""
        pass
    
    @abstractmethod
    def file_exists(self, file_path: str) -> bool:
        """Check if file exists"""
        pass 