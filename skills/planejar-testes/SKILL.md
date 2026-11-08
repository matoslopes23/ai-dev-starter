---
name: planejar-testes
description: Escolha e implemente verificações para regras, contratos e jornadas conforme risco e stack.
---

# planejar-testes

Entrada: mudança ou área a proteger, baseline e gates existentes. Leia [qualidade](../../docs/12-qualidade.md).

1. Relacione regra/risco a comportamento e fronteira observável em [test-plan](../../templates/test-plan.md).
2. Escolha unidade, integração, contrato ou E2E pelo defeito que precisa detectar. Inclua casos negativos e concorrência quando mudarem a correção.
3. Use dados sintéticos, relógio/aleatoriedade controláveis e recursos isolados. Mocks em fronteiras não comprovam semântica real de banco ou rede.
4. Se implementação estiver no escopo, introduza o menor conjunto de testes útil. Evite cobrir detalhes privados ou exigir um percentual universal.
5. Execute e registre ambiente e resultado. Investigue flaky tests; não use retry ou exclusão silenciosa como aprovação.

Saída: matriz de risco/cenário, testes necessários e evidência. Distingua check dispensado com justificativa de check obrigatório não executado.
