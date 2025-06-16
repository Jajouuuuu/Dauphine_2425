from ariadne import gql, QueryType, make_executable_schema
from infrastructure.adapter.neo4j_review_repository import Neo4jReviewRepository

repo = Neo4jReviewRepository()

type_defs = gql("""
    type Content {
        title: String
        type: String
        platform: String
    }

    type Review {
        rating: Int
        comment: String
        content: Content
    }

    type FriendReview {
        friendName: String
        review: Review
    }

    type Query {
        friendReviews(username: String!): [FriendReview]
        publicReviews: [Review]
    }
""")

query = QueryType()

@query.field("friendReviews")
def resolve_friend_reviews(_, info, username):
    return [
        {
            "friendName": fr.friend_name,
            "review": {
                "rating": fr.review.rating,
                "comment": fr.review.comment,
                "content": vars(fr.review.content)
            }
        }
        for fr in repo.get_friend_reviews(username)
    ]

@query.field("publicReviews")
def resolve_public_reviews(_, info):
    return [
        {
            "rating": r.rating,
            "comment": r.comment,
            "content": vars(r.content)
        }
        for r in repo.get_public_reviews()
    ]

schema = make_executable_schema(type_defs, query)