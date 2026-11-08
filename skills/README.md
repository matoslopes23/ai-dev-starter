# Catálogo de skills de engenharia

Cada skill é um procedimento acionável para um objetivo específico. Leia o contrato e a configuração do projeto primeiro; depois carregue só a skill necessária. O catálogo cobre o ciclo de vida comum e pode ser ampliado com conhecimento da stack ou do domínio quando houver necessidade concreta.

Uso manual: `Leia .ai-kit/skills/corrigir-bug/SKILL.md e corrija <comportamento>, com aceite <resultado> e limites <escopo>.` No checkout central do kit, retire o prefixo `.ai-kit/`. Descoberta automática depende do agente; metadados YAML não garantem instalação em toda ferramenta.

| Skill | Quando usar |
|---|---|
| [iniciar-projeto](iniciar-projeto/SKILL.md) | Defina e inicie uma aplicação nova, da descoberta à primeira entrega vertical verificável. |
| [adotar-sistema](adotar-sistema/SKILL.md) | Diagnostique um projeto existente e planeje a adoção incremental das práticas sem reestruturar o produto de imediato. |
| [mapear-sistema](mapear-sistema/SKILL.md) | Mapeie jornadas, dados, contratos e dependências de um sistema, inclusive distribuído por vários repositórios. |
| [especificar-feature](especificar-feature/SKILL.md) | Transforme uma necessidade em critérios de aceite, contratos e fatias de implementação. |
| [desenhar-arquitetura](desenhar-arquitetura/SKILL.md) | Avalie ou defina fronteiras e decisões arquiteturais a partir de requisitos e restrições concretos. |
| [implementar-feature](implementar-feature/SKILL.md) | Implemente uma funcionalidade especificada com mudança pequena, contratos preservados e validação proporcional. |
| [corrigir-bug](corrigir-bug/SKILL.md) | Reproduza e corrija um defeito com causa confirmada e proteção contra regressão. |
| [refatorar-codigo](refatorar-codigo/SKILL.md) | Melhore a estrutura interna de código existente preservando comportamento e contratos observáveis. |
| [revisar-diff](revisar-diff/SKILL.md) | Revise alterações de código ou documentação e relate defeitos concretos por impacto e reprodução. |
| [planejar-testes](planejar-testes/SKILL.md) | Escolha e implemente verificações para regras, contratos e jornadas conforme risco e stack. |
| [revisar-seguranca](revisar-seguranca/SKILL.md) | Avalie ameaças e controles de uma mudança ou aplicação com evidências e escopo de segurança explícito. |
| [evoluir-contratos](evoluir-contratos/SKILL.md) | Crie ou altere APIs, schemas e eventos preservando consumidores e compatibilidade de versões. |
| [migrar-dados](migrar-dados/SKILL.md) | Planeje e implemente mudanças de schema ou dados com compatibilidade, ensaio e recuperação. |
| [implementar-interface](implementar-interface/SKILL.md) | Implemente ou ajuste interfaces web/mobile com estados, acessibilidade e navegação verificáveis. |
| [otimizar-performance](otimizar-performance/SKILL.md) | Diagnostique gargalos e otimize desempenho com baseline, metas e comparação reproduzível. |
| [gerenciar-git](gerenciar-git/SKILL.md) | Aplique a política Git existente ou defina um fluxo de branches, revisão e releases adequado ao projeto. |
| [configurar-ci](configurar-ci/SKILL.md) | Crie ou melhore integração contínua usando gates e runtimes reais do projeto com privilégio mínimo. |
| [preparar-release](preparar-release/SKILL.md) | Prepare uma versão com compatibilidade, rollout, observação e recuperação antes de publicar. |
| [atualizar-dependencias](atualizar-dependencias/SKILL.md) | Atualize bibliotecas, runtimes ou imagens com análise de compatibilidade, vulnerabilidade e licença. |
| [instrumentar-sistema](instrumentar-sistema/SKILL.md) | Defina e implemente sinais de observabilidade e objetivos de confiabilidade ligados a jornadas reais. |
| [gerenciar-infraestrutura](gerenciar-infraestrutura/SKILL.md) | Revise ou altere infraestrutura como código com estado, permissões, custo e recuperação explícitos. |
| [responder-incidente](responder-incidente/SKILL.md) | Investigue e coordene um incidente com mitigação autorizada, evidências e análise posterior. |
| [documentar-sistema](documentar-sistema/SKILL.md) | Atualize documentação técnica, mapas e decisões com fatos verificáveis e comandos reproduzíveis. |
| [preparar-handoff](preparar-handoff/SKILL.md) | Registre estado verificável para retomar ou transferir trabalho sem perder decisões e limitações. |

As skills usam o escopo e a autorização já presentes no pedido. Referências internas são carregadas por necessidade, não todas de uma vez. Especialização de domínio, auditoria formal e operação de produção exigem contexto e responsáveis próprios. Para adicionar uma skill, defina gatilho claro, entrada, decisão que melhora, saída e verificações; evite um procedimento que apenas repete o contrato geral.
