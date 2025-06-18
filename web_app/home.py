## This page is the home page of your front application
import streamlit as st
import sys
from pathlib import Path

# Add the project root to Python path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Import the navigation component
from web_app.components.navigation import render_top_navigation, create_page_navigation

# Configure the page
st.set_page_config(
    page_title="Media Finder - Home",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"  # Hide sidebar for top navigation
)

# Modern Netflix-like CSS
st.markdown("""
<style>
/* Global styling */
.stApp {
    background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
}

/* Hero section */
.hero-section {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 4rem 2rem;
    border-radius: 20px;
    margin: 2rem 0;
    color: white;
    text-align: center;
    box-shadow: 0 15px 40px rgba(102, 126, 234, 0.3);
    position: relative;
    overflow: hidden;
}

.hero-section::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><circle cx="20" cy="20" r="2" fill="white" opacity="0.1"/><circle cx="80" cy="30" r="1.5" fill="white" opacity="0.1"/><circle cx="40" cy="70" r="1" fill="white" opacity="0.1"/><circle cx="90" cy="80" r="2.5" fill="white" opacity="0.1"/></svg>');
    pointer-events: none;
}

.hero-content {
    position: relative;
    z-index: 1;
}

.hero-title {
    font-size: 3.5rem;
    font-weight: 800;
    margin-bottom: 1rem;
    text-shadow: 0 4px 8px rgba(0,0,0,0.3);
    background: linear-gradient(45deg, #ffffff, #f0f0ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.hero-subtitle {
    font-size: 1.3rem;
    margin-bottom: 2rem;
    opacity: 0.9;
    line-height: 1.6;
}

/* Feature cards */
.feature-card {
    background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255,255,255,0.2);
    border-radius: 20px;
    padding: 2.5rem 2rem;
    text-align: center;
    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    height: 280px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    position: relative;
    overflow: hidden;
}

.feature-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    opacity: 0;
    transition: all 0.3s ease;
    border-radius: 20px;
}

.feature-card:hover::before {
    opacity: 0.1;
}

.feature-card:hover {
    transform: translateY(-10px) scale(1.02);
    box-shadow: 0 20px 50px rgba(102, 126, 234, 0.4);
    border: 1px solid rgba(102, 126, 234, 0.5);
}

.feature-icon {
    font-size: 3rem;
    margin-bottom: 1.5rem;
    display: block;
    position: relative;
    z-index: 1;
}

.feature-title {
    font-size: 1.5rem;
    font-weight: 700;
    margin-bottom: 1rem;
    color: white;
    position: relative;
    z-index: 1;
}

.feature-description {
    font-size: 1rem;
    line-height: 1.6;
    color: rgba(255,255,255,0.8);
    position: relative;
    z-index: 1;
}

/* Call to action section */
.cta-section {
    background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
    border: 1px solid rgba(102, 126, 234, 0.3);
    border-radius: 20px;
    padding: 3rem 2rem;
    text-align: center;
    margin: 3rem 0;
    backdrop-filter: blur(10px);
}

.cta-title {
    font-size: 2rem;
    font-weight: 700;
    color: white;
    margin-bottom: 2rem;
}

/* Footer */
.footer {
    text-align: center;
    color: rgba(255,255,255,0.6);
    margin-top: 4rem;
    padding: 2rem 0;
    border-top: 1px solid rgba(255,255,255,0.1);
}

/* Responsive design */
@media (max-width: 768px) {
    .hero-title {
        font-size: 2.5rem;
    }
    
    .hero-subtitle {
        font-size: 1.1rem;
    }
    
    .feature-card {
        height: auto;
        padding: 2rem 1.5rem;
    }
}
</style>
""", unsafe_allow_html=True)

# Render the top navigation
render_top_navigation()

# Hero section
st.markdown("""
<div class="hero-section">
    <div class="hero-content">
        <h1 class="hero-title">MEDIA FINDER</h1>
        <p class="hero-subtitle">
            Discover the future of smart streaming. Our revolutionary AI helps you navigate 
            the infinite world of cinema and gaming to find exactly what you're looking for.
        </p>
    </div>
</div>
""", unsafe_allow_html=True)

# Features section
st.markdown("### ✨ Start to explore our features")

col1, col2, col3 = st.columns(3, gap="large")

with col1:
    st.markdown("""
    <div class="feature-card">
        <span class="feature-icon">🎬</span>
            <h3 class="feature-title">Multi-platform streaming</h3>
            <p class="feature-description">
                Explore Netflix, Amazon Prime, Disney+, and more. 
                Instantly find where to watch your favorite movies.
            </p>
</div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
    <span class="feature-icon">🤖</span>
    <h3 class="feature-title">Conversational AI</h3>
    <p class="feature-description">
        Chat with our intelligent assistant for personalized recommendations 
        based on your tastes.
    </p>
</div>

    """, unsafe_allow_html=True)

with col3:
   st.markdown("""
<div class="feature-card">
    <span class="feature-icon">👥</span>
    <h3 class="feature-title">Community</h3>
    <p class="feature-description">
        Share your discoveries with your community and explore 
        the latest trends together.
    </p>
</div>

""", unsafe_allow_html=True)

# Call to action section


# Navigation buttons
create_page_navigation()

# Footer
st.markdown("""
<div class="footer">
    <p>Media Finder © 2024 - Powered by AI for the ultimate streaming experience</p>
</div>
""", unsafe_allow_html=True)
