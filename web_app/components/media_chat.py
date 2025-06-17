"""
Media Chat Component
- Provides a sidebar for initiating chat from media items
- Displays movie/game posters with chat functionality
- Maintains session continuity when switching to main chat
"""

import streamlit as st
from typing import Optional, Dict, Any
import json
from pathlib import Path

def create_media_chat_sidebar(rag_service, media_items: list = None):
    """
    Create a media/poster chat sidebar that allows users to start conversations
    about specific media items.
    
    Args:
        rag_service: The RAG service instance
        media_items: List of media items to display (optional)
    """
    
    # Custom CSS for the media chat sidebar
    st.markdown("""
    <style>
    .media-chat-sidebar {
        background: linear-gradient(135deg, rgba(15,15,35,0.95) 0%, rgba(26,26,46,0.95) 100%);
        backdrop-filter: blur(20px);
        border-radius: 15px;
        padding: 1.5rem;
        margin-bottom: 2rem;
        border: 1px solid rgba(102, 126, 234, 0.3);
    }
    
    .media-item-card {
        background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%);
        border: 1px solid rgba(102, 126, 234, 0.3);
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 1rem;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .media-item-card:hover {
        border-color: rgba(102, 126, 234, 0.6);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
        transform: translateY(-2px);
    }
    
    .media-title {
        color: white;
        font-size: 1rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
        line-height: 1.3;
    }
    
    .media-type {
        color: rgba(102, 126, 234, 0.9);
        font-size: 0.8rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.5rem;
    }
    
    .media-description {
        color: rgba(255,255,255,0.7);
        font-size: 0.85rem;
        line-height: 1.4;
        margin-bottom: 1rem;
        display: -webkit-box;
        -webkit-line-clamp: 3;
        -webkit-box-orient: vertical;
        overflow: hidden;
    }
    
    .quick-chat-prompt {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.2) 0%, rgba(118, 75, 162, 0.2) 100%);
        border: 1px solid rgba(102, 126, 234, 0.3);
        border-radius: 8px;
        padding: 0.5rem;
        margin-bottom: 0.5rem;
        color: rgba(255,255,255,0.8);
        font-size: 0.8rem;
        cursor: pointer;
        transition: all 0.2s ease;
    }
    
    .quick-chat-prompt:hover {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.3) 0%, rgba(118, 75, 162, 0.3) 100%);
        color: white;
    }
    
    .chat-with-media-btn {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.6rem 1rem;
        border-radius: 8px;
        font-weight: 600;
        font-size: 0.85rem;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .chat-with-media-btn:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }
    </style>
    """, unsafe_allow_html=True)
    
    with st.sidebar:
        st.markdown("### 🎬 Chat avec les Médias")
        
        # If no specific media items provided, show featured/popular ones
        if not media_items:
            media_items = get_featured_media_items(rag_service)
        
        if media_items:
            st.markdown('<div class="media-chat-sidebar">', unsafe_allow_html=True)
            
            for item in media_items[:5]:  # Show top 5 items
                with st.container():
                    # Media item card
                    st.markdown(f"""
                    <div class="media-item-card">
                        <div class="media-type">{get_media_type_display(item.type)}</div>
                        <div class="media-title">{item.title}</div>
                        <div class="media-description">{item.description[:150]}...</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Quick chat prompts
                    quick_prompts = get_quick_prompts(item)
                    
                    for i, prompt in enumerate(quick_prompts):
                        if st.button(
                            prompt, 
                            key=f"quick_prompt_{item.id}_{i}",
                            help=f"Commencer une conversation sur {item.title}"
                        ):
                            start_media_chat(item, prompt, rag_service)
                    
                    # Main chat button
                    if st.button(
                        f"💬 Discuter de {item.title}",
                        key=f"chat_with_{item.id}",
                        help=f"Ouvrir une conversation détaillée sur {item.title}"
                    ):
                        start_media_chat(item, f"Parle-moi de {item.title}", rag_service)
                    
                    st.markdown("---")
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        else:
            st.info("Aucun média disponible pour le chat. Chargez d'abord un dataset.")

def get_featured_media_items(rag_service):
    """Get featured/popular media items for the sidebar"""
    try:
        # Get all items and sort by popularity/rating
        all_items = rag_service.media_repository.get_all_items()
        
        # Sort by vote_average and popularity
        featured_items = sorted(
            all_items, 
            key=lambda x: (getattr(x, 'vote_average', 0) * getattr(x, 'popularity', 0)), 
            reverse=True
        )
        
        return featured_items[:10]  # Return top 10
        
    except Exception as e:
        print(f"Error getting featured items: {e}")
        return []

def get_media_type_display(media_type: str) -> str:
    """Get display name for media type"""
    return "🎬 Film" if media_type == "movie" else "🎮 Jeu"

def get_quick_prompts(item) -> list:
    """Generate quick chat prompts for a media item"""
    if item.type == "movie":
        return [
            f"Recommande-moi des films comme {item.title}",
            f"Analyse les thèmes de {item.title}",
            f"Qui devrait regarder {item.title} ?"
        ]
    else:  # game
        return [
            f"Recommande-moi des jeux comme {item.title}",
            f"Analyse le gameplay de {item.title}",
            f"À qui s'adresse {item.title} ?"
        ]

def start_media_chat(item, prompt: str, rag_service):
    """Start a chat conversation about a specific media item"""
    try:
        # Initialize chat history if not exists
        if "messages" not in st.session_state:
            st.session_state.messages = []
        
        # Add context about the media item to the prompt
        enhanced_prompt = f"{prompt}\n\nContexte: Je m'intéresse particulièrement à '{item.title}' ({get_media_type_display(item.type)})"
        
        # Add user message to chat history
        st.session_state.messages.append({
            "role": "user", 
            "content": prompt,
            "media_context": {
                "title": item.title,
                "type": item.type,
                "id": item.id
            }
        })
        
        # Get response from RAG service
        response = rag_service.query_with_text(enhanced_prompt, media_type=item.type)
        
        # Add assistant response
        st.session_state.messages.append({
            "role": "assistant", 
            "content": response,
            "media_context": {
                "title": item.title,
                "type": item.type,
                "id": item.id
            }
        })
        
        # Show success message
        st.success(f"💬 Conversation démarrée sur {item.title}!")
        
        # Auto-redirect to chat page if not already there
        if st.session_state.get("current_page") != "chat":
            st.info("🔄 Redirection vers la page de chat...")
            st.switch_page("pages/chat.py")
        
    except Exception as e:
        st.error(f"Erreur lors du démarrage de la conversation: {e}")

def render_media_chat_history():
    """Render chat messages with media context highlighting"""
    if "messages" not in st.session_state:
        return
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            # Show media context if available
            if "media_context" in message:
                media_ctx = message["media_context"]
                st.markdown(f"""
                <div style="
                    background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
                    border: 1px solid rgba(102, 126, 234, 0.3);
                    border-radius: 8px;
                    padding: 0.5rem;
                    margin-bottom: 0.5rem;
                    font-size: 0.8rem;
                    color: rgba(255,255,255,0.8);
                ">
                    💬 Conversation sur: <strong>{media_ctx['title']}</strong> ({get_media_type_display(media_ctx['type'])})
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown(message["content"])

def get_media_poster_url(item) -> Optional[str]:
    """Get poster URL for a media item"""
    return getattr(item, 'poster_url', None)

def create_floating_media_chat():
    """Create a floating media chat button that can be used on any page"""
    st.markdown("""
    <style>
    .floating-media-chat {
        position: fixed;
        bottom: 100px;
        right: 20px;
        width: 60px;
        height: 60px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 1.5rem;
        cursor: pointer;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
        transition: all 0.3s ease;
        z-index: 1000;
        border: none;
    }
    
    .floating-media-chat:hover {
        transform: scale(1.1);
        box-shadow: 0 12px 35px rgba(102, 126, 234, 0.6);
    }
    
    @media (max-width: 768px) {
        .floating-media-chat {
            bottom: 80px;
            right: 15px;
            width: 50px;
            height: 50px;
            font-size: 1.2rem;
        }
    }
    </style>
    
    <button class="floating-media-chat" onclick="window.location.href='/chat'" title="Chat avec les médias">
        🎬
    </button>
    """, unsafe_allow_html=True) 