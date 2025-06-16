from dataclasses import dataclass
from typing import Optional
from .content import Content
from .user import User

@dataclass
class Review:
    id: str
    rating: int
    comment: str
    createdAt: str
    content: Content

@dataclass
class FriendReview:
    friend: User
    review: Review