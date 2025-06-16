from domain.model.review import Review

class FriendReview:
    def __init__(self, friend_name, review: Review):
        self.friend_name = friend_name
        self.review = review