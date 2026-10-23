from langchain_ollama import OllamaEmbeddings

def get_embeddings():
    """Instancia o modelo de embeddings nomic-embed-text via Ollama."""
    return OllamaEmbeddings(
        model="nomic-embed-text",
        base_url="http://localhost:11434"
    )
