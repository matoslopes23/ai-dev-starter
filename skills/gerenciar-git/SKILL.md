---
name: gerenciar-git
description: Aplique a política Git existente ou defina um fluxo de branches, revisão e releases adequado ao projeto.
---

# gerenciar-git

Entrada: operação pedida, checkout, política atual e destino quando houver publicação. Leia [Git](../../docs/11-git-e-colaboracao.md).

1. Confira branch, HEAD, status e mudanças alheias. Descubra base e política em configuração/CI; `main` não é sempre a base de feature.
2. Para escolher política, compare frequência de entrega e versões mantidas. Para Gitflow, configure também retorno de hotfix/release e gates; não apenas nomes.
3. Prepare a mudança em fronteira isolada quando necessário. Não faça reset/clean/force push ou rebase de histórico compartilhado para facilitar o trabalho.
4. Antes de commit/publicação autorizados, revise arquivos novos e diff completo, checks do estado final e destino sem imprimir credenciais. Stage apenas arquivos da tarefa.
5. Use [pull-request](../../templates/pull-request.md). Registre base/head e resultado verificável da operação; templates não ativam branch protection.

Saída: política/PR/operação pedida e evidência, conforme escopo. Se publicação não estiver autorizada, entregue o diff e texto revisáveis sem executá-la.
