# 🧪 Modelo de Teste — ChargeBot GoodWe
### Sprint 1 · EV Challenge 2026

---

## Metodologia de Avaliação

Cada resposta do ChargeBot será avaliada em três dimensões:

| Critério | Peso | Descrição |
|----------|------|-----------|
| **Precisão** | 40% | A resposta contém as informações corretas e completas? |
| **Tom e Persona** | 30% | A resposta é adequada ao perfil do operador comercial, clara e objetiva? |
| **Acionabilidade** | 30% | A resposta orienta o usuário a uma próxima ação concreta? |

---

## Caso de Teste 1 — Status Operacional

**Pergunta do Usuário:**
> "Quantos carregadores estão online agora e tem algum com problema?"

**Contexto Injetado (simulado):**
```json
{
  "chargers_total": 12,
  "chargers_online": 10,
  "chargers_offline": 1,
  "chargers_fault": 1,
  "fault_details": [{"id": "CG-03", "error": "E-07", "since": "14:32"}],
  "offline_details": [{"id": "CG-09", "reason": "maintenance_scheduled"}]
}
```

**Resposta Esperada (ideal):**
> "Atualmente **10 de 12 carregadores** estão operando normalmente.
>
> ⚠️ **CG-03** está em falha desde as 14h32 com erro **E-07** (falha na comunicação OCPP). Recomendo verificar a conectividade de rede desse ponto.
>
> 🔧 **CG-09** está offline por manutenção programada.
>
> Deseja que eu gere um relatório de disponibilidade detalhado ou abra um chamado para o CG-03?"

**Critérios de Aprovação:**
- [ ] Cita os números corretos (10/12)
- [ ] Identifica os dois carregadores problemáticos com seus IDs
- [ ] Menciona o código de erro E-07
- [ ] Oferece próximo passo acionável
- [ ] Tom profissional e direto

---

## Caso de Teste 2 — Faturamento

**Pergunta do Usuário:**
> "Qual foi a receita da rede hoje? Tá dentro do esperado?"

**Contexto Injetado (simulado):**
```json
{
  "revenue_today": 847.50,
  "revenue_yesterday": 923.00,
  "revenue_monthly_avg_daily": 810.00,
  "sessions_today": 34,
  "currency": "BRL"
}
```

**Resposta Esperada (ideal):**
> "Hoje a rede gerou **R$ 847,50** em **34 sessões de carga**.
>
> 📊 Comparando:
> - vs. ontem: **-8,2%** (R$ 923,00)
> - vs. média diária do mês: **+4,6%** (R$ 810,00)
>
> O desempenho está **acima da média mensal**, embora um pouco abaixo de ontem. Isso é consistente com padrões de menor movimento em dias de semana similares.
>
> Quer ver o detalhamento por carregador ou por horário?"

**Critérios de Aprovação:**
- [ ] Informa o valor correto (R$ 847,50)
- [ ] Informa número de sessões (34)
- [ ] Compara com referências relevantes (ontem e média mensal)
- [ ] Oferece contexto analítico, não apenas o número bruto
- [ ] Propõe aprofundamento

---

## Caso de Teste 3 — Alerta e Anomalia

**Pergunta do Usuário:**
> "O sistema mandou um alerta agora pouco, o que aconteceu?"

**Contexto Injetado (simulado):**
```json
{
  "alerts": [{
    "timestamp": "16:47",
    "type": "power_spike",
    "severity": "medium",
    "affected_charger": "CG-01",
    "details": "Consumo de 22kW detectado em carregador configurado para máx 11kW",
    "suggested_action": "Verificar configuração de limite de potência ou trocar cabo"
  }]
}
```

**Resposta Esperada (ideal):**
> "O alerta das **16h47** é referente ao **CG-01** e indica um **pico de consumo anômalo**: o carregador registrou **22 kW**, o dobro do limite configurado de 11 kW.
>
> ⚡ **Risco:** Esse comportamento pode indicar falha na proteção de potência ou uso de cabo inadequado pelo usuário.
>
> **Ação recomendada:**
> 1. Verifique se o cabo utilizado é compatível com o padrão do ponto.
> 2. Confirme o limite de potência nas configurações do CG-01.
> 3. Se o problema persistir, isole o carregador e acione suporte técnico.
>
> Deseja que eu registre um chamado técnico agora?"

**Critérios de Aprovação:**
- [ ] Identifica o carregador afetado (CG-01)
- [ ] Explica o problema de forma não-técnica (consumo dobrado)
- [ ] Apresenta riscos e consequências
- [ ] Oferece passos acionáveis numerados
- [ ] Oferece encaminhamento para chamado técnico

---

## Caso de Teste 4 — Relatório e Projeção

**Pergunta do Usuário:**
> "Me dá um resumo do desempenho da semana passada e quanto a gente deve fechar esse mês."

