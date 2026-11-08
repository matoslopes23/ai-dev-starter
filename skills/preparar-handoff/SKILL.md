---
name: preparar-handoff
description: Registre estado verificável para retomar ou transferir trabalho sem perder decisões e limitações.
---

# preparar-handoff

Entrada: tarefa ativa, código atual e verificações realizadas.

1. Confira branch, HEAD e diff de cada repositório afetado, inclusive arquivos novos. Não confie em estado registrado antes da última edição.
2. Atualize `.ai/current-task.md` com fatos, decisões, arquivos e verificações do estado final. Não guarde transcrição ou dados sensíveis.
3. Use [handoff](../../templates/handoff.md): resultado versus aceite, comandos/resultados, pendências, riscos e próxima ação concreta.
4. Em multi-repo, registre commits/branches e ordem das etapas restantes. Alterações locais não são transferidas para outra máquina apenas por atualizar o documento.
5. Não publique, descarte mudanças ou faça commit só para encerrar a sessão. Use o escopo e autorização existentes.

Saída: estado e próxima ação que outro operador consiga conferir. Evidência expirada deve ser marcada, não reaproveitada como aprovação.
