---
name: implementar-feature
description: Implemente uma funcionalidade especificada com mudança pequena, contratos preservados e validação proporcional.
---

# implementar-feature

Entrada: aceite, escopo e componentes autorizados. Leia contratos e equivalente existente antes de editar.

1. Confira baseline, políticas do componente e consumidores. Se o requisito ainda muda a solução, especifique a parte incerta antes da implementação dependente.
2. Registre arquivos, riscos, plano e verificações em `.ai/current-task.md`. Evite refatoração incidental e dependências sem necessidade.
3. Implemente a menor fatia de ponta a ponta. Valide entrada, invariantes, autorização e erros nas fronteiras apropriadas; preserve a direção das dependências.
4. Adicione testes onde protegem regra ou contrato novo; valide estados de UI ou consumidores conforme impacto. Não escreva testes que apenas reproduzem funções privadas.
5. Execute gates afetados, revise o diff completo e atualize a documentação necessária. Revalide após mudanças relevantes.

Saída: comportamento demonstrável, arquivos, comandos/resultados, riscos e próxima ação. Use [fluxo e gates](../../docs/03-fluxo-e-gates.md) como definição de pronto.
