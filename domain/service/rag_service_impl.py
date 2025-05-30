from typing import List
import cohere
from domain.port.rag_service import RAGService
from domain.port.media_repository import MediaRepository
from domain.model.media_item import MediaItem
import numpy as np
from PIL import Image
import requests
from io import BytesIO
import os
from dotenv import load_dotenv
import cv2
from skimage import color

load_dotenv()

class RAGServiceImpl(RAGService):
    def __init__(self, media_repository: MediaRepository, embedding_model: str = "embed-english-v3.0"):
        self.media_repository = media_repository
        self.co = cohere.Client(os.getenv('COHERE_API_KEY'))
        self.embedding_model = embedding_model
        self.embedding_dim = 1024  # Cohere's embedding dimension

    def _get_text_embedding(self, text: str) -> np.ndarray:
        """Get text embedding using Cohere"""
        response = self.co.embed(
            texts=[text],
            model=self.embedding_model,
            input_type="search_query"
        )
        return np.array(response.embeddings[0])

    def _get_image_array(self, image_url: str):
        """Download and convert image to numpy array."""
        response = requests.get(image_url)
        img = Image.open(BytesIO(response.content)).convert('RGB')
        img = img.resize((224, 336))  # Standard movie poster ratio
        return np.array(img)

    def _extract_image_features(self, img_array: np.ndarray) -> dict:
        """Extract basic visual features from image."""
        # Convert to HSV for better color analysis
        hsv = cv2.cvtColor(img_array, cv2.COLOR_RGB2HSV)
        
        # Calculate color statistics
        avg_color = np.mean(hsv, axis=(0, 1))
        avg_brightness = avg_color[2] / 255.0
        avg_saturation = avg_color[1] / 255.0
        
        # Convert to grayscale for texture analysis
        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        
        # Calculate basic texture features
        texture_features = {
            "is_dark": avg_brightness < 0.4,
            "is_bright": avg_brightness > 0.6,
            "is_colorful": avg_saturation > 0.5,
            "avg_brightness": avg_brightness,
            "avg_saturation": avg_saturation
        }
        
        # Simple face detection
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        
        return {
            **texture_features,
            "face_count": len(faces),
            "has_faces": len(faces) > 0
        }

    def _get_image_embedding(self, image_url: str) -> np.ndarray:
        """Create simple image embedding from basic features."""
        try:
            # Get image array
            img_array = self._get_image_array(image_url)
            
            # Extract features
            features = self._extract_image_features(img_array)
            
            # Create a simple feature vector
            feature_vector = np.array([
                features["avg_brightness"],
                features["avg_saturation"],
                float(features["is_dark"]),
                float(features["is_bright"]),
                float(features["is_colorful"]),
                float(features["has_faces"]),
                features["face_count"] / 10.0  # Normalize face count
            ])
            
            # Pad to match embedding dimension
            padded_vector = np.zeros(self.embedding_dim)
            padded_vector[:len(feature_vector)] = feature_vector
            
            return padded_vector / np.linalg.norm(padded_vector)
            
        except Exception as e:
            print(f"Error processing image: {str(e)}")
            return np.zeros(self.embedding_dim)

    def _analyze_image_content(self, image_url: str) -> List[str]:
        """Analyze image content using basic features."""
        try:
            # Get image array
            img_array = self._get_image_array(image_url)
            
            # Extract features
            features = self._extract_image_features(img_array)
            
            # Build description
            description = []
            
            # Add color/brightness descriptions
            if features["is_dark"]:
                description.append("dark atmosphere")
            if features["is_bright"]:
                description.append("bright and vibrant")
            if features["is_colorful"]:
                description.append("colorful")
            
            # Add face detection results
            if features["has_faces"]:
                if features["face_count"] == 1:
                    description.append("single person")
                else:
                    description.append(f"group of {features['face_count']} people")
            
            return description
            
        except Exception as e:
            print(f"Error analyzing image: {str(e)}")
            return []

    def query_with_text(self, query: str, media_type: str = None) -> str:
        try:
            # Get query embedding
            query_embedding = self._get_text_embedding(query)
            
            # Get relevant context with more items for better coverage
            relevant_items = self.media_repository.search_by_text_embedding(
                query_embedding,
                media_type=media_type,
                top_k=8  # Increased for better context
            )
            
            if not relevant_items:
                return f"I couldn't find any relevant {'movies' if media_type == 'movie' else 'games' if media_type == 'game' else 'content'} for that. Could you try rephrasing your question or asking about something else?"
            
            # Prepare context for LLM
            context = "\n".join([self._format_media_item(item) for item in relevant_items])
            
            # Generate response using Cohere with improved prompting
            response = self.co.chat(
                message=f"""Based on the user's question: "{query}"
Please provide a helpful and engaging response using the context provided.""",
                preamble=f"""You are a friendly and knowledgeable expert on {'movies' if media_type == 'movie' else 'games' if media_type == 'game' else 'movies and games'}. 
Your goal is to provide helpful, engaging, and natural responses that feel like a conversation with a real expert.

Here's how you should approach responses:
1. Be conversational and engaging, but maintain professionalism
2. Connect information from multiple sources when relevant
3. Provide specific examples and explain your recommendations
4. Consider both content and visual aspects in your analysis
5. If you're not sure about something, be honest about it
6. Use natural transitions between topics
7. Avoid listing items - instead, weave them into a narrative
8. Reference specific titles to support your points

Here's the relevant information to help answer the question:

{context}

Remember to:
- Focus on the most relevant information for the user's question
- Make connections between different titles when appropriate
- Explain your reasoning for recommendations
- Keep the tone conversational and engaging""",
                temperature=0.8,  # Slightly increased for more creative responses
                max_tokens=800,  # Increased for more detailed responses
                k=5,  # More diverse sampling
                p=0.75  # Balanced between focused and creative responses
            )
            
            return response.text
        except Exception as e:
            return f"I apologize, but I encountered an error while processing your question. Could you try asking in a different way?"

    def _format_media_item(self, item: MediaItem) -> str:
        """Format a media item into a readable context string."""
        # Get visual features if poster exists
        visual_features = []
        if item.poster_url:
            visual_features = self._analyze_image_content(item.poster_url)
        
        visual_desc = f"\nVisual features: {', '.join(visual_features)}" if visual_features else ""
        
        # Format based on media type
        if item.type == "game":
            return f"""
Title: {item.title} (Game)
Release Date: {item.release_date}
Developer: {item.metadata.get('developer', 'Unknown')}
Publisher: {item.metadata.get('publisher', 'Unknown')}
Rating: {item.vote_average}/10
Genres: {', '.join(item.genres)}
Price: ${item.metadata.get('price', 0.0)}
Overview: {item.description}{visual_desc}
"""
        else:  # movie
            return f"""
Title: {item.title} (Movie)
Release Date: {item.release_date}
Rating: {item.vote_average}/10 ({item.vote_count} votes)
Popularity: {item.popularity}
Genres: {', '.join(item.genres)}
Overview: {item.description}{visual_desc}
"""

    def query_with_image(self, image_url: str, media_type: str = None) -> str:
        try:
            # Get image embedding
            image_embedding = self._get_image_embedding(image_url)
            
            # Get relevant items
            relevant_items = self.media_repository.search_by_image_embedding(
                image_embedding,
                media_type=media_type,
                top_k=5
            )
            
            if not relevant_items:
                return f"I couldn't find any matching {'movies' if media_type == 'movie' else 'games' if media_type == 'game' else 'content'} for this image. Try uploading a different image or adjusting the image quality."
            
            # Analyze uploaded image
            uploaded_features = self._analyze_image_content(image_url)
            
            # Prepare context for LLM
            context = "\n".join([self._format_media_item(item) for item in relevant_items])
            
            # Generate response using Cohere with improved prompting
            response = self.co.chat(
                message=f"""Analyze the visual similarities between the uploaded image and the potential matches.
The uploaded image features: {', '.join(uploaded_features)}

Please provide an engaging analysis that helps understand the visual connections.""",
                preamble=f"""You are a friendly and insightful visual analyst specializing in {'movies' if media_type == 'movie' else 'games' if media_type == 'game' else 'movies and games'}. 
Your goal is to help users understand the visual connections between their uploaded image and the matches found.

When analyzing visual similarities:
1. Start with the most interesting or striking connections
2. Explain the visual elements that make each match relevant
3. Consider both obvious and subtle similarities
4. Discuss how the visual elements contribute to the overall feel
5. Make connections between multiple matches if patterns emerge
6. Keep your analysis conversational and engaging

Here are the most visually similar items found:

{context}

Focus on these aspects in your analysis:
- Overall mood and atmosphere
- Color palette and lighting
- Visual composition and style
- Character or object placement
- Thematic visual elements

Remember to maintain a natural, conversational tone while providing expert insights.""",
                temperature=0.8,
                max_tokens=800,
                k=5,
                p=0.75
            )
            
            return response.text
        except Exception as e:
            return f"I apologize, but I had trouble analyzing this image. Could you try uploading a different image?"

    def _get_relevant_chat_history(self) -> List[dict]:
        """Get relevant chat history for context."""
        # This would be implemented to maintain conversation context
        # For now, return empty list
        return []

    def get_relevant_context(self, query: str) -> List[MediaItem]:
        query_embedding = self._get_text_embedding(query)
        return self.media_repository.search_by_text_embedding(query_embedding) 