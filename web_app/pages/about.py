import streamlit as st
import sys
from pathlib import Path

# Add the project root to Python path for imports
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Import the navigation component
from web_app.components.navigation import render_top_navigation

# Page config
st.set_page_config(
    page_title="Team - RAG Movies & Games",
    page_icon="👥",
    layout="wide",
    initial_sidebar_state="collapsed"  # Hide sidebar for top navigation
)

# Render the top navigation
render_top_navigation()

# Modern Netflix-like CSS for Teams page
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
            margin: 2rem 0 3rem;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            text-shadow: none;
        }
        
        /* Section titles */
        .section-title {
            font-size: 2.5rem;
            font-weight: 800;
            margin: 3rem 0 2rem;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
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
        
        /* Team member cards */
        .team-section {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
            gap: 2.5rem;
            padding: 2rem 0;
            margin: 2rem 0;
        }
        
        .team-member {
            background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(102, 126, 234, 0.3);
            border-radius: 20px;
            padding: 2.5rem;
            text-align: center;
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            position: relative;
            overflow: hidden;
        }
        
        .team-member::before {
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
        
        .team-member:hover::before {
            opacity: 0.1;
        }
        
        .team-member:hover {
            transform: translateY(-10px) scale(1.02);
            box-shadow: 0 20px 50px rgba(102, 126, 234, 0.4);
            border: 1px solid rgba(102, 126, 234, 0.6);
        }
        
        .team-member img {
            width: 120px;
            height: 120px;
            border-radius: 50%;
            margin-bottom: 1.5rem;
            border: 4px solid transparent;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            background-clip: border-box;
            transition: all 0.3s ease;
            position: relative;
            z-index: 1;
        }
        
        .team-member:hover img {
            transform: scale(1.1);
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.5);
        }
        
        .team-member h3 {
            font-size: 1.5rem;
            font-weight: 700;
            color: white;
            margin: 1rem 0 0.5rem;
            position: relative;
            z-index: 1;
        }
        
        .team-member .role {
            color: rgba(102, 126, 234, 0.9);
            font-size: 1rem;
            font-weight: 600;
            margin-bottom: 1rem;
            text-transform: uppercase;
            letter-spacing: 1px;
            position: relative;
            z-index: 1;
        }
        
        .team-member p {
            color: rgba(255,255,255,0.8);
            line-height: 1.6;
            font-size: 0.95rem;
            position: relative;
            z-index: 1;
        }
        
        /* Tech stack */
        .tech-stack {
            display: flex;
            flex-wrap: wrap;
            gap: 1rem;
            justify-content: center;
            margin: 3rem 0;
            padding: 2rem;
        }
        
        .tech-item {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 0.8rem 1.5rem;
            border-radius: 25px;
            font-size: 0.9rem;
            font-weight: 600;
            border: 1px solid rgba(255,255,255,0.2);
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        }
        
        .tech-item:hover {
            transform: translateY(-3px) scale(1.05);
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.5);
        }
        
        /* Project sections */
        .project-section {
            background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(102, 126, 234, 0.3);
            padding: 2.5rem;
            border-radius: 20px;
            margin: 2rem 0;
            transition: all 0.3s ease;
        }
        
        .project-section:hover {
            border: 1px solid rgba(102, 126, 234, 0.5);
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.2);
        }
        
        .project-section h2 {
            color: white;
            font-size: 1.8rem;
            font-weight: 700;
            margin-bottom: 1.5rem;
        }
        
        .project-section h3 {
            color: rgba(102, 126, 234, 0.9);
            font-size: 1.3rem;
            font-weight: 600;
            margin: 1.5rem 0 1rem;
        }
        
        .project-section p {
            color: rgba(255,255,255,0.8);
            line-height: 1.6;
            font-size: 1rem;
        }
        
        .project-section ul {
            color: rgba(255,255,255,0.8);
            line-height: 1.8;
        }
        
        .project-section li {
            margin-bottom: 0.5rem;
            position: relative;
            padding-left: 1.5rem;
        }
        
        .project-section li::before {
            content: '▶';
            position: absolute;
            left: 0;
            color: #667eea;
            font-size: 0.8rem;
        }
        
        /* Responsive design */
        @media (max-width: 768px) {
            .page-title {
                font-size: 2.5rem;
            }
            
            .section-title {
                font-size: 1.8rem;
            }
            
            .team-section {
                grid-template-columns: 1fr;
                gap: 2rem;
            }
            
            .team-member {
                padding: 2rem;
            }
        }
    </style>
""", unsafe_allow_html=True)

# Move the project title to the very top, centered
st.markdown('<h1 class="page-title">About Media Finder</h1>', unsafe_allow_html=True)

# Add more vertical space before the description
st.markdown('<div style="height: 1.5rem;"></div>', unsafe_allow_html=True)

# Project description, centered and with more spacing
st.markdown('''<div class="simple-section" style="text-align:center; margin-bottom:2.5rem;">
    <p style="font-size:1.15rem; line-height:1.7; max-width:600px; margin:0 auto;">
        <b>Media Finder</b> is a smart, AI-powered platform that helps you discover movies and games faster.<br>
        It combines the power of Retrieval-Augmented Generation (RAG), computer vision, and a modern UI to centralize your entertainment choices and reviews in one place.
    </p>
</div>''', unsafe_allow_html=True)

# Tech stack section with a clear header and more spacing
st.markdown('<div class="simple-section" style="text-align:center;">', unsafe_allow_html=True)
st.markdown('<h2 style="margin-bottom:1.5rem; color:#aab6ff; font-size:1.4rem;">Tech Stack</h2>', unsafe_allow_html=True)
st.markdown('''<div class="tech-stack" style="justify-content:center; margin-bottom:1.5rem;">
    <span class="tech-item">🐍 Python</span>
    <span class="tech-item">⚡ Streamlit</span>
    <span class="tech-item">🤖 Cohere AI</span>
    <span class="tech-item">🔍 RAG</span>
</div>''', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Team members data
team_members = [
    {
        "name": "Abdelhalim",
        "role": "Lead full-stack developer",
    },
    {
        "name": "Fabien",
        "role": "Data engineer",
    },
    {
        "name": "Jeanne-Emma",
        "role": "AI developper",
    },
]

# Display team members
st.markdown('<h2 class="section-title">Our team</h2>', unsafe_allow_html=True)
st.markdown('<div class="team-section">', unsafe_allow_html=True)
for member in team_members:
    st.markdown(f"""
        <div class="team-member">
            <h3>{member['name']}</h3>
            <div class="role">{member['role']}</div>
        </div>
    """, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

