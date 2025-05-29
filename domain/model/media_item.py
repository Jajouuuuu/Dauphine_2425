from dataclasses import dataclass
from typing import Optional, List
import numpy as np

@dataclass
class MediaItem:
    id: str
    title: str
    type: str  # 'movie' or 'game'
    description: str
    release_year: int
    genres: List[str]
    image_url: Optional[str] = None
    text_embedding: Optional[np.ndarray] = None
    image_embedding: Optional[np.ndarray] = None

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "type": self.type,
            "description": self.description,
            "release_year": self.release_year,
            "genres": self.genres,
            "image_url": self.image_url
        } 