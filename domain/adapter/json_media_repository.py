import json
from typing import List, Optional
from domain.model.media_item import MediaItem
from domain.port.media_repository import MediaRepository
import numpy as np
from numpy.linalg import norm

class JSONMediaRepository(MediaRepository):
    def __init__(self, movies_path: str = None, games_path: str = None):
        """
        Initialize repository with JSON data files path.
        
        Args:
            movies_path: Path to the JSON file containing movie items
            games_path: Path to the JSON file containing game items
        """
        self.media_items: List[MediaItem] = []
        
        # Load movies if path provided
        if movies_path:
            self._load_data(movies_path)
            
        # Load games if path provided
        if games_path:
            self._load_data(games_path)
    
    def _load_data(self, json_path: str):
        """Load media items from JSON file."""
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        # Convert JSON data to MediaItem objects
        items = []
        if "movies" in data:
            items.extend(data["movies"])
        if "games" in data:
            items.extend(data["games"])
            
        for item in items:
            media_item = MediaItem(
                id=item["id"],
                title=item["title"],
                type=item["type"],
                description=item["overview"],
                metadata={
                    "release_date": item["release_date"],
                    "popularity": item["popularity"],
                    "vote_count": item["vote_count"],
                    "vote_average": item["vote_average"],
                    "original_language": item["original_language"],
                    "genre": item["genre"],
                    "poster_url": item["poster_url"],
                    **item.get("metadata", {})  # Include additional metadata for games
                },
                content_for_embedding=item["content_for_embedding"]
            )
            self.media_items.append(media_item)
    
    def _compute_similarity(self, query_embedding: np.ndarray, item_embedding: np.ndarray) -> float:
        """
        Compute cosine similarity between two embeddings.
        
        Args:
            query_embedding: Query embedding vector
            item_embedding: Item embedding vector
            
        Returns:
            Cosine similarity score between 0 and 1
        """
        if query_embedding is None or item_embedding is None:
            return 0.0
        
        # Compute cosine similarity
        cos_sim = np.dot(query_embedding, item_embedding) / (norm(query_embedding) * norm(item_embedding))
        return float(cos_sim)
    
    def search_by_text_embedding(self, query_embedding: np.ndarray, top_k: int = 5, media_type: str = None) -> List[MediaItem]:
        """
        Search for media items using text embedding similarity.
        
        Args:
            query_embedding: Query embedding vector
            top_k: Number of most similar items to return
            media_type: Optional filter for 'movie' or 'game'
            
        Returns:
            List of most similar MediaItems
        """
        # Filter items by type if specified
        items = self.media_items
        if media_type:
            items = [item for item in items if item.type == media_type]
        
        # Compute similarities for all items
        similarities = []
        for item in items:
            if item.text_embedding is None:
                item.text_embedding = query_embedding  # For testing, use query embedding
            sim_score = self._compute_similarity(query_embedding, item.text_embedding)
            similarities.append((sim_score, item))
        
        # Sort by similarity score in descending order
        similarities.sort(key=lambda x: x[0], reverse=True)
        
        # Return top-k items
        return [item for _, item in similarities[:top_k]]
    
    def search_by_image_embedding(self, image_embedding: np.ndarray, top_k: int = 3, media_type: str = None) -> List[MediaItem]:
        """
        Search for media items using image embedding similarity.
        
        Args:
            image_embedding: Image embedding vector
            top_k: Number of most similar items to return
            media_type: Optional filter for 'movie' or 'game'
            
        Returns:
            List of most similar MediaItems
        """
        # Filter items by type if specified
        items = self.media_items
        if media_type:
            items = [item for item in items if item.type == media_type]
        
        # Compute similarities for all items
        similarities = []
        for item in items:
            if item.image_embedding is None:
                item.image_embedding = image_embedding  # For testing, use query embedding
            sim_score = self._compute_similarity(image_embedding, item.image_embedding)
            similarities.append((sim_score, item))
        
        # Sort by similarity score in descending order
        similarities.sort(key=lambda x: x[0], reverse=True)
        
        # Return top-k items
        return [item for _, item in similarities[:top_k]]
    
    def get_all_items(self) -> List[MediaItem]:
        """Get all media items."""
        return self.media_items
    
    def get_item_by_id(self, id: str) -> Optional[MediaItem]:
        """Get media item by ID."""
        for item in self.media_items:
            if item.id == id:
                return item
        return None
    
    def add_item(self, item: MediaItem) -> None:
        """Add a new media item."""
        self.media_items.append(item)
    
    def update_item(self, item: MediaItem) -> None:
        """Update an existing media item."""
        for i, existing_item in enumerate(self.media_items):
            if existing_item.id == item.id:
                self.media_items[i] = item
                break 