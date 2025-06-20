from typing import List, Optional, Dict, Any
import os
import numpy as np
import time
from pathlib import Path
import threading
from functools import lru_cache
import torch
from PIL import Image
import requests
import chromadb
from sentence_transformers import SentenceTransformer
import cohere
from dotenv import load_dotenv
import cv2
from io import BytesIO

# Try to import CLIP
try:
    import clip
    CLIP_AVAILABLE = True
except ImportError:
    CLIP_AVAILABLE = False

from domain.port.rag_service import RAGService
from domain.port.media_repository import MediaRepository
from domain.model.media_item import MediaItem

load_dotenv()

class RAGServiceImpl(RAGService):
    """
    Production-ready RAG service for movies/games with COHERE integration.
    - Text: SentenceTransformer + ChromaDB
    - Visual: CLIP (optional) + ChromaDB
    - LLM: COHERE for response generation
    """
    
    def __init__(self, media_repository: MediaRepository, db_path: str = "./chroma_db", 
                 text_model: str = "all-MiniLM-L6-v2", enable_visual: bool = False, 
                 batch_size: int = 32, ensure_index: bool = True):
        self.media_repository = media_repository
        self.batch_size = batch_size
        self.enable_visual = enable_visual
        self.db_path = db_path
        self.text_model = text_model
        
        # Initialize COHERE client
        cohere_api_key = os.getenv('COHERE_API_KEY')
        if not cohere_api_key:
            raise ValueError("COHERE_API_KEY not found in environment variables")
        self.cohere_client = cohere.Client(cohere_api_key)
        
        # Device setup
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        # Threading locks for thread safety
        self.embedding_lock = threading.Lock()
        self.db_lock = threading.Lock()
        
        # Initialize ChromaDB
        self.chroma_client = chromadb.PersistentClient(path=db_path)
        self.text_collection = self.chroma_client.get_or_create_collection(
            name="text_embeddings",
            metadata={"hnsw:space": "cosine"}
        )
        
        # Only create visual collection if enabled
        if self.enable_visual:
            self.visual_collection = self.chroma_client.get_or_create_collection(
                name="visual_embeddings",
                metadata={"hnsw:space": "cosine"}
            )
            # Initialize CLIP if available
            if CLIP_AVAILABLE:
                self.clip_model, self.clip_preprocess = clip.load("ViT-B/32", device=self.device)
                self.clip_available = True
            else:
                self.clip_available = False
        else:
            self.visual_collection = None
            self.clip_available = False
        
        # Initialize text encoder
        self.text_encoder = SentenceTransformer(text_model, device=self.device)
        
        # Only index if ensure_index is True
        if ensure_index:
            self._ensure_data_indexed()

    def _ensure_data_indexed(self):
        """Ensure all media items are indexed in the vector database"""
        media_items = self.media_repository.get_all_items()
        text_count = self.text_collection.count()
        
        # Index text embeddings if needed
        if text_count < len(media_items):
            print(f"Indexing {len(media_items) - text_count} new text embeddings...")
            self._index_text_embeddings(media_items)
        
        # Index visual embeddings if enabled and needed
        if self.enable_visual and self.visual_collection:
            visual_count = self.visual_collection.count()
            items_with_posters = [i for i in media_items if getattr(i, 'poster_url', None)]
            if visual_count < len(items_with_posters):
                print(f"Indexing {len(items_with_posters) - visual_count} new visual embeddings...")
                self._index_visual_embeddings(media_items)

    def _index_text_embeddings(self, media_items: List[MediaItem]):
        """Index text embeddings for media items"""
        for i in range(0, len(media_items), self.batch_size):
            batch = media_items[i:i+self.batch_size]
            texts = [getattr(item, 'content_for_embedding', self._create_text_for_embedding(item)) for item in batch]
            ids = [f"text_{item.id}" for item in batch]
            metadatas = [self._create_metadata(item) for item in batch]
            
            # Generate embeddings
            with self.embedding_lock:
                embeddings = self.text_encoder.encode(
                    texts,
                    show_progress_bar=False,
                    convert_to_numpy=True,
                    normalize_embeddings=True
                )
            
            # Add to collection
            with self.db_lock:
                self.text_collection.add(
                    embeddings=embeddings.tolist(),
                    documents=texts,
                    metadatas=metadatas,
                    ids=ids
                )

    def _index_visual_embeddings(self, media_items: List[MediaItem]):
        """Index visual embeddings for media items with posters"""
        if not self.enable_visual or not self.visual_collection:
            return
            
        items_with_posters = [item for item in media_items if getattr(item, 'poster_url', None)]
        
        for i in range(0, len(items_with_posters), self.batch_size):
            batch = items_with_posters[i:i+self.batch_size]
            embeddings, ids, metadatas, docs = [], [], [], []
            
            for item in batch:
                emb = self._get_visual_embedding(item.poster_url)
                if emb is not None:
                    embeddings.append(emb.tolist())
                    ids.append(f"visual_{item.id}")
                    metadatas.append(self._create_metadata(item))
                    docs.append(f"{item.title} - {item.type}")
            
            if embeddings:
                with self.db_lock:
                    self.visual_collection.add(
                        embeddings=embeddings,
                        documents=docs,
                        metadatas=metadatas,
                        ids=ids
                    )

    def _create_text_for_embedding(self, item: MediaItem) -> str:
        """Create text representation for embedding"""
        parts = [
            f"Title: {item.title}",
            f"Type: {item.type}",
            f"Genres: {', '.join(getattr(item, 'genres', []))}",
            f"Release: {getattr(item, 'release_date', '')}",
            f"Rating: {getattr(item, 'vote_average', 0)}/10",
            f"Description: {item.description}"
        ]
        return " | ".join(parts)

    def _create_metadata(self, item: MediaItem) -> Dict[str, Any]:
        """Create metadata dictionary for ChromaDB"""
        return {
            "id": item.id,
            "title": item.title,
            "type": item.type,
            "release_date": getattr(item, 'release_date', ''),
            "genres": str(getattr(item, 'genres', [])),
            "vote_average": float(getattr(item, 'vote_average', 0)),
            "popularity": float(getattr(item, 'popularity', 0))
        }

    def _get_visual_embedding(self, image_url: str) -> Optional[np.ndarray]:
        """Get visual embedding for an image URL"""
        if not self.clip_available:
            return None
            
        try:
            response = requests.get(image_url, timeout=10)
            image = Image.open(BytesIO(response.content))
            image_input = self.clip_preprocess(image).unsqueeze(0).to(self.device)
            
            with torch.no_grad():
                embedding = self.clip_model.encode_image(image_input)
                embedding = embedding.cpu().numpy().flatten()
                embedding = embedding / np.linalg.norm(embedding)
                
            return embedding
        except Exception as e:
            print(f"Error processing image {image_url}: {e}")
            return None

    def query_with_text(self, query: str, media_type: Optional[str] = None) -> str:
        """Query the RAG system with text input"""
        try:
            # Generate query embedding
            query_embedding = self.text_encoder.encode([query], normalize_embeddings=True)[0]
            
            # Search in vector database
            where_filter = {"type": media_type} if media_type else None
            results = self.text_collection.query(
                query_embeddings=[query_embedding.tolist()],
                n_results=5,
                where=where_filter
            )
            
            # Convert results to MediaItem objects
            relevant_items = []
            for i, metadata in enumerate(results['metadatas'][0]):
                item = self.media_repository.get_item_by_id(metadata['id'])
                if item:
                    relevant_items.append(item)
            
            # Generate response using COHERE
            return self._generate_response(query, relevant_items, media_type)
            
        except Exception as e:
            print(f"Error in text query: {e}")
            return "I'm experiencing technical difficulties. Could you please rephrase your question?"

    def query_with_image(self, image_data, media_type: Optional[str] = None) -> str:
        """Query the RAG system with image input"""
        if not self.enable_visual or not self.visual_collection:
            return "Visual search is not enabled. Please use text search instead."
            
        try:
            # Handle different image input types
            if hasattr(image_data, 'read'):
                # Streamlit uploaded file
                image_bytes = image_data.read()
                image_data.seek(0)  # Reset file pointer
                image = Image.open(BytesIO(image_bytes))
            else:
                # Direct image data
                image = Image.open(BytesIO(image_data))
            
            # Get visual embedding
            if self.clip_available:
                image_input = self.clip_preprocess(image).unsqueeze(0).to(self.device)
                with torch.no_grad():
                    query_embedding = self.clip_model.encode_image(image_input)
                    query_embedding = query_embedding.cpu().numpy().flatten()
                    query_embedding = query_embedding / np.linalg.norm(query_embedding)
                method = "CLIP ViT-B/32"
            else:
                return "Visual search requires CLIP. Please use text search instead."
            
            # Search in visual database
            where_filter = {"type": media_type} if media_type else None
            results = self.visual_collection.query(
                query_embeddings=[query_embedding.tolist()],
                n_results=5,
                where=where_filter
            )
            
            # Convert results to MediaItem objects
            relevant_items = []
            for metadata in results['metadatas'][0]:
                item = self.media_repository.get_item_by_id(metadata['id'])
                if item:
                    relevant_items.append(item)
            
            return self._generate_visual_response(relevant_items, media_type, method)
            
        except Exception as e:
            print(f"Error in image query: {e}")
            return "I had trouble analyzing this image. Please try a different one."

    def _generate_response(self, query: str, items: List[MediaItem], media_type: Optional[str]) -> str:
        """Generate response using COHERE"""
        if not items:
            return "I couldn't find any relevant content for your search. Please try different keywords."
        
        # Create context from retrieved items
        context = "\n".join([self._format_media_item(item) for item in items])
        content_type = 'movies' if media_type == 'movie' else 'games' if media_type == 'game' else 'movies and games'
        
        # Generate response with COHERE
        try:
            response = self.cohere_client.chat(
                message=f"User question: '{query}'\n\nPlease provide a helpful and engaging answer using the provided context.",
                preamble=f"""You are an expert assistant in {content_type}.\n\nGuidelines:\n- Be conversational and engaging\n- Reference specific titles from the context\n- Clearly explain your recommendations\n- Connect information between multiple items when relevant\n- Provide insights on themes, genres, or trends\n- Respond in English\n\nContext:\n{context}""",
                temperature=0.8,
                max_tokens=800
            )
            return response.text
        except Exception as e:
            print(f"Error generating COHERE response: {e}")
            return "I'm having trouble with the text generation service. Here are the relevant items I found:\n\n" + context

    def _generate_visual_response(self, items: List[MediaItem], media_type: Optional[str], method: str) -> str:
        """Generate visual analysis response using COHERE"""
        if not items:
            return "I couldn't find any visually similar content to your image."
        
        context = "\n".join([self._format_media_item(item) for item in items])
        content_type = 'movies' if media_type == 'movie' else 'games' if media_type == 'game' else 'entertainment content'
        
        try:
            response = self.cohere_client.chat(
                message=f"Analyze the visual similarities between the uploaded image and these matches using {method}. Focus on visual elements, styles, and aesthetic connections.",
                preamble=f"""You are a visual analysis expert for {content_type}.\n\nAnalyze the visual connections focusing on:\n- Color palettes and lighting\n- Composition and style\n- Character design or poster aesthetics\n- Visual genre cues\n- Mood and atmosphere\n- Respond in English\n\nAnalysis method: {method}\nMost similar items found:\n{context}""",
                temperature=0.8,
                max_tokens=800
            )
            return response.text
        except Exception as e:
            print(f"Error generating visual COHERE response: {e}")
            return f"Visual analysis with {method}:\n\n" + context

    def _format_media_item(self, item: MediaItem) -> str:
        """Format media item for display"""
        if item.type == "game":
            return f"Title: {item.title} (Game)\nRelease: {getattr(item, 'release_date', '')}\nRating: {getattr(item, 'vote_average', 0)}/10\nGenres: {', '.join(getattr(item, 'genres', []))}\nSummary: {item.description}"
        else:
            return f"Title: {item.title} (Movie)\nRelease: {getattr(item, 'release_date', '')}\nRating: {getattr(item, 'vote_average', 0)}/10 ({getattr(item, 'vote_count', 0)} votes)\nGenres: {', '.join(getattr(item, 'genres', []))}\nSummary: {item.description}"

    def get_relevant_context(self, query: str, media_type: Optional[str] = None) -> List[MediaItem]:
        """Get relevant media items for a given query"""
        try:
            # Generate query embedding
            query_embedding = self.text_encoder.encode([query], normalize_embeddings=True)[0]
            
            # Search in vector database
            where_filter = {"type": media_type} if media_type else None
            results = self.text_collection.query(
                query_embeddings=[query_embedding.tolist()],
                n_results=10,  # Get more items for context
                where=where_filter
            )
            
            # Convert results to MediaItem objects
            relevant_items = []
            for metadata in results['metadatas'][0]:
                item = self.media_repository.get_item_by_id(metadata['id'])
                if item:
                    relevant_items.append(item)
            
            return relevant_items
            
        except Exception as e:
            print(f"Error getting relevant context: {e}")
            return []

    def get_stats(self) -> Dict[str, Any]:
        """Get system statistics"""
        stats = {
            "text_embeddings": self.text_collection.count(),
            "model": self.text_model,
            "vector_db": "ChromaDB",
            "visual_enabled": self.enable_visual,
            "clip_available": self.clip_available,
            "status": "ready"
        }
        
        if self.enable_visual and self.visual_collection:
            stats["visual_embeddings"] = self.visual_collection.count()
        
        return stats 