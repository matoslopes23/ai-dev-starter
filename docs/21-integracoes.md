# Integrações nativas opcionais

A instalação continua funcionando como playbook manual. Para expor skills nos diretórios de descoberta das ferramentas, selecione adaptadores:

```sh
# Do checkout central, destino já existente:
python3 scripts/adopt.py --target ../produto --name Produto --adapter codex --adapter claude
# Revise o plano e repita com --apply para gravar.
```

| Adaptador | Diretório de projeto usado | Fonte oficial consultada em 2026-11-08 |
|---|---|---|
| codex | `.agents/skills/ai-kit-*/SKILL.md` | [OpenAI: skills locais](https://learn.chatgpt.com/docs/build-skills) |
| copilot | `.agents/skills/ai-kit-*/SKILL.md` | [GitHub: diretórios aceitos](https://docs.github.com/en/copilot/concepts/customizations/agent-skills) |
| cursor | `.agents/skills/ai-kit-*/SKILL.md` | [Cursor: Agent Skills](https://cursor.com/docs/skills) |
| claude | `.claude/skills/ai-kit-*/SKILL.md` | [Claude Code: skills de projeto](https://code.claude.com/docs/en/skills) |

Codex, Copilot e Cursor compartilham um diretório suportado; selecionar os três gera um único conjunto de entradas. O adaptador Claude usa seu diretório próprio. Ferramentas que também leem o diretório de outra podem mostrar entradas sobrepostas; escolha somente os adaptadores necessários. A versão, as políticas e a modalidade local/cloud da ferramenta podem limitar a descoberta.

Cada entrada contém nome, descrição e link relativo para `.ai-kit/skills/<nome>/SKILL.md`. A implementação do procedimento permanece em uma fonte. Os adaptadores não alteram configurações globais, permissões, hooks, MCP ou arquivos de instruções de terceiros. Um arquivo no destino de uma entrada causa recusa da adoção, mesmo que pareça equivalente: use uma atualização revisada.

Para adicionar um adaptador a uma instalação existente:

```sh
# Da raiz do consumidor; origem local revisada:
python3 .ai-kit/scripts/update.py --target . --source ../kit --adapter codex
# --adapter define a lista completa desejada; repita para manter outros adaptadores.
```

Sem `--adapter`, update mantém a seleção registrada na origem. Remover um adaptador da seleção remove somente suas entradas gerenciadas intactas. Modificações locais em entradas que precisariam mudar/remover geram conflitos.

## Verificar a integração

Os testes determinísticos conferem nomes, descrições, links, preservação e colisões, mas não comprovam que uma ferramenta acionou uma skill. Abra uma sessão nova no produto e confira se `ai-kit-corrigir-bug` aparece na lista de skills da sua ferramenta. Faça uma avaliação conforme [evals](23-avaliacoes.md) para verificar a ativação e o comportamento.

Os adaptadores locais não garantem instalação em serviços cloud que usam outra fonte de skills. Use a documentação oficial da ferramenta e registre o ambiente efetivamente avaliado. Nunca reduza permissões ou contorne aprovações para fazer uma avaliação passar.
