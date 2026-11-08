---
name: especificar-feature
description: Transforme uma necessidade em critérios de aceite, contratos e fatias de implementação.
---

# especificar-feature

Entrada: problema e comportamento desejado; leia o fluxo atual antes de propor mudanças.

1. Identifique usuário, gatilho, resultado, regra de domínio e fora de escopo. Resolva ambiguidades que mudam dados, autorização ou compatibilidade; prossiga nas partes independentes.
2. Especifique sucesso e falha, vazio, autorização, concorrência e requisitos não funcionais relevantes. Use exemplos observáveis em [feature](../../templates/feature.md).
3. Localize componentes e contratos afetados. Registre consumidor e estados intermediários se houver vários repos. Não presuma persistência ou integrações novas.
4. Divida em fatias verticais com valor demonstrável e dependências explícitas; estime incerteza e risco, sem prometer prazo sem base.
5. Relacione aceite a verificação e defina a primeira tarefa executável.

Saída: especificação, aceite, limites, impactos e plano mínimo. Evite um backlog genérico sem ligação com o comportamento solicitado.
