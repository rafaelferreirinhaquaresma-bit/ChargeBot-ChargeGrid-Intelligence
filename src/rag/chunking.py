from langchain_text_splitters import RecursiveCharacterTextSplitter

def get_chunker(chunk_size: int = 1000, chunk_overlap: int = 200):
    """Retorna o divisor de texto parametrizado."""
    return RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        add_start_index=True
    )
