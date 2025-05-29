from typing import List
import cohere
from domain.port.rag_service import RAGService
from domain.port.media_repository import MediaRepository
from domain.model.media_item import MediaItem
import numpy as np
from PIL import Image
import requests
from io import BytesIO
import os
from dotenv import load_dotenv

load_dotenv()

class RAGServiceImpl(RAGService):
    def __init__(self, media_repository: MediaRepository, embedding_model: str = "embed-english-v3.0"):
        self.media_repository = media_repository
        self.co = cohere.Client(os.getenv('COHERE_API_KEY'))
        self.embedding_model = embedding_model
        self.embedding_dim = 1024  # Cohere's embedding dimension

    def _get_text_embedding(self, text: str) -> np.ndarray:
        """Get text embedding using Cohere"""
        response = self.co.embed(
            texts=[text],
            model=self.embedding_model,
            input_type="search_query"
        )
        return np.array(response.embeddings[0])

    def _get_image_embedding(self, image_url: str) -> np.ndarray:
        """Get image embedding (placeholder - in real implementation, use CLIP or similar)"""
        # This is a placeholder. In a real implementation, you would:
        # 1. Load the image using PIL
        # 2. Use a vision model (like CLIP) to get embeddings
        # For now, we'll return a random embedding
        return np.random.rand(self.embedding_dim)

    def query_with_text(self, query: str) -> str:
        try:
            # Get query embedding
            query_embedding = self._get_text_embedding(query)
            
            # Get relevant context
            relevant_items = self.media_repository.search_by_text_embedding(query_embedding)
            
            # Prepare context for LLM
            context = "\n".join([
                f"Title: {item.title}\nType: {item.type}\nDescription: {item.description}\nYear: {item.release_year}\nGenres: {', '.join(item.genres)}\n"
                for item in relevant_items
            ])
            
            # Generate response using Cohere
            response = self.co.chat(
                message=query,
                preamble=f"You are an expert on movies and video games. Use the following context to answer the question. If the context doesn't contain relevant information, say so:\n{context}",
                temperature=0.7,
            )
            
            return response.text
        except Exception as e:
            return f"Error processing query: {str(e)}"

    def query_with_image(self, image_url: str, similarity_threshold: float = 0.7) -> str:
        try:
            # Get image embedding
            image_embedding = self._get_image_embedding(image_url)
            
            # Get relevant items
            relevant_items = self.media_repository.search_by_image_embedding(image_embedding)
            
            if not relevant_items:
                return "I couldn't find any matching or similar content for this image."
            
            # Get the most similar item (first in the list)
            best_match = relevant_items[0]
            
            # Prepare context for LLM
            context = "\n".join([
                f"Title: {item.title}\nType: {item.type}\nDescription: {item.description}\nYear: {item.release_year}\nGenres: {', '.join(item.genres)}\n"
                for item in relevant_items[:3]  # Use top 3 matches for context
            ])
            
            # Generate response using Cohere
            response = self.co.chat(
                message="Analyze these potential matches and explain how they relate to the uploaded image. Focus on visual similarities and thematic connections.",
                preamble=f"You are an expert on movies and video games. Based on an uploaded image, these are the most relevant matches found:\n{context}",
                temperature=0.7,
            )
            
            return response.text
        except Exception as e:
            return f"Error processing image: {str(e)}"

    def get_relevant_context(self, query: str) -> List[MediaItem]:
        query_embedding = self._get_text_embedding(query)
        return self.media_repository.search_by_text_embedding(query_embedding) 