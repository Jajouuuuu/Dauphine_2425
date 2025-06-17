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

# Import clean RAG service
from application.rag_factory import create_rag_service
from domain.adapter.json_media_repository import JSONMediaRepository

st.set_page_config(
    page_title="Chat with RAG",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"  # Hide sidebar for top navigation
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
        
        /* File uploader styling */
        .stFileUpload > div {
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
            border: 2px dashed rgba(102, 126, 234, 0.3);
            border-radius: 15px;
            padding: 2rem;
            text-align: center;
            transition: all 0.3s ease;
        }
        
        .stFileUpload > div:hover {
            border-color: rgba(102, 126, 234, 0.6);
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.2) 0%, rgba(118, 75, 162, 0.2) 100%);
        }
        
        /* Button styling - Exclude navigation buttons by their key */
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
        
        /* Info box styling */
        .stInfo {
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
            border: 1px solid rgba(102, 126, 234, 0.3);
            border-radius: 15px;
            color: white;
        }
        
        /* Success box styling */
        .stSuccess {
            background: linear-gradient(135deg, rgba(76, 175, 80, 0.1) 0%, rgba(56, 142, 60, 0.1) 100%);
            border: 1px solid rgba(76, 175, 80, 0.3);
            border-radius: 15px;
            color: white;
        }
        
        /* Spinner styling */
        .stSpinner > div {
            border-color: #667eea !important;
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
        
        /* Features list */
        .features-list {
            background: linear-gradient(135deg, rgba(255,255,255,0.05) 0%, rgba(255,255,255,0.02) 100%);
            border-radius: 15px;
            padding: 1.5rem;
            margin: 1rem 0;
        }
        
        .features-list ul {
            list-style: none;
            padding: 0;
            margin: 0;
        }
        
        .features-list li {
            padding: 0.5rem 0;
            color: rgba(255,255,255,0.8);
            position: relative;
            padding-left: 2rem;
        }
        
        .features-list li::before {
            content: '✨';
            position: absolute;
            left: 0;
            color: #667eea;
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
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant", 
                "content": "🎬🎮 Salut ! Je suis votre assistant IA pour films et jeux vidéo, propulsé par un système RAG vectoriel optimisé. Posez-moi n'importe quelle question sur le cinéma ou le gaming !"
            }
        ]

def get_available_datasets():
    """Get available dataset options"""
    datasets = {}
    
    # Check for full datasets
    if os.path.exists("data/processed/movies.json") and os.path.exists("data/processed/games.json"):
        datasets["🎯 Full Dataset"] = {
            "movies": "data/processed/movies.json",
            "games": "data/processed/games.json",
            "description": "Complete dataset (may be slow for first load)"
        }
    
    # Check for chunk datasets
    chunks_dir = Path("data/processed/chunks")
    if chunks_dir.exists():
        for i in range(1, 4):  # part1, part2, part3
            movies_chunk = chunks_dir / f"movies_part{i}.json"
            games_chunk = chunks_dir / f"games_part{i}.json"
            
            if movies_chunk.exists() and games_chunk.exists():
                datasets[f"📦 Chunk {i}/3"] = {
                    "movies": str(movies_chunk),
                    "games": str(games_chunk),
                    "description": f"1/3 of dataset - faster loading"
                }
    
    # Fallback to small sample if no data found
    if not datasets:
        datasets["⚠️ No Data Found"] = {
            "movies": None,
            "games": None,
            "description": "Run 'python scripts/split_data.py' to create chunks"
        }
    
    return datasets

def initialize_rag_service():
    if "rag_service" not in st.session_state:
        # Dataset selection
        datasets = get_available_datasets()
        
        # Use the first available dataset (prefer chunks for faster loading)
        if "📦 Chunk 1/3" in datasets:
            selected_dataset = datasets["📦 Chunk 1/3"]
        elif "🎯 Full Dataset" in datasets:
            selected_dataset = datasets["🎯 Full Dataset"]
        else:
            st.error("❌ No dataset found! Please check your data files.")
            return
        
        if selected_dataset["movies"] and selected_dataset["games"]:
            repository = JSONMediaRepository(
                movies_path=selected_dataset["movies"],
                games_path=selected_dataset["games"]
            )
            # Use Clean RAG Service
            st.session_state.rag_service = create_rag_service(repository)
            
            # Store dataset info
            st.session_state.current_dataset = selected_dataset

