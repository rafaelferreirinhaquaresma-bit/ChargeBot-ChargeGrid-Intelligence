"""
ChargeBot — ChargeGrid Intelligence Assistant
GoodWe × FIAP · EV Challenge 2026 · Sprint 2
Motor: Ollama (local, gratuito, sem API Key)

Pré-requisitos:
  1. Instale o Ollama: https://ollama.com/download
  2. Baixe o modelo: ollama pull llama3.2
  3. Instale a lib:   pip install -r requirements.txt
  4. Execute:         python src/chargebot.py

Técnicas utilizadas:
  - System prompt contextualizado (ChargeGrid Intelligence)
  - Gerenciamento de histórico de mensagens (memória de contexto)
  - Few-shot prompting com exemplos reais do domínio
  - Injeção de dados simulados de telemetria (mock API ChargeGrid)
  - Interface CLI interativa
"""

import json
import random
from datetime import datetime, timedelta
import ollama

# ---------------------------------------------------------------------------
# CONFIGURAÇÃO
# Modelo padrão: llama3.2 (leve, ~2GB, ótimo custo-benefício)
# Alternativas:  mistral, llama3.1, phi3, gemma2
# Troque MODEL abaixo se quiser usar outro modelo já baixado.
# ---------------------------------------------------------------------------

MODEL = "llama3.2"


def check_ollama():
    """Verifica se o Ollama está rodando e se o modelo está disponível."""
    try:
        models = [m.model for m in ollama.list().models]
        # Aceita match parcial: "llama3.2" bate com "llama3.2:latest"
        available = any(MODEL in m for m in models)
        if not available:
            raise EnvironmentError(
                f"Modelo '{MODEL}' não encontrado no Ollama.\n"
                f"  Baixe com:  ollama pull {MODEL}\n"
                f"  Modelos disponíveis: {models}"
            )
    except ollama.ResponseError:
        raise EnvironmentError(
            "Ollama não está rodando.\n"
            "  Inicie com:  ollama serve\n"
            "  Ou abra o aplicativo Ollama no seu computador."
        )


# ---------------------------------------------------------------------------
# MOCK: DADOS SIMULADOS DA API CHARGERID
# ---------------------------------------------------------------------------

def get_network_status() -> dict:
    pool = ["online"] * 5 + ["in_use"] * 3 + ["fault"] * 2 + ["offline"] * 2
    chargers = []
    for i in range(1, 13):
        s = random.choice(pool)
        c = {
            "id": f"CG-{i:02d}",
            "status": s,
            "power_kw": round(random.uniform(7.0, 22.0), 1) if s == "in_use" else 0,
            "sessions_today": random.randint(0, 12) if s != "offline" else 0,
        }
        if s == "fault":
            c["error_code"] = random.choice(["E-04", "E-07", "E-12"])
            c["fault_since"] = (
                datetime.now() - timedelta(minutes=random.randint(10, 180))
            ).strftime("%H:%M")
        chargers.append(c)

    faults  = [c for c in chargers if c["status"] == "fault"]
    offline = [c for c in chargers if c["status"] == "offline"]
    return {
        "total_carregadores": 12,
        "online_ou_em_uso": sum(1 for c in chargers if c["status"] in ["online", "in_use"]),
        "em_falha": len(faults),
        "offline": len(offline),
        "em_uso_agora": sum(1 for c in chargers if c["status"] == "in_use"),
        "potencia_total_kw": round(sum(c["power_kw"] for c in chargers), 1),
        "carregadores_com_falha": faults,
        "carregadores_offline": offline,
    }


def get_financial_data() -> dict:
    rt = round(random.uniform(600, 1100), 2)
    return {
        "receita_hoje_brl":            rt,
        "receita_ontem_brl":           round(random.uniform(700, 1050), 2),
        "media_diaria_mensal_brl":     round(random.uniform(780, 870), 2),
        "sessoes_hoje":                random.randint(22, 48),
        "duracao_media_sessao_min":    random.randint(28, 55),
        "horario_pico":                "18h-20h",
        "receita_mes_atual_brl":       round(rt * datetime.now().day * 0.95, 2),
        "projecao_mes_brl":            round(rt * 30, 2),
        "meta_mensal_brl":             22000.00,
    }


