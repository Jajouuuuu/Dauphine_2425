# backend.py

from ariadne import gql, QueryType, MutationType, make_executable_schema, graphql_sync
from ariadne.explorer import ExplorerGraphiQL
from flask import Flask, request, jsonify
from neo4j import GraphDatabase
from dotenv import load_dotenv
import os

load_dotenv()

# --- Configuration Neo4j ---
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "password")

# Connexion à la base de données
driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
driver.verify_connectivity()
print("Connexion à Neo4j réussie.")

# --- Schéma GraphQL ---
# J'ai enrichi le schéma pour inclure les utilisateurs, amis, et les mutations.
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
        createdAt: String # On utilise String pour la simplicité du transport
        content: Content
    }
    
    # Cet objet est pour le fil d'actualité des amis
    type FriendReview {
        friend: User
        review: Review
    }
    
    type Query {
        # Renvoie les avis des amis d'un utilisateur
        friendReviews(username: String!): [FriendReview]
        # Renvoie les avis de l'utilisateur lui-même
        myReviews(username: String!): [Review]
        # Renvoie la liste des amis d'un utilisateur
        myFriends(username: String!): [User]
        # Renvoie tous les utilisateurs (pour pouvoir en ajouter)
        allUsers: [User]
        # Renvoie tous les contenus disponibles pour noter
        allContent: [Content]
    }

    type Mutation {
        # Permet de créer un nouvel avis
        createReview(username: String!, contentTitle: String!, rating: Int!, comment: String!): Review
        # Permet d'ajouter un ami
        addFriend(username: String!, friendName: String!): User
        # Permet de supprimer un ami
        removeFriend(username: String!, friendName: String!): User
        # Permet de supprimer un avis
        deleteReview(reviewId: ID!): Boolean
    }
