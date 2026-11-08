---
name: otimizar-performance
description: Diagnostique gargalos e otimize desempenho com baseline, metas e comparação reproduzível.
---

# otimizar-performance

Entrada: sintoma, jornada, carga esperada e ambiente permitido.

1. Defina métrica e meta: latência e percentis, throughput, memória, CPU, fila, custo ou tamanho de payload. Registre condições e variabilidade.
2. Meça e localize gargalo com profiling, consultas ou telemetria sanitizada. Diferencie tempo de rede, computação, I/O e espera; não otimize pela aparência do código.
3. Compare alternativas e efeitos: índice, consulta, algoritmo, batching, pool, cache ou paralelismo. Cache exige invalidação e isolamento; retry/concorrência podem aumentar sobrecarga.
4. Faça mudança pequena, mantenha correção e compare cenário idêntico antes/depois, incluindo degradação sob carga e custo relevante.
5. Registre ganho, regressões e limites estatísticos. Proponha escala horizontal/distribuição só com justificativa operacional.

Saída: causa medida, alteração e resultados. Não execute carga contra produção ou serviço de terceiro sem autorização específica de ambiente e limites.
