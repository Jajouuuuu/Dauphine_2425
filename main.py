#!/usr/bin/env python3
"""
Main Application Entry Point
- Initializes RAG system with part1 dataset for fast startup
- Starts GraphQL server, REST API, and Streamlit web interface
"""

import warnings
import os
import sys
import time
import threading
import requests
from pathlib import Path

# Suppress warnings
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", message=".*torch.classes.*")

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def setup_rag_system():
    """Initialize RAG system with part1 dataset"""
    print("🚀 Initializing RAG System...")
    print("=" * 50)

    from domain.adapter.json_media_repository import JSONMediaRepository
    from domain.service.rag_service_impl import RAGServiceImpl

    movies_path = "data/processed/chunks/movies_part1.json"
    games_path = "data/processed/chunks/games_part1.json"

    if not os.path.exists(movies_path) or not os.path.exists(games_path):
        print("⚠️  Part1 chunks not found, using full dataset...")
        movies_path = "data/processed/movies.json"
        games_path = "data/processed/games.json"

    if not os.path.exists(movies_path) or not os.path.exists(games_path):
        print("❌ No data files found! Please check your data directory.")
        return False

    try:
        print(f"📚 Loading data from:\n   - Movies: {movies_path}\n   - Games: {games_path}")
        start_time = time.time()

        repository = JSONMediaRepository(
            movies_path=movies_path,
            games_path=games_path
        )

        rag_service = RAGServiceImpl(
            media_repository=repository,
            db_path="./chroma_db",
            text_model="all-MiniLM-L6-v2",
            enable_visual=False,
            batch_size=32
        )

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
        print(f"   - Database: ChromaDB\n")

        return True

    except Exception as e:
        print(f"❌ Error setting up RAG system: {e}")
        return False

def check_neo4j_connection():
    """Check if Neo4j is available for community features"""
    try:
        from config.env_config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD
        from neo4j import GraphDatabase
        
        if not all([NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD]):
            print("⚠️  Neo4j environment variables not set - Community features will be limited")
            return False
            
        driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
        
        # Test connection
        with driver.session() as session:
            result = session.run("RETURN 1")
            result.single()
        
        driver.close()
        print("✅ Neo4j connection successful - Community features available")
        return True
        
    except Exception as e:
        print(f"⚠️  Neo4j connection failed: {e}")
        print("   Community features will be limited")
        return False

def start_graphql_server():
    """Start GraphQL server in a separate thread"""
    try:
        print("🔗 Starting GraphQL server on port 5050...")
        from interface.graphql.server import app
        app.run(host='0.0.0.0', port=5050, debug=False, use_reloader=False)
    except Exception as e:
        print(f"❌ Error starting GraphQL server: {e}")

def start_rest_api():
    """Start REST API server in a separate thread"""
    try:
        print("🌐 Starting REST API server on port 8000...")
        import uvicorn
        from env_config import EnvConfig
        uvicorn.run(
            "rest.api:rest_api", 
            host=EnvConfig.get_api_host(), 
            port=EnvConfig.get_api_port_int(),
            log_level="warning"
        )
    except Exception as e:
        print(f"❌ Error starting REST API: {e}")

def wait_for_service(url, service_name, timeout=30):
    """Wait for a service to become available"""
    print(f"⏳ Waiting for {service_name} to start...")
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print(f"✅ {service_name} is ready!")
                return True
        except requests.exceptions.RequestException:
            pass
        time.sleep(1)
    
    print(f"⚠️  {service_name} did not start within {timeout} seconds")
    return False

def main():
    """Main application entry point"""
    print("🎬 MEDIA FINDER - Complete RAG Assistant with Community Features")
    print("=" * 70)

    # Setup RAG system
    if not setup_rag_system():
        print("❌ Failed to initialize RAG system. Please check your setup.")
        sys.exit(1)

    # Check Neo4j for community features
    neo4j_available = check_neo4j_connection()
    
    if not neo4j_available:
        print("⚠️  Neo4j not available. Run 'python setup_neo4j.py' to set it up.")
        print("   Community features will be limited without Neo4j.")

    print("\n🚀 Starting all services...")
    print("=" * 50)

    # Start GraphQL server in background thread
    graphql_thread = threading.Thread(target=start_graphql_server, daemon=True)
    graphql_thread.start()
    
    # Start REST API in background thread  
    rest_thread = threading.Thread(target=start_rest_api, daemon=True)
    rest_thread.start()

    # Wait for services to start
    graphql_ready = wait_for_service("http://localhost:5050/graphql", "GraphQL Server", timeout=15)
    rest_ready = wait_for_service("http://localhost:8000/docs", "REST API", timeout=10)

    print("\n🌟 Service Status:")
    print(f"   - RAG System: ✅ Ready")
    print(f"   - GraphQL Server: {'✅ Ready' if graphql_ready else '❌ Failed'}")
    print(f"   - REST API: {'✅ Ready' if rest_ready else '❌ Failed'}")
    print(f"   - Neo4j Database: {'✅ Ready' if neo4j_available else '⚠️  Limited'}")

    if not graphql_ready:
        print("\n⚠️  GraphQL server failed to start. Community features may not work.")
        print("   The app will continue with limited functionality.")

    print("\n🌐 Starting Streamlit Web Interface...")
    print("   Navigate to: http://localhost:8501")
    print("   Available pages:")
    print("   - 🏠 Home: Main dashboard")
    print("   - 💬 Chat: RAG-powered conversations")
    print("   - 🔍 Discover: Content exploration") 
    print("   - 👥 Community: Social features" + (" (limited)" if not (neo4j_available and graphql_ready) else ""))
    print("   - ℹ️  About: System information")
    print("\n   Press Ctrl+C to stop all services")
    print("=" * 70)

    # Start Streamlit (main interface)
    try:
        os.system("streamlit run web_app/home.py")
    except KeyboardInterrupt:
        print("\n👋 Shutting down all services...")
    except Exception as e:
        print(f"❌ Error starting Streamlit: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()