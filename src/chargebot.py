"""
ChargeBot — ChargeGrid Intelligence Assistant
GoodWe × FIAP · EV Challenge 2026 · Sprint 2
Motor: Google Gemini (gemini-2.0-flash) — camada gratuita

Técnicas utilizadas:
  - System prompt contextualizado (ChargeGrid Intelligence)
  - Gerenciamento de histórico de mensagens (memória de contexto)
  - Few-shot prompting com exemplos reais do domínio
  - Injeção de dados simulados de telemetria (mock API ChargeGrid)
  - Interface CLI interativa
"""

import os
import json
import random
from datetime import datetime, timedelta
import google.generativeai as genai

# ---------------------------------------------------------------------------
# CONFIGURAÇÃO
# API Key gratuita em: aistudio.google.com/app/apikey
# Configure com: export GOOGLE_API_KEY="sua-chave"
# No Google Colab: use Secrets (ícone 🔑) com nome GOOGLE_API_KEY
# ---------------------------------------------------------------------------

def get_client():
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "Variável GOOGLE_API_KEY não definida.\n"
            "  Obtenha sua chave GRATUITA em: aistudio.google.com/app/apikey\n"
            "  Local:  export GOOGLE_API_KEY='sua-chave'\n"
            "  Colab:  Secrets → GOOGLE_API_KEY"
        )
    genai.configure(api_key=api_key)
    return genai.GenerativeModel(
        model_name="gemini-2.0-flash",
        system_instruction=SYSTEM_PROMPT,
        generation_config=genai.GenerationConfig(
            temperature=0.3,
            max_output_tokens=800,
        )
    )


# ---------------------------------------------------------------------------
# MOCK: DADOS SIMULADOS DA API CHARGERID
# ---------------------------------------------------------------------------

def get_network_status() -> dict:
    pool = ["online"] * 5 + ["in_use"] * 3 + ["fault"] * 2 + ["offline"] * 2
    chargers = []
    for i in range(1, 13):
        status = random.choice(pool)
        c = {
            "id": f"CG-{i:02d}",
            "status": status,
            "power_kw": round(random.uniform(7.0, 22.0), 1) if status == "in_use" else 0,
            "sessions_today": random.randint(0, 12) if status != "offline" else 0,
        }
        if status == "fault":
            c["error_code"] = random.choice(["E-04", "E-07", "E-12"])
            c["fault_since"] = (
                datetime.now() - timedelta(minutes=random.randint(10, 180))
            ).strftime("%H:%M")
        chargers.append(c)

    faults  = [c for c in chargers if c["status"] == "fault"]
    offline = [c for c in chargers if c["status"] == "offline"]
    return {
        "total_chargers": 12,
        "online": sum(1 for c in chargers if c["status"] in ["online", "in_use"]),
        "fault": len(faults),
        "offline": len(offline),
        "in_use": sum(1 for c in chargers if c["status"] == "in_use"),
        "total_power_kw": round(sum(c["power_kw"] for c in chargers), 1),
        "faults": faults,
        "offline_units": offline,
    }


def get_financial_data() -> dict:
    rt = round(random.uniform(600, 1100), 2)
    return {
        "receita_hoje_brl":             rt,
        "receita_ontem_brl":            round(random.uniform(700, 1050), 2),
        "media_diaria_mensal_brl":      round(random.uniform(780, 870), 2),
        "sessoes_hoje":                 random.randint(22, 48),
        "duracao_media_sessao_min":     random.randint(28, 55),
        "horario_pico":                 "18h–20h",
        "receita_mes_atual_brl":        round(rt * datetime.now().day * 0.95, 2),
        "projecao_mes_brl":             round(rt * 30, 2),
        "meta_mensal_brl":              22000.00,
    }


def get_active_alerts() -> list:
    pool = [
        {
            "id": "ALT-001",
            "hora": (datetime.now() - timedelta(minutes=23)).strftime("%H:%M"),
            "tipo": "power_spike", "severidade": "medio",
            "carregador": "CG-05",
            "mensagem": "Consumo 24kW detectado — limite: 11kW",
            "acao": "Verificar cabo e config de potência do CG-05",
        },
        {
            "id": "ALT-002",
            "hora": (datetime.now() - timedelta(minutes=67)).strftime("%H:%M"),
            "tipo": "communication_loss", "severidade": "alto",
            "carregador": "CG-08",
            "mensagem": "Perda de comunicação OCPP há 67 minutos",
            "acao": "Verificar conectividade de rede do CG-08",
        },
    ]
    return pool[:random.choice([0, 0, 1, 2])]


def build_context_block() -> str:
    ctx = {
        "horario": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "rede": get_network_status(),
        "financeiro": get_financial_data(),
        "alertas_ativos": get_active_alerts(),
    }
    return json.dumps(ctx, ensure_ascii=False, indent=2)


