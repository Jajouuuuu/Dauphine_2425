from datetime import datetime
import streamlit as st
import sys
from pathlib import Path

# Add the project root to Python path for imports
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Import the navigation component
from web_app.components.navigation import render_top_navigation

# Page configuration
st.set_page_config(
    page_title="Community - Media Finder",
    page_icon="👥",
    layout="wide",
    initial_sidebar_state="expanded"  # Show sidebar for community features
)

# Render the top navigation
render_top_navigation()

# Modern Netflix-like CSS for Community page
st.markdown("""
    <style>
        /* Global app styling */
        .stApp {
            background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
            color: white;
        }
        
        /* Page title styling */
        .page-title {
            font-size: 3.5rem;
            font-weight: 800;
            text-align: center;
            margin: 2rem 0 1rem;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            text-shadow: none;
        }
        
        .page-subtitle {
            text-align: center;
            font-size: 1.2rem;
            color: rgba(255,255,255,0.7);
            margin-bottom: 3rem;
        }
        
        /* Enhanced containers */
        .stContainer > div {
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(102, 126, 234, 0.3);
            border-radius: 15px;
            padding: 1.5rem;
            margin: 1rem 0;
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
        }
        
        /* Tab styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 1rem;
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
            border-radius: 25px;
            padding: 0.5rem;
            margin-bottom: 2rem;
        }
        
        .stTabs [data-baseweb="tab"] {
            background: transparent;
            border-radius: 20px;
            color: rgba(255,255,255,0.7);
            font-weight: 600;
            padding: 1rem 2rem;
            transition: all 0.3s ease;
        }
        
        .stTabs [data-baseweb="tab"]:hover {
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.3) 0%, rgba(118, 75, 162, 0.3) 100%);
            color: white;
        }
        
        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
            color: white !important;
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
        }
        
        /* Sidebar styling */
        .css-1d391kg {
            background: linear-gradient(135deg, rgba(15,15,35,0.95) 0%, rgba(26,26,46,0.95) 100%);
            backdrop-filter: blur(20px);
            border-right: 1px solid rgba(102, 126, 234, 0.3);
        }
        
        /* Friend cards styling */
        .friend-card {
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
            border: 1px solid rgba(102, 126, 234, 0.3);
            border-radius: 15px;
            padding: 1rem;
            margin: 0.5rem 0;
        }
        
        /* Review cards styling */
        .review-card {
            background: linear-gradient(135deg, rgba(255,255,255,0.05) 0%, rgba(255,255,255,0.02) 100%);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(102, 126, 234, 0.3);
            border-radius: 20px;
            padding: 2rem;
            margin: 1.5rem 0;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
            transition: all 0.3s ease;
        }
        
        .review-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 40px rgba(102, 126, 234, 0.2);
            border-color: rgba(102, 126, 234, 0.5);
        }
        
        /* Star rating styling */
        .star-rating {
            font-size: 1.5rem;
            margin: 1rem 0;
            text-shadow: 0 2px 4px rgba(0,0,0,0.3);
        }
        
        /* Form styling */
        .stForm {
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
            border: 1px solid rgba(102, 126, 234, 0.3);
            border-radius: 20px;
            padding: 2rem;
            backdrop-filter: blur(20px);
        }
        
        /* Input styling */
        .stSelectbox > div > div, .stTextArea > div > div, .stSlider > div {
            background: rgba(255,255,255,0.1) !important;
            border: 1px solid rgba(102, 126, 234, 0.3) !important;
            border-radius: 10px !important;
            color: white !important;
        }
        
        /* Button styling - matches other pages */
        div.stButton > button:not([key*="nav"]) {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 0.8rem 2rem;
            border-radius: 25px;
            font-weight: 600;
            font-size: 1rem;
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
            transition: all 0.3s ease;
            width: 100%;
        }
        
        div.stButton > button:not([key*="nav"]):hover {
            background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
            transform: translateY(-2px);
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.5);
        }
        
        /* Image styling */
        .stImage > img {
            border-radius: 10px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        }
        
        /* Error and info messages styling */
        .stAlert {
            background: linear-gradient(135deg, rgba(244, 67, 54, 0.1) 0%, rgba(211, 47, 47, 0.1) 100%);
            border: 1px solid rgba(244, 67, 54, 0.3);
            border-radius: 15px;
            backdrop-filter: blur(20px);
        }
        
        .stInfo {
            background: linear-gradient(135deg, rgba(33, 150, 243, 0.1) 0%, rgba(21, 101, 192, 0.1) 100%);
            border: 1px solid rgba(33, 150, 243, 0.3);
            border-radius: 15px;
            backdrop-filter: blur(20px);
        }
        
        .stSuccess {
            background: linear-gradient(135deg, rgba(76, 175, 80, 0.1) 0%, rgba(56, 142, 60, 0.1) 100%);
            border: 1px solid rgba(76, 175, 80, 0.3);
            border-radius: 15px;
            backdrop-filter: blur(20px);
        }
        
        /* Welcome title styling */
        .welcome-title {
            font-size: 2.5rem;
            font-weight: 700;
            text-align: center;
            margin: 2rem 0;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        /* Responsive design */
        @media (max-width: 768px) {
            .page-title {
                font-size: 2.5rem;
            }
            
            .welcome-title {
                font-size: 2rem;
            }
            
            .stContainer > div {
                padding: 1rem;
            }
        }
    </style>
    """, unsafe_allow_html=True)

