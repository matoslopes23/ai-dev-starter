---
name: desenhar-arquitetura
description: Avalie ou defina fronteiras e decisões arquiteturais a partir de requisitos e restrições concretos.
---

# desenhar-arquitetura

Entrada: jornada, requisitos não funcionais, arquitetura atual e decisão necessária. Leia [arquitetura](../../docs/02-arquitetura.md).

1. Trace responsabilidades, dependências, dados e operação atuais; diferencie acoplamento observado de risco hipotético.
2. Compare alternativas incluindo manter o desenho atual com uma melhoria local. Avalie custo de mudança, testes, consistência, segurança e operação, além da estrutura de pastas.
3. Mantenha regras independentes dos detalhes de I/O. Crie abstração quando houver dependência ou variação real; prefira coesão a camadas por simetria.
4. Para escala, declare carga/metas e plano de medição; não distribua serviços sem justificar limites e custo de coordenação.
5. Registre [ADR](../../templates/adr.md), fronteiras, contratos e migração gradual quando necessária. Se implementar estiver autorizado, mantenha a primeira mudança reversível.

Saída: decisão justificada, consequências, validação e condição de revisão. Uma arquitetura proposta não é automaticamente a arquitetura observada do sistema.
