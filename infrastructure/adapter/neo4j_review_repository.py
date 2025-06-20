from typing import List, Optional
from config.env_config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD
from neo4j import GraphDatabase
from domain.model.user import User
from domain.model.content import Content
from domain.model.review import Review, FriendReview
from domain.port.review_repository import ReviewRepository


class Neo4jReviewRepository(ReviewRepository):
    def __init__(self, driver=None):
        if driver is None:
            self.driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
        else:
            self.driver = driver

    def get_all_users(self) -> List[User]:
        with self.driver.session() as session:
            result = session.run("""
                MATCH (u:User)
                RETURN u.name AS name, u.avatarUrl AS avatarUrl
                ORDER BY u.name
            """)
            return [User(**record.data()) for record in result]

    def get_user_friends(self, username: str) -> List[User]:
        with self.driver.session() as session:
            result = session.run("""
                MATCH (:User {name: $username})-[:FRIENDS_WITH]->(f:User)
                RETURN f.name AS name, f.avatarUrl AS avatarUrl
                ORDER BY f.name
            """, username=username)
            return [User(**record.data()) for record in result]

    def get_all_content(self) -> List[Content]:
        with self.driver.session() as session:
            result = session.run("""
                MATCH (c:Content)
                RETURN c.title AS title, c.type AS type, c.platform AS platform, c.posterUrl AS posterUrl
                ORDER BY c.title
            """)
            return [
                Content(
                    title=record["title"],
                    type_=record["type"],
                    platform=record["platform"],
                    posterUrl=record["posterUrl"]
                )
                for record in result
            ]

    def get_friend_reviews(self, username: str) -> List[FriendReview]:
        with self.driver.session() as session:
            result = session.run("""
                MATCH (:User {name: $username})-[:FRIENDS_WITH]->(f:User)-[:WROTE]->(r:Review)-[:REVIEWS]->(c:Content)
                RETURN 
                    f.name AS friendName, f.avatarUrl AS friendAvatar,
                    id(r) AS reviewId, r.rating AS rating, r.comment AS comment, 
                    toString(r.createdAt) AS createdAt,
                    c.title AS title, c.type AS type, c.platform AS platform, c.posterUrl AS posterUrl
                ORDER BY r.createdAt DESC
            """, username=username)

            reviews = []
            for record in result:
                friend = User(name=record["friendName"], avatarUrl=record["friendAvatar"])
                content = Content(
                    title=record["title"],
                    type_=record["type"],
                    platform=record["platform"],
                    posterUrl=record["posterUrl"]
                )
                review = Review(
                    id=str(record["reviewId"]),
                    rating=record["rating"],
                    comment=record["comment"],
                    createdAt=record["createdAt"],
                    content=content
                )
                reviews.append(FriendReview(friend=friend, review=review))
            return reviews

    def get_user_reviews(self, username: str) -> List[Review]:
        with self.driver.session() as session:
            result = session.run("""
                MATCH (:User {name: $username})-[:WROTE]->(r:Review)-[:REVIEWS]->(c:Content)
                RETURN 
                    id(r) AS reviewId, r.rating AS rating, r.comment AS comment,
                    toString(r.createdAt) AS createdAt,
                    c.title AS title, c.type AS type, c.platform AS platform, c.posterUrl AS posterUrl
                ORDER BY r.createdAt DESC
            """, username=username)

            reviews = []
            for record in result:
                content = Content(
                    title=record["title"],
                    type_=record["type"],
                    platform=record["platform"],
                    posterUrl=record["posterUrl"]
                )
                review = Review(
                    id=str(record["reviewId"]),
                    rating=record["rating"],
                    comment=record["comment"],
                    createdAt=record["createdAt"],
                    content=content
                )
                reviews.append(review)
            return reviews

    def get_public_reviews(self) -> List[Review]:
        with self.driver.session() as session:
            result = session.run("""
                MATCH (r:Review)-[:REVIEWS]->(c:Content)
                RETURN 
                    id(r) AS reviewId, r.rating AS rating, r.comment AS comment,
                    toString(r.createdAt) AS createdAt,
                    c.title AS title, c.type AS type, c.platform AS platform, c.posterUrl AS posterUrl
                ORDER BY r.createdAt DESC
                LIMIT 50
            """)
            reviews = []
            for record in result:
                content = Content(
                    title=record["title"],
                    type_=record["type"],
                    platform=record["platform"],
                    posterUrl=record["posterUrl"]
                )
                review = Review(
                    id=str(record["reviewId"]),
                    rating=record["rating"],
                    comment=record["comment"],
                    createdAt=record["createdAt"],
                    content=content
                )
                reviews.append(review)
            return reviews

    def add_friend(self, username: str, friend_name: str) -> Optional[User]:
        with self.driver.session() as session:
            result = session.run("""
                MATCH (u:User {name: $username})
                MATCH (f:User {name: $friendName})
                MERGE (u)-[:FRIENDS_WITH]->(f)
                RETURN f.name AS name, f.avatarUrl AS avatarUrl
            """, username=username, friendName=friend_name).single()
            return User(**result.data()) if result else None

    def remove_friend(self, username: str, friend_name: str) -> bool:
        with self.driver.session() as session:
            result = session.run("""
                MATCH (u:User {name: $username})-[r:FRIENDS_WITH]->(f:User {name: $friendName})
                DELETE r
                RETURN count(r) AS deleted_count
            """, username=username, friendName=friend_name).single()
            return result and result["deleted_count"] > 0

    def create_review(self, username: str, content_title: str, rating: int, comment: str) -> Optional[Review]:
        with self.driver.session() as session:
            result = session.run("""
                MATCH (u:User {name: $username})
                MATCH (c:Content {title: $contentTitle})
                CREATE (r:Review {rating: $rating, comment: $comment, createdAt: datetime()})
                CREATE (u)-[:WROTE]->(r)
                CREATE (r)-[:REVIEWS]->(c)
                RETURN 
                    id(r) AS reviewId, r.rating AS rating, r.comment AS comment,
                    toString(r.createdAt) AS createdAt,
                    c.title AS title, c.type AS type, c.platform AS platform, c.posterUrl AS posterUrl
            """, username=username, contentTitle=content_title, rating=rating, comment=comment).single()

            if result:
                content = Content(
                    title=result["title"],
                    type_=result["type"],
                    platform=result["platform"],
                    posterUrl=result["posterUrl"]
                )
                return Review(
                    id=str(result["reviewId"]),
                    rating=result["rating"],
                    comment=result["comment"],
                    createdAt=result["createdAt"],
                    content=content
                )
            return None

    def delete_review(self, review_id: str) -> bool:
        try:
            with self.driver.session() as session:
                result = session.run("""
                    MATCH (r:Review) WHERE id(r) = $review_id
                    DETACH DELETE r
                    RETURN count(r) AS deleted_count
                """, review_id=int(review_id)).single()
            return result and result["deleted_count"] > 0
        except (ValueError, TypeError):
            return False
