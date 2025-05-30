from abc import ABC, abstractmethod
from typing import List, Optional
from domain.model.media_item import MediaItem

class RAGService(ABC):
    @abstractmethod
    def query_with_text(self, query: str) -> str:
        """Process a text query using RAG and return a response"""
        pass

    @abstractmethod
    def query_with_image(self, image_url: str) -> str:
        """Process an image query using RAG and return a response"""
        pass

    @abstractmethod
    def get_relevant_context(self, query: str) -> List[MediaItem]:
        """Get relevant media items for a given query"""
        pass 