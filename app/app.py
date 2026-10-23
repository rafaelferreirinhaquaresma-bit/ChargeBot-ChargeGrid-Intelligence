import gradio as gr
from langchain_ollama import ChatOllama
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from src.rag.retriever import get_rag_retriever
from src.rag.prompt_rag import get_prompt

retriever = get_rag_retriever(top_k=4)
prompt = get_prompt("v2")
llm = ChatOllama(model="llama3", temperature=0.0)

def format_docs(docs):
    formatted = []
    for doc in docs:
        source = doc.metadata.get("source_file", "Documento Interno")
        page = doc.metadata.get("page", "N/A")
        formatted.append(f"--- [Fonte: {source} | Pág. {page}] ---\n{doc.page_content}")
    return "\n\n".join(formatted)

rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

def respond(message, history):
    try:
        return rag_chain.invoke(message)
    except Exception as e:
        return f"Erro ao processar consulta: {str(e)}"

demo = gr.ChatInterface(
    fn=respond,
    title="⚡ ChargeBot - ChargeGrid Intelligence",
    description="Interface RAG com grounding e citação obrigatória para carregamento elétrico GoodWe.",
    theme="soft"
)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
