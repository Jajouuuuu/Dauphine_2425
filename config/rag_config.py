"""
RAG System Configuration
Adjust these settings to optimize performance for your use case.
"""

# Vector Database Settings
VECTOR_DB_CONFIG = {
    "db_path": "./chroma_db",
    "collection_settings": {
        "hnsw_space": "cosine",  # cosine, l2, ip
        "hnsw_construction_ef": 200,  # Higher = better quality, slower build
        "hnsw_search_ef": 100,  # Higher = better recall, slower search
    }
}

# Text Embedding Models (choose based on performance needs)
TEXT_EMBEDDING_MODELS = {
    "fast": "all-MiniLM-L6-v2",  # Fastest, good quality
    "balanced": "all-mpnet-base-v2",  # Best balance
    "best": "all-MiniLM-L12-v2",  # Highest quality, slower
}

# Visual Embedding Models
VISUAL_EMBEDDING_MODELS = {
    "fast": "ViT-B/32",  # Fastest CLIP model
    "balanced": "ViT-B/16",  # Better quality
    "best": "ViT-L/14",  # Highest quality, requires more VRAM
}

# Search Configuration
SEARCH_CONFIG = {
    "text_search": {
        "top_k": 10,  # Number of results to retrieve
        "min_similarity": 0.3,  # Minimum similarity threshold
    },
    "visual_search": {
        "top_k": 8,  # Number of visual results
        "min_similarity": 0.2,
    }
}

# Generation Configuration
GENERATION_CONFIG = {
    "cohere": {
        "model": "command-r",
        "temperature": 0.8,
        "max_tokens": 800,
        "k": 5,
        "p": 0.75,
    }
}

# Performance Settings
PERFORMANCE_CONFIG = {
    "batch_size": 32,  # Batch size for embeddings
    "enable_gpu": True,  # Use GPU if available
    "cache_embeddings": True,  # Cache computed embeddings
    "parallel_processing": True,  # Use multiprocessing
    "num_workers": 4,  # Number of worker processes
}

# Model Selection (change these to tune performance)
CURRENT_CONFIG = {
    "text_model": TEXT_EMBEDDING_MODELS["fast"],  # Change to "balanced" or "best"
    "visual_model": VISUAL_EMBEDDING_MODELS["fast"],  # Change to "balanced" or "best"
    "enable_visual_search": True,
    "enable_text_search": True,
}

# Quality vs Speed Presets
PRESETS = {
    "maximum_speed": {
        "text_model": TEXT_EMBEDDING_MODELS["fast"],
        "visual_model": VISUAL_EMBEDDING_MODELS["fast"],
        "batch_size": 64,
        "top_k": 5,
    },
    "balanced": {
        "text_model": TEXT_EMBEDDING_MODELS["balanced"],
        "visual_model": VISUAL_EMBEDDING_MODELS["balanced"],
        "batch_size": 32,
        "top_k": 8,
    },
    "maximum_quality": {
        "text_model": TEXT_EMBEDDING_MODELS["best"],
        "visual_model": VISUAL_EMBEDDING_MODELS["best"],
        "batch_size": 16,
        "top_k": 12,
    }
}

def get_config(preset="balanced"):
    """Get configuration for a specific preset"""
    if preset in PRESETS:
        config = PRESETS[preset].copy()
        config.update({
            "vector_db": VECTOR_DB_CONFIG,
            "search": SEARCH_CONFIG,
            "generation": GENERATION_CONFIG,
            "performance": PERFORMANCE_CONFIG,
        })
        return config
    else:
        raise ValueError(f"Unknown preset: {preset}. Available: {list(PRESETS.keys())}")

def print_config_info():
    """Print information about configuration options"""
    print("🔧 RAG Configuration Options:")
    print("=" * 40)
    print("\n📊 Available Presets:")
    for preset, config in PRESETS.items():
        print(f"   • {preset:15} - {config['text_model']} + {config['visual_model']}")
    
    print(f"\n⚙️  Current Config: {CURRENT_CONFIG['text_model']} + {CURRENT_CONFIG['visual_model']}")
    print(f"🔍 Text Search: {'✅' if CURRENT_CONFIG['enable_text_search'] else '❌'}")
    print(f"🖼️  Visual Search: {'✅' if CURRENT_CONFIG['enable_visual_search'] else '❌'}")
    print(f"💾 Vector DB: {VECTOR_DB_CONFIG['db_path']}")
    print()
    
    print("💡 Performance Tips:")
    print("   • Use 'maximum_speed' for real-time applications")
    print("   • Use 'balanced' for most use cases")
    print("   • Use 'maximum_quality' for best results (slower)")
    print("   • Enable GPU for significant speed improvements")
    print("   • Increase batch_size if you have more RAM")

if __name__ == "__main__":
    print_config_info() 