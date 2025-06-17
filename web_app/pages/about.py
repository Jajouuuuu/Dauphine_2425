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

# Page title
st.markdown('<h1 class="page-title">👥 Notre Équipe</h1>', unsafe_allow_html=True)

# Project Overview Section
st.markdown('<h2 class="section-title">À propos du projet</h2>', unsafe_allow_html=True)

st.markdown("""
    <div class="project-section">
        <h2>🎯 Vision du Projet</h2>
        <p>Notre équipe a développé un système de recommandation intelligent alimenté par la technologie RAG, 
        combinant la puissance des grands modèles de langage avec une base de données soigneusement organisée 
        de films et de jeux vidéo.</p>
        
        <h3>🚀 Fonctionnalités Clés</h3>
        <ul>
            <li>Conversation intelligente sur les films et jeux vidéo</li>
            <li>Recherche par similarité visuelle utilisant l'analyse d'affiches</li>
            <li>Recommandations cross-média innovantes</li>
            <li>Analyses détaillées et insights personnalisés</li>
            <li>Interface utilisateur moderne et intuitive</li>
        </ul>
    </div>
""", unsafe_allow_html=True)

# Technology Stack
st.markdown('<h2 class="section-title">💻 Notre Stack Technologique</h2>', unsafe_allow_html=True)
st.markdown("""
    <div class="tech-stack">
        <span class="tech-item">🐍 Python</span>
        <span class="tech-item">⚡ Streamlit</span>
        <span class="tech-item">🤖 Cohere AI</span>
        <span class="tech-item">🔍 RAG</span>
        <span class="tech-item">👁️ Computer Vision</span>
        <span class="tech-item">📝 NLP</span>
        <span class="tech-item">🎨 Modern CSS</span>
        <span class="tech-item">📊 Data Analysis</span>
    </div>
""", unsafe_allow_html=True)

# Team members data
team_members = [
    {
        "name": "Abdelhalim",
        "role": "Lead AI Developer",
        "description": "Expert en implémentation RAG et intégration de modèles d'IA. Spécialisé dans l'optimisation des performances et l'architecture des systèmes intelligents.",
        "image": "https://api.dicebear.com/7.x/avataaars/svg?seed=Abdelhalim&backgroundColor=667eea"
    },
    {
        "name": "Fabien",
        "role": "Data Architect",
        "description": "Maître du traitement de données et de l'architecture système. Responsable de l'optimisation des pipelines de données et des performances backend.",
        "image": "https://api.dicebear.com/7.x/avataaars/svg?seed=Fabien&backgroundColor=764ba2"
    },
    {
        "name": "Jeanne-Emma",
        "role": "Full-Stack Designer",
        "description": "Leader du design UI/UX et développement full-stack. Créatrice de l'interface moderne et responsable de l'expérience utilisateur exceptionnelle.",
        "image": "https://api.dicebear.com/7.x/avataaars/svg?seed=JeanneEmma&backgroundColor=667eea"
    },
    {
        "name": "Leïla",
        "role": "ML Specialist",
        "description": "Experte en analyse de données et algorithmes de recommandation. Focus sur l'amélioration continue des modèles et la précision des suggestions.",
        "image": "https://api.dicebear.com/7.x/avataaars/svg?seed=Leila&backgroundColor=764ba2"
    }
]

# Display team members
st.markdown('<h2 class="section-title">🌟 Rencontrez l\'équipe</h2>', unsafe_allow_html=True)
st.markdown('<div class="team-section">', unsafe_allow_html=True)
for member in team_members:
    st.markdown(f"""
        <div class="team-member">
            <img src="{member['image']}" alt="{member['name']}">
            <h3>{member['name']}</h3>
            <div class="role">{member['role']}</div>
            <p>{member['description']}</p>
        </div>
    """, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Project Journey
st.markdown('<h2 class="section-title">🎯 Notre Parcours</h2>', unsafe_allow_html=True)
st.markdown("""
    <div class="project-section">
        <h2>📈 Étapes Clés du Développement</h2>
        <ul>
            <li><strong>Phase 1:</strong> Recherche approfondie et planification stratégique</li>
            <li><strong>Phase 2:</strong> Collecte et traitement intelligent des données</li>
            <li><strong>Phase 3:</strong> Implémentation avancée du système RAG</li>
            <li><strong>Phase 4:</strong> Développement UI/UX moderne et responsive</li>
            <li><strong>Phase 5:</strong> Tests rigoureux et optimisation des performances</li>
            <li><strong>Phase 6:</strong> Déploiement et amélioration continue</li>
        </ul>
        
        <h3>🎖️ Réalisations</h3>
        <p>En seulement quelques mois, notre équipe a créé une plateforme révolutionnaire qui transforme 
        la façon dont les utilisateurs découvrent et interagissent avec le contenu multimédia. 
        Notre approche innovante combine intelligence artificielle et design moderne pour offrir 
        une expérience utilisateur sans précédent.</p>
    </div>
""", unsafe_allow_html=True)