from ariadne import gql, QueryType, make_executable_schema, MutationType
from infrastructure.adapter.neo4j_review_repository import Neo4jReviewRepository

repo = Neo4jReviewRepository()

type_defs = gql("""
    type Content {
        title: String
        type: String
        platform: String
        posterUrl: String
    }

    type Review {
        id: ID
        rating: Int
        comment: String
        createdAt: String
        content: Content
    }

    type FriendReview {
        friend: User
        review: Review
    }


    type User {
        name: String
        avatarUrl: String
    }

    type Query {
        friendReviews(username: String!): [FriendReview]
        publicReviews: [Review]
        userReviews(username: String!): [Review]
        allUsers: [User]
        allContent: [Content]
        userFriends(username: String!): [User]
    }

    type Mutation {
        addFriend(username: String!, friendName: String!): User
        removeFriend(username: String!, friendName: String!): Boolean
        postReview(username: String!, contentTitle: String!, rating: Int!, comment: String!): Review
        deleteReview(reviewId: ID!): Boolean
    }
""")

query = QueryType()

@query.field("friendReviews")
def resolve_friend_reviews(_, info, username):
    return [
        {
            "friend": {
                "name": fr.friend.name,
                "avatarUrl": fr.friend.avatarUrl
            },
            "review": {
                "id": fr.review.id,
                "rating": fr.review.rating,
                "comment": fr.review.comment,
                "createdAt": fr.review.createdAt,
                "content": {
                    "title": fr.review.content.title,
                    "type": fr.review.content.type_,
                    "platform": fr.review.content.platform,
                    "posterUrl": fr.review.content.posterUrl
                }
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

@query.field("allUsers")
def resolve_all_users(_, info):
    return [vars(u) for u in repo.get_all_users()]

@query.field("userFriends")
def resolve_user_friends(_, info, username):
    return [vars(f) for f in repo.get_user_friends(username)]

@query.field("userReviews")
def resolve_user_reviews(_, info, username):
    reviews = repo.get_user_reviews(username)
    return [
        {
            "id": r.id,
            "rating": r.rating,
            "comment": r.comment,
            "createdAt": r.createdAt,
            "content": vars(r.content)
        }
        for r in reviews
    ]

@query.field("allContent")
def resolve_all_content(_, info):
    return [vars(c) for c in repo.get_all_content()]

mutation = MutationType()

@mutation.field("addFriend")
def resolve_add_friend(_, info, username, friendName):
    user = repo.add_friend(username, friendName)
    return vars(user) if user else None

@mutation.field("removeFriend")
def resolve_remove_friend(_, info, username, friendName):
    return repo.remove_friend(username, friendName)

@mutation.field("postReview")
def resolve_post_review(_, info, username, contentTitle, rating, comment):
    review = repo.create_review(username, contentTitle, rating, comment)
    if review:
        return {
            "id": review.id,
            "rating": review.rating,
            "comment": review.comment,
            "createdAt": review.createdAt,
            "content": vars(review.content)
        }
    return None

@mutation.field("deleteReview")
def resolve_delete_review(_, info, reviewId):
    return repo.delete_review(reviewId)

schema = make_executable_schema(type_defs, query, mutation)
