---
name: preparar-release
description: Prepare uma versão com compatibilidade, rollout, observação e recuperação antes de publicar.
---

# preparar-release

Entrada: escopo da versão, commit/artefato, ambientes e autorização. Use [release](../../templates/release.md).

1. Confirme checks e aceite do estado final, dependências, contratos, migrações e notas para consumidores. Identifique alterações incompatíveis e versão conforme política vigente.
2. Defina artefato imutável/origem, configuração externa, etapas e responsáveis. Para vários repos, planeje estados intermediários e ordem explicitamente.
3. Registre rollout, health checks, métricas, janela, critérios de interrupção e rollback/roll-forward, incluindo dados incompatíveis.
4. Prepare comandos/runbook concretos e revise o destino. Se a operação já estiver autorizada, execute dentro desses limites e verifique a versão/saúde resultantes.
5. Caso contrário entregue o pacote revisável para a decisão final, sem tratar “preparar release” como autorização para deploy.

Saída: prontidão, riscos, plano e resultado observado das operações realizadas. Não afirme versão publicada a partir de tag ou branch apenas local.
