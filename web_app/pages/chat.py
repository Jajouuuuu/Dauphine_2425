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
from web_app.components.media_chat import render_media_chat_history

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

        /* Add CSS to hide the Streamlit sidebar and set chat input background */
        [data-testid="stSidebar"],
        [data-testid="stSidebarContent"],
        [data-testid="stSidebarHeader"],
        [data-testid="stSidebarCollapseButton"],
        [data-testid="stSidebarNav"],
        [data-testid="stSidebarNavItems"],
        [data-testid="stSidebarNavLinkContainer"],
        [data-testid="stSidebarNavLink"],
        [data-testid="stSidebarUserContent"],
        [data-testid="collapsedControl"] {
            display: none !important;
        }
        [data-testid="stBottomBlockContainer"] {
            background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%) !important;
        }
    </style>
""", unsafe_allow_html=True)

def initialize_chat_history():
    """Initialize chat history with welcome message"""
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant", 
                "content": "🎬🎮 Hi! I'm your AI assistant for movies and video games, powered by COHERE and a vector-based RAG system. Ask me anything about cinema or gaming!"
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
                    "description": f"1/3 of the dataset - fast loading"
                }
    
    # Check for full datasets
    if os.path.exists("data/processed/movies.json") and os.path.exists("data/processed/games.json"):
        datasets["🎯 Full Dataset"] = {
            "movies": "data/processed/movies.json",
            "games": "data/processed/games.json",
            "description": "Full dataset (slower on first load)"
        }
    
    # Fallback if no data found
    if not datasets:
        datasets["⚠️ No Data"] = {
            "movies": None,
            "games": None,
            "description": "Run 'python scripts/split_data.py' to create the chunks"
        }
    
    return datasets

def initialize_rag_service():
    """Initialize RAG service with status tracking"""
    if "rag_service" not in st.session_state:
        # Show loading status
        status_placeholder = st.empty()
        status_placeholder.markdown(
            """
            <div class="status-indicator loading">
                🔄 Initializing the RAG system...
            </div>
            """, unsafe_allow_html=True)
        try:
            datasets = get_available_datasets()
            if "📦 Chunk 1/3" in datasets:
                selected_dataset = datasets["📦 Chunk 1/3"]
                dataset_name = "Chunk 1/3"
            elif "🎯 Full Dataset" in datasets:
                selected_dataset = datasets["🎯 Full Dataset"]
                dataset_name = "Full Dataset"
            else:
                status_placeholder.markdown(
                    """
                    <div class="status-indicator error">
                        ❌ No dataset found! Check your data files.
                    </div>
                    """, unsafe_allow_html=True)
                return False
            if selected_dataset["movies"] and selected_dataset["games"]:
                repository = JSONMediaRepository(
                    movies_path=selected_dataset["movies"],
                    games_path=selected_dataset["games"]
                )
                st.session_state.rag_service = create_rag_service(
                    repository,
                    db_path="./chroma_db",
                    text_model="all-MiniLM-L6-v2",
                    enable_visual=True,  # Enable visual for poster queries
                    batch_size=32,
                    ensure_index=False  # Prevent re-indexing in UI
                )
                st.session_state.current_dataset = selected_dataset
                st.session_state.dataset_name = dataset_name
                # Get stats (but do not show success indicator)
                # stats = st.session_state.rag_service.get_stats()
                status_placeholder.empty()  # Remove the status indicator
                return True
            else:
                status_placeholder.markdown(
                    """
                    <div class="status-indicator error">
                        ❌ Missing data files!
                    </div>
                    """, unsafe_allow_html=True)
                return False
        except Exception as e:
            status_placeholder.markdown(f"""
                <div class="status-indicator error">
                    ❌ Error during initialization: {str(e)}
                </div>
            """, unsafe_allow_html=True)
            return False
    return True

def main():
    """Main chat application"""
    # Page title and subtitle
    st.markdown('<h1 class="page-title">🤖 AI Assistant for Movies & Games</h1>', unsafe_allow_html=True)
    st.markdown('<p class="page-subtitle">Powered by COHERE and RAG technology - Your personal entertainment expert</p>', unsafe_allow_html=True)

    # Initialize services
    initialize_chat_history()
    rag_initialized = initialize_rag_service()
    
    # Main content area
    if not rag_initialized or "rag_service" not in st.session_state:
        st.warning("⚠️ The RAG system is not ready yet. Please wait...")
        return

    # --- New: Image uploader for poster-based queries ---
    uploaded_image = st.file_uploader(
        "Upload a movie or game poster to ask about it:",
        type=["jpg", "jpeg", "png"],
        accept_multiple_files=False,
        key="poster_uploader"
    )
    if uploaded_image:
        with st.spinner("Analyzing poster and searching for similar media..."):
            try:
                response = st.session_state.rag_service.query_with_image(uploaded_image)
                st.markdown("### Visual RAG Response:")
                st.markdown(response)
            except Exception as e:
                st.error(f"Error analyzing image: {e}")

    # Welcome message for new users
    if len(st.session_state.messages) == 1:
        st.markdown("""
            <div class="welcome-message">
                <h3>🌟 Welcome to your AI Assistant!</h3>
                <p>
                    I'm here to help you discover your next favorite movie or game.
                    Start by telling me what you like or ask me any question!
                    You can also upload a poster above to ask about a specific movie or game.
                </p>
            </div>
        """, unsafe_allow_html=True)

    # Content type selector for text chat
    st.markdown("### 🎯 What would you like to explore?")
    content_type = st.radio(
        "Choose the type of content:",
        ["Movies & Games", "Movies only", "Games only"],
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
    if prompt := st.chat_input("Ask me a question about movies and video games!"):
        # Add user message
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Get media type filter based on selection
        media_type = None
        if content_type == "Movies only":
            media_type = "movie"
        elif content_type == "Games only":
            media_type = "game"

        # Get and display assistant response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    response = st.session_state.rag_service.query_with_text(prompt, media_type=media_type)
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                except Exception as e:
                    error_msg = f"Sorry, I encountered an error: {str(e)}"
                    st.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})

if __name__ == "__main__":
    main() 