import streamlit as st
import json
from pathlib import Path
import base64

# Page configuration
st.set_page_config(page_title="Sorties Multi-Plateformes", layout="wide")
st.title("🎬🎮 Dernières sorties par plateforme")

# Custom CSS for header, hero, and carousel
st.markdown(
    """
    <style>
    /* Hero section */
    .hero {
        position: relative;
        width: 100%;
        height: 60vh;
        background-size: cover;
        background-position: center;
        margin-bottom: 2rem;
        border-radius: 0.5rem;
        overflow: hidden;
    }
    .hero-overlay {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(to bottom, rgba(0,0,0,0.2), rgba(0,0,0,0.5));
    }
    .hero-content {
        position: absolute;
        bottom: 15%;
        left: 5%;
        z-index: 1;
        color: #fff;
    }
    .hero-title {
        font-size: 2.5rem;
        font-weight: bold;
        margin: 0;
    }
    .hero-subtitle {
        font-size: 1rem;
        margin: 0.5rem 0 1rem;
    }
    .btn-primary {
        display: inline-block;
        padding: 0.8em 2em;
        font-size: 1.2rem;
        border-radius: 0.3rem;
        text-decoration: none;
        font-weight: bold;
        background-color: #e50914;
        color: #ffffff;
        transition: background-color 0.2s ease;
    }
    .btn-primary:hover {
        background-color: #f40612;
    }
    /* Section titles */
    .section-title {
        font-size: 1.5rem;
        margin: 2.5rem 0 1rem;  /* Increased top margin for more space between sections */
        color: #fff;
    }
    /* Netflix-style card */
    .netflix-card {
        position: relative;
        width: 100%;
        max-width: 200px;
        margin: 0 auto;
        transition: transform 0.3s ease, z-index 0s 0.3s;
    }
    .netflix-card:hover {
        transform: scale(1.2);
        z-index: 100;
        transition: transform 0.3s ease, z-index 0s;
    }
    .card-image-container {
        position: relative;
        width: 100%;
        padding-top: 150%; /* 2:3 aspect ratio */
        overflow: hidden;
        border-radius: 4px;
        margin-bottom: 1.5rem; 
        box-shadow: 0 2px 10px rgba(0,0,0,0.3);
    }
    .card-image {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        object-fit: cover;
    }
    .card-overlay {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(to bottom, rgba(0,0,0,0), rgba(0,0,0,0.8));
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
        padding: 10px;
        color: white;
        transform: translateY(100%);
        transition: transform 0.3s ease;
        background: linear-gradient(to top, rgba(0,0,0,0.9), rgba(0,0,0,0));
    }
    .netflix-card:hover .card-content {
        transform: translateY(0);
    }
    .card-title {
        font-size: 0.9rem;
        font-weight: bold;
        margin: 0;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    .card-subtitle {
        font-size: 0.8rem;
        color: #ccc;
        margin-top: 4px;
    }
    /* Hide scrollbar */
    .element-container::-webkit-scrollbar {
        display: none;
    }
    .element-container {
        scrollbar-width: none;
    }
    .hero-video {
        position: relative;
        width: 100%;
        height: 0;
        padding-bottom: 40%; /* Reduced from 56.25% to 40% for a shorter height */
        margin-bottom: 2rem;
        border-radius: 0.5rem;
        overflow: hidden;
    }
    .hero-video iframe {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        border: none;
        border-radius: 0.5rem;
    }
    .hero-info {
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        padding: 1.5rem; /* Slightly reduced padding */
        background: linear-gradient(transparent, rgba(0,0,0,0.8));
        color: white;
        z-index: 1;
    }
    .hero-info h2 {
        font-size: 2rem; /* Slightly reduced font size */
        margin-bottom: 0.5rem;
    }
    .hero-info p {
        font-size: 1rem; /* Slightly reduced font size */
        margin-bottom: 0.8rem;
        opacity: 0.9;
    }
    /* Content row spacing */
    .row-container {
        margin-bottom: 3rem;  /* Add space between rows */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Header navigation bar
st.markdown(
    """
    <div class="header">
    </div>
    """,
    unsafe_allow_html=True
)

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
    
    # YouTube trailer embed with responsive container
    st.markdown(
        """
        <style>
        .hero-video {
            position: relative;
            width: 100%;
            height: 0;
            padding-bottom: 40%; /* Reduced from 56.25% to 40% for a shorter height */
            margin-bottom: 2rem;
            border-radius: 0.5rem;
            overflow: hidden;
        }
        .hero-video iframe {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            border: none;
            border-radius: 0.5rem;
        }
        .hero-info {
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            padding: 1.5rem; /* Slightly reduced padding */
            background: linear-gradient(transparent, rgba(0,0,0,0.8));
            color: white;
            z-index: 1;
        }
        .hero-info h2 {
            font-size: 2rem; /* Slightly reduced font size */
            margin-bottom: 0.5rem;
        }
        .hero-info p {
            font-size: 1rem; /* Slightly reduced font size */
            margin-bottom: 0.8rem;
            opacity: 0.9;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    
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
                <a href="{hero['url']}" target="_blank" class="btn-primary">Watch Now</a>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# Display each platform in a carousel
platforms = [
    ("#netflix", "Netflix"),
    ("#amazon", "Amazon Prime"),
    ("#steam", "Steam"),
]

for anchor, platform in platforms:
    st.markdown(f'<h3 id="{anchor[1:]}" class="section-title">{platform}</h3>', unsafe_allow_html=True)
    data = load_data(platform)
    
    # Start row container for spacing
    st.markdown('<div class="row-container">', unsafe_allow_html=True)
    
    # Display items in columns
    for i in range(0, len(data), 6):
        cols = st.columns(6)
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
