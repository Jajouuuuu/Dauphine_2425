from abc import ABC, abstractmethod
from typing import List, Optional
from domain.model.media_item import MediaItem
import numpy as np

class MediaRepository(ABC):
    """Port for media repository operations following hexagonal architecture"""
    
    @abstractmethod
    def add_item(self, item: MediaItem) -> None:
        """Add a media item to the repository
        
        Args:
            item: The media item to add
        """
        pass

    @abstractmethod
    def get_item_by_id(self, item_id: str) -> Optional[MediaItem]:
        """Retrieve a media item by its ID
        
        Args:
            item_id: The unique identifier of the media item
            
        Returns:
            The media item if found, None otherwise
        """
        pass

    @abstractmethod
    def search_by_text_embedding(self, embedding: np.ndarray, limit: int = 5, media_type: Optional[str] = None) -> List[MediaItem]:
        """Search media items by text embedding similarity
        
        Args:
            embedding: The text embedding to search with
            limit: Maximum number of results to return
            media_type: Optional filter for media type ('movie', 'game', or None for all)
            
        Returns:
            List of similar media items
        """
        pass

    @abstractmethod
    def search_by_image_embedding(self, embedding: np.ndarray, limit: int = 5, media_type: Optional[str] = None) -> List[MediaItem]:
        """Search media items by image embedding similarity
        
        Args:
            embedding: The image embedding to search with
            limit: Maximum number of results to return
            media_type: Optional filter for media type ('movie', 'game', or None for all)
            
        Returns:
            List of similar media items
        """
        pass

    @abstractmethod
    def get_all_items(self, media_type: Optional[str] = None) -> List[MediaItem]:
        """Get all media items
        
        Args:
            media_type: Optional filter for media type ('movie', 'game', or None for all)
            
        Returns:
            List of all media items matching the filter
        """
        pass 