from dataclasses import dataclass
from typing import Optional

@dataclass
class Content:
    title: str
    type_: str
    platform: str
    posterUrl: Optional[str] = None
