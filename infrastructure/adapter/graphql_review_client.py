import requests
import pprint

GRAPHQL_ENDPOINT = "http://localhost:5050/graphql"

def execute_query(query, variables=None):
    response = requests.post(
        GRAPHQL_ENDPOINT,
        json={"query": query, "variables": variables}
    )
    response.raise_for_status()
    return response.json()["data"]

# --- QUERIES ---

def get_friend_reviews(username):
    query = """
    query($username: String!) {
        friendReviews(username: $username) {
            friend {
                name
                avatarUrl
            }
            review {
                id
                rating
                comment
                createdAt
                content {
                    title
                    type
                    platform
                    posterUrl
                }
            }
        }
    }
    """

    variables = {"username": username}
    result = execute_query(query, variables)
    return result.get("friendReviews", [])


def get_public_reviews():
    query = """
    {
      publicReviews {
        rating
        comment
        content {
          title
          type
          platform
          posterUrl
        }
      }
    }
    """
    return execute_query(query)["publicReviews"]

def get_all_users():
    query = """
    {
      allUsers {
        name
        avatarUrl
      }
    }
    """
    return execute_query(query)["allUsers"]

def get_my_friends(username):
    query = """
    query($username: String!) {
      userFriends(username: $username) {
        name
        avatarUrl
      }
    }
    """
    return execute_query(query, {"username": username})["userFriends"]

def get_my_reviews(username):
    query = """
    query($username: String!) {
      userReviews(username: $username) {
        id
        rating
        comment
        createdAt
        content {
          title
          type
          platform
          posterUrl
        }
      }
    }
    """
    variables = {"username": username}
    result = execute_query(query, variables)
    print("DEBUG get_my_reviews:", result)  # <-- à garder temporairement
    return result.get("userReviews", [])




def get_all_content():
    query = """
    {
      allContent {
        title
      }
    }
    """
    result = execute_query(query)
    print("DEBUG get_all_content result:", result)  # <-- ajoute ceci
    return [item["title"] for item in result.get("allContent", []) if item]



# --- MUTATIONS ---

def add_friend(username, friend_name):
    mutation = """
    mutation($username: String!, $friendName: String!) {
      addFriend(username: $username, friendName: $friendName) {
        name
        avatarUrl
      }
    }
    """
    return execute_query(mutation, {"username": username, "friendName": friend_name})["addFriend"]

def remove_friend(username, friend_name):
    mutation = """
    mutation($username: String!, $friendName: String!) {
      removeFriend(username: $username, friendName: $friendName)
    }
    """
    return execute_query(mutation, {"username": username, "friendName": friend_name})["removeFriend"]

def post_review(username, content_title, rating, comment):
    mutation = """
    mutation($username: String!, $contentTitle: String!, $rating: Int!, $comment: String!) {
      postReview(username: $username, contentTitle: $contentTitle, rating: $rating, comment: $comment) {
        id
        rating
        comment
        createdAt
        content {
          title
          type
          platform
          posterUrl
        }
      }
    }
    """
    return execute_query(mutation, {
        "username": username,
        "contentTitle": content_title,
        "rating": rating,
        "comment": comment
    })["postReview"]

def delete_review(review_id):
    mutation = """
    mutation($reviewId: ID!) {
      deleteReview(reviewId: $reviewId)
    }
    """
    return execute_query(mutation, {"reviewId": review_id})["deleteReview"]
