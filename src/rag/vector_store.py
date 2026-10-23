import os
from langchain_chroma import Chroma
from src.rag.embeddings import get_embeddings
from src.rag.loader import load_documents
from src.rag.chunking import get_chunker

PERSIST_DIRECTORY = "./chroma_db"

def get_vector_store(documents=None):
    """Carrega ou inicializa a base vetorial no ChromaDB persistente."""
    embeddings = get_embeddings()
    
    if os.path.exists(PERSIST_DIRECTORY) and os.listdir(PERSIST_DIRECTORY):
        return Chroma(
            persist_directory=PERSIST_DIRECTORY,
            embedding_function=embeddings
        )
    
    if documents is None:
        documents = load_documents()
    
    chunker = get_chunker()
    chunks = chunker.split_documents(documents)
    
    return Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=PERSIST_DIRECTORY
    )
