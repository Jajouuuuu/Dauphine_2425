from abc import ABC, abstractmethod
from typing import List, Optional
from domain.model.media_item import MediaItem

class RAGService(ABC):
    """Port for RAG service operations following hexagonal architecture"""
    
    @abstractmethod
    def query_with_text(self, query: str, media_type: Optional[str] = None) -> str:
        """Process a text query using RAG and return a response
        
        Args:
            query: The text query to process
            media_type: Optional filter for media type ('movie', 'game', or None for all)
        
        Returns:
            The RAG response as a string
        """
        pass

    @abstractmethod
    def query_with_image(self, image_url: str, media_type: Optional[str] = None) -> str:
        """Process an image query using RAG and return a response
        
        Args:
            image_url: The URL or path to the image
            media_type: Optional filter for media type ('movie', 'game', or None for all)
        
        Returns:
            The RAG response as a string
        """
        pass

    @abstractmethod
    def get_relevant_context(self, query: str, media_type: Optional[str] = None) -> List[MediaItem]:
        """Get relevant media items for a given query
        
        Args:
            query: The search query
            media_type: Optional filter for media type ('movie', 'game', or None for all)
        
        Returns:
            List of relevant media items
        """
        pass 