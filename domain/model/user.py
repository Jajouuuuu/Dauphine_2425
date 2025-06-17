from dataclasses import dataclass
from typing import Optional

@dataclass
class User:
    name: str
    avatarUrl: Optional[str] = None