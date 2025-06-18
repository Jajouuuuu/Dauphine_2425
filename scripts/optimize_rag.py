#!/usr/bin/env python3
import sys
import os
from pathlib import Path
import time
import json

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from domain.adapter.json_media_repository import JSONMediaRepository
from application.rag_factory import create_rag_service
from config.rag_config import VECTOR_DB_CONFIG, TEXT_EMBEDDING_MODELS, PERFORMANCE_CONFIG

def main():
    """Main optimization routine"""
    print("Starting RAG Optimization...")
    print("=" * 50)
    
    # Paths to your data
    movies_path = "data/processed/movies.json"
    games_path = "data/processed/games.json"
    
    # Check if data files exist
    if not os.path.exists(movies_path):
        print(f"Movies data not found at: {movies_path}")
        return
    
    if not os.path.exists(games_path):
        print(f"Games data not found at: {games_path}")
        return
    
    print("Found data files:")
    print(f"   Movies: {movies_path}")
    print(f"   Games: {games_path}")
    print()
    
    # Initialize repository
    print("Loading media repository...")
    start_time = time.time()
    
    repository = JSONMediaRepository(
        movies_path=movies_path,
        games_path=games_path
    )
    
    load_time = time.time() - start_time
    total_items = len(repository.get_all_items())
    
    print(f"Loaded {total_items:,} media items in {load_time:.2f}s")
    print()
    
    # Initialize enhanced RAG service (this will automatically index data)
    print("Initializing Enhanced RAG Service...")
    print("   - Loading embedding models (CLIP + SentenceTransformers)")
    print("   - Setting up ChromaDB vector database")
    print("   - Computing embeddings for all items...")
    print("   (This may take several minutes for large datasets)")
    print()
    
    start_time = time.time()
    
    rag_service = create_rag_service(
        repository,
        db_path=VECTOR_DB_CONFIG["db_path"],
        text_model=TEXT_EMBEDDING_MODELS["fast"],
        batch_size=PERFORMANCE_CONFIG["batch_size"]
    )
    
    setup_time = time.time() - start_time
    
    print(f"RAG service initialized in {setup_time:.2f}s")
    print()
    
    # Test the system
    print("Testing RAG Performance...")
    
    # Test text search
    test_queries = [
        "action movies with superheroes",
        "scary horror games",
        "romantic comedies",
        "space exploration games"
    ]
    
    total_query_time = 0
    
    for query in test_queries:
        start_time = time.time()
        response = rag_service.query_with_text(query)
        query_time = time.time() - start_time
        total_query_time += query_time
        
        print(f"   Query: '{query}' - {query_time:.3f}s")
    
    avg_query_time = total_query_time / len(test_queries)
    print(f"   Average query time: {avg_query_time:.3f}s")
    print()
    
    # Performance summary
    print("Optimization Summary:")
    print("=" * 30)
    print(f"Total media items: {total_items:,}")
    print(f"Setup time: {setup_time:.2f}s")
    print(f"Average query time: {avg_query_time:.3f}s")
    print("Vector database: ./chroma_db")
    print("Text embeddings: sentence-transformers")
    print("Visual embeddings: CLIP ViT-B/32")
    print()
    
    # Usage instructions
    print("🎯 Usage Instructions:")
    print("=" * 25)
    print("1. Your RAG system is now optimized!")
    print("2. Start the Streamlit app: streamlit run web_app/Home.py")
    print("3. Go to the Chat page to test the enhanced RAG")
    print("4. Try both text queries and image uploads")
    print()
    print("Tips for best performance:")
    print("   - Keep the chroma_db folder for persistence")
    print("   - Larger batch sizes improve indexing speed")
    print("   - GPU acceleration works if PyTorch + CUDA available")
    print()
    
    print("RAG Optimization Complete!")

if __name__ == "__main__":
    main() 