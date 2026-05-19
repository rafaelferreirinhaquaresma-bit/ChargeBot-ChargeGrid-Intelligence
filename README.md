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

---

## 🔗 Links do Projeto

- **Repositório GitHub:** `[URL DO REPOSITÓRIO]`
- **Fluxograma:** `docs/fluxograma.png`
- **Modelo de Teste:** `docs/modelo_de_teste.md`
- **System Prompt:** `docs/system_prompt.md`

---

*Projeto desenvolvido no contexto do EV Challenge 2026 — FIAP × GoodWe*
