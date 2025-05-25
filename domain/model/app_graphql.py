from ariadne import gql, QueryType, make_executable_schema, graphql_sync
from ariadne.explorer import ExplorerGraphiQL
from flask import Flask, request, jsonify
from neo4j import GraphDatabase

# Connexion Neo4j
driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "sitn2425"))

# Schéma GraphQL
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
    with driver.session() as session:
        result = session.run("""
            MATCH (:User {name: $username})-[:FRIENDS_WITH]->(f:User)-[:WROTE]->(r:Review)-[:REVIEWS]->(c:Content)
            RETURN f.name AS friendName, r.rating AS rating, r.comment AS comment,
                   c.title AS title, c.type AS type, c.platform AS platform
        """, username=username)

        return [
            {
                "friendName": record["friendName"],
                "review": {
                    "rating": record["rating"],
                    "comment": record["comment"],
                    "content": {
                        "title": record["title"],
                        "type": record["type"],
                        "platform": record["platform"]
                    }
                }
            }
            for record in result
        ]

@query.field("publicReviews")
def resolve_public_reviews(_, info):
    with driver.session() as session:
        result = session.run("""
            MATCH (u:User)-[:WROTE]->(r:Review)-[:REVIEWS]->(c:Content)
            RETURN r.rating AS rating, r.comment AS comment,
                   c.title AS title, c.type AS type, c.platform AS platform
            LIMIT 5
        """)
        return [
            {
                "rating": record["rating"],
                "comment": record["comment"],
                "content": {
                    "title": record["title"],
                    "type": record["type"],
                    "platform": record["platform"]
                }
            }
            for record in result
        ]

schema = make_executable_schema(type_defs, query)

# Flask app
app = Flask(__name__)

@app.route("/graphql", methods=["GET"])
def graphql_playground():
    return ExplorerGraphiQL().html(None), 200

@app.route("/graphql", methods=["POST"])
def graphql_server():
    data = request.get_json()
    success, result = graphql_sync(schema, data, context_value=request)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True, port=5050)
