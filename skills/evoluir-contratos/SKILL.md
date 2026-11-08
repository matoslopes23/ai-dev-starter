---
name: evoluir-contratos
description: Crie ou altere APIs, schemas e eventos preservando consumidores e compatibilidade de versões.
---

# evoluir-contratos

Entrada: contrato atual, mudança desejada, produtores e consumidores. Consulte [multi-repo](../../docs/10-multi-repositorio.md) se necessário.

1. Encontre schema e implementação reais: payload, semântica, erros, status, autenticação, paginação, timeout e idempotência conforme o protocolo.
2. Identifique consumidores conhecidos e lacunas; avalie remoção, renomeação, nulabilidade, enum, defaults, precisão e ordem. Adição de campo também pode quebrar consumidor estrito.
3. Para eventos, defina entrega, duplicação, ordenação, chave, retenção, replay e tratamento de mensagens inválidas. Não assuma exactly-once por conveniência.
4. Escolha mudança compatível ou versão/migração explícita. Use [cross-repo-change](../../templates/cross-repo-change.md) para estados antigo/novo e ordem de rollout.
5. Implemente quando autorizado, valide schema e contrato com versões coexistentes e atualize documentação/depreciação.

Saída: contrato, matriz de compatibilidade, testes e plano de migração. Não remova a versão antiga antes da evidência de migração dos consumidores.
