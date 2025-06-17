import json
import pickle
from pathlib import Path
from typing import Any, Optional
from domain.port.file_storage import FileStoragePort

class FileStorageAdapter(FileStoragePort):
    """Concrete implementation of file storage following hexagonal architecture"""
    
    def __init__(self, base_path: str = "."):
        """Initialize the file storage adapter
        
        Args:
            base_path: Base directory for file operations
        """
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)
    
    def save_file(self, file_path: str, content: Any) -> bool:
        """Save content to a file
        
        Args:
            file_path: Path to the file
            content: Content to save
            
        Returns:
            True if successful, False otherwise
        """
        try:
            full_path = self.base_path / file_path
            full_path.parent.mkdir(parents=True, exist_ok=True)
            
            if file_path.endswith('.json'):
                with open(full_path, 'w', encoding='utf-8') as f:
                    json.dump(content, f, indent=2, ensure_ascii=False)
            elif file_path.endswith('.pkl'):
                with open(full_path, 'wb') as f:
                    pickle.dump(content, f)
            else:
                # Text file
                with open(full_path, 'w', encoding='utf-8') as f:
                    f.write(str(content))
            
            return True
        except Exception:
            return False
    
    def load_file(self, file_path: str) -> Optional[Any]:
        """Load content from a file
        
        Args:
            file_path: Path to the file
            
        Returns:
            File content or None if error
        """
        try:
            full_path = self.base_path / file_path
            
            if not full_path.exists():
                return None
                
            if file_path.endswith('.json'):
                with open(full_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            elif file_path.endswith('.pkl'):
                with open(full_path, 'rb') as f:
                    return pickle.load(f)
            else:
                # Text file
                with open(full_path, 'r', encoding='utf-8') as f:
                    return f.read()
                    
        except Exception:
            return None
    
    def delete_file(self, file_path: str) -> bool:
        """Delete a file
        
        Args:
            file_path: Path to the file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            full_path = self.base_path / file_path
            if full_path.exists():
                full_path.unlink()
                return True
            return False
        except Exception:
            return False
    
    def file_exists(self, file_path: str) -> bool:
        """Check if file exists
        
        Args:
            file_path: Path to the file
            
        Returns:
            True if file exists, False otherwise
        """
        full_path = self.base_path / file_path
        return full_path.exists() 