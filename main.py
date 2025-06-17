<<<<<<< graphql-requests
import subprocess
import uvicorn
import os
import time
import requests
import sys
import shutil
from multiprocessing import Process
=======
#!/usr/bin/env python3
"""
Main Application Entry Point
- Initializes RAG system with part1 dataset for fast startup
- Precomputes embeddings if needed
- Starts Streamlit web interface
"""
>>>>>>> poc_rag

import warnings
import os
import sys
import time
from pathlib import Path

# Suppress warnings
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", message=".*torch.classes.*")

<<<<<<< graphql-requests
def run_streamlit():
    home_py_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'web_app/Home.py'))
    if not os.path.exists(home_py_path):
        raise FileNotFoundError(f"❌ Fichier introuvable : {home_py_path}")

    streamlit_executable = shutil.which("streamlit")
    if not streamlit_executable:
        possible_path = os.path.join(os.path.dirname(sys.executable), "Scripts", "streamlit.exe")
        if os.path.exists(possible_path):
            streamlit_executable = possible_path
        else:
            raise FileNotFoundError(
                "❌ Impossible de trouver l'exécutable 'streamlit'. Vérifie ton environnement virtuel ou le PATH.")
    if not streamlit_executable:
        raise FileNotFoundError("❌ Impossible de trouver l'exécutable 'streamlit'. Assure-toi qu'il est installé et dans le PATH.")

    subprocess.run([streamlit_executable, "run", home_py_path])

def run_graphql_server():
    from interface.graphql.server import app
    app.run(debug=True, port=5050, use_reloader=False)

def wait_for_graphql(host="localhost", port=5050, timeout=10):
    url = f"http://{host}:{port}/graphql"
    for _ in range(timeout * 2):
        try:
            r = requests.get(url)
            if r.status_code == 200:
                print("✅ GraphQL server is up.")
                return True
        except requests.exceptions.ConnectionError:
            pass
        time.sleep(0.5)
    raise RuntimeError("❌ GraphQL server did not start in time.")

if __name__ == "__main__":
    p1 = Process(target=run_uvicorn)
    p3 = Process(target=run_graphql_server)

    p1.start()
    p3.start()

    wait_for_graphql()

    p2 = Process(target=run_streamlit)
    p2.start()

    p1.join()
    p2.join()
    p3.join()
=======
# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def setup_rag_system():
    """Initialize RAG system with part1 dataset"""
    print("🚀 Initializing RAG System...")
    print("=" * 50)
    
    # Import after path setup
    from domain.adapter.json_media_repository import JSONMediaRepository
    from domain.service.rag_service_impl import RAGServiceImpl
    
    # Use part1 dataset for fast startup
    movies_path = "data/processed/chunks/movies_part1.json"
    games_path = "data/processed/chunks/games_part1.json"
    
    # Check if part1 files exist
    if not os.path.exists(movies_path) or not os.path.exists(games_path):
        print("⚠️  Part1 chunks not found, using full dataset...")
        movies_path = "data/processed/movies.json"
        games_path = "data/processed/games.json"
    
    if not os.path.exists(movies_path) or not os.path.exists(games_path):
        print("❌ No data files found! Please check your data directory.")
        return False
    
    try:
        print(f"📚 Loading data from:")
        print(f"   - Movies: {movies_path}")
        print(f"   - Games: {games_path}")
        
        start_time = time.time()
        
        # Initialize repository
        repository = JSONMediaRepository(
            movies_path=movies_path,
            games_path=games_path
        )
        
        # Initialize RAG service (text-only for fast startup)
        rag_service = RAGServiceImpl(
            media_repository=repository,
            db_path="./chroma_db",
            text_model="all-MiniLM-L6-v2",
            enable_visual=False,  # Disable visual for faster startup
            batch_size=32
        )
        
        # Check if we need to index data
        stats = rag_service.get_stats()
        total_items = len(repository.get_all_items())
        
        if stats["text_embeddings"] < total_items:
            print(f"🔄 Indexing {total_items} items...")
            rag_service._ensure_data_indexed()
        else:
            print(f"✅ Using existing embeddings ({stats['text_embeddings']} items)")
        
        setup_time = time.time() - start_time
        final_stats = rag_service.get_stats()
        
        print(f"✅ RAG System Ready!")
        print(f"   - Setup time: {setup_time:.2f}s")
        print(f"   - Text embeddings: {final_stats['text_embeddings']:,}")
        print(f"   - Model: {final_stats['model']}")
        print(f"   - Database: ChromaDB")
        print()
        
        return True
        
    except Exception as e:
        print(f"❌ Error setting up RAG system: {e}")
        return False

def main():
    """Main application entry point"""
    print("🎬 MEDIA FINDER - RAG Assistant")
    print("=" * 40)
    
    # Setup RAG system
    if setup_rag_system():
        print("🌐 Starting Streamlit application...")
        print("   Navigate to: http://localhost:8501")
        print("   Press Ctrl+C to stop")
        print()
        
        # Start Streamlit
        os.system("streamlit run web_app/home.py")
    else:
        print("❌ Failed to initialize RAG system. Please check your setup.")
        sys.exit(1)

if __name__ == "__main__":
    main()
>>>>>>> poc_rag
