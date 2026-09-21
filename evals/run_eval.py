import json
import time
from src.chain.builder import executar_interacao

def rodar_avaliacao():
    with open("evals/eval_dataset.json", "r", encoding="utf-8") as f:
        dataset = json.load(f)
        
    resultados = []
    sucessos = 0
    tempo_total = 0

    print("=== INICIANDO AVALIAÇÃO DA SPRINT 03 ===")
    for item in dataset:
        inicio = time.time()
        res = executar_interacao(session_id=f"eval_test_{item['id']}", input_texto=item["entrada"])
        duracao = time.time() - inicio
        tempo_total += duracao
        
        # Lógica de validação do resultado
        aprovado = False
        if item["categoria"] == "happy_path" and not res.get("fora_de_escopo"):
            aprovado = True
        elif item.get("espera_recusa") and res.get("fora_de_escopo"):
            aprovado = True
            
        if aprovado:
            sucessos += 1

        resultados.append({
            "id": item["id"],
            "categoria": item["categoria"],
            "entrada": item["entrada"],
            "latencia_segundos": round(duracao, 2),
            "aprovado": aprovado,
            "resposta": res
        })

    acuracia = (sucessos / len(dataset)) * 100
    latencia_media = tempo_total / len(dataset)

    relatorio_final = {
        "acuracia_geral": round(acuracia, 2),
        "latencia_media_s": round(latencia_media, 2),
        "total_testes": len(dataset),
        "sucessos": sucessos,
        "detalhes": resultados
    }

    with open("evals/sprint3_results.json", "w", encoding="utf-8") as f:
        json.dump(relatorio_final, f, indent=2, ensure_ascii=False)

    print(f"Avaliação Concluída! Acurácia: {acuracia}% | Latência Média: {latencia_media:.2f}s")

if __name__ == "__main__":
    rodar_avaliacao()
