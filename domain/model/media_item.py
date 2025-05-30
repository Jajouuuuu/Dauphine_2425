from dataclasses import dataclass
from typing import Optional, List, Dict, Any
import numpy as np

@dataclass
class MediaItem:
    id: str
    title: str
    type: str  # 'movie' or 'game'
    description: str
    metadata: Dict[str, Any]
    content_for_embedding: str
    text_embedding: Optional[np.ndarray] = None
    image_embedding: Optional[np.ndarray] = None

    @property
    def release_date(self) -> str:
        return self.metadata.get("release_date", "")
    
    @property
    def genres(self) -> List[str]:
        return self.metadata.get("genre", [])
    
    @property
    def popularity(self) -> float:
        return float(self.metadata.get("popularity", 0.0))
    
    @property
    def vote_average(self) -> float:
        return float(self.metadata.get("vote_average", 0.0))
    
    @property
    def vote_count(self) -> int:
        return int(self.metadata.get("vote_count", 0))
    
    @property
    def poster_url(self) -> str:
        return self.metadata.get("poster_url", "")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "type": self.type,
            "description": self.description,
            "metadata": self.metadata,
            "content_for_embedding": self.content_for_embedding
        } 