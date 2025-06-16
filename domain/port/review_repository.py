from abc import ABC, abstractmethod

class ReviewRepository(ABC):
    @abstractmethod
    def get_friend_reviews(self, username): pass

    @abstractmethod
    def get_public_reviews(self): pass