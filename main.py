#!/usr/bin/env python3
"""
Main Application Entry Point
- Initializes RAG system with part1 dataset for fast startup
- Precomputes embeddings if needed
- Starts Streamlit web interface
"""

import warnings
import os
import sys
import time
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