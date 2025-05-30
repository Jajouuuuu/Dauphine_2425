import streamlit as st

# Page config
st.set_page_config(
    page_title="Team - RAG Movies & Games",
    page_icon="👥",
    layout="wide"
)


# Custom CSS adjustments
st.markdown("""
    <style>
        /* Team member cards */
        .team-section {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 2rem;
            padding: 2rem 0;
        }
        
        .team-member {
            background-color: var(--background-card);
            border-radius: 10px;
            padding: 2rem;
            text-align: center;
            transition: transform 0.3s;
        }
        
        .team-member:hover {
            transform: translateY(-5px);
        }
        
        .team-member img {
            width: 120px;
            height: 120px;
            border-radius: 50%;
            margin-bottom: 1rem;
            border: 3px solid var(--primary-color);
        }
        
        .team-member h3 {
            color: var(--primary-color);
            margin: 0.5rem 0;
        }
        
        .team-member .role {
            color: var(--text-gray);
            font-size: 0.9rem;
            margin-bottom: 1rem;
        }
        
        /* Tech stack */
        .tech-stack {
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
            justify-content: center;
            margin: 2rem 0;
        }
        
        .tech-item {
            background-color: var(--background-card);
            color: var(--text-light);
            padding: 0.5rem 1rem;
            border-radius: 20px;
            font-size: 0.9rem;
            border: 1px solid var(--primary-color);
        }
        
        /* Project sections */
        .project-section {
            background-color: var(--background-card);
            padding: 2rem;
            border-radius: 10px;
            margin: 1rem 0;
        }
        
        .project-section h2 {
            color: var(--primary-color);
            margin-bottom: 1rem;
        }
    </style>
""", unsafe_allow_html=True)

# Project Overview Section
st.markdown('<h1 class="section-header">Meet Our Team</h1>', unsafe_allow_html=True)

st.markdown("""
    <div class="project-section">
        <h2>About the Project</h2>
        <p>Our team has developed an intelligent recommendation system powered by RAG technology, 
        combining the power of large language models with a curated database of movies and games.</p>
        
        <h3>Key Features</h3>
        <ul>
            <li>Intelligent conversation about movies and games</li>
            <li>Visual similarity search using poster analysis</li>
            <li>Cross-media recommendations</li>
            <li>Detailed insights about content</li>
        </ul>
    </div>
""", unsafe_allow_html=True)

# Technology Stack
st.markdown('<h2 class="section-header">Our Tech Stack</h2>', unsafe_allow_html=True)
st.markdown("""
    <div class="tech-stack">
        <span class="tech-item">Python</span>
        <span class="tech-item">Streamlit</span>
        <span class="tech-item">Cohere</span>
        <span class="tech-item">RAG</span>
        <span class="tech-item">Computer Vision</span>
        <span class="tech-item">Natural Language Processing</span>
    </div>
""", unsafe_allow_html=True)

# Team members data
team_members = [
    {
        "name": "Abdelhalim",
        "role": "dev 1",
        "description": "Specializing in RAG implementation and AI model integration",
        "image": "https://api.dicebear.com/7.x/avataaars/svg?seed=Abdelhalim"
    },
    {
        "name": "Fabien",
        "role": "dev 2",
        "description": "Expert in data processing and system architecture",
        "image": "https://api.dicebear.com/7.x/avataaars/svg?seed=Fabien"
    },
    {
        "name": "Jeanne-Emma",
        "role": "dev 3",
        "description": "Leading UI/UX design and full-stack implementation",
        "image": "https://api.dicebear.com/7.x/avataaars/svg?seed=JeanneEmma"
    },
    {
        "name": "Leïla",
        "role": "dev 4",
        "description": "Focusing on data analysis and recommendation algorithms",
        "image": "https://api.dicebear.com/7.x/avataaars/svg?seed=Leila"
    }
]

# Display team members
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
st.markdown('<h2 class="section-header">Our Journey</h2>', unsafe_allow_html=True)
st.markdown("""
    <div class="project-section">
        <h3>Key Milestones</h3>
        <ul>
            <li>Initial Research and Planning</li>
            <li>Data Collection and Processing</li>
            <li>RAG Implementation</li>
            <li>UI/UX Development</li>
            <li>Testing and Optimization</li>
        </ul>
    </div>
""", unsafe_allow_html=True)