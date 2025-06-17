import streamlit as st
import sys
from pathlib import Path
import tempfile
import os
import warnings

# Suppress torch warnings that don't affect functionality
warnings.filterwarnings("ignore", category=UserWarning, module="torch")
warnings.filterwarnings("ignore", message=".*torch.classes.*")

# Add the project root to Python path for imports
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Import the navigation component
from web_app.components.navigation import render_top_navigation
from web_app.components.media_chat import create_media_chat_sidebar, render_media_chat_history

# Import RAG service
from application.rag_factory import create_rag_service
from domain.adapter.json_media_repository import JSONMediaRepository

st.set_page_config(
    page_title="Chat with RAG",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"  # Show sidebar for media chat
)

# Render the top navigation
render_top_navigation()

# Modern Netflix-like CSS for Chat page
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
        
        /* Status indicator */
        .status-indicator {
            background: linear-gradient(135deg, rgba(76, 175, 80, 0.1) 0%, rgba(56, 142, 60, 0.1) 100%);
            border: 1px solid rgba(76, 175, 80, 0.3);
            border-radius: 15px;
            padding: 1rem;
            margin-bottom: 2rem;
            text-align: center;
        }
        
        .status-indicator.loading {
            background: linear-gradient(135deg, rgba(255, 193, 7, 0.1) 0%, rgba(255, 152, 0, 0.1) 100%);
            border: 1px solid rgba(255, 193, 7, 0.3);
        }
        
        .status-indicator.error {
            background: linear-gradient(135deg, rgba(244, 67, 54, 0.1) 0%, rgba(211, 47, 47, 0.1) 100%);
            border: 1px solid rgba(244, 67, 54, 0.3);
        }
        
        /* Chat container styling */
        .stChatFloatingInputContainer {
            bottom: 20px;
            left: 20px;
            right: 20px;
            padding: 1.5rem;
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(102, 126, 234, 0.3);
            border-radius: 25px;
            box-shadow: 0 15px 35px rgba(102, 126, 234, 0.3);
            z-index: 100;
        }
        
        /* Chat input styling */
        .stChatInputContainer input {
            background: rgba(255,255,255,0.1) !important;
            border: 1px solid rgba(102, 126, 234, 0.3) !important;
            border-radius: 25px !important;
            color: white !important;
            padding: 1rem 1.5rem !important;
            font-size: 1rem !important;
        }
        
        .stChatInputContainer input:focus {
            border: 1px solid rgba(102, 126, 234, 0.6) !important;
            box-shadow: 0 0 20px rgba(102, 126, 234, 0.3) !important;
        }
        
        /* Message container styling */
        [data-testid="stChatMessageContainer"] {
            min-height: calc(100vh - 250px);
            padding-bottom: 150px;
            overflow-y: auto;
        }
        
        /* Individual message styling */
        .stChatMessage {
            margin: 1rem 0;
            padding: 1.5rem;
            border-radius: 20px;
            max-width: 85%;
            position: relative;
        }
        
        /* User message styling */
        [data-testid="stChatMessage"][data-testid-user="true"] {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            margin-left: auto;
            margin-right: 0;
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
        }
        
        /* Assistant message styling */
        [data-testid="stChatMessage"][data-testid-user="false"] {
            background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(102, 126, 234, 0.3);
            margin-left: 0;
            margin-right: auto;
        }
        
        /* Content type selector styling */
        .stRadio > div {
            display: flex;
            gap: 1rem;
            justify-content: center;
            margin: 2rem 0;
        }
        
        .stRadio > div > label {
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.2) 0%, rgba(118, 75, 162, 0.2) 100%);
            border: 1px solid rgba(102, 126, 234, 0.3);
            border-radius: 25px;
            padding: 0.8rem 1.5rem;
            color: white;
            font-weight: 600;
            transition: all 0.3s ease;
            cursor: pointer;
        }
        
        .stRadio > div > label:hover {
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.3) 0%, rgba(118, 75, 162, 0.3) 100%);
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3);
        }
        
        .stRadio > div > label[data-checked="true"] {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
        }
        
        /* Sidebar styling */
        .css-1d391kg {
            background: linear-gradient(135deg, rgba(15,15,35,0.95) 0%, rgba(26,26,46,0.95) 100%);
            backdrop-filter: blur(20px);
        }
        
        /* Button styling */
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
        
        /* Welcome message */
        .welcome-message {
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
            border: 1px solid rgba(102, 126, 234, 0.3);
            border-radius: 20px;
            padding: 2rem;
            margin: 2rem 0;
            text-align: center;
            backdrop-filter: blur(10px);
        }
        
        .welcome-message h3 {
            color: white;
            font-size: 1.5rem;
            font-weight: 700;
            margin-bottom: 1rem;
        }
        
        .welcome-message p {
            color: rgba(255,255,255,0.8);
            line-height: 1.6;
            margin-bottom: 0;
        }
        
        /* Responsive design */
        @media (max-width: 768px) {
            .page-title {
                font-size: 2.5rem;
            }
            
            .stChatMessage {
                max-width: 95%;
                padding: 1rem;
            }
            
            .stChatFloatingInputContainer {
                left: 10px;
                right: 10px;
                padding: 1rem;
            }
        }
    </style>
