KEYWORDS_FORA_ESCOPO = [
    "receita de bolo", "futebol", "criptomoeda", "politica",
    "carregador tesla", "investimento em acoes"
]

TERMOS_PERIGO_ELETRICO = [
    "abrir painel", "fio descascado", "gambiarra", "trocar disjuntor", "curto circuito"
]

def validar_escopo_mensagem(mensagem: str) -> dict:
    msg_lower = mensagem.lower()
    
    # Valida perigo elétrico
    for termo in TERMOS_PERIGO_ELETRICO:
        if termo in msg_lower:
            return {
                "valido": False,
                "motivo": "segurança_eletrica",
                "resposta": "Atenção: Por razões de segurança elétrica, intervenções físicas ou reparos em componentes energizados só devem ser realizados por profissionais eletrotecnistas habilitados ou rede autorizada GoodWe."
            }
            
    # Valida escopo
    for kw in KEYWORDS_FORA_ESCOPO:
        if kw in msg_lower:
            return {
                "valido": False,
                "motivo": "fora_de_escopo",
                "resposta": "Sou o ChargeBot, assistente focado na linha de carregadores e soluções de mobilidade elétrica da GoodWe Brasil. Não posso ajudar com assuntos fora deste domínio."
            }
            
    return {"valido": True, "motivo": None, "resposta": None}
