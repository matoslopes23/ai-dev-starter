---
name: configurar-ci
description: Crie ou melhore integração contínua usando gates e runtimes reais do projeto com privilégio mínimo.
---

# configurar-ci

Entrada: stack, comandos locais, CI existente e requisitos de contribuição. Leia [operação](../../docs/13-operacao.md).

1. Reproduza os gates locais e confirme versões, lockfiles, diretórios e serviços necessários. Não copie o workflow Python deste kit para outra stack.
2. Defina eventos e matriz por versões efetivamente suportadas; evite executar código não confiável com segredos ou permissões de escrita desnecessárias.
3. Separe checks rápidos, integração e build conforme custo; mantenha resultado obrigatório inequívoco. Cache deve poder ser descartado sem alterar correção.
4. Fixe versões/origem das dependências e actions conforme política do projeto; planeje atualização e verificação de artefatos.
5. Valide sintaxe e comandos, registre o que depende de execução remota. Configure checks obrigatórios no provedor apenas quando autorizado e após existirem nomes estáveis.

Saída: pipeline revisável, gates reais, permissões e evidência. Arquivo YAML validado localmente não significa CI remota aprovada.