# Add error handling for GraphQL imports
try:
    from infrastructure.adapter.graphql_review_client import (
        get_all_users,
        get_my_friends,
        get_friend_reviews,
        get_my_reviews,
        get_all_content,
        add_friend,
        remove_friend,
        post_review,
        delete_review
    )
    GRAPHQL_AVAILABLE = True
except Exception as e:
    GRAPHQL_AVAILABLE = False
    GRAPHQL_ERROR = str(e)

# Initialize session state
if "current_user" not in st.session_state:
    st.session_state.current_user = None

# Check if GraphQL services are available
if not GRAPHQL_AVAILABLE:
    st.error("🚫 Community Features Unavailable")
    st.markdown("""
    **The Community page requires GraphQL services to be running.**
    
    **Possible causes:**
    - GraphQL server is not running on port 5050
    - Neo4j database is not available
    - Network connectivity issues
    
    **To fix this:**
    1. Ensure you started the app with `python main.py` (not directly with Streamlit)
    2. Check if Neo4j is running: `python setup_neo4j.py`
    3. Wait for all services to start (may take 30-60 seconds)
    
    **Error details:**
    ```
    {GRAPHQL_ERROR}
    ```
    """)
    
    # Show a basic community preview
    st.markdown("---")
    st.subheader("🌟 Community Features Preview")
    st.markdown("""
    When all services are running, you'll have access to:
    
    - **👥 Friends System**: Add and manage friends
    - **📝 Reviews**: Share your thoughts on movies and games  
    - **🎯 Activity Feed**: See what your friends are watching/playing
    - **🌍 Global Trends**: Discover popular content
    - **💬 Social Interactions**: Like and comment on reviews
    """)
    
    st.info("💡 **Tip**: Restart the application with `python main.py` to enable all features!")
    st.stop()

with st.sidebar:
    st.title("Profil & Amis")

    # Récupérer la liste des utilisateurs pour le sélecteur
    try:
        all_users = get_all_users()
    except Exception as e:
        st.error(f"❌ Unable to load users: {e}")
        st.info("Please ensure GraphQL server is running on port 5050")
        st.stop()
        
    if all_users:
        user_names = [user['name'] for user in all_users]

        # Sélecteur d'utilisateur
        selected_user = st.selectbox(
            "👤 **Choisissez votre profil**",
            options=user_names,
            index=user_names.index(st.session_state.current_user) if st.session_state.current_user in user_names else 0,
            key="user_selector"
        )
        # Mettre à jour l'utilisateur courant si le sélecteur change
        if st.session_state.current_user != selected_user:
            st.session_state.current_user = selected_user
            st.rerun()  # On rafraîchit toute la page

    else:
        st.warning("Aucun utilisateur trouvé dans la base de données.")
        st.info("💡 Run `python setup_neo4j.py` to create sample data")
        st.stop()  # Arrête l'exécution si on ne peut rien afficher

    st.markdown("---")

    # --- Section de gestion des amis ---
    st.header("🤝 Mes Amis")

    current_user_name = st.session_state.current_user
    
    try:
        my_friends = get_my_friends(current_user_name)
    except Exception as e:
        st.error(f"❌ Unable to load friends: {e}")
        my_friends = []

    # Afficher les amis actuels avec un bouton de suppression
    for friend in my_friends:
        col1, col2, col3 = st.columns([1, 3, 2])
        with col1:
            st.image(friend['avatarUrl'], width=30)
        with col2:
            st.text(friend['name'])
        with col3:
            if st.button("❌", key=f"remove_{friend['name']}", help=f"Retirer {friend['name']} de vos amis"):
                try:
                    remove_friend(current_user_name, friend['name'])
                    st.toast(f"{friend['name']} a été retiré(e) de vos amis.")
                    st.cache_data.clear()  # Vider le cache pour rafraîchir la liste
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error removing friend: {e}")

    st.markdown("---")

    # Ajouter un nouvel ami
    st.subheader("➕ Ajouter un ami")
    friend_names = [f['name'] for f in my_friends]
    available_to_add = [u['name'] for u in all_users if
                        u['name'] not in friend_names and u['name'] != current_user_name]

    if available_to_add:
        friend_to_add = st.selectbox("Qui voulez-vous ajouter ?", available_to_add)
        if st.button("Ajouter cet ami"):
            try:
                add_friend(current_user_name, friend_to_add)
                st.toast(f"Vous êtes maintenant ami(e) avec {friend_to_add} !")
                st.cache_data.clear()
                st.rerun()
            except Exception as e:
                st.error(f"❌ Error adding friend: {e}")
    else:
        st.info("Tous les utilisateurs sont déjà vos amis !")

# --- CORPS PRINCIPAL DE LA PAGE ---
st.markdown(f'<h1 class="welcome-title">👥 Bienvenue, {st.session_state.current_user} !</h1>', unsafe_allow_html=True)

main_col, right_sidebar = st.columns([2.5, 1])

with main_col:
    # --- Création des onglets pour naviguer entre les vues ---
    tab_friends, tab_my_reviews, tab_publish = st.tabs([
        "👥 Activité des amis",
        "📝 Mes avis",
        "✍️ Publier un avis"
    ])

    # --- Onglet 1 : Fil d'actualité des amis ---
    with tab_friends:
        st.header("Quoi de neuf chez vos amis ?")
        
        try:
            friend_reviews = get_friend_reviews(st.session_state.current_user)
        except Exception as e:
            st.error(f"❌ Unable to load friend reviews: {e}")
            friend_reviews = []
            
        if not friend_reviews:
            st.info("Vos amis sont bien silencieux... Soyez le premier à partager un avis ou ajoutez des amis !")
        else:
            for item in friend_reviews:
                review = item['review']
                content = review['content']
                friend = item['friend']

                with st.container(border=True):
                    col1, col2 = st.columns([1, 6])
                    with col1:
                        st.image(friend['avatarUrl'], width=60, caption=friend['name'])
                    with col2:
                        st.markdown(f"**{friend['name']}** a donné son avis sur **{content['title']}**")
                        # Formater la date pour un affichage plus lisible
                        date_obj = datetime.fromisoformat(review['createdAt'].replace('Z', '+00:00'))
                        st.caption(
                            f"{date_obj.strftime('%d %b %Y à %H:%M')} · {content['type']} sur {content['platform']}")

                    st.markdown(
                        f"##### Note : {'⭐' * review['rating']}{'☆' * (10 - review['rating'])} ({review['rating']}/10)")

                    col_poster, col_comment = st.columns([1, 2])
                    if content['posterUrl']:
                        with col_poster:
                            st.image(content['posterUrl'])

                    with col_comment:
                        st.markdown(f"> _{review['comment']}_")

    # --- Onglet 2 : Gérer ses propres avis ---
    with tab_my_reviews:
        st.header("Vos publications")
        
        try:
            my_reviews = get_my_reviews(st.session_state.current_user)
        except Exception as e:
            st.error(f"❌ Unable to load your reviews: {e}")
            my_reviews = []
            
        if not my_reviews:
            st.info("Vous n'avez encore publié aucun avis. Rendez-vous dans l'onglet 'Publier' !")
        else:
            for review in my_reviews:
                content = review['content']
                with st.container(border=True):
                    col1, col2 = st.columns([4, 1])
                    with col1:
                        st.subheader(f"Votre avis sur : {content['title']}")
                        st.markdown(f"**Note : {'⭐' * review['rating']}{'☆' * (10 - review['rating'])}**")
                        st.markdown(f"> {review['comment']}")
                    with col2:
                        st.image(content['posterUrl'], width=100)
                        if st.button("🗑️ Supprimer", key=f"delete_{review['id']}", type="primary"):
                            try:
                                delete_review(review['id'])
                                st.toast("Avis supprimé !")
                                st.cache_data.clear()
                                st.rerun()
                            except Exception as e:
                                st.error(f"❌ Error deleting review: {e}")

    # --- Onglet 3 : Publier un nouvel avis ---
    with tab_publish:
        st.header("Partagez votre opinion")

        # Récupérer la liste des contenus pour le formulaire
        try:
            content_list = get_all_content()
        except Exception as e:
            st.error(f"❌ Unable to load content: {e}")
            content_list = []

        if not content_list:
            st.warning("Aucun contenu à noter n'a été trouvé dans la base de données.")
            st.info("💡 Run `python setup_neo4j.py` to create sample content")
        else:
            with st.form("new_review_form"):
                selected_content = st.selectbox("Quel contenu avez-vous consulté ?", content_list)
                rating = st.slider("Votre note", 1, 10, 8)
                comment = st.text_area("Votre avis", placeholder="Dites à vos amis ce que vous en avez pensé...")

                submitted = st.form_submit_button("Publier mon avis")

                if submitted:
                    if not comment:
                        st.warning("Veuillez écrire un commentaire.")
                    else:
                        try:
                            result = post_review(st.session_state.current_user, selected_content, rating, comment)
                            if result:
                                st.success(f"Votre avis sur **{selected_content}** a été publié ! 🎉")
                                # Vider le cache pour que le nouvel avis apparaisse immédiatement
                                st.cache_data.clear()
                            else:
                                st.error("Une erreur est survenue lors de la publication.")
                        except Exception as e:
                            st.error(f"❌ Error posting review: {e}")

# --- BARRE LATÉRALE DE DROITE : Tendances Mondiales (données en dur) ---
with right_sidebar:
    st.header("🌍 Tendances Mondiales")
    st.caption("Avis et scores issus de la presse spécialisée")

    MOCK_GLOBAL_API_DATA = [
        {"source": "IGN", "title": "Final Fantasy VII Rebirth", "snippet": "Un chef-d'œuvre, 9/10."},
        {"source": "Rotten Tomatoes", "title": "Fallout (Série)",
         "snippet": "Score de 94% - Une adaptation fidèle et inspirée."},
        {"source": "JeuxVideo.com", "title": "Dragon's Dogma 2",
         "snippet": "Une aventure unique mais techniquement datée. 16/20."},
        {"source": "Le Monde", "title": "Oppenheimer", "snippet": "Un biopic intense et spectaculaire."},
    ]

    for item in MOCK_GLOBAL_API_DATA:
        with st.container(border=True):
            st.markdown(f"**{item['title']}**")
            st.markdown(f"_{item['snippet']}_")
            st.caption(f"Source : {item['source']}")