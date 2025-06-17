from abc import ABC, abstractmethod
from typing import List, Optional
from domain.model.user import User
from domain.model.content import Content
from domain.model.review import Review, FriendReview

class ReviewRepository(ABC):

    @abstractmethod
    def get_all_users(self) -> List[User]:
        pass

    @abstractmethod
    def get_user_friends(self, username: str) -> List[User]:
        pass

    @abstractmethod
    def get_friend_reviews(self, username: str) -> List[FriendReview]:
        pass

    @abstractmethod
    def get_user_reviews(self, username: str) -> List[Review]:
        pass

    @abstractmethod
    def get_public_reviews(self) -> List[Review]:
        pass

    @abstractmethod
    def get_all_content(self) -> List[Content]:
        pass

    @abstractmethod
    def add_friend(self, username: str, friend_name: str) -> Optional[User]:
        pass

    @abstractmethod
    def remove_friend(self, username: str, friend_name: str) -> bool:
        pass

    @abstractmethod
    def create_review(self, username: str, content_title: str, rating: int, comment: str) -> Optional[Review]:
        pass

    @abstractmethod
    def delete_review(self, review_id: str) -> bool:
        pass
