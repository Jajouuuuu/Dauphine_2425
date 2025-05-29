import streamlit as st
from domain.service.rag_service_impl import RAGServiceImpl
from domain.adapter.in_memory_media_repository import InMemoryMediaRepository

st.set_page_config(
    page_title="Chat with RAG",
    page_icon="🤖",
    layout="wide"  # Use wide layout for better spacing
)

def initialize_chat_history():
    if "messages" not in st.session_state:
        st.session_state.messages = []

def initialize_rag_service():
    if "rag_service" not in st.session_state:
        repository = InMemoryMediaRepository()
        st.session_state.rag_service = RAGServiceImpl(repository)

def main():
    st.title("Chat with movies & games expert 🎮🎬")
    
    initialize_chat_history()
    initialize_rag_service()

    # Add some spacing and a divider
    st.markdown("---")

    # Create two columns with better ratio and spacing
    chat_col, spacing_col, visual_col = st.columns([3, 0.2, 2])

    with chat_col:
       
        # Create a container for chat messages with fixed height
        chat_container = st.container()
        with chat_container:
           
            
            st.markdown('<div class="chat-container">', unsafe_allow_html=True)
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])
            st.markdown('</div>', unsafe_allow_html=True)

        # Chat input at the bottom
        if prompt := st.chat_input("Ask me about movies and games!"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = st.session_state.rag_service.query_with_text(prompt)
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})

    # Empty column for spacing
    with spacing_col:
        st.empty()

    with visual_col:
        st.markdown("### 🔍 Visual Search")
        st.info("""
        Upload an image to:
        - Identify a specific movie or game
        - Find similar content based on visual elements
        """)
        
        # Create a container for the visual search
        visual_container = st.container()
        with visual_container:
            uploaded_file = st.file_uploader(
                "Upload your image:",
                type=["jpg", "png", "jpeg"],
                help="Upload a screenshot, movie scene, or related image"
            )
            
            if uploaded_file is not None:
                # Add some spacing
                st.write("")
                
                # Display the image with a border
                st.markdown("""
                    <style>
                        .uploaded-image {
                            border: 2px solid #e0e0e0;
                            border-radius: 10px;
                            padding: 10px;
                        }
                    </style>
                """, unsafe_allow_html=True)
                
                st.markdown('<div class="uploaded-image">', unsafe_allow_html=True)
                st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Add some spacing
                st.write("")
                
                with st.expander("Search Options", expanded=True):
                    search_type = st.radio(
                        "What would you like to find?",
                        ["Identify this content", "Find similar content"],
                        help="Choose whether to identify the specific movie/game or find similar content"
                    )
                
                if st.button("🔎 Search", type="primary", use_container_width=True):
                    with st.spinner("Analyzing image..."):
                        if search_type == "Identify this content":
                            response = st.session_state.rag_service.query_with_image("placeholder_url")
                            st.success("### Potential Matches")
                            st.markdown(response)
                        else:  # Find similar content
                            response = st.session_state.rag_service.query_with_image("placeholder_url")
                            st.success("### Similar Content")
                            st.markdown(response)

if __name__ == "__main__":
    main() 