def main():
    # Page title and subtitle
    st.markdown('<h1 class="page-title">🤖 Assistant IA Films & Jeux</h1>', unsafe_allow_html=True)
    st.markdown('<p class="page-subtitle">Propulsé par la technologie RAG - Votre expert personnel en divertissement</p>', unsafe_allow_html=True)

    # Initialize services
    initialize_chat_history()
    initialize_rag_service()

    # Sidebar with description and controls
    with st.sidebar:
        # Dataset selector
        st.markdown("### 📊 Dataset Selection")
        datasets = get_available_datasets()
        
        if len(datasets) > 1:
            dataset_options = list(datasets.keys())
            current_dataset_name = None
            
            # Find current dataset
            if "current_dataset" in st.session_state:
                for name, info in datasets.items():
                    if (info["movies"] == st.session_state.current_dataset.get("movies") and 
                        info["games"] == st.session_state.current_dataset.get("games")):
                        current_dataset_name = name
                        break
            
            if current_dataset_name:
                current_index = dataset_options.index(current_dataset_name)
            else:
                current_index = 0
            
            selected_dataset_name = st.selectbox(
                "Choose dataset:",
                dataset_options,
                index=current_index,
                help="Chunks load faster, full dataset has all data"
            )
            
            # Show dataset info
            selected_info = datasets[selected_dataset_name]
            st.info(f"📝 {selected_info['description']}")
            
            # Reload button if dataset changed
            if (selected_dataset_name != current_dataset_name and 
                selected_info["movies"] and selected_info["games"]):
                if st.button("🔄 Switch Dataset", type="secondary"):
                    # Clear current service
                    if "rag_service" in st.session_state:
                        del st.session_state.rag_service
                    
                    # Load new dataset
                    repository = JSONMediaRepository(
                        movies_path=selected_info["movies"],
                        games_path=selected_info["games"]
                    )
                    st.session_state.rag_service = create_rag_service(repository)
                    st.session_state.current_dataset = selected_info
                    st.rerun()
        
        st.markdown("---")
        
        # Data management
        st.markdown("### 🛠️ Data Management")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📊 Split Data", help="Split large files into chunks"):
                with st.spinner("Splitting data..."):
                    import subprocess
                    try:
                        result = subprocess.run(
                            ["python", "scripts/split_data.py"], 
                            capture_output=True, 
                            text=True
                        )
                        if result.returncode == 0:
                            st.success("✅ Data split successfully!")
                            st.rerun()
                        else:
                            st.error(f"❌ Error: {result.stderr}")
                    except Exception as e:
                        st.error(f"❌ Error: {e}")
        
        with col2:
            if st.button("🔄 Refresh", help="Refresh available datasets"):
                st.rerun()
        
        st.markdown("---")
        
        st.markdown("""
            <div class="features-list">
                <h3 style="color: white; text-align: center; margin-bottom: 1rem;">🎯 Mes Capacités</h3>
                <ul>
                    <li>Recommandations personnalisées de films et jeux</li>
                    <li>Analyse des similarités entre différents titres</li>
                    <li>Découverte de perles cachées qui pourraient vous plaire</li>
                    <li>Compréhension des thèmes et connexions</li>
                    <li>Recherche par similarité visuelle</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 🔍 Recherche Visuelle")
        st.info("Uploadez une image pour trouver des films et jeux visuellement similaires !")
        
        uploaded_file = st.file_uploader(
            "Choisir une image:",
            type=["jpg", "png", "jpeg"]
        )
        
        if uploaded_file is not None:
            st.image(uploaded_file, caption="Image uploadée", use_column_width=True)
            
            # Add content type selector for visual search
            visual_content_type = st.radio(
                "Rechercher dans:",
                ["Films & Jeux", "Films uniquement", "Jeux uniquement"],
                horizontal=False,
                key="visual_content_type",
                label_visibility="visible"
            )
            
            if st.button("🔎 Trouver des similaires", type="primary", use_container_width=True):
                if "rag_service" not in st.session_state:
                    st.error("⚠️ Please select a dataset first!")
                else:
                    with st.spinner("Analyse de l'image en cours..."):
                        try:
                            # Get media type filter based on selection
                            media_type = None
                            if visual_content_type == "Films uniquement":
                                media_type = "movie"
                            elif visual_content_type == "Jeux uniquement":
                                media_type = "game"
                            
                            response = st.session_state.rag_service.query_with_image(
                                uploaded_file,  # Pass the actual uploaded file
                                media_type=media_type
                            )
                            
                            # Display results in chat format
                            with st.chat_message("assistant"):
                                st.markdown("🎨 **Analyse visuelle terminée!**")
                                st.markdown(response)
                            
                            # Add to chat history
                            st.session_state.messages.append({
                                "role": "assistant", 
                                "content": f"🎨 **Analyse visuelle:**\n\n{response}"
                            })
                            
                        except Exception as e:
                            st.error(f"Erreur lors de l'analyse: {str(e)}")
                            st.info("Essayez avec une image différente ou vérifiez que l'image est lisible.")

    # Main content area
    if "rag_service" not in st.session_state:
        st.warning("⚠️ Please select a dataset in the sidebar to start chatting!")
        return

    # Welcome message for new users
    if len(st.session_state.messages) == 1:
        st.markdown("""
            <div class="welcome-message">
                <h3>🌟 Bienvenue dans votre Assistant IA !</h3>
                <p>
                    Je suis là pour vous aider à découvrir votre prochain film ou jeu préféré. 
                    Commencez par me dire ce que vous aimez ou posez-moi n'importe quelle question !
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

    # Display chat messages
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
                response = st.session_state.rag_service.query_with_text(prompt, media_type=media_type)
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main() 