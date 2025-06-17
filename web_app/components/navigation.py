import streamlit as st
from pathlib import Path
import base64

def get_base64_image(image_path):
    """Convert image to base64 string"""
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except FileNotFoundError:
        return None

def get_svg_content(svg_path):
    """Get SVG content as string"""
    try:
        with open(svg_path, "r") as svg_file:
            return svg_file.read()
    except FileNotFoundError:
        return None

def render_top_navigation():
    """Render the top navigation bar with logo and navigation buttons"""
    
    # Inject global button CSS for beautiful gradient buttons
    st.markdown(
        """
        <style>
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
        </style>
        """,
        unsafe_allow_html=True
    )
    
    # Try to get logo (PNG first, then SVG)
    logo_png_path = Path(__file__).parent.parent.parent / "assets" / "img" / "logo_no_back.png"
    
    logo_content = ""
    if logo_png_path.exists():
        logo_base64 = get_base64_image(logo_png_path)
        if logo_base64:
            logo_content = f'<img src="data:image/png;base64,{logo_base64}" alt="Media Finder Logo" style="height: 100px; margin-right: 15px; border-radius: 8px;">'
    else:
        # Fallback to emoji if no image
        logo_content = '<span style="font-size: 2rem; margin-right: 15px;">📱</span>'
    
    # Create the navigation header with page-matching background
    nav_html = f"""
    <style>
    .top-nav {{
        backdrop-filter: blur(10px);
        padding: 1rem 2rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin: -1rem -1rem 2rem -1rem;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        border-bottom: 1px solid rgba(0, 0, 0, 0.1);
    }}
    
    .nav-logo {{
        display: flex;
        align-items: center;
        color: #333;
        text-decoration: none;
    }}
    
    .nav-logo h1 {{
        margin: 0;
        font-size: 4rem;
        font-weight: 700;
        color: #FFFFFF;
        letter-spacing: 1px;
    }}
    
    .nav-buttons {{
        display: flex;
        gap: 1rem;
        align-items: center;
    }}
    
    /* Custom styling for navigation buttons - THIS IS THE SINGLE SOURCE OF TRUTH */
    div[data-testid="stHorizontalBlock"] div[data-testid="column"] div.stButton > button[key*="nav"] {{
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        padding: 0.8rem 2rem !important;
        border-radius: 25px !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4) !important;
        transition: all 0.3s ease !important;
        min-width: 140px !important;
        height: 50px !important;
        width: auto !important;
    }}
    
    div[data-testid="stHorizontalBlock"] div[data-testid="column"] div.stButton > button[key*="nav"]:hover {{
        transform: translateY(-2px) !important;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.5) !important;
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%) !important;
    }}
    
    div[data-testid="stHorizontalBlock"] div[data-testid="column"] div.stButton > button[key*="nav"]:active {{
        transform: translateY(0px) !important;
    }}

    /* Mobile responsive */
    @media (max-width: 768px) {{
        .top-nav {{
            flex-direction: column;
            gap: 1rem;
            padding: 1rem;
        }}
        
        .nav-buttons {{
            gap: 0.5rem;
            flex-wrap: wrap;
            justify-content: center;
        }}
        
        .nav-logo h1 {{
            font-size: 1.4rem;
        }}
        
        div[data-testid="stHorizontalBlock"] div[data-testid="column"] div.stButton > button[key*="nav"] {{
            min-width: 100px !important;
            max-width: 120px !important;
            padding: 0.5rem 1rem !important;
            font-size: 0.8rem !important;
        }}
    }}
   
    </style>
    
    <div class="top-nav">
        <div class="nav-logo">
            {logo_content}
            <h1>MEDIA FINDER</h1>
        </div>
        <div class="nav-buttons">
            <!-- Navigation buttons will be rendered using Streamlit buttons below -->
        </div>
    </div>
    """
    
    # Display the navigation header
    st.markdown(nav_html, unsafe_allow_html=True)
    
    # Create navigation buttons using Streamlit columns and buttons
    # Use 6 columns to center the 4 buttons
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    
    with c2:
        if st.button("🏠 Home", key="top_nav_home", use_container_width=True):
            st.switch_page("Home.py")
    
    with c3:
        if st.button("🎬 What's new ?", key="top_nav_platforms", use_container_width=True):
            st.switch_page("pages/discover.py")
    
    with c4:
        if st.button("💬 Media Chat", key="top_nav_chat", use_container_width=True):
            st.switch_page("pages/chat.py")
    
    with c5:
        if st.button("👥 About us", key="top_nav_teams", use_container_width=True):
            st.switch_page("pages/about.py")


def create_page_navigation():
    """Create navigation buttons for switching between pages"""
    
    # Custom CSS for navigation buttons
    st.markdown("""
    <style>
    .nav-button-container {
        display: flex;
        gap: 1rem;
        justify-content: center;
        margin: 2rem 0;
        flex-wrap: wrap;
    }
    
    div.stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 25px;
        font-weight: 600;
        font-size: 0.95rem;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        transition: all 0.3s ease;
        min-width: 140px;
    }
    
    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    
    div.stButton > button:active {
        transform: translateY(0px);
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Create navigation buttons in columns
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🏠 Home", key="nav_home", use_container_width=True):
            st.switch_page("Home.py")
    
    with col2:
        if st.button("🎬 What's new ?", key="nav_platforms", use_container_width=True):
            st.switch_page("pages/discover.py")
    
    with col3:
        if st.button("💬 Media Chat", key="nav_chat", use_container_width=True):
            st.switch_page("pages/chat.py")
    
    with col4:
        if st.button("👥 About us", key="nav_teams", use_container_width=True):
            st.switch_page("pages/about.py")

def create_floating_navigation():
    """Create modern floating navigation buttons"""
    
    # Get current page name for highlighting active page
    try:
        current_page = st.session_state.get('current_page', 'Home')
    except:
        current_page = 'Home'
    
    nav_html = f"""
    <style>
    .floating-nav {{
        position: fixed;
        top: 50%;
        right: 20px;
        transform: translateY(-50%);
        background: rgba(102, 126, 234, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 25px;
        padding: 1rem 0.5rem;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
        z-index: 1000;
        display: flex;
        flex-direction: column;
        gap: 1rem;
    }}
    
    .nav-icon {{
        width: 45px;
        height: 45px;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.2);
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        text-decoration: none;
        font-size: 1.2rem;
        transition: all 0.3s ease;
        cursor: pointer;
    }}
    
    .nav-icon:hover {{
        background: rgba(255, 255, 255, 0.3);
        transform: scale(1.1);
    }}
    
    .nav-icon.active {{
        background: rgba(255, 255, 255, 0.4);
    }}
    
    @media (max-width: 768px) {{
        .floating-nav {{
            display: none;
        }}
    }}
    </style>
    
    <div class="floating-nav">
        <a href="#" class="nav-icon {'active' if current_page == 'Home' else ''}" onclick="window.location.reload()">🏠</a>
        <a href="#" class="nav-icon {'active' if current_page == 'Platforms' else ''}">🎬</a>
        <a href="#" class="nav-icon {'active' if current_page == 'Teams' else ''}">👥</a>
        <a href="#" class="nav-icon {'active' if current_page == 'Chat' else ''}">💬</a>
    </div>
    """
    
    st.markdown(nav_html, unsafe_allow_html=True) 