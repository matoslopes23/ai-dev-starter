# Template de desenvolvimento com IA

Um método versionado para transformar pedidos em alterações pequenas, verificáveis e retomáveis. Não é um gerador universal nem garante economia de tokens. O núcleo é independente de linguagem, IDE, modelo e provedor. A demonstração Python é opcional.

## Comece em cinco minutos

Requisitos da demonstração: Python 3.10+ e navegador. Git é necessário apenas para versionamento. Sem pacotes externos, API de IA, Docker ou conta cloud.

```sh
python3 scripts/verify.py
python3 examples/taskboard/server.py
# Abra http://127.0.0.1:8000
```

Abra uma segunda janela de terminal para os testes; Ctrl+C encerra o servidor. O estado da demonstração existe apenas na memória do navegador e se perde ao recarregar. Não use dados reais.

## Use em qualquer projeto

1. Clone ou use “Use this template” se o proprietário ativar esse recurso no GitHub.
2. Leia `AGENTS.md` e `docs/01-adaptacao.md`.
3. Preencha `project.json`: objetivo, linguagem, componentes, comandos, branch base e riscos. Não invente comandos nem passe credenciais.
4. Troque a demo pelo seu produto. Preserve o método; não preserve camadas desnecessárias.
5. Escreva o primeiro pacote de trabalho com `templates/task.md` e use `prompts/iniciar.md`.
6. Execute os gates configurados, revise o diff e entregue `templates/handoff.md`.

Se clonar para criar outro produto, configure um remoto novo antes de publicar. Não envie alterações ao template por acidente. Ao remover `examples/`, atualize `scripts/verify.py`, workflow e testes de acordo com a stack escolhida.

## Mapa

- `AGENTS.md`: contrato curto para agentes e pessoas.
- `ia-context/CONTEXT_ROUTER.md`: o que ler para cada tarefa.
- `docs/`: adaptação, arquitetura, fluxo, tokens, segurança e publicação.
- `skills/`: procedimentos Markdown acionáveis manualmente, sem dependência de runtime.
- `templates/`: plano, ADR, revisão e continuidade.
- `examples/taskboard/`: aplicação pequena com domínio independente da interface.
- `workshop/`: roteiro ao vivo, aceite e solução de referência separada.
- `scripts/verify.py`: gate reproduzível da demo e integridade do template.

## O que se transfere para outra stack

Critérios de aceite, fronteiras, comandos explícitos, revisão por risco, leitura seletiva e evidência continuam. Sintaxe, framework, estrutura física, testes e CI devem mudar. Consulte `docs/02-arquitetura.md` para API, mobile, dados e monorepo.

## Limites

O scanner incluído é heurístico, não prova ausência de segredos. Não há autenticação, banco ou produção na demo. Nenhum Markdown sozinho impõe segurança a um agente. Um teste verde não substitui revisão humana nem valida todos os ambientes.

Licença: MIT, código e documentação originais deste template. Dependências futuras terão suas próprias licenças.
# ai-dev-starter
