---
name: refatorar-codigo
description: Melhore a estrutura interna de código existente preservando comportamento e contratos observáveis.
---

# refatorar-codigo

Entrada: problema estrutural concreto e fronteira autorizada; leia [arquitetura](../../docs/02-arquitetura.md).

1. Explicite o custo atual: motivos de mudança misturados, duplicação de regra, dependência difícil de testar ou acoplamento entre módulos. Métrica isolada não comprova defeito.
2. Identifique invariantes e API pública. Em legado frágil, crie caracterização dos comportamentos críticos antes de mover código.
3. Planeje passos pequenos, mantendo a aplicação executável. Não misture mudança de comportamento, atualização de stack e reorganização ampla sem necessidade.
4. Extraia fronteiras pelo conhecimento e pelos efeitos, não apenas pela semelhança textual. Elimine abstrações sem consumidor quando isso reduzir custo demonstrável.
5. Execute gates a cada passo relevante e compare contratos/resultados. Revise chamadas e consumidores depois de mover símbolos.

Saída: estrutura melhorada com motivo observável, comportamento preservado e evidências. Mudança de regra deve ser declarada e tratada com aceite próprio.
