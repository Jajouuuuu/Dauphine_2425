"""
RAGServiceImpl - Unified Retrieval-Augmented Generation Service
Hexagonal Architecture | Vector Search | LLM | Visual & Text Search

- Uses ChromaDB for vector search (text & visual collections)
- SentenceTransformer for text embeddings (GPU/CPU auto)
- CLIP for visual embeddings (if available, fallback to basic features)
- Cohere for LLM generation
- Efficient batch indexing
- Compatible with Streamlit and factory
- Implements domain.port.rag_service.RAGService
"""

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
    Unified RAG service for movies/games with text & visual search.
    - Text: SentenceTransformer + ChromaDB
    - Visual: CLIP (if available) + ChromaDB (fallback: basic features)
    - LLM: Cohere
    """
    def __init__(self, media_repository: MediaRepository, db_path: str = "./chroma_db", text_model: str = "all-MiniLM-L6-v2", batch_size: int = 64):
        self.media_repository = media_repository
        self.batch_size = batch_size
        self.cohere_client = cohere.Client(os.getenv('COHERE_API_KEY'))
        self.clip_available = CLIP_AVAILABLE
        self.db_path = db_path
        self.text_model = text_model
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.embedding_lock = threading.Lock()
        self.db_lock = threading.Lock()

        # Text encoder
        self.text_encoder = SentenceTransformer(text_model, device=self.device)
        if hasattr(self.text_encoder, 'max_seq_length'):
            self.text_encoder.max_seq_length = 256

        # CLIP
        if self.clip_available:
            try:
                self.clip_model, self.clip_preprocess = clip.load("ViT-B/32", device=self.device)
                if self.device == "cuda":
                    self.clip_model = self.clip_model.half()
            except Exception:
                self.clip_available = False

        # ChromaDB
        self.chroma_client = chromadb.PersistentClient(path=db_path)
        self.text_collection = self.chroma_client.get_or_create_collection(
            name="media_text_embeddings",
            metadata={"hnsw:space": "cosine"}
        )
        self.visual_collection = self.chroma_client.get_or_create_collection(
            name="media_visual_embeddings",
            metadata={"hnsw:space": "cosine"}
        )
        self._ensure_data_indexed()

    def _ensure_data_indexed(self):
        media_items = self.media_repository.get_all_items()
        text_count = self.text_collection.count()
        visual_count = self.visual_collection.count()
        if text_count < len(media_items):
            self._index_text_embeddings(media_items)
        if visual_count < len([i for i in media_items if getattr(i, 'poster_url', None)]):
            self._index_visual_embeddings(media_items)

    def _index_text_embeddings(self, media_items: List[MediaItem]):
        for i in range(0, len(media_items), self.batch_size):
            batch = media_items[i:i+self.batch_size]
            texts = [getattr(item, 'content_for_embedding', self._create_text_for_embedding(item)) for item in batch]
            ids = [f"text_{item.id}" for item in batch]
            metadatas = [self._create_metadata(item) for item in batch]
            with self.embedding_lock:
                embeddings = self.text_encoder.encode(
                    texts,
                    show_progress_bar=False,
                    convert_to_numpy=True,
                    normalize_embeddings=True
                )
            with self.db_lock:
                self.text_collection.add(
                    embeddings=embeddings.tolist(),
                    documents=texts,
                    metadatas=metadatas,
                    ids=ids
                )

    def _index_visual_embeddings(self, media_items: List[MediaItem]):
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
        return {
            "id": item.id,
            "title": item.title,
            "type": item.type,
            "release_date": getattr(item, 'release_date', ''),
            "genres": str(getattr(item, 'genres', [])),
            "vote_average": float(getattr(item, 'vote_average', 0)),
            "popularity": float(getattr(item, 'popularity', 0))
        }

    def _get_text_embedding(self, text: str) -> np.ndarray:
        with self.embedding_lock:
            return self.text_encoder.encode([text], normalize_embeddings=True)[0]

    @lru_cache(maxsize=1000)
    def _get_clip_embedding(self, image_url: str) -> Optional[np.ndarray]:
        if not self.clip_available:
            return self._get_basic_visual_embedding(image_url)
        try:
            if image_url.startswith('http'):
                response = requests.get(image_url, timeout=5, stream=True)
                response.raise_for_status()
                image = Image.open(BytesIO(response.content)).convert('RGB')
            else:
                image = Image.open(image_url).convert('RGB')
            image_input = self.clip_preprocess(image).unsqueeze(0).to(self.device)
            if self.device == "cuda":
                image_input = image_input.half()
            with torch.no_grad():
                image_features = self.clip_model.encode_image(image_input)
                image_features = image_features / image_features.norm(dim=-1, keepdim=True)
                return image_features.cpu().float().numpy().flatten()
        except Exception:
            return self._get_basic_visual_embedding(image_url)

    def _get_basic_visual_embedding(self, image_source) -> Optional[np.ndarray]:
        try:
            if isinstance(image_source, str):
                if image_source.startswith('http'):
                    response = requests.get(image_source, timeout=5, stream=True)
                    response.raise_for_status()
                    image = Image.open(BytesIO(response.content)).convert('RGB')
                else:
                    image = Image.open(image_source).convert('RGB')
            else:
                image = Image.open(image_source).convert('RGB')
            img_array = np.array(image)
            img_array = cv2.resize(img_array, (128, 128))
            features = []
            for channel in range(3):
                hist = cv2.calcHist([img_array], [channel], None, [16], [0, 256])
                features.extend(hist.flatten())
            gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
            features.extend([
                np.mean(gray),
                np.std(gray),
                np.min(gray),
                np.max(gray)
            ])
            embedding = np.zeros(512)
            embedding[:len(features)] = features[:len(embedding)]
            norm = np.linalg.norm(embedding)
            if norm > 0:
                embedding = embedding / norm
            return embedding
        except Exception:
            return None

    def _get_visual_embedding(self, image_url: str) -> Optional[np.ndarray]:
        if self.clip_available:
            return self._get_clip_embedding(image_url)
        return self._get_basic_visual_embedding(image_url)

    def query_with_text(self, query: str, media_type: Optional[str] = None) -> str:
        try:
            query_embedding = self._get_text_embedding(query)
            where_filter = {"type": media_type} if media_type else None
            results = self.text_collection.query(
                query_embeddings=[query_embedding.tolist()],
                n_results=8,
                where=where_filter,
                include=["metadatas", "documents", "distances"]
            )
            if not results['documents'][0]:
                return self._no_results_response(media_type)
            relevant_items = []
            for i, metadata in enumerate(results['metadatas'][0]):
                item_id = metadata['id']
                item = self.media_repository.get_item_by_id(item_id)
                if item:
                    relevant_items.append((results['distances'][0][i], item))
            relevant_items.sort(key=lambda x: x[0])
            top_items = [item for _, item in relevant_items[:6]]
            return self._generate_response(query, top_items, media_type)
        except Exception as e:
            print(f"Error in text query: {e}")
            return "I apologize, but I encountered an error processing your question. Please try again."

    def query_with_image(self, image_data, media_type: Optional[str] = None) -> str:
        try:
            if isinstance(image_data, str):
                image_embedding = self._get_visual_embedding(image_data)
            else:
                if self.clip_available:
                    if hasattr(image_data, 'read'):
                        image = Image.open(image_data).convert('RGB')
                    else:
                        image = image_data
                    image_input = self.clip_preprocess(image).unsqueeze(0).to(self.device)
                    if self.device == "cuda":
                        image_input = image_input.half()
                    with torch.no_grad():
                        image_features = self.clip_model.encode_image(image_input)
                        image_features = image_features / image_features.norm(dim=-1, keepdim=True)
                        image_embedding = image_features.cpu().float().numpy().flatten()
                else:
                    image_embedding = self._get_basic_visual_embedding(image_data)
            if image_embedding is None:
                return "I couldn't process the uploaded image. Please try a different image."
            where_filter = {"type": media_type} if media_type else None
            results = self.visual_collection.query(
                query_embeddings=[image_embedding.tolist()],
                n_results=8,
                where=where_filter,
                include=["metadatas", "documents"]
            )
            if not results['documents'][0]:
                return self._no_results_response(media_type, visual=True)
            relevant_items = []
            for metadata in results['metadatas'][0]:
                item_id = metadata['id']
                item = self.media_repository.get_item_by_id(item_id)
                if item:
                    relevant_items.append(item)
            method = "CLIP embeddings" if self.clip_available else "basic visual features"
            return self._generate_visual_response(relevant_items, media_type, method)
        except Exception as e:
            print(f"Error in image query: {e}")
            return "I had trouble analyzing this image. Please try uploading a different image."

    def _generate_response(self, query: str, items: List[MediaItem], media_type: Optional[str]) -> str:
        context = "\n".join([self._format_media_item(item) for item in items])
        content_type = 'movies' if media_type == 'movie' else 'games' if media_type == 'game' else 'movies and games'
        response = self.cohere_client.chat(
            message=f"User question: '{query}'\n\nPlease provide a helpful, engaging response using the provided context.",
            preamble=f"""You are an expert assistant for {content_type}.\n\nGuidelines:\n- Be conversational and engaging\n- Reference specific titles from the context\n- Explain your recommendations clearly\n- Connect information across multiple items when relevant\n- Provide insights about themes, genres, or trends\n\nContext:\n{context}""",
            temperature=0.8,
            max_tokens=800
        )
        return response.text

    def _generate_visual_response(self, items: List[MediaItem], media_type: Optional[str], method: str) -> str:
        context = "\n".join([self._format_media_item(item) for item in items])
        content_type = 'movies' if media_type == 'movie' else 'games' if media_type == 'game' else 'entertainment content'
        response = self.cohere_client.chat(
            message=f"Analyze the visual similarities between the uploaded image and these matches using {method}. Focus on visual elements, styles, and aesthetic connections.",
            preamble=f"""You are a visual analysis expert for {content_type}.\n\nAnalyze visual connections focusing on:\n- Color palettes and lighting\n- Composition and style\n- Character design or poster aesthetics\n- Genre visual cues\n- Mood and atmosphere\n\nAnalysis method: {method}\nMost similar items found:\n{context}""",
            temperature=0.8,
            max_tokens=800
        )
        return response.text

    def _format_media_item(self, item: MediaItem) -> str:
        if item.type == "game":
            return f"Title: {item.title} (Game)\nRelease: {getattr(item, 'release_date', '')}\nRating: {getattr(item, 'vote_average', 0)}/10\nGenres: {', '.join(getattr(item, 'genres', []))}\nOverview: {item.description}"
        else:
            return f"Title: {item.title} (Movie)\nRelease: {getattr(item, 'release_date', '')}\nRating: {getattr(item, 'vote_average', 0)}/10 ({getattr(item, 'vote_count', 0)} votes)\nGenres: {', '.join(getattr(item, 'genres', []))}\nOverview: {item.description}"

    def _no_results_response(self, media_type: Optional[str], visual: bool = False) -> str:
        if visual:
            content_type = 'movies' if media_type == 'movie' else 'games' if media_type == 'game' else 'content'
            return f"I couldn't find any visually similar {content_type} for this image."
        content_type = 'movies' if media_type == 'movie' else 'games' if media_type == 'game' else 'content'
        return f"I couldn't find any relevant {content_type} for your query. Try rephrasing your question or asking about different topics."

    def get_relevant_context(self, query: str, media_type: Optional[str] = None) -> List[MediaItem]:
        query_embedding = self._get_text_embedding(query)
        where_filter = {"type": media_type} if media_type else None
        results = self.text_collection.query(
            query_embeddings=[query_embedding.tolist()],
            n_results=5,
            where=where_filter
        )
        items = []
        for metadata in results['metadatas'][0]:
            item_id = metadata['id']
            item = self.media_repository.get_item_by_id(item_id)
            if item:
                items.append(item)
        return items

    def reset_database(self):
        try:
            self.chroma_client.reset()
            self.text_collection = self.chroma_client.get_or_create_collection(
                name="media_text_embeddings",
                metadata={"hnsw:space": "cosine"}
            )
            self.visual_collection = self.chroma_client.get_or_create_collection(
                name="media_visual_embeddings",
                metadata={"hnsw:space": "cosine"}
            )
            self._ensure_data_indexed()
        except Exception as e:
            print(f"Error resetting database: {e}")

    def get_stats(self) -> Dict[str, Any]:
        return {
            "text_embeddings": self.text_collection.count(),
            "visual_embeddings": self.visual_collection.count(),
            "batch_size": self.batch_size,
            "model": self.text_model,
            "vector_db": "ChromaDB",
            "clip_available": self.clip_available,
            "status": "ready"
        }

    def get_performance_stats(self) -> Dict[str, Any]:
        return {
            "text_embeddings": self.text_collection.count(),
            "visual_embeddings": self.visual_collection.count(),
            "batch_size": self.batch_size,
            "device": self.device,
            "clip_available": self.clip_available
        } 