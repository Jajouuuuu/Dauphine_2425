from domain.service.rag_service_impl import RAGServiceImpl
from domain.port.media_repository import MediaRepository


def create_rag_service(media_repository: MediaRepository, **kwargs) -> RAGServiceImpl:
    """Factory that instantiates the default RAG service used by the UI.

    This indirection gives the frontend a stable API and keeps Streamlit
    separate from domain-layer classes, enabling future swaps (e.g. another
    RAG implementation) without touching the UI code.
    """
    return RAGServiceImpl(media_repository, **kwargs) 