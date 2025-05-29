from abc import ABC, abstractmethod
from typing import List, Optional
from domain.model.media_item import MediaItem
import numpy as np

class MediaRepository(ABC):
    @abstractmethod
    def add_item(self, item: MediaItem) -> None:
        """Add a media item to the repository"""
        pass

    @abstractmethod
    def get_item_by_id(self, item_id: str) -> Optional[MediaItem]:
        """Retrieve a media item by its ID"""
        pass

    @abstractmethod
    def search_by_text_embedding(self, embedding: np.ndarray, limit: int = 5) -> List[MediaItem]:
        """Search media items by text embedding similarity"""
        pass

    @abstractmethod
    def search_by_image_embedding(self, embedding: np.ndarray, limit: int = 5) -> List[MediaItem]:
        """Search media items by image embedding similarity"""
        pass

    @abstractmethod
    def get_all_items(self) -> List[MediaItem]:
        """Get all media items"""
        pass 