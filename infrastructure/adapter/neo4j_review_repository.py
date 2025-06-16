from neo4j import GraphDatabase
from config.env_config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD
from domain.model.content import Content
from domain.model.review import Review
from domain.model.friend_review import FriendReview
from domain.port.review_repository import ReviewRepository

class Neo4jReviewRepository(ReviewRepository):
    def __init__(self):
        self.driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

    def get_friend_reviews(self, username):
        with self.driver.session() as session:
            result = session.run("""
                MATCH (:User {name: $username})-[:FRIENDS_WITH]->(f:User)-[:WROTE]->(r:Review)-[:REVIEWS]->(c:Content)
                RETURN f.name AS friendName, r.rating AS rating, r.comment AS comment,
                       c.title AS title, c.type AS type, c.platform AS platform
            """, username=username)

            return [
                FriendReview(
                    friend_name=record["friendName"],
                    review=Review(
                        rating=record["rating"],
                        comment=record["comment"],
                        content=Content(
                            title=record["title"],
                            type_=record["type"],
                            platform=record["platform"]
                        )
                    )
                )
                for record in result
            ]

    def get_public_reviews(self):
        with self.driver.session() as session:
            result = session.run("""
                MATCH (u:User)-[:WROTE]->(r:Review)-[:REVIEWS]->(c:Content)
                RETURN r.rating AS rating, r.comment AS comment,
                       c.title AS title, c.type AS type, c.platform AS platform
                LIMIT 5
            """)
            return [
                Review(
                    rating=record["rating"],
                    comment=record["comment"],
                    content=Content(
                        title=record["title"],
                        type_=record["type"],
                        platform=record["platform"]
                    )
                )
                for record in result
            ]