""")

query = QueryType()
mutation = MutationType()

# --- Résolveurs pour les QUERIES ---

@query.field("allUsers")
def resolve_all_users(_, info):
    with driver.session() as session:
        result = session.run("MATCH (u:User) RETURN u.name AS name, u.avatarUrl AS avatarUrl ORDER BY u.name")
        return [{"name": record["name"], "avatarUrl": record["avatarUrl"]} for record in result]
        
@query.field("myFriends")
def resolve_my_friends(_, info, username):
    with driver.session() as session:
        result = session.run("""
            MATCH (:User {name: $username})-[:FRIENDS_WITH]->(f:User)
            RETURN f.name as name, f.avatarUrl as avatarUrl ORDER BY f.name
        """, username=username)
        return [{"name": record["name"], "avatarUrl": record["avatarUrl"]} for record in result]

@query.field("allContent")
def resolve_all_content(_, info):
    with driver.session() as session:
        result = session.run("MATCH (c:Content) RETURN c.title as title, c.posterUrl as posterUrl ORDER BY c.title")
        return [{"title": record["title"], "posterUrl": record["posterUrl"]} for record in result]

@query.field("friendReviews")
def resolve_friend_reviews(_, info, username):
    with driver.session() as session:
        result = session.run("""
            MATCH (currentUser:User {name: $username})-[:FRIENDS_WITH]->(friend:User)-[:WROTE]->(review:Review)-[:REVIEWS]->(content:Content)
            RETURN 
                friend.name AS friendName, 
                friend.avatarUrl AS friendAvatar,
                id(review) as reviewId,
                review.rating AS rating, 
                review.comment AS comment, 
                toString(review.createdAt) as createdAt,
                content.title AS title, 
                content.type AS type, 
                content.platform AS platform,
                content.posterUrl as posterUrl
            ORDER BY review.createdAt DESC
        """, username=username)

        return [
            {
                "friend": { "name": record["friendName"], "avatarUrl": record["friendAvatar"] },
                "review": {
                    "id": record["reviewId"],
                    "rating": record["rating"],
                    "comment": record["comment"],
                    "createdAt": record["createdAt"],
                    "content": {
                        "title": record["title"],
                        "type": record["type"],
                        "platform": record["platform"],
                        "posterUrl": record["posterUrl"]
                    }
                }
            }
            for record in result
        ]

@query.field("myReviews")
def resolve_my_reviews(_, info, username):
    with driver.session() as session:
        result = session.run("""
            MATCH (:User {name: $username})-[:WROTE]->(review:Review)-[:REVIEWS]->(content:Content)
            RETURN 
                id(review) as reviewId,
                review.rating AS rating, 
                review.comment AS comment, 
                toString(review.createdAt) as createdAt,
                content.title AS title, 
                content.type AS type, 
                content.platform AS platform,
                content.posterUrl as posterUrl
            ORDER BY review.createdAt DESC
        """, username=username)

        return [
            {
                "id": record["reviewId"],
                "rating": record["rating"],
                "comment": record["comment"],
                "createdAt": record["createdAt"],
                "content": {
                    "title": record["title"],
                    "type": record["type"],
                    "platform": record["platform"],
                    "posterUrl": record["posterUrl"]
                }
            }
            for record in result
        ]

# --- Résolveurs pour les MUTATIONS ---

@mutation.field("addFriend")
def resolve_add_friend(_, info, username, friendName):
    with driver.session() as session:
        result = session.run("""
            MATCH (u:User {name: $username})
            MATCH (f:User {name: $friendName})
            MERGE (u)-[:FRIENDS_WITH]->(f)
            RETURN f.name as name, f.avatarUrl as avatarUrl
        """, username=username, friendName=friendName)
        return result.single()

@mutation.field("removeFriend")
def resolve_remove_friend(_, info, username, friendName):
    with driver.session() as session:
        session.run("""
            MATCH (u:User {name: $username})-[r:FRIENDS_WITH]->(f:User {name: $friendName})
            DELETE r
        """, username=username, friendName=friendName)
    # On renvoie une confirmation simple
    return {"name": friendName, "avatarUrl": ""}

@mutation.field("createReview")
def resolve_create_review(_, info, username, contentTitle, rating, comment):
    with driver.session() as session:
        result = session.run("""
            MATCH (u:User {name: $username})
            MATCH (c:Content {title: $contentTitle})
            CREATE (r:Review {rating: $rating, comment: $comment, createdAt: datetime()})
            CREATE (u)-[:WROTE]->(r)
            CREATE (r)-[:REVIEWS]->(c)
            RETURN 
                id(r) as reviewId, r.rating as rating, r.comment as comment, 
                toString(r.createdAt) as createdAt, c.title as title, c.posterUrl as posterUrl
        """, username=username, contentTitle=contentTitle, rating=rating, comment=comment)
        
        record = result.single()
        return {
            "id": record["reviewId"],
            "rating": record["rating"],
            "comment": record["comment"],
            "createdAt": record["createdAt"],
            "content": {"title": record["title"], "posterUrl": record["posterUrl"]}
        }
        
@mutation.field("deleteReview")
def resolve_delete_review(_, info, reviewId):
    try:
        # L'ID de Neo4j est un entier, il faut le convertir
        review_id_int = int(reviewId)
        with driver.session() as session:
            session.run("""
                MATCH (r:Review)
                WHERE id(r) = $review_id_int
                DETACH DELETE r
            """, review_id_int=review_id_int)
        return True
    except (ValueError, TypeError):
        # L'ID n'était pas un entier valide
        return False
    except Exception as e:
        print(f"Error deleting review: {e}")
        return False


# --- Configuration Flask ---
schema = make_executable_schema(type_defs, query, mutation)
app = Flask(__name__)

@app.route("/graphql", methods=["GET"])
def graphql_playground():
    return ExplorerGraphiQL().html(None), 200

@app.route("/graphql", methods=["POST"])
def graphql_server():
    data = request.get_json()
    success, result = graphql_sync(schema, data, context_value=request)
    status_code = 200 if success else 400
    return jsonify(result), status_code

if __name__ == "__main__":
    app.run(debug=True, port=5050)