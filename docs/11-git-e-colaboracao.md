# Git, branches e colaboração

Preserve o fluxo do projeto até uma decisão explícita. Não há uma política adequada a toda aplicação. Registre `git_workflow` em `project.json` com justificativa em ADR quando mudar uma política existente.

| Política | Uso a considerar | Operação |
|---|---|---|
| GitHub Flow | Produto com uma linha principal e entrega frequente | Branch curta → PR → checks/review → main → release/deploy |
| Trunk-based | Integração frequente, lotes pequenos e CI confiável | Branches muito curtas ou integração controlada em main; flags para trabalho incompleto |
| Gitflow | Releases coordenadas e versões explicitamente mantidas | main + develop + feature/release/hotfix, com reintegração disciplinada |

O autor do Gitflow recomenda considerar um fluxo mais simples para entrega contínua; consulte [as fontes](15-referencias.md). Para um projeto novo, GitHub Flow é um ponto de partida possível; confirme requisitos de release antes de adotá-lo. `undecided` é válido durante descoberta.

## Gitflow, quando escolhido

- `main`: histórico de versões liberadas. `develop`: integração da próxima versão.
- `feature/<id>-<assunto>` parte de `develop` e retorna via PR para `develop`.
- `release/<versao>` parte de `develop`; recebe estabilização, sem novas features. Ao liberar, integra em `main`, recebe tag e suas correções retornam a `develop`.
- `hotfix/<id>` parte da versão liberada em `main`; após validação, integra em `main` com nova versão e retorna a `develop` e à release ativa quando necessário.
- Defina em quais branches o CI roda, quem mantém versões antigas e quem verifica os retornos. Tags e backports devem apontar para correções comprovadas. Não basta criar nomes de branches.

PRs devem indicar base correta, problema, comportamento resultante, validação e riscos. Merge commits preservam a topologia tradicional do Gitflow; squash/rebase podem servir a outros fluxos. Escolha uma política coerente e evite rebase de histórico compartilhado. Nomes `feat/`, `fix/`, `chore/` e commits convencionais são convenções opcionais, não garantias de qualidade.

## Proteções verificáveis

Defina rulesets/branch protection conforme recursos do provedor: PR, revisão proporcional ao risco, checks reais obrigatórios e bloqueio de force push/exclusão em branches protegidas. Templates não ativam essas proteções. Registre configuração desejada e estado observado; aplique remotamente apenas no escopo autorizado. CODEOWNERS precisa de responsáveis reais e política de revisão correspondente; não gere usuários fictícios.

## Trabalho local

Antes de editar: branch, HEAD, status e fronteira autorizada. Para começar uma branch, confirme base, alterações preexistentes e necessidade de atualização remota. Worktree isolada pode preservar trabalho em curso; não use reset ou stash destrutivo como preparação automática.

Antes de publicar: confira remoto e conta sem exibir credenciais, arquivos novos e diff completo, testes do estado final, informações privadas e autorização de destino. `git diff --check` sozinho não inclui arquivos não rastreados. Revise-os explicitamente. Stage apenas os arquivos da tarefa; não faça `git add .` em um checkout com alterações alheias.

Use [pull-request](../templates/pull-request.md) e [gerenciar-git](../skills/gerenciar-git/SKILL.md). O kit não exige commit, push ou merge para concluir trabalho local.
