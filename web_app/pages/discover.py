import streamlit as st
import json
from pathlib import Path
import base64
import sys

# Add the project root to Python path for imports
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Import the navigation component
from web_app.components.navigation import render_top_navigation

# Page configuration
st.set_page_config(
    page_title="Sorties Multi-Plateformes",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"  # Hide sidebar for top navigation
)

# Render the top navigation
render_top_navigation()

# Modern Netflix-like CSS with improvements
st.markdown(
    """
    <style>
    /* Global app styling */
    .stApp {
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
        color: white;
    }
    
    /* Hero section improvements */
    .hero {
        position: relative;
        width: 100%;
        height: 50vh;
        background-size: cover;
        background-position: center;
        margin-bottom: 3rem;
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 15px 40px rgba(0,0,0,0.4);
    }
    
    .hero-overlay {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(to bottom, rgba(0,0,0,0.2), rgba(15,15,35,0.8));
    }
    
    .hero-content {
        position: absolute;
        bottom: 8%;
        left: 5%;
        z-index: 1;
        color: #fff;
    }
    
    .hero-title {
        font-size: 3rem;
        font-weight: 800;
        margin: 0;
        text-shadow: 0 4px 15px rgba(0,0,0,0.7);
        background: linear-gradient(45deg, #ffffff, #f0f0ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .hero-subtitle {
        font-size: 1.2rem;
        margin: 0.5rem 0 1.5rem;
        opacity: 0.9;
        text-shadow: 0 2px 8px rgba(0,0,0,0.5);
    }
    
    .btn-primary {
        display: inline-block;
        padding: 1rem 2.5rem;
        font-size: 1.1rem;
        border-radius: 25px;
        text-decoration: none !important;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: #ffffff;
        transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
        border: none;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .btn-primary:hover {
        transform: translateY(-3px) scale(1.05);
        box-shadow: 0 15px 35px rgba(102, 126, 234, 0.6);
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
        text-decoration: none !important;
        color: #ffffff;
    }
    
    /* Section titles with gradient */
    .section-title {
        font-size: 2.5rem;
        margin: 4rem 0 2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-shadow: none;
        position: relative;
    }
    
    .section-title::after {
        content: '';
        position: absolute;
        bottom: -10px;
        left: 0;
        width: 80px;
        height: 4px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 2px;
    }
    
    /* Enhanced Netflix-style cards */
    .netflix-card {
        position: relative;
        width: 100%;
        max-width: 220px;
        margin: 0 auto 2rem;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        border-radius: 12px;
        overflow: hidden;
    }
    
    .netflix-card:hover {
        transform: scale(1.15) translateY(-10px);
        z-index: 100;
    }
    
    .card-image-container {
        position: relative;
        width: 100%;
        padding-top: 150%; /* 2:3 aspect ratio */
        overflow: hidden;
        border-radius: 12px;
        box-shadow: 0 8px 30px rgba(0,0,0,0.5);
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .card-image {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        object-fit: cover;
        transition: all 0.3s ease;
    }
    
    .netflix-card:hover .card-image {
        transform: scale(1.1);
    }
    
    .card-overlay {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(to bottom, 
            rgba(0,0,0,0) 0%, 
            rgba(0,0,0,0.3) 50%, 
            rgba(15,15,35,0.95) 100%);
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .netflix-card:hover .card-overlay {
        opacity: 1;
    }
    
    .card-content {
        position: absolute;
        bottom: 0;
        left: 0;
        width: 100%;
        padding: 20px 15px;
        color: white;
        transform: translateY(100%);
        transition: transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    
    .netflix-card:hover .card-content {
        transform: translateY(0);
    }
    
    .card-title {
        font-size: 1rem;
        font-weight: 700;
        margin: 0 0 8px 0;
        line-height: 1.3;
        text-shadow: 0 2px 4px rgba(0,0,0,0.5);
    }
    
    .card-subtitle {
        font-size: 0.85rem;
        color: rgba(255,255,255,0.8);
        margin: 0;
        font-weight: 500;
    }
    
    /* Platform-specific gradient accents */
    .netflix-accent {
        background: linear-gradient(135deg, #e50914 0%, #b20710 100%);
    }
    
    .amazon-accent {
        background: linear-gradient(135deg, #ff9900 0%, #cc7700 100%);
    }
    
    .steam-accent {
        background: linear-gradient(135deg, #1b2838 0%, #2a475e 100%);
    }
    
    /* Hero video improvements */
    .hero-video {
        position: relative;
        width: 100%;
        height: 0;
        padding-bottom: 35%;
        margin-bottom: 3rem;
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 15px 50px rgba(0,0,0,0.6);
    }
    
    .hero-video iframe {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        border: none;
        border-radius: 15px;
    }
    
    .hero-info {
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        padding: 2rem;
        background: linear-gradient(transparent, rgba(15,15,35,0.95));
        color: white;
        z-index: 1;
    }
    
    .hero-info h2 {
        font-size: 2.5rem;
        margin-bottom: 0.8rem;
        font-weight: 800;
    }
    
    .hero-info p {
        font-size: 1.1rem;
        margin-bottom: 1.2rem;
        opacity: 0.9;
        line-height: 1.6;
    }
    
    /* Row spacing */
    .row-container {
        margin-bottom: 4rem;
    }
    
    /* Responsive improvements */
    @media (max-width: 768px) {
        .hero-title {
            font-size: 2rem;
        }
        
        .section-title {
            font-size: 1.8rem;
        }
        
        .netflix-card {
            max-width: 160px;
        }
        
        .hero-video {
            padding-bottom: 45%;
        }
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🎬🎮 Dernières sorties par plateforme")

# Utility functions
def load_data(platform_name):
    path = Path("assets/dataset/platforms") / f"{platform_name}.json"
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def image_to_base64(path: Path) -> str:
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

# Hero feature: showcase Lost in Starlight trailer
netflix_data = load_data("Netflix")
if netflix_data:
    # Find Lost in Starlight in the data
    hero = next((item for item in netflix_data if "Lost in Starlight" in item["title"]), netflix_data[0])
    
    st.markdown(
        f"""
        <div class="hero-video">
            <iframe
                src="https://www.youtube.com/embed/pV_-COLJOiY?autoplay=1&mute=1&controls=1&showinfo=0&rel=0"
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                allowfullscreen
            ></iframe>
            <div class="hero-info">
                <h2>{hero['title']}</h2>
                <p>{hero.get('type','')}</p>
                <a href="{hero['url']}" target="_blank" class="btn-primary">▶ Regarder maintenant</a>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# Display each platform in a carousel
platforms = [
    ("Netflix", "netflix-accent"),
    ("Amazon Prime", "amazon-accent"),
    ("Steam", "steam-accent"),
]

for platform, accent_class in platforms:
    st.markdown(f'<h3 class="section-title">{platform}</h3>', unsafe_allow_html=True)
    data = load_data(platform)
    
    # Start row container for spacing
    st.markdown('<div class="row-container">', unsafe_allow_html=True)
    
    # Display items in columns
    for i in range(0, len(data), 6):
        cols = st.columns(6, gap="medium")
        for j in range(6):
            if i + j < len(data):
                with cols[j]:
                    item = data[i + j]
                    path = Path("assets/img") / platform / item["image"]
                    if not path.exists():
                        continue
                    b64 = image_to_base64(path)
                    st.markdown(
                        f"""
                        <div class="netflix-card">
                            <a href="{item['url']}" target="_blank" style="text-decoration: none;">
                                <div class="card-image-container">
                                    <img src="data:image/jpeg;base64,{b64}" class="card-image" />
                                    <div class="card-overlay"></div>
                                    <div class="card-content">
                                        <div class="card-title">{item['title']}</div>
                                        <div class="card-subtitle">{item.get('type','')}</div>
                                    </div>
                                </div>
                            </a>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
    
    # Close row container
    st.markdown('</div>', unsafe_allow_html=True)
