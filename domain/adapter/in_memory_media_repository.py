from typing import List, Optional
import numpy as np
from domain.port.media_repository import MediaRepository
from domain.model.media_item import MediaItem

class InMemoryMediaRepository(MediaRepository):
    def __init__(self):
        self.items: List[MediaItem] = []
        self.embedding_dim = 1024  # Match Cohere's embedding dimension
        # Initialize with some synthetic data
        self._initialize_synthetic_data()

    def add_item(self, item: MediaItem) -> None:
        self.items.append(item)

    def get_item_by_id(self, item_id: str) -> Optional[MediaItem]:
        for item in self.items:
            if item.id == item_id:
                return item
        return None

    def search_by_text_embedding(self, embedding: np.ndarray, limit: int = 5) -> List[MediaItem]:
        # Compute cosine similarity between query embedding and all items
        similarities = []
        for item in self.items:
            if item.text_embedding is not None:
                try:
                    similarity = np.dot(embedding, item.text_embedding) / (
                        np.linalg.norm(embedding) * np.linalg.norm(item.text_embedding)
                    )
                    similarities.append((similarity, item))
                except Exception as e:
                    print(f"Error computing similarity: {e}")
                    continue
        
        # Sort by similarity and return top k items
        similarities.sort(key=lambda x: x[0], reverse=True)
        return [item for _, item in similarities[:limit]]

    def search_by_image_embedding(self, embedding: np.ndarray, limit: int = 5) -> List[MediaItem]:
        # Similar to text embedding search but using image embeddings
        similarities = []
        for item in self.items:
            if item.image_embedding is not None:
                try:
                    similarity = np.dot(embedding, item.image_embedding) / (
                        np.linalg.norm(embedding) * np.linalg.norm(item.image_embedding)
                    )
                    similarities.append((similarity, item))
                except Exception as e:
                    print(f"Error computing similarity: {e}")
                    continue
        
        similarities.sort(key=lambda x: x[0], reverse=True)
        return [item for _, item in similarities[:limit]]

    def get_all_items(self) -> List[MediaItem]:
        return self.items

    def _initialize_synthetic_data(self):
        # Add some synthetic movies and games
        synthetic_data = [
            {
                "id": "m1",
                "title": "The Matrix",
                "type": "movie",
                "description": "A computer programmer discovers a mysterious world of artificial reality.",
                "release_year": 1999,
                "genres": ["Sci-Fi", "Action"],
                "image_url": "https://example.com/matrix.jpg"
            },
            {
                "id": "m2",
                "title": "Inception",
                "type": "movie",
                "description": "A thief who enters the dreams of others to steal secrets.",
                "release_year": 2010,
                "genres": ["Sci-Fi", "Action", "Thriller"],
                "image_url": "https://example.com/inception.jpg"
            },
            {
                "id": "g1",
                "title": "The Last of Us",
                "type": "game",
                "description": "A post-apocalyptic action-adventure game about survival.",
                "release_year": 2013,
                "genres": ["Action", "Adventure", "Horror"],
                "image_url": "https://example.com/lastofus.jpg"
            },
            {
                "id": "g2",
                "title": "Red Dead Redemption 2",
                "type": "game",
                "description": "An epic tale of life in America's unforgiving heartland.",
                "release_year": 2018,
                "genres": ["Action", "Adventure", "Western"],
                "image_url": "https://store-images.s-microsoft.com/image/apps.58752.13942869738016799.078aba97-2f28-440f-97b6-b852e1af307a.95fdf1a1-efd6-4938-8100-8abae91695d6?q=90&w=480&h=270"
            }
        ]

        for data in synthetic_data:
            item = MediaItem(**data)
            # Generate random embeddings for demonstration
            item.text_embedding = np.random.rand(self.embedding_dim)  # Match Cohere's embedding dimension
            item.image_embedding = np.random.rand(self.embedding_dim)  # Same dimension for consistency
            self.add_item(item) 