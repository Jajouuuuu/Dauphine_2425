from dataclasses import dataclass
from typing import Optional

@dataclass
class Content:
    title: str
    type: Optional[str] = None
    platform: Optional[str] = None
    posterUrl: Optional[str] = None