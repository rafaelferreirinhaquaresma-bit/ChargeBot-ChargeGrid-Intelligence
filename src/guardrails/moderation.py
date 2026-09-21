import re

PATROES_JAILBREAK = [
    r"ignore\s+all\s+previous\s+instructions",
    r"ignore\s+suas\s+instruções",
    r"you\s+are\s+now\s+DAN",
    r"modo\s+developer",
    r"pretend\s+you\s+have\s+no\s+rules",
    r"suprima\s+as\s+regras"
]

def verificar_jailbreak(texto: str) -> bool:
    """Retorna True se for detectada tentativa de prompt injection ou jailbreak."""
    texto_lower = texto.lower()
    for padrão in PATROES_JAILBREAK:
        if re.search(padrão, texto_lower):
            return True
    return False