**Contexto Injetado (simulado):**
```json
{
  "last_week": {
    "revenue": 5840.00,
    "sessions": 231,
    "avg_session_minutes": 38,
    "peak_hour": "18h-20h",
    "best_day": "Sexta-feira",
    "availability_pct": 94.2
  },
  "current_month": {
    "days_elapsed": 13,
    "revenue_so_far": 10420.00,
    "projected_month_end": 24180.00,
    "target": 22000.00
  }
}
```

**Resposta Esperada (ideal):**
> "**Resumo da semana passada:**
>
> | Métrica | Resultado |
> |---------|-----------|
> | Receita | R$ 5.840,00 |
> | Sessões | 231 cargas |
> | Duração média | 38 min/sessão |
> | Disponibilidade | 94,2% |
> | Horário de pico | 18h–20h |
> | Melhor dia | Sexta-feira |
>
> **Projeção do mês:**
> Com R$ 10.420 já faturados em 13 dias, a projeção é fechar em torno de **R$ 24.180** — **+9,9% acima da meta** de R$ 22.000.
>
> 📈 O desempenho está sólido. O maior pico às 18h sugere oportunidade de tarifa dinâmica nesse horário para aumentar margem. Quer explorar essa configuração?"

**Critérios de Aprovação:**
- [ ] Apresenta todos os dados semanais de forma organizada (tabela ou lista)
- [ ] Calcula e exibe a projeção mensal
- [ ] Compara projeção com a meta
- [ ] Gera insight proativo (tarifa dinâmica)
- [ ] Propõe próximo passo de valor

---

## Caso de Teste 5 — Suporte Operacional

**Pergunta do Usuário:**
> "Como eu configuro uma tarifa diferente pra horário de pico? Quero cobrar mais entre 18h e 20h."

**Contexto Injetado (simulado):**
```json
{
  "user_role": "commercial_operator",
  "platform": "GoodWe ChargeGrid Dashboard v2.3",
  "feature_available": true,
  "feature_name": "Dynamic Pricing"
}
```

**Resposta Esperada (ideal):**
> "Ótima estratégia! O ChargeGrid suporta **tarifas dinâmicas por horário**. Veja como configurar:
>
> 1. Acesse o **Dashboard ChargeGrid** → menu lateral **Configurações** → **Tarifas**.
> 2. Clique em **Nova Regra Tarifária**.
> 3. Defina o intervalo: **18:00 às 20:00**, dias da semana desejados.
> 4. Insira o valor por kWh para esse período (ex: R$ 1,80/kWh vs. R$ 1,20 no horário normal).
> 5. Ative a regra e confirme.
>
> ⏱️ A mudança entra em vigor na próxima sessão iniciada após o horário configurado.
>
> 💡 **Dica:** Comunique a mudança via app aos usuários frequentes para evitar surpresas na cobrança.
>
> Quer ajuda para calcular qual tarifa maximiza receita sem reduzir o volume de sessões?"

**Critérios de Aprovação:**
- [ ] Confirma que a funcionalidade existe na plataforma
- [ ] Fornece passos numerados e claros
- [ ] Inclui detalhe técnico relevante (quando a mudança entra em vigor)
- [ ] Oferece dica proativa de UX para os motoristas
- [ ] Propõe análise de precificação como próximo passo

---

## Caso de Teste 6 — Código de Erro (Bonus)

**Pergunta do Usuário:**
> "Apareceu o erro E-04 no carregador 7. O que é isso?"

**Resposta Esperada (ideal):**
> "O erro **E-04** no **CG-07** indica **falha de autenticação RFID** — o leitor de cartão não conseguiu validar a credencial do usuário.
>
> **Causas mais comuns:**
> - Cartão RFID danificado ou desmagnetizado
> - Leitor sujo ou com interferência física
> - Credencial expirada no sistema de gestão
>
> **O que fazer:**
> 1. Peça ao usuário que tente outro cartão ou use autenticação via app.
> 2. Limpe o leitor com pano seco.
> 3. Se persistir, verifique no painel de usuários se a credencial está ativa.
>
> O carregador continua operacional — apenas a sessão por RFID está bloqueada. Autenticação via QR Code ou app está disponível como alternativa."

**Critérios de Aprovação:**
- [ ] Identifica corretamente o erro E-04 (RFID)
- [ ] Lista causas possíveis
- [ ] Oferece workaround imediato (QR/app)
- [ ] Informa que o carregador não está completamente inoperante
- [ ] Tom tranquilizador, não alarmista

---

## Escala de Avaliação por Caso de Teste

| Score | Descrição |
|-------|-----------|
| 5/5 critérios | ✅ Excelente — resposta ideal |
| 4/5 critérios | 🟡 Bom — aprovado com ressalvas menores |
| 3/5 critérios | 🟠 Regular — necessita ajuste no prompt |
| ≤ 2/5 critérios | ❌ Reprovado — revisão profunda do contexto |

---

*Modelo de Teste — Sprint 1 · ChargeBot GoodWe · EV Challenge 2026 · FIAP*
