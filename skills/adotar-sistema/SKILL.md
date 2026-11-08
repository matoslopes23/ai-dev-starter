---
name: adotar-sistema
description: Diagnostique um projeto existente e planeje a adoção incremental das práticas sem reestruturar o produto de imediato.
---

# adotar-sistema

Entrada: repositórios/caminhos autorizados, objetivo da adoção e limites. Leia [sistema existente](../../docs/09-sistema-existente.md).

1. Confirme inventário, acesso, instruções, branch/HEAD e mudanças de cada checkout. Liste repositórios desconhecidos ou ausentes.
2. Descubra stack, instalação, CI e checks nos manifests e scripts. Inspecione efeitos antes de executar; não abra segredos. Registre baseline com passou/falhou/não executado/não configurado.
3. Trace jornadas críticas e contratos com [mapa](../../templates/system-map.md). Distinga evidência de hipótese e marque cobertura parcial. Não execute todos os scripts preventivamente.
4. Compare riscos observados com arquitetura, qualidade, segurança e operação aplicáveis. Preencha [diagnóstico](../../templates/diagnostic.md) com impacto e reprodução, sem tratar gosto como defeito.
5. Monte [adoção](../../templates/adoption-plan.md) por impacto, esforço e dependências, com primeira melhoria pequena e evidência de conclusão. Preserve o fluxo e a arquitetura existentes até decisão justificada.

Saída: baseline, mapa, lacunas e plano incremental. Diagnóstico sozinho não autoriza alterar código, repositórios remotos ou produção; se melhorias já estiverem autorizadas, execute as fatias correspondentes.
