# Instalação local, uso central e atualização

## Dois modos de consumo

**Central:** mantenha este kit separado e indique seu caminho nos prompts. O mapa do sistema fica em uma pasta própria, com `system.json` preenchido a partir do [exemplo](../templates/system.example.json). É útil para diagnóstico antes de tocar nos repositórios.

**Instalado:** `scripts/adopt.py` copia um snapshot em `.ai-kit/`, cria configuração específica e acrescenta referências em `AGENTS.md` e `.gitignore` do destino. Cada repo pode operar sem o checkout central. Documentos do kit ficam relativos a `.ai-kit/`; código e estado continuam na raiz da aplicação. O snapshot inclui configuração, diagnóstico, inventário e update/restore em `scripts/`, além de adaptadores opcionais fora de `.ai-kit/`. Não contém demo, workshop, CI, instalador, harness de evals ou gate do kit; configure gates próprios do consumidor.

## Contrato do comando de adoção

Execute da raiz do kit, com Python 3.10+:

```sh
python3 scripts/adopt.py --target ../produto --name Produto --mode existing
python3 scripts/adopt.py --target ../produto --name Produto --mode existing --apply
```

O destino deve ser um diretório local existente. O primeiro comando valida e mostra os arquivos que seriam escritos; somente `--apply` grava. Modos: `new` (aplicação a iniciar), `existing` (aplicação existente), `multi-repo` (workspace). `--git-workflow` aceita `undecided`, `github-flow`, `trunk-based` ou `gitflow`; padrão `undecided`. Não altera branches nem configura o servidor Git.

O comando preserva os bytes anteriores de `AGENTS.md` e `.gitignore`, acrescentando apenas um bloco delimitado e entradas de ignore locais. Recusa instalação existente, marcador anterior inconsistente, colisões, nomes inválidos e symlinks nos destinos de escrita. Não faz merge automático de duas instalações. `.ai-kit/origin.json` registra versão do kit, commit de origem e se havia mudanças locais; um commit com dirty=true não identifica sozinho os bytes copiados. Revise o snapshot antes de versionar.

No formato 2 do manifesto, `managed` registra hashes dos arquivos relativos à raiz da aplicação, incluindo adaptadores; `sha256` mantém a visão relativa do payload para compatibilidade. Arquivos de configuração e instruções da raiz não são gerenciados pelo update. `--adapter` seleciona [integrações](21-integracoes.md) sem sobrescrever entradas existentes.

Uma adoção exige executar sem outro processo editando os mesmos arquivos. Em falha de gravação, o comando tenta restaurar os arquivos que escreveu; confira o estado do destino antes de repetir. Sem `--apply`, não cria diretórios ou arquivos no destino.

## Configuração após a cópia

Configure `.ai-kit/project.json` com stack, arquitetura, componentes, comandos e riscos reais usando [configure.py e doctor.py](20-configuracao.md), ou edite o JSON diretamente. Os campos de stack e estilo aceitam texto livre. `.ai-kit/system.json` começa com `repositories: []` e não descobre repos no GitHub. Preencha paths explícitos e dependências confirmadas. [O inventário](10-multi-repositorio.md) é somente leitura e só examina os paths informados.

Abra a aplicação e instrua o agente a ler o `AGENTS.md` da raiz. Se o agente não descobrir skills automaticamente, informe `.ai-kit/skills/<nome>/SKILL.md` no prompt. Isso não depende de instalar nada em sua pasta global de agentes.

## Atualizar sem perder decisões

Use [update com plano e recuperação](22-atualizacao.md). Ele compara hashes-base/local/nova origem, preserva configuração e personalizações quando a origem não mudou, e recusa conflitos sem force. Se o kit instalado ainda não contém update, execute `scripts/update.py` pelo checkout central revisado. Instalações 2.1 com hashes legados são reconhecidas; instalações sem base confiável exigem migração manual. Execute os gates da aplicação após a revisão.

Versione o snapshot e configurações sem segredos conforme a política do projeto. `.ai/` é estado local descartável. Não publique inventário privado, caminhos pessoais ou dados do sistema por acidente. O comando não modifica workflows, dependências, remotos ou proteções do repositório.
