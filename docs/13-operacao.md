# Entrega, observabilidade e operação

A arquitetura inclui como implantar, observar, recuperar e pagar pelo sistema. Registre ambientes, responsáveis, configuração por ambiente sem valores secretos e origem de artefatos. Não infira produção a partir da branch principal.

## CI e release

Pipelines devem executar os gates reais em ambientes reproduzíveis, com privilégio mínimo e isolamento de código não confiável. Selecione ferramentas da stack; fixe versões e planeje atualização. Cache é otimização, não fonte de verdade. Não use segredos de produção para testes de PR.

Promova artefatos identificáveis pelo mesmo commit/digest, com configuração e segredos externos apropriados. Em [release](../templates/release.md), registre escopo, compatibilidade, dependências, rollout gradual quando útil, health checks, métricas e critérios de interrupção. Migração de dados pode impedir rollback simples: planeje roll-forward, backup e recuperação testada.

## Confiabilidade

Defina objetivos de serviço a partir da jornada: indicador, meta, janela e orçamento de erro. Não invente 99,99% sem custo e impacto. Defina limites de latência, erro, saturação e tamanho de fila, e quem responde quando excedidos.

Logs estruturados sanitizados, métricas e traces devem permitir seguir uma operação entre fronteiras. Use correlação sem dados pessoais e limite cardinalidade; IDs de usuário como label podem gerar custo e risco. Alertas devem acionar uma ação com responsável e runbook. Health checks precisam distinguir disponibilidade para servir de dependências não críticas.

## Dados e recuperação

Declare RPO/RTO com o negócio, política de backup e evidência de restauração em ambiente seguro. Backup existente não comprova recuperabilidade. Filas precisam de retenção, reprocessamento e tratamento de mensagens problemáticas. Retry e replay precisam preservar idempotência e regras de domínio.

## Infraestrutura e incidentes

Infraestrutura como código exige revisão de plan, gerenciamento de estado/locks, detecção de drift, custo e recuperação. Não aplique um plan de outro estado nem exponha valores sensíveis na saída.

Durante incidente: confirme impacto e escopo, priorize mitigação reversível autorizada, preserve evidências sanitizadas e coordene o responsável. Não confunda correlação com causa. Após estabilizar, registre linha do tempo, causa confirmada, fatores contribuintes e ações com dono. Use [runbook](../templates/runbook.md) e [incident](../templates/incident.md).
