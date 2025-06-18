from domain.service.rag_service_impl import RAGServiceImpl
from domain.port.media_repository import MediaRepository
from config.rag_config import VECTOR_DB_CONFIG, TEXT_EMBEDDING_MODELS, PERFORMANCE_CONFIG


def create_rag_service(media_repository: MediaRepository, db_path=None, text_model=None, enable_visual=False, batch_size=None, ensure_index=True) -> RAGServiceImpl:
    """Factory that instantiates the default RAG service used by the UI and backend.
    Set ensure_index=False in the UI to avoid re-indexing on every instantiation.
    """
    return RAGServiceImpl(
        media_repository,
        db_path=db_path or VECTOR_DB_CONFIG["db_path"],
        text_model=text_model or TEXT_EMBEDDING_MODELS["fast"],
        enable_visual=enable_visual,
        batch_size=batch_size or PERFORMANCE_CONFIG["batch_size"],
        ensure_index=ensure_index
    ) 