# ---------------------------------------------------------------------------
# SYSTEM PROMPT + FEW-SHOT
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = """Você é o ChargeBot, assistente operacional da plataforma ChargeGrid Intelligence da GoodWe.

## Identidade
- Especialista em gestão de redes de eletropostos (EVSE) e plataforma GoodWe ChargeGrid.
- Atende exclusivamente operadores comerciais de redes de recarga de veículos elétricos.
- Tom: profissional, direto, orientado a dados. Responde SEMPRE em Português do Brasil.

## Contexto do Negócio
A GoodWe fornece hardware e software para redes EVSE. O ChargeGrid Intelligence integra:
orquestração de potência, registro de ciclos, faturamento automatizado, alertas em tempo real e relatórios operacionais.

## Regras
SEMPRE: use os dados do [CONTEXTO] injetado · cite IDs dos carregadores (ex: CG-03) · compare dados financeiros com referências (ontem, meta, média) · ofereça próximo passo acionável · use emojis moderadamente (✅⚠️❌📊💡).
NUNCA: invente dados ausentes no contexto · use tom alarmista · finalize conversa sobre falha sem próximo passo.

## Códigos de Erro GoodWe
E-04: Falha autenticação RFID | E-07: Falha comunicação OCPP | E-12: Sobrecarga de potência | E-15: Temperatura crítica | E-21: Falha no relé

## Configurações no Dashboard
Tarifas dinâmicas: Configurações → Tarifas → Nova Regra Tarifária
Limite de potência: Equipamentos → [ID] → Configurações → Potência Máxima
Relatórios: Relatórios → Exportar (PDF/CSV)

=== EXEMPLOS DE COMPORTAMENTO ===

[Status] Usuário: Quantos carregadores online?
ChargeBot: Temos **10/12** operando (8 disponíveis, 2 em uso). ⚠️ CG-03 em falha (E-07 — OCPP). 🔧 CG-09 offline (manutenção). Quer abrir chamado técnico para o CG-03?

[Receita] Usuário: Receita hoje?
ChargeBot: R$ 847,50 em 34 sessões. 📊 vs. ontem: -8,2% · vs. média mensal: +4,6%. Acima da média. Quer detalhes por carregador?

[Alerta] Usuário: Teve algum alerta?
ChargeBot: ⚠️ ALERTA (MÉDIO) — CG-05 às 16h47. Consumo **24kW** (limite: 11kW). Verifique cabo e configuração de potência. Quer abrir chamado?

[Erro] Usuário: Erro E-04 no CG-03?
ChargeBot: E-04 = falha de autenticação RFID. Causas: cartão danificado, leitor sujo, credencial expirada. Workaround: QR Code ou app. CG-03 segue operacional para outros métodos.

[Config] Usuário: Como configuro tarifa para horário de pico?
ChargeBot: Dashboard → Configurações → Tarifas → Nova Regra Tarifária. Defina 18h–20h, valor por kWh e ative. Mudança entra na próxima sessão. 💡 Avise os usuários frequentes pelo app antes de ativar.

=== FIM DOS EXEMPLOS ==="""


# ---------------------------------------------------------------------------
# GERENCIADOR DE HISTÓRICO
# O Gemini usa formato {"role": "user"/"model", "parts": ["texto"]}
# ---------------------------------------------------------------------------

class ConversationHistory:
    def __init__(self, max_turns: int = 10):
        self.max_turns = max_turns
        self._history = []

    def add(self, role: str, text: str):
        # Gemini usa "model" em vez de "assistant"
        gemini_role = "model" if role == "assistant" else "user"
        self._history.append({"role": gemini_role, "parts": [text]})
        max_messages = self.max_turns * 2
        if len(self._history) > max_messages:
            self._history = self._history[-max_messages:]

    def get(self):
        return self._history.copy()

    def clear(self):
        self._history = []
        print("\n🗑️  Histórico limpo. Nova conversa iniciada.\n")


# ---------------------------------------------------------------------------
# MOTOR DO CHATBOT
# ---------------------------------------------------------------------------

class ChargeBot:
    def __init__(self):
        self.model   = get_client()
        self.history = ConversationHistory(max_turns=10)

    def chat(self, user_message: str) -> str:
        context_block = build_context_block()
        enriched = f"{user_message}\n\n[CONTEXTO]\n{context_block}"

        # Inicia sessão de chat com histórico
        session = self.model.start_chat(history=self.history.get())
        response = session.send_message(enriched)
        reply = response.text.strip()

        # Salva no histórico a mensagem original (sem o bloco de contexto)
        self.history.add("user",      user_message)
        self.history.add("assistant", reply)
        return reply

    def reset(self):
        self.history.clear()


# ---------------------------------------------------------------------------
# INTERFACE CLI
# ---------------------------------------------------------------------------

BANNER = """
╔══════════════════════════════════════════════════════════════╗
║         ⚡ ChargeBot — ChargeGrid Intelligence              ║
║         GoodWe × FIAP · EV Challenge 2026 · Sprint 2       ║
║         Motor: Google Gemini (gratuito)                     ║
╠══════════════════════════════════════════════════════════════╣
║  /reset  → limpa o histórico                                ║
║  /status → exibe dados brutos da rede (JSON)               ║
║  /ajuda  → exibe este menu                                  ║
║  /sair   → encerra o chatbot                               ║
╚══════════════════════════════════════════════════════════════╝
"""

def run_cli():
    print(BANNER)
    try:
        bot = ChargeBot()
    except EnvironmentError as e:
        print(f"❌ Erro de configuração:\n{e}")
        return

    print("✅ ChargeBot pronto! Digite sua pergunta sobre a rede de eletropostos.\n")

    while True:
        try:
            user_input = input("Você: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n\nChargeBot encerrado. Até logo! ⚡")
            break

        if not user_input:
            continue

        cmd = user_input.lower()
        if cmd == "/sair":
            print("\nChargeBot encerrado. Até logo! ⚡")
            break
        elif cmd == "/reset":
            bot.reset()
        elif cmd == "/status":
            print("\n📡 Dados brutos da rede:\n")
            print(build_context_block())
            print()
        elif cmd == "/ajuda":
            print(BANNER)
        else:
            print("\nChargeBot: ", end="", flush=True)
            try:
                print(bot.chat(user_input))
            except Exception as e:
                print(f"❌ Erro: {e}")
            print()

if __name__ == "__main__":
    run_cli()
