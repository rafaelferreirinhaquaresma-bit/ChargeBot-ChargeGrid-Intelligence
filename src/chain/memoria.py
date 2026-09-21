from typing import Dict
import tiktoken
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory

# Repositório de memórias em memória (em produção utilizar Redis/SQL)
_session_store: Dict[str, ChatMessageHistory] = {}

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in _session_store:
        _session_store[session_id] = ChatMessageHistory()
    return _session_store[session_id]

def contar_tokens_historico(mensagens, model_name: str = "gpt-4") -> int:
    try:
        encoding = tiktoken.encoding_for_model(model_name)
    except KeyError:
        encoding = tiktoken.get_encoding("cl100k_base")
    
    total_tokens = 0
    for msg in mensagens:
        total_tokens += 4 + len(encoding.encode(msg.content))
    return total_tokens

def podar_historico_por_tokens(history: ChatMessageHistory, max_tokens: int = 1500, model_name: str = "gpt-4"):
    """Garante que o histórico não exceda o limite de tokens especificado."""
    mensagens = history.messages
    while contar_tokens_historico(mensagens, model_name) > max_tokens and len(mensagens) > 1:
        # Remove a mensagem mais antiga preservando a coerência
        mensagens.pop(0)
    history.clear()
    history.add_messages(mensagens)
