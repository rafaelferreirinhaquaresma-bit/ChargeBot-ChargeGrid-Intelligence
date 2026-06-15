# ChargeBot - ChargeGrid Intelligence
# ChargeGrid Intelligence — Chatbot GoodWe
### EV Challenge 2026 · FIAP

---

## 👥 Integrantes do Grupo

| Nome | RM |
|------|----|
|Rafael Ferreirinha Quaresma | RM571949 |
|Pedro Andreassa Zamai  | RM569318 |
|Pedro Yoshikado Garcia | RM570449 |
|Thiago Maluf Hofmann | RM569852 |
|Lucas Klein da Veiga | RM570029 |

---

## 🔍 Problema Abordado

A GoodWe, fabricante global de inversores e equipamentos de energia, identificou um gap crítico na infraestrutura de eletropostos (EVSE): **a ausência de mecanismos integrados nos eletropostos para orquestrar potência, registrar ciclos de carga, faturar sessões e comunicar eventos de forma autônoma e inteligente** — conceito denominado **ChargeGrid Intelligence**.

### Dor Central

Os operadores comerciais de eletropostos enfrentam diariamente:

- **Falta de visibilidade em tempo real** sobre o status dos carregadores e consumo de potência.
- **Dificuldade de faturamento automatizado** — sessões de carga sem registro adequado geram perda de receita.
- **Ausência de comunicação proativa** sobre falhas, picos de demanda ou ciclos anômalos.
- **Fragmentação de dados** entre o hardware (EVSE), o sistema de gestão de energia (EMS) e o backoffice comercial.
- **Alto custo operacional** por dependência de suporte técnico para dúvidas rotineiras sobre o dashboard e os relatórios.

Esses problemas se traduzem em **perda de receita, downtime não planejado e baixa escalabilidade** para redes de recarga em expansão.

---

## 🤖 Proposta do Chatbot

### Nome: **ChargeBot**

O **ChargeBot** é um assistente conversacional com IA desenvolvido especificamente para **operadores comerciais de redes de eletropostos GoodWe**. Ele atua como uma camada de inteligência conversacional sobre o sistema ChargeGrid, permitindo que os operadores consultem dados operacionais, entendam alertas, compreendam relatórios de faturamento e tomem decisões sem precisar navegar por dashboards complexos ou acionar suporte técnico.

### Persona Atendida: Operador Comercial

**Justificativa da escolha:** O operador comercial é o perfil com maior volume de interações repetitivas e de baixa complexidade técnica — exatamente onde um chatbot gera maior ROI. Diferente do técnico de campo (que precisa de diagnósticos hands-on), o operador comercial busca respostas rápidas sobre: status do sistema, receita gerada, alertas ativos e agendamentos. Esse perfil também é o **decisor financeiro** que justifica o investimento na plataforma, tornando a experiência dele crítica para retenção e expansão da base de clientes GoodWe.

### Perguntas que o ChatBot deverá Responder

**Categoria: Status Operacional**
- Quantos carregadores estão online agora?
- Há algum eletroposto em falha ou offline?
- Qual é a potência total sendo consumida neste momento?

**Categoria: Faturamento e Receita**
- Qual foi a receita gerada hoje / esta semana / este mês?
- Quantas sessões de carga foram registradas hoje?
- Qual é o tempo médio de sessão por carregador?

**Categoria: Alertas e Anomalias**
- Há algum alerta ativo no sistema?
- Qual carregador registrou mais falhas nos últimos 7 dias?
- O sistema detectou algum ciclo de carga anômalo?

**Categoria: Relatórios e Projeções**
- Gere um resumo de desempenho da última semana.
- Qual horário de pico de uso da rede?
- Qual é a projeção de receita para o mês com base no ritmo atual?

**Categoria: Suporte e Orientação**
- Como configurar uma tarifa diferenciada para horário de pico?
- O que significa o código de erro E-04 no carregador #3?
- Como exportar o relatório de faturamento em PDF?

---

## 🛠️ Tecnologias Selecionadas e Justificativa Técnica

### Modelo de IA

| Tecnologia | Função | Justificativa |
|------------|--------|---------------|
| **OpenAI GPT-4o** (via API) | Motor de linguagem principal | Melhor custo-benefício para RAG em português; suporte nativo a function calling para integração com APIs de dados em tempo real; latência adequada para uso conversacional |
| **LangChain** | Orquestração de cadeia de prompts e RAG | Framework maduro com conectores prontos para vetorização, memória de conversação e integração com múltiplas fontes de dados |
| **FAISS / ChromaDB** | Vector Store para RAG | Armazenamento e busca semântica eficiente da base de conhecimento GoodWe (manuais, FAQs, códigos de erro) |
| **Python 3.11+** | Backend do chatbot | Ecossistema robusto para IA; integração nativa com LangChain e OpenAI SDK |

### Infraestrutura

| Tecnologia | Função | Justificativa |
|------------|--------|---------------|
| **FastAPI** | API REST do chatbot | Assíncrono, performático, tipagem forte com Pydantic |
| **Streamlit** | Interface de demonstração (MVP) | Prototipagem rápida sem necessidade de frontend dedicado |
| **Docker** | Containerização | Portabilidade e reprodutibilidade do ambiente |
| **GitHub Actions** | CI/CD | Automação de testes e deploy |

### Estratégia de IA: RAG (Retrieval-Augmented Generation)

O ChargeBot utiliza **RAG** em vez de fine-tuning por três razões:

1. **Atualização de dados sem retreinamento** — os manuais, tabelas de tarifas e códigos de erro da GoodWe podem ser atualizados no vector store sem modificar o modelo.
2. **Redução de alucinações** — o modelo responde com base em documentação real injetada no contexto, não em padrões aprendidos no pré-treinamento.
3. **Custo operacional inferior** — RAG com GPT-4o é mais barato e flexível que manter um modelo fine-tuned proprietário.

---

## 📁 Estrutura do Repositório

```
chargebot-goodwe/
├── README.md
├── docs/
│   ├── fluxograma.png
│   ├── modelo_de_teste.md
│   └── system_prompt.md
├── src/
│   ├── chatbot/
│   │   ├── main.py
│   │   ├── chain.py
│   │   └── retriever.py
│   ├── api/
│   │   └── routes.py
│   └── ui/
│       └── app.py
├── data/
│   └── knowledge_base/
│       ├── manual_goodwe.pdf
│       ├── codigos_erro.json
│       └── faq_operacional.md
├── tests/
│   └── test_responses.py
├── docker-compose.yml
├── requirements.txt
└── .env.example
```
## 🚀 Como Executar

### Opção 1 — Google Colab (Recomendado)

1. Faça upload do arquivo `ChargeBot_Colab.ipynb` no [Google Colab](https://colab.research.google.com)
2. Adicione sua chave OpenAI nos **Secrets do Colab**:
   - Clique no ícone 🔑 no painel esquerdo
   - Adicione: `OPENAI_API_KEY` = `sk-sua-chave-aqui`
3. Execute as células em ordem (Ctrl+F9 para rodar todas)
4. Use a interface visual na Célula 6 para interagir com o ChargeBot

### Opção 2 — Execução Local

**Requisitos:** Python 3.10+ instalado

```bash
# 1. Clone o repositório
git clone https://github.com/[usuario]/chargebot-goodwe.git
cd chargebot-goodwe

# 2. Crie e ative um ambiente virtual (recomendado)
python -m venv venv
source venv/bin/activate        # Linux/macOS
# venv\Scripts\activate         # Windows

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Configure a variável de ambiente com sua chave OpenAI
# OPÇÃO A: Arquivo .env (copie o template)
cp .env.example .env
# Edite .env e preencha: OPENAI_API_KEY=sk-sua-chave-aqui

# OPÇÃO B: Variável de ambiente direta
export OPENAI_API_KEY="sk-sua-chave-aqui"   # Linux/macOS
# set OPENAI_API_KEY=sk-sua-chave-aqui      # Windows CMD

# 5. Execute o chatbot
python src/chargebot.py
```

### Variáveis de Ambiente

| Variável | Obrigatória | Descrição |
|----------|-------------|-----------|
| `OPENAI_API_KEY` | ✅ Sim | Chave de acesso à API OpenAI |

> ⚠️ **Segurança:** Nunca exponha a API Key no código ou faça commit do arquivo `.env`. O `.gitignore` já está configurado para ignorá-lo.

---

## 💬 Exemplos de Uso

```
Você: Quantos carregadores estão online agora?

ChargeBot: Temos 10 de 12 carregadores operando agora (8 disponíveis, 2 em uso).
⚠️ CG-07 em falha desde 14h23 com erro E-07 (falha de comunicação OCPP).
🔧 CG-11 offline — verifique se há manutenção programada.
Quer que eu registre um chamado técnico para o CG-07?
```

```
Você: Qual foi a receita hoje?

ChargeBot: Hoje a rede gerou R$ 912,30 em 37 sessões — resultado sólido.
📊 vs. ontem: +3,9% · vs. média do mês: +9,3%
Com esse ritmo, projeção mensal: R$ 27.369 (+24,4% acima da meta de R$ 22.000).
💡 Momento ideal para tarifa diferenciada no pico (18h–20h). Quer configurar?
```

```
Você: Apareceu o erro E-04 no carregador 3. O que é isso?

ChargeBot: E-04 = falha de autenticação RFID no CG-03.
Causas: cartão danificado, leitor sujo, credencial expirada.
Workaround: QR Code ou app GoodWe. CG-03 continua operacional para outros métodos.
```

---

## 🧪 Resultados dos Testes

Ver arquivo completo: [`tests/resultados_testes.md`](tests/resultados_testes.md)

| # | Caso de Teste | Avaliação |
|---|--------------|-----------|
| 1 | Status Operacional | ✅ Adequada |
| 2 | Faturamento e Receita | ✅ Adequada |
| 3 | Alerta e Anomalia | ✅ Adequada |
| 4 | Relatório + Memória de Contexto | ✅ Adequada |
| 5 | Suporte Operacional (configuração) | ✅ Adequada |
| 6 | Código de Erro (bônus) | ✅ Adequada |

**Taxa de aprovação: 6/6 (100%)**

---

## 🔗 Links do Projeto

- **Repositório GitHub:** `https://github.com/rafaelferreirinhaquaresma-bit/ChargeBot-ChargeGrid-Intelligence`
- **Fluxograma:** `fluxograma.html`
- **Modelo de Teste:** `modelo_de_teste.md`
- **System Prompt:** `system_prompt.md`

---

*Projeto desenvolvido no contexto do EV Challenge 2026 — FIAP × GoodWe*
