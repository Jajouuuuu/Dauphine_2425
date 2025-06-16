from domain.model.content import Content

class Review:
    def __init__(self, rating, comment, content: Content):
        self.rating = rating
        self.comment = comment
        self.content = content