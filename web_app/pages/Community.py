from datetime import datetime

import streamlit as st
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


if "current_user" not in st.session_state:
    st.session_state.current_user = None

with st.sidebar:
    st.title("Profil & Amis")

    # Récupérer la liste des utilisateurs pour le sélecteur
    all_users = get_all_users()
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
        st.stop()  # Arrête l'exécution si on ne peut rien afficher

    st.markdown("---")

    # --- Section de gestion des amis ---
    st.header("🤝 Mes Amis")

    current_user_name = st.session_state.current_user
    my_friends = get_my_friends(current_user_name)

    # Afficher les amis actuels avec un bouton de suppression
    for friend in my_friends:
        col1, col2, col3 = st.columns([1, 3, 2])
        with col1:
            st.image(friend['avatarUrl'], width=30)
        with col2:
            st.text(friend['name'])
        with col3:
            if st.button("❌", key=f"remove_{friend['name']}", help=f"Retirer {friend['name']} de vos amis"):
                remove_friend(current_user_name, friend['name'])
                st.toast(f"{friend['name']} a été retiré(e) de vos amis.")
                st.cache_data.clear()  # Vider le cache pour rafraîchir la liste
                st.rerun()

    st.markdown("---")

    # Ajouter un nouvel ami
    st.subheader("➕ Ajouter un ami")
    friend_names = [f['name'] for f in my_friends]
    available_to_add = [u['name'] for u in all_users if
                        u['name'] not in friend_names and u['name'] != current_user_name]

    if available_to_add:
        friend_to_add = st.selectbox("Qui voulez-vous ajouter ?", available_to_add)
        if st.button("Ajouter cet ami"):
            add_friend(current_user_name, friend_to_add)
            st.toast(f"Vous êtes maintenant ami(e) avec {friend_to_add} !")
            st.cache_data.clear()
            st.rerun()
    else:
        st.info("Tous les utilisateurs sont déjà vos amis !")

# --- CORPS PRINCIPAL DE LA PAGE ---
st.title(f"Bienvenue, {st.session_state.current_user} !")

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
        friend_reviews = get_friend_reviews(st.session_state.current_user)
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
        my_reviews = get_my_reviews(st.session_state.current_user)
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
                            delete_review(review['id'])
                            st.toast("Avis supprimé !")
                            st.cache_data.clear()
                            st.rerun()

    # --- Onglet 3 : Publier un nouvel avis ---
    with tab_publish:
        st.header("Partagez votre opinion")

        # Récupérer la liste des contenus pour le formulaire
        content_list = get_all_content()

        if not content_list:
            st.warning("Aucun contenu à noter n'a été trouvé dans la base de données.")
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
                        result = post_review(st.session_state.current_user, selected_content, rating, comment)
                        if result:
                            st.success(f"Votre avis sur **{selected_content}** a été publié ! 🎉")
                            # Vider le cache pour que le nouvel avis apparaisse immédiatement
                            st.cache_data.clear()
                        else:
                            st.error("Une erreur est survenue lors de la publication.")

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