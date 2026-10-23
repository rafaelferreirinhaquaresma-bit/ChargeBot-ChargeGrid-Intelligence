import os
from langchain_community.document_loaders import PyMuPDFLoader

def load_documents(data_dir: str = "data/knowledge_base/"):
    """Carrega todos os manuais e documentos PDF da base de conhecimento."""
    documents = []
    if not os.path.exists(data_dir):
        os.makedirs(data_dir, exist_ok=True)
        return documents
    
    for filename in os.listdir(data_dir):
        if filename.endswith(".pdf"):
            filepath = os.path.join(data_dir, filename)
            loader = PyMuPDFLoader(filepath)
            docs = loader.load()
            for doc in docs:
                doc.metadata["source_file"] = filename
            documents.extend(docs)
    return documents
