# Roteador de contexto

Entrada mínima: `AGENTS.md` → `project.json` → estado ativo. Use a tabela e leia somente as referências necessárias. Em instalação `.ai-kit/`, caminhos abaixo partem da raiz do kit; o código é procurado na raiz da aplicação.

| Pedido | Primeiro procedimento | Referências condicionais |
|---|---|---|
| Primeiro contato / não sei por onde começar | [Entrada inicial](../COMECE_AQUI.md) | [Prompt inicial](../prompts/inicial.md) |
| Configurar ou conferir o kit | [Configuração](../docs/20-configuracao.md) | [Neutralidade de stack](../docs/19-neutralidade.md) |
| Integrar ferramentas / atualizar instalação | [Integrações](../docs/21-integracoes.md) e [update](../docs/22-atualizacao.md) | Plano, conflitos e hashes da instalação |
| Avaliar skills | [Avaliações](../docs/23-avaliacoes.md) | Harness do checkout central, fixtures e revisão independente |
| Aplicação do zero | [iniciar-projeto](../skills/iniciar-projeto/SKILL.md) | [Projeto novo](../docs/08-projeto-novo.md) |
| Primeira adoção / sistema existente | [adotar-sistema](../skills/adotar-sistema/SKILL.md) | [Sistema existente](../docs/09-sistema-existente.md) |
| Contexto global / vários repositórios | [mapear-sistema](../skills/mapear-sistema/SKILL.md) | [Multi-repo](../docs/10-multi-repositorio.md) |
| Requisito / plano de entrega | [especificar-feature](../skills/especificar-feature/SKILL.md) | [Feature](../templates/feature.md) |
| Decisão arquitetural | [desenhar-arquitetura](../skills/desenhar-arquitetura/SKILL.md) | [Arquitetura](../docs/02-arquitetura.md) |
| Feature | [implementar-feature](../skills/implementar-feature/SKILL.md) | Aceite e contratos locais |
| Bug | [corrigir-bug](../skills/corrigir-bug/SKILL.md) | Testes e chamadores |
| Refatoração | [refatorar-codigo](../skills/refatorar-codigo/SKILL.md) | Invariantes e [qualidade](../docs/12-qualidade.md) |
| Revisão | [revisar-diff](../skills/revisar-diff/SKILL.md) | Diff, consumidores e testes |
| Estratégia de testes | [planejar-testes](../skills/planejar-testes/SKILL.md) | [Plano](../templates/test-plan.md) |
| Segurança | [revisar-seguranca](../skills/revisar-seguranca/SKILL.md) | [Modelo de ameaças](../templates/threat-model.md) |
| API / eventos | [evoluir-contratos](../skills/evoluir-contratos/SKILL.md) | Produtores, consumidores e schemas |
| Banco / dados | [migrar-dados](../skills/migrar-dados/SKILL.md) | [Plano](../templates/migration.md) |
| Frontend / mobile / acessibilidade | [implementar-interface](../skills/implementar-interface/SKILL.md) | [Perfis](../docs/14-perfis.md) |
| Performance / escala | [otimizar-performance](../skills/otimizar-performance/SKILL.md) | Baseline e [operação](../docs/13-operacao.md) |
| Git / PR / Gitflow | [gerenciar-git](../skills/gerenciar-git/SKILL.md) | [Política Git](../docs/11-git-e-colaboracao.md) |
| CI / cadeia de entrega | [configurar-ci](../skills/configurar-ci/SKILL.md) | Gates reais do projeto |
| Release / rollout | [preparar-release](../skills/preparar-release/SKILL.md) | [Release](../templates/release.md) |
| Dependências / licenças | [atualizar-dependencias](../skills/atualizar-dependencias/SKILL.md) | Lockfile e avisos oficiais |
| Observabilidade / confiabilidade | [instrumentar-sistema](../skills/instrumentar-sistema/SKILL.md) | [Runbook](../templates/runbook.md) |
| Infraestrutura como código | [gerenciar-infraestrutura](../skills/gerenciar-infraestrutura/SKILL.md) | Plan, estado e blast radius |
| Incidente | [responder-incidente](../skills/responder-incidente/SKILL.md) | Runbook e escopo autorizado |
| Documentação | [documentar-sistema](../skills/documentar-sistema/SKILL.md) | Mapa e ADRs afetados |
| Retomada / transferência | [preparar-handoff](../skills/preparar-handoff/SKILL.md) | Estado, HEAD e diff atuais |

Busque símbolos com `rg`; exclua builds, caches, dependências e diretórios sensíveis. Expanda um componente por vez. Estado anterior não é prova: confronte com código e commit. Se faltar acesso, registre a lacuna e continue a parte independente.
