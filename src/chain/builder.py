import os
from typing import Optional
from dotenv import load_dotenv

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama

from src.schemas.recarga import RespostaChatbot
from src.chain.memoria import get_session_history, podar_historico_por_tokens
from src.guardrails.moderation import verificar_jailbreak
from src.guardrails.scope_validator import validar_escopo_mensagem

load_dotenv()


def carregar_prompt_sistema(filepath: str = "prompts/system_prompt_v2.md") -> str:
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()


def obter_llm(provider: str = "ollama", model_name: str = "gpt-oss:120b", temperature: float = 0.2):
    """
    Suporte Multi-provider (Bônus): Permite chavear entre Ollama e OpenAI/Provedor em nuvem.
    """
    if provider == "ollama":
        return ChatOllama(
            model=model_name,
            temperature=temperature
        )
    elif provider == "openai":
        return ChatOpenAI(
            model=model_name or "gpt-4o-mini",
            temperature=temperature,
            api_key=os.getenv("OPENAI_API_KEY")
        )
    else:
        raise ValueError(f"Provedor {provider} não suportado.")


def criar_chargebot_chain(provider: str = "ollama", model_name: str = "gpt-oss:120b"):
    system_content = carregar_prompt_sistema()
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_content),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}")
    ])
    
    llm = obter_llm(provider=provider, model_name=model_name)
    structured_llm = llm.with_structured_output(RespostaChatbot)
    
    chain_base = prompt | structured_llm
    
    chain_com_memoria = RunnableWithMessageHistory(
        chain_base,
        get_session_history,
        input_messages_key="input",
        history_messages_key="history"
    )
    
    return chain_com_memoria


def executar_interacao(session_id: str, input_texto: str, provider: str = "ollama", model_name: str = "gpt-oss:120b") -> dict:
    """
    Pipeline com Guardrails + Poda de Tokens + Chain LCEL.
    """
    # 1. Guardrail - Jailbreak
    if verificar_jailbreak(input_texto):
        return {
            "resposta_texto": "Tentativa de violação das diretrizes de segurança detectada. Requisição negada.",
            "fora_de_escopo": True,
            "alerta_seguranca": True
        }
        
    # 2. Guardrail - Escopo
    validacao = validar_escopo_mensagem(input_texto)
    if not validacao["valido"]:
        return {
            "resposta_texto": validacao["resposta"],
            "fora_de_escopo": True,
            "alerta_seguranca": (validacao["motivo"] == "segurança_eletrica")
        }

    # 3. Poda de histórico (Gestão de tokens)
    history = get_session_history(session_id)
    podar_historico_por_tokens(history, max_tokens=1500)

    # 4. Invocação da Chain
    chain = criar_chargebot_chain(provider=provider, model_name=model_name)
    resultado = chain.invoke(
        {"input": input_texto},
        config={"configurable": {"session_id": session_id}}
    )
    
    return resultado
