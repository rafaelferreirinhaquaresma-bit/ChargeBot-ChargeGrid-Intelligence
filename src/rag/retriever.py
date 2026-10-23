from src.rag.vector_store import get_vector_store

def get_rag_retriever(top_k: int = 4):
    """Cria o retriever para busca semântica por similaridade."""
    vector_store = get_vector_store()
    return vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": top_k}
    )
