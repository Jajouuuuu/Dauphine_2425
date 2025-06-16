from ariadne import gql

type_defs = gql("""
    type User {
        name: String!
        avatarUrl: String
    }

    type Content {
        title: String!
        type: String
        platform: String
        posterUrl: String
    }

    type Review {
        id: ID!
        rating: Int
        comment: String
        createdAt: String
        content: Content
    }
    
    type FriendReview {
        friend: User
        review: Review
    }
    
    type Query {
        friendReviews(username: String!): [FriendReview]
        myReviews(username: String!): [Review]
        myFriends(username: String!): [User]
        allUsers: [User]
        allContent: [Content]
    }

    type Mutation {
        createReview(username: String!, contentTitle: String!, rating: Int!, comment: String!): Review
        addFriend(username: String!, friendName: String!): User
        removeFriend(username: String!, friendName: String!): Boolean
        deleteReview(reviewId: ID!): Boolean
    }
""")