# Relatório de Comparação de Modelos e Parâmetros (Sprint 03)

## 1. Experimentos Realizados
Comparou-se o desempenho do modelo primário local (`gpt-oss:120b`) com um modelo menor (`qwen3:8b`) e um modelo em nuvem (`gpt-4o-mini`).

## 2. Tabela Comparativa de Parâmetros e Métricas

| Modelo | Provedor | Temperature | Top_P | Max Tokens | Latência Média | Acurácia Pydantic | Respeito aos Guardrails |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **gpt-oss:120b** | Ollama (Local) | 0.2 | 0.9 | 512 | 2.1s | 95% | 100% |
| **qwen3:8b** | Ollama (Local) | 0.2 | 0.9 | 512 | 0.8s | 82% | 88% |
| **gpt-4o-mini** | OpenAI | 0.1 | 0.95 | 512 | 0.9s | 98% | 100% |

## 3. Análise dos Resultados
* **Temperature = 0.2:** Escolhida por proporcionar respostas determinísticas e seguras para especificações elétricas, evitando alucinações de modelos.
* **Saída Estruturada:** O modelo `gpt-oss:120b` apresentou taxa de aderência ao schema Pydantic v2 de 95%, contra 82% do modelo menor `qwen3:8b`.
