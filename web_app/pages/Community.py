import streamlit as st
import requests

# Configuration de l'endpoint GraphQL local
GRAPHQL_ENDPOINT = "http://localhost:5050/graphql"

# Requête 1 : Avis des amis
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

# Requête 2 : Avis publics
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

# Interface utilisateur Streamlit
st.title("💬 Avis communautaires")

username = st.selectbox("Choisissez un utilisateur", ["Alice", "Bob", "Charlie", "Diana"])

# Deux colonnes : amis à gauche, public à droite
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("🎯 Avis de vos amis")
    reviews = get_friend_reviews(username)
    if reviews:
        for r in reviews:
            st.markdown(f"**{r['friendName']}** a noté **{r['review']['content']['title']}** ({r['review']['content']['type']}) sur {r['review']['content']['platform']}")
            st.markdown(f"⭐ {r['review']['rating']} – _{r['review']['comment']}_")
            st.markdown("---")
    else:
        st.info("Aucun avis d'amis disponible.")

with col2:
    st.subheader("🌍 Avis du monde entier")
    public = get_public_reviews()
    for r in public:
        st.markdown(f"**{r['content']['title']}** ({r['content']['type']}) sur {r['content']['platform']}")
        st.markdown(f"⭐ {r['rating']} – _{r['comment']}_")
        st.markdown("---")
