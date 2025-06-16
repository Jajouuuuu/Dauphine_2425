import requests

GRAPHQL_ENDPOINT = "http://localhost:5050/graphql"

def get_friend_reviews(username):
    query = """
    query($username: String!) {
      friendReviews(username: $username) {
        friendName
        review {
          rating
          comment
          content {
            title
            type
            platform
          }
        }
      }
    }
    """
    variables = {"username": username}
    response = requests.post(GRAPHQL_ENDPOINT, json={"query": query, "variables": variables})
    return response.json()["data"]["friendReviews"]

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
        }
      }
    }
    """
    response = requests.post(GRAPHQL_ENDPOINT, json={"query": query})
    return response.json()["data"]["publicReviews"]
