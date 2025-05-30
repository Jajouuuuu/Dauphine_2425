import streamlit as st
from domain.service.rag_service_impl import RAGServiceImpl
from domain.adapter.json_media_repository import JSONMediaRepository

st.set_page_config(
    page_title="Chat with RAG",
    page_icon="🤖",
    layout="wide"
)

# Custom CSS for chat layout
st.markdown("""
    <style>
        /* Hide Streamlit Branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        
        /* Main container styling */
        .main > div:first-child {
            padding-bottom: 100px;
        }
        
        /* Chat container styling */
        .stChatFloatingInputContainer {
            bottom: 0;
            left: 0;
            padding: 1rem 2rem;
            position: fixed;
            right: 0;
            background: white;
            box-shadow: 0 -4px 8px rgba(0,0,0,0.1);
            z-index: 100;
        }
        
        /* Message container styling */
        [data-testid="stChatMessageContainer"] {
            min-height: calc(100vh - 200px);
            padding-bottom: 120px;
            overflow-y: auto;
        }
        
        /* Individual message styling */
        .message {
            padding: 1rem;
            margin: 0.5rem 0;
            border-radius: 0.5rem;
            max-width: 80%;
        }
        
        .user-message {
            background-color: #e9ecef;
            margin-left: auto;
        }
        
        .assistant-message {
            background-color: #f8f9fa;
            margin-right: auto;
        }
        
        /* Visual search column styling */
        .visual-search {
            position: sticky;
            top: 0;
            padding: 1rem;
            background: white;
            border-radius: 0.5rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
    </style>
""", unsafe_allow_html=True)

def initialize_chat_history():
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "Hi! I'm your movies and games expert. Ask me anything about movies or games - I can help you find recommendations, analyze similarities, or discuss specific titles!"}]

def initialize_rag_service():
    if "rag_service" not in st.session_state:
        repository = JSONMediaRepository(
            movies_path="data/processed/movies.json",
            games_path="data/processed/games.json"
        )
        st.session_state.rag_service = RAGServiceImpl(repository)

def main():
    st.title("💬 Movies & Games Expert")
    st.caption("🎮🎬 Powered by RAG - Ask me anything about movies and games!")

    # Initialize services
    initialize_chat_history()
    initialize_rag_service()

    # Sidebar with description and controls
    with st.sidebar:
        st.markdown("""
            Welcome to your personal movies and games expert! I can help you with:
            - Finding movies and games based on your interests
            - Analyzing similarities between different titles
            - Discovering hidden gems you might enjoy
            - Understanding themes and connections
            - Visual similarity search
        """)
        
        st.header("🔍 Visual Search")
        st.info("Upload an image to find visually similar movies and games!")
        
        uploaded_file = st.file_uploader(
            "Upload image:",
            type=["jpg", "png", "jpeg"]
        )
        
        if uploaded_file is not None:
            st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
            
            # Add content type selector for visual search
            visual_content_type = st.radio(
                "Search in:",
                ["Both Movies & Games", "Movies Only", "Games Only"],
                horizontal=True,
                key="visual_content_type"
            )
            
            if st.button("🔎 Find Similar", type="primary", use_container_width=True):
                with st.spinner("Analyzing image..."):
                    # Get media type filter based on selection
                    media_type = None
                    if visual_content_type == "Movies Only":
                        media_type = "movie"
                    elif visual_content_type == "Games Only":
                        media_type = "game"
                    
                    response = st.session_state.rag_service.query_with_image(
                        "placeholder_url",  # Replace with actual image handling
                        media_type=media_type
                    )
                    st.success("Found similar content!")
                    st.markdown(response)

    # Main chat interface
    st.markdown("---")

    # Content type selector for text chat
    content_type = st.radio(
        "What would you like to explore?",
        ["Both Movies & Games", "Movies Only", "Games Only"],
        horizontal=True,
        key="content_type"
    )

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("Ask me about movies and games!"):
        # Add user message
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Get media type filter based on selection
        media_type = None
        if content_type == "Movies Only":
            media_type = "movie"
        elif content_type == "Games Only":
            media_type = "game"

        # Get and display assistant response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = st.session_state.rag_service.query_with_text(prompt, media_type=media_type)
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main() 