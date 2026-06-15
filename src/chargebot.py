"""
ChargeBot — ChargeGrid Intelligence
EV Challenge 2026 · FIAP × GoodWe
Sprint 2 — Implementação do Chatbot

Tecnologias:
  - OpenAI GPT-4o via openai SDK
  - Few-shot prompting + system prompt contextualizado
  - Gerenciamento de histórico de mensagens (memória de sessão)
  - Dados operacionais simulados via função interna (mock da API ChargeGrid)

Uso:
  python chargebot.py
"""

import os
import json
import random
import re
from datetime import datetime, timedelta
from openai import OpenAI


# ──────────────────────────────────────────────────────────────────────────────
# CONFIGURAÇÃO
# ──────────────────────────────────────────────────────────────────────────────

def get_client() -> OpenAI:
    """Inicializa o cliente OpenAI a partir de variável de ambiente."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "\n[ERRO] OPENAI_API_KEY não encontrada.\n"
            "  → Terminal: export OPENAI_API_KEY='sua-chave'\n"
            "  → Colab:    use Secrets (cadeado) e habilite para o notebook\n"
        )
    return OpenAI(api_key=api_key)


# ──────────────────────────────────────────────────────────────────────────────
# MOCK DA API CHARGERID
# ──────────────────────────────────────────────────────────────────────────────

def get_network_status() -> dict:
    now = datetime.now()
    statuses = ["online","online","online","online","in_use","in_use",
                "in_use","in_use","online","offline","fault","in_use"]
    chargers = []
    for i, st in enumerate(statuses, 1):
        cg = {
            "id": f"CG-{i:02d}",
            "status": st,
            "power_kw": round(random.uniform(6, 22), 1) if st == "in_use" else 0,
        }
        if i == 10 and st == "fault":
            cg["error_code"] = "E-07"
            cg["error_desc"] = "Falha na comunicação OCPP"
        if i == 9 and st == "offline":
            cg["offline_reason"] = "Manutenção programada"
        chargers.append(cg)

    return {
        "timestamp": now.isoformat(),
        "network": {
            "total_chargers": len(chargers),
            "online": sum(1 for c in chargers if c["status"] in ("online","in_use")),
            "in_use": sum(1 for c in chargers if c["status"] == "in_use"),
            "offline": sum(1 for c in chargers if c["status"] == "offline"),
            "fault": sum(1 for c in chargers if c["status"] == "fault"),
            "total_power_kw": round(sum(c["power_kw"] for c in chargers), 1),
        },
        "chargers": chargers,
        "active_alerts": [{
            "charger_id": "CG-10",
            "severity": "medium",
            "code": "E-07",
            "message": "Falha na comunicação OCPP",
            "since": (now - timedelta(hours=2, minutes=15)).strftime("%H:%M"),
        }],
    }


def get_financials(period: str = "today") -> dict:
    data = {
        "today":  {"revenue": 847.50,  "sessions": 34,  "avg_min": 38},
        "week":   {"revenue": 5840.00, "sessions": 231, "avg_min": 36},
        "month":  {"revenue": 10420.00,"sessions": 412, "avg_min": 37},
    }.get(period, {"revenue": 847.50, "sessions": 34, "avg_min": 38})
    return {
        "period": period, "currency": "BRL",
        "revenue": data["revenue"], "sessions": data["sessions"],
        "avg_session_duration_min": data["avg_min"],
        "peak_hour": "18h–20h", "best_day": "Sexta-feira",
        "monthly_target": 22000.00, "monthly_projection": 24180.00,
        "yesterday_revenue": 923.00, "monthly_avg_daily": 810.00,
    }


def get_error_info(code: str) -> dict:
    db = {
        "E-04": {
            "name": "Falha de autenticação RFID",
            "causes": ["Cartão danificado/desmagnetizado","Leitor sujo","Credencial expirada"],
            "workaround": "Usar autenticação via QR Code ou app.",
            "severity": "low", "charger_operational": True,
        },
        "E-07": {
            "name": "Falha na comunicação OCPP",
            "causes": ["Queda de rede no local","Servidor OCPP inacessível","Certificado SSL expirado"],
            "workaround": "Reiniciar módulo de comunicação via painel remoto.",
            "severity": "medium", "charger_operational": False,
        },
        "E-12": {
            "name": "Sobrecorrente detectada",
            "causes": ["Cabo de carga danificado","Falha no contator interno","Veículo com BMS defeituoso"],
            "workaround": "Isolar o carregador e acionar suporte técnico imediatamente.",
            "severity": "high", "charger_operational": False,
        },
    }
    return db.get(code.upper(), {
        "name": "Código não encontrado",
        "causes": ["Consulte o manual técnico GoodWe ou suporte."],
        "workaround": "Acione suporte GoodWe.",
        "severity": "unknown", "charger_operational": None,
    })


# ──────────────────────────────────────────────────────────────────────────────
# SYSTEM PROMPT
# ──────────────────────────────────────────────────────────────────────────────

SYSTEM_PROMPT = """Você é o ChargeBot, assistente operacional inteligente da plataforma ChargeGrid Intelligence da GoodWe.

## Identidade e Tom
- Especialista em gestão de redes de eletropostos (EVSE) e na plataforma GoodWe ChargeGrid.
- Atende exclusivamente operadores comerciais de redes de recarga de veículos elétricos.
- Tom: profissional, direto, orientado a dados.
- Use emojis moderadamente: ✅ online, ⚠️ atenção, ❌ falha, 📊 dados, 💡 dica.
- Responda SEMPRE em Português do Brasil.

## Contexto — GoodWe ChargeGrid Intelligence
Plataforma que integra: orquestração de potência, registro de ciclos de carga,
faturamento automatizado, comunicação de alertas (OCPP) e relatórios operacionais/financeiros.

## Persona do Usuário
Operador comercial: responsável por rentabilidade e disponibilidade.
Não é técnico de campo. Precisa de respostas rápidas e acionáveis.

## Regras
SEMPRE: números importantes primeiro; ao identificar problemas: o que é → causas → próximos passos;
compare financeiros com referências; cite ID do carregador; ofereça próximo passo.
NUNCA: invente dados fora do contexto; use linguagem alarmista; ignore alertas elétricos.

## Exemplos (few-shot)

Pergunta: "Quantos carregadores estão online?"
Resposta: "✅ 10 de 12 carregadores estão operando normalmente (7 em uso ativo).
⚠️ CG-10 está em falha (E-07 — comunicação OCPP) desde as 14h15.
🔧 CG-09 offline por manutenção programada.
Quer que eu abra um chamado para o CG-10 ou gere um relatório de disponibilidade?"

Pergunta: "Quanto faturamos hoje?"
Resposta: "📊 Hoje: R$ 847,50 em 34 sessões.
vs. ontem: -8,2% (R$ 923,00) | vs. média mensal diária: +4,6% (R$ 810,00)
Desempenho acima da média do mês, levemente abaixo de ontem — consistente para este dia da semana.
Quer detalhamento por carregador ou projeção mensal?"

Pergunta: "O que é o erro E-07?"
Resposta: "E-07 = Falha na comunicação OCPP — o carregador perdeu contato com o servidor.
Causas comuns: queda de rede, servidor OCPP reiniciando, certificado SSL expirado.
O carregador fica offline durante a falha (sem aceitar novas sessões).
Ação: reinicie o módulo de comunicação pelo painel remoto. Persiste > 15 min → acione suporte."
"""


# ──────────────────────────────────────────────────────────────────────────────
# INJEÇÃO DE CONTEXTO DINÂMICO
# ──────────────────────────────────────────────────────────────────────────────

def build_context_injection(message: str) -> str:
    msg = message.lower()
    parts = []

    if any(k in msg for k in ["online","offline","status","carregador","rede","falha",
                                "erro","alerta","potência","quantos","problema","funciona"]):
        parts.append("[DADOS EM TEMPO REAL — Rede]\n" +
                     json.dumps(get_network_status(), ensure_ascii=False, indent=2))

    if any(k in msg for k in ["receita","faturamento","sessão","sessões","hoje",
                                "semana","mês","mes","meta","projeção","faturou"]):
        period = "week" if "semana" in msg else ("month" if "mês" in msg or "mes" in msg else "today")
        parts.append(f"[DADOS EM TEMPO REAL — Financeiro ({period})]\n" +
                     json.dumps(get_financials(period), ensure_ascii=False, indent=2))

    for code in re.findall(r'\bE-\d{2}\b', message.upper()):
        parts.append(f"[BASE DE CONHECIMENTO — {code}]\n" +
                     json.dumps(get_error_info(code), ensure_ascii=False, indent=2))

    return "\n\n".join(parts)


# ──────────────────────────────────────────────────────────────────────────────
# GERENCIADOR DE HISTÓRICO
# ──────────────────────────────────────────────────────────────────────────────

class ConversationHistory:
    MAX_TURNS = 10

    def __init__(self):
        self.messages: list[dict] = []

    def add(self, role: str, content: str):
        self.messages.append({"role": role, "content": content})
        if len(self.messages) > self.MAX_TURNS * 2:
            self.messages = self.messages[-(self.MAX_TURNS * 2):]

    def get(self) -> list[dict]:
        return self.messages.copy()

    def clear(self):
        self.messages = []


# ──────────────────────────────────────────────────────────────────────────────
# CHARGEBOT
# ──────────────────────────────────────────────────────────────────────────────

class ChargeBot:
    MODEL       = "gpt-4o"
    TEMPERATURE = 0.3
    MAX_TOKENS  = 800

    def __init__(self):
        self.client  = get_client()
        self.history = ConversationHistory()

    def chat(self, user_message: str) -> str:
        context = build_context_injection(user_message)
        augmented = user_message + ("\n\n" + context if context else "")

        self.history.add("user", user_message)

        hist = self.history.get()
        payload = [{"role": "system", "content": SYSTEM_PROMPT}]
        if len(hist) > 1:
            payload.extend(hist[:-1])
        payload.append({"role": "user", "content": augmented})

        response = self.client.chat.completions.create(
            model=self.MODEL,
            temperature=self.TEMPERATURE,
            max_tokens=self.MAX_TOKENS,
            messages=payload,
        )
        reply = response.choices[0].message.content.strip()
        self.history.add("assistant", reply)
        return reply

    def run(self):
        print("\n" + "═"*58)
        print("  ⚡  ChargeBot — GoodWe ChargeGrid Intelligence")
        print("  EV Challenge 2026 · FIAP")
        print("  Modelo: GPT-4o | Temp: 0.3 | Memória: 10 turnos")
        print("═"*58)
        print("  Comandos: 'limpar' | 'status' | 'sair'")
        print("═"*58 + "\n")

        while True:
            try:
                user_input = input("Você: ").strip()
            except (KeyboardInterrupt, EOFError):
                print("\n\n👋 Sessão encerrada.")
                break

            if not user_input:
                continue
            if user_input.lower() == "sair":
                print("\n👋 Sessão encerrada.")
                break
            if user_input.lower() == "limpar":
                self.history.clear()
                print("🗑️  Histórico limpo.\n")
                continue
            if user_input.lower() == "status":
                print(json.dumps(get_network_status(), ensure_ascii=False, indent=2) + "\n")
                continue

            print("\nChargeBot: ", end="", flush=True)
            try:
                print(self.chat(user_input))
            except Exception as e:
                print(f"[ERRO] {e}")
            print()


if __name__ == "__main__":
    bot = ChargeBot()
    bot.run()