def get_active_alerts() -> list:
    pool = [
        {
            "id": "ALT-001",
            "hora": (datetime.now() - timedelta(minutes=23)).strftime("%H:%M"),
            "tipo": "power_spike", "severidade": "medio",
            "carregador": "CG-05",
            "mensagem": "Consumo 24kW detectado — limite: 11kW",
            "acao": "Verificar cabo e config de potencia do CG-05",
        },
        {
            "id": "ALT-002",
            "hora": (datetime.now() - timedelta(minutes=67)).strftime("%H:%M"),
            "tipo": "communication_loss", "severidade": "alto",
            "carregador": "CG-08",
            "mensagem": "Perda de comunicacao OCPP ha 67 minutos",
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
SEMPRE: use os dados do [CONTEXTO] injetado com cada mensagem · cite IDs dos carregadores (ex: CG-03) · compare dados financeiros com referências (ontem, meta, média) · ofereça próximo passo acionável · use emojis moderadamente (✅ ⚠️ ❌ 📊 💡).
NUNCA: invente dados ausentes no contexto · use tom alarmista · finalize conversa sobre falha sem próximo passo.

## Códigos de Erro GoodWe
E-04: Falha autenticacao RFID | E-07: Falha comunicacao OCPP | E-12: Sobrecarga de potencia | E-15: Temperatura critica | E-21: Falha no rele

## Configurações no Dashboard
Tarifas dinamicas: Configuracoes > Tarifas > Nova Regra Tarifaria
Limite de potencia: Equipamentos > [ID] > Configuracoes > Potencia Maxima
Relatorios: Relatorios > Exportar (PDF/CSV)

=== EXEMPLOS DE COMPORTAMENTO ===

[Status] Usuario: Quantos carregadores online?
ChargeBot: Temos **10/12** operando (8 disponiveis, 2 em uso). ⚠️ CG-03 em falha (E-07 — OCPP). 🔧 CG-09 offline (manutencao). Quer abrir chamado tecnico para o CG-03?

[Receita] Usuario: Receita hoje?
ChargeBot: R$ 847,50 em 34 sessoes. 📊 vs. ontem: -8,2% vs. media mensal: +4,6%. Acima da media. Quer detalhes por carregador?

[Alerta] Usuario: Teve algum alerta?
ChargeBot: ⚠️ ALERTA (MEDIO) — CG-05 as 16h47. Consumo **24kW** (limite: 11kW). Verifique cabo e configuracao de potencia. Quer abrir chamado?

[Erro] Usuario: Erro E-04 no CG-03?
ChargeBot: E-04 = falha de autenticacao RFID. Causas: cartao danificado, leitor sujo, credencial expirada. Workaround: QR Code ou app. CG-03 segue operacional para outros metodos.

[Config] Usuario: Como configuro tarifa para horario de pico?
ChargeBot: Dashboard > Configuracoes > Tarifas > Nova Regra Tarifaria. Defina 18h-20h, valor por kWh e ative. Mudanca entra na proxima sessao. 💡 Avise usuarios frequentes pelo app antes de ativar.

=== FIM DOS EXEMPLOS ==="""


# ---------------------------------------------------------------------------
# GERENCIADOR DE HISTÓRICO
# O Ollama usa o mesmo formato da OpenAI:
# {"role": "user"|"assistant"|"system", "content": "texto"}
# ---------------------------------------------------------------------------

class ConversationHistory:
    def __init__(self, max_turns: int = 10):
        self.max_turns = max_turns
        self._history: list[dict] = []

    def add(self, role: str, content: str):
        self._history.append({"role": role, "content": content})
        max_messages = self.max_turns * 2
        if len(self._history) > max_messages:
            self._history = self._history[-max_messages:]

    def get(self) -> list[dict]:
        return self._history.copy()

    def clear(self):
        self._history = []
        print("\n🗑️  Histórico limpo. Nova conversa iniciada.\n")


# ---------------------------------------------------------------------------
# MOTOR DO CHATBOT
# ---------------------------------------------------------------------------

class ChargeBot:
    def __init__(self):
        check_ollama()
        self.history = ConversationHistory(max_turns=10)
        print(f"✅ Ollama conectado · Modelo: {MODEL}\n")

    def chat(self, user_message: str) -> str:
        context_block = build_context_block()
        enriched = f"{user_message}\n\n[CONTEXTO]\n{context_block}"

        # Monta o array de mensagens:
        # 1. System prompt
        # 2. Histórico da conversa
        # 3. Mensagem atual com dados injetados
        messages = [
            {"role": "system",    "content": SYSTEM_PROMPT},
            *self.history.get(),
            {"role": "user",      "content": enriched},
        ]

        response = ollama.chat(
            model=MODEL,
            messages=messages,
            options={
                "temperature": 0.3,   # Respostas precisas e consistentes
                "num_predict": 800,   # Equivalente ao max_tokens
            }
        )

        reply = response["message"]["content"].strip()

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
║         Motor: Ollama local · Modelo: llama3.2             ║
╠══════════════════════════════════════════════════════════════╣
║  /reset  → limpa o histórico da conversa                    ║
║  /status → exibe dados brutos da rede (JSON)               ║
║  /modelo → exibe o modelo Ollama em uso                     ║
║  /ajuda  → exibe este menu                                  ║
║  /sair   → encerra o chatbot                               ║
╚══════════════════════════════════════════════════════════════╝
"""


def run_cli():
    print(BANNER)
    print("Conectando ao Ollama...\n")

    try:
        bot = ChargeBot()
    except EnvironmentError as e:
        print(f"❌ Erro:\n{e}")
        return

    print("Digite sua pergunta sobre a rede de eletropostos.\n")

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
        elif cmd == "/modelo":
            print(f"\n🤖 Modelo em uso: {MODEL}\n")
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