""", unsafe_allow_html=True)

def initialize_chat_history():
    """Initialize chat history with welcome message"""
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant", 
                "content": "🎬🎮 Salut ! Je suis votre assistant IA pour films et jeux vidéo, propulsé par COHERE et un système RAG vectoriel. Posez-moi n'importe quelle question sur le cinéma ou le gaming !"
            }
        ]

def get_available_datasets():
    """Get available dataset options"""
    datasets = {}
    
    # Check for chunk datasets (prioritize these for faster loading)
    chunks_dir = Path("data/processed/chunks")
    if chunks_dir.exists():
        for i in range(1, 4):  # part1, part2, part3
            movies_chunk = chunks_dir / f"movies_part{i}.json"
            games_chunk = chunks_dir / f"games_part{i}.json"
            
            if movies_chunk.exists() and games_chunk.exists():
                datasets[f"📦 Chunk {i}/3"] = {
                    "movies": str(movies_chunk),
                    "games": str(games_chunk),
                    "description": f"1/3 du dataset - chargement rapide"
                }
    
    # Check for full datasets
    if os.path.exists("data/processed/movies.json") and os.path.exists("data/processed/games.json"):
        datasets["🎯 Dataset Complet"] = {
            "movies": "data/processed/movies.json",
            "games": "data/processed/games.json",
            "description": "Dataset complet (plus lent au premier chargement)"
        }
    
    # Fallback if no data found
    if not datasets:
        datasets["⚠️ Aucune Donnée"] = {
            "movies": None,
            "games": None,
            "description": "Exécutez 'python scripts/split_data.py' pour créer les chunks"
        }
    
    return datasets

def initialize_rag_service():
    """Initialize RAG service with status tracking"""
    if "rag_service" not in st.session_state:
        
        # Show loading status
        status_placeholder = st.empty()
        status_placeholder.markdown("""
            <div class="status-indicator loading">
                🔄 Initialisation du système RAG en cours...
            </div>
        """, unsafe_allow_html=True)
        
        try:
            # Get available datasets
            datasets = get_available_datasets()
            
            # Use part1 chunk by default for faster startup
            if "📦 Chunk 1/3" in datasets:
                selected_dataset = datasets["📦 Chunk 1/3"]
                dataset_name = "Chunk 1/3"
            elif "🎯 Dataset Complet" in datasets:
                selected_dataset = datasets["🎯 Dataset Complet"]
                dataset_name = "Dataset Complet"
            else:
                status_placeholder.markdown("""
                    <div class="status-indicator error">
                        ❌ Aucun dataset trouvé ! Vérifiez vos fichiers de données.
                    </div>
                """, unsafe_allow_html=True)
                return False
            
            if selected_dataset["movies"] and selected_dataset["games"]:
                # Initialize repository
                repository = JSONMediaRepository(
                    movies_path=selected_dataset["movies"],
                    games_path=selected_dataset["games"]
                )
                
                # Create RAG service (text-only for faster startup)
                st.session_state.rag_service = create_rag_service(
                    repository,
                    db_path="./chroma_db",
                    text_model="all-MiniLM-L6-v2",
                    enable_visual=False,  # Disable visual for faster startup
                    batch_size=32
                )
                
                # Store dataset info
                st.session_state.current_dataset = selected_dataset
                st.session_state.dataset_name = dataset_name
                
                # Get stats
                stats = st.session_state.rag_service.get_stats()
                
                # Show success status
                status_placeholder.markdown(f"""
                    <div class="status-indicator">
                        ✅ Système RAG initialisé avec succès !<br>
                        📊 Dataset: {dataset_name}<br>
                        🔤 Embeddings texte: {stats['text_embeddings']:,}<br>
                        🤖 Modèle: {stats['model']}<br>
                        💾 Base: {stats['vector_db']}
                    </div>
                """, unsafe_allow_html=True)
                
                return True
            else:
                status_placeholder.markdown("""
                    <div class="status-indicator error">
                        ❌ Fichiers de données manquants !
                    </div>
                """, unsafe_allow_html=True)
                return False
                
        except Exception as e:
            status_placeholder.markdown(f"""
                <div class="status-indicator error">
                    ❌ Erreur lors de l'initialisation: {str(e)}
                </div>
            """, unsafe_allow_html=True)
            return False
    
    return True

def main():
    """Main chat application"""
    # Page title and subtitle
    st.markdown('<h1 class="page-title">🤖 Assistant IA Films & Jeux</h1>', unsafe_allow_html=True)
    st.markdown('<p class="page-subtitle">Propulsé par COHERE et la technologie RAG - Votre expert personnel en divertissement</p>', unsafe_allow_html=True)

    # Initialize services
    initialize_chat_history()
    rag_initialized = initialize_rag_service()
    
    # Media chat sidebar (only if RAG is initialized)
    if rag_initialized and "rag_service" in st.session_state:
        create_media_chat_sidebar(st.session_state.rag_service)

    # Main content area
    if not rag_initialized or "rag_service" not in st.session_state:
        st.warning("⚠️ Le système RAG n'est pas encore prêt. Veuillez patienter...")
        return

    # Welcome message for new users
    if len(st.session_state.messages) == 1:
        st.markdown("""
            <div class="welcome-message">
                <h3>🌟 Bienvenue dans votre Assistant IA !</h3>
                <p>
                    Je suis là pour vous aider à découvrir votre prochain film ou jeu préféré. 
                    Commencez par me dire ce que vous aimez ou posez-moi n'importe quelle question !
                    Vous pouvez aussi utiliser la barre latérale pour discuter d'un média spécifique.
                </p>
            </div>
        """, unsafe_allow_html=True)

    # Content type selector for text chat
    st.markdown("### 🎯 Que souhaitez-vous explorer ?")
    content_type = st.radio(
        "Choisissez le type de contenu:",
        ["Films & Jeux", "Films uniquement", "Jeux uniquement"],
        horizontal=True,
        key="content_type",
        label_visibility="collapsed"
    )

    # Display chat messages (use custom renderer for media context)
    if any("media_context" in msg for msg in st.session_state.messages):
        render_media_chat_history()
    else:
        # Standard chat display
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("Posez-moi une question sur les films et jeux vidéo !"):
        # Add user message
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Get media type filter based on selection
        media_type = None
        if content_type == "Films uniquement":
            media_type = "movie"
        elif content_type == "Jeux uniquement":
            media_type = "game"

        # Get and display assistant response
        with st.chat_message("assistant"):
            with st.spinner("Réflexion en cours..."):
                try:
                    response = st.session_state.rag_service.query_with_text(prompt, media_type=media_type)
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                except Exception as e:
                    error_msg = f"Désolé, j'ai rencontré une erreur: {str(e)}"
                    st.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})

if __name__ == "__main__":
    main() 