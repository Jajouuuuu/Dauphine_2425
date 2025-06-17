from dataclasses import dataclass
from typing import Optional
from domain.model.content import Content
from domain.model.user import User


@dataclass
class Review:
    id: str
    rating: int
    comment: str
    createdAt: str  # ISO format string
    content: Content

@dataclass
class FriendReview:
    friend: User
    review: Review