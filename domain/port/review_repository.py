from typing import Protocol, List, Optional
from domain.model.user import User
from domain.model.content import Content
from domain.model.review import Review, FriendReview

class ReviewRepository(Protocol):
    """
    Interface définissant les opérations de persistance pour les avis et les utilisateurs.
    """
    def get_all_users(self) -> List[User]:
        ...

    def get_user_friends(self, username: str) -> List[User]:
        ...
        
    def get_all_content(self) -> List[Content]:
        ...

    def get_friend_reviews(self, username: str) -> List[FriendReview]:
        ...

    def get_user_reviews(self, username: str) -> List[Review]:
        ...

    def add_friend(self, username: str, friend_name: str) -> Optional[User]:
        ...

    def remove_friend(self, username: str, friend_name: str) -> bool:
        ...

    def create_review(self, username: str, content_title: str, rating: int, comment: str) -> Optional[Review]:
        ...

    def delete_review(self, review_id: str) -> bool:
        ...