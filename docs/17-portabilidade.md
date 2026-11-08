# Instalação local, uso central e atualização

## Dois modos de consumo

**Central:** mantenha este kit separado e indique seu caminho nos prompts. O mapa do sistema fica em uma pasta própria, com `system.json` preenchido a partir do [exemplo](../templates/system.example.json). É útil para diagnóstico antes de tocar nos repositórios.

**Instalado:** `scripts/adopt.py` copia um snapshot em `.ai-kit/`, cria configuração específica e acrescenta referências em `AGENTS.md` e `.gitignore` do destino. Cada repo pode operar sem o checkout central. Documentos do kit ficam relativos a `.ai-kit/`; código e estado continuam na raiz da aplicação. O snapshot inclui entrada inicial, configuração, diagnóstico e inventário em `scripts/`. Não contém demo, workshop, workflow, instalador ou gate do kit; configure gates próprios do consumidor.

## Contrato do comando de adoção

Execute da raiz do kit, com Python 3.10+:

```sh
python3 scripts/adopt.py --target ../produto --name Produto --mode existing
python3 scripts/adopt.py --target ../produto --name Produto --mode existing --apply
```

O destino deve ser um diretório local existente. O primeiro comando valida e mostra os arquivos que seriam escritos; somente `--apply` grava. Modos: `new` (aplicação a iniciar), `existing` (aplicação existente), `multi-repo` (workspace). `--git-workflow` aceita `undecided`, `github-flow`, `trunk-based` ou `gitflow`; padrão `undecided`. Não altera branches nem configura o servidor Git.

O comando preserva os bytes anteriores de `AGENTS.md` e `.gitignore`, acrescentando apenas um bloco delimitado e entradas de ignore locais. Recusa instalação existente, marcador anterior inconsistente, colisões, nomes inválidos e symlinks nos destinos de escrita. Não faz merge automático de duas instalações. `.ai-kit/origin.json` registra versão do kit, commit de origem e se havia mudanças locais; um commit com dirty=true não identifica sozinho os bytes copiados. Revise o snapshot antes de versionar.

Uma adoção exige executar sem outro processo editando os mesmos arquivos. Em falha de gravação, o comando tenta restaurar os arquivos que escreveu; confira o estado do destino antes de repetir. Sem `--apply`, não cria diretórios ou arquivos no destino.

## Configuração após a cópia

Configure `.ai-kit/project.json` com stack, arquitetura, componentes, comandos e riscos reais usando [configure.py e doctor.py](20-configuracao.md), ou edite o JSON diretamente. Os campos de stack e estilo aceitam texto livre. `.ai-kit/system.json` começa com `repositories: []` e não descobre repos no GitHub. Preencha paths explícitos e dependências confirmadas. [O inventário](10-multi-repositorio.md) é somente leitura e só examina os paths informados.

Abra a aplicação e instrua o agente a ler o `AGENTS.md` da raiz. Se o agente não descobrir skills automaticamente, informe `.ai-kit/skills/<nome>/SKILL.md` no prompt. Isso não depende de instalar nada em sua pasta global de agentes.

## Atualizar sem perder decisões

Não rode uma cópia forçada por cima do kit adotado. Leia `origin.json`, compare a versão instalada com o kit desejado e gere a nova instalação em um diretório temporário vazio. Revise as diferenças de docs/skills/templates/scripts, preserve `project.json`, `system.json` e as decisões locais, e aplique o diff em uma tarefa dedicada. Registre nova origem após a revisão. Execute links e gates da aplicação e confira instruções da raiz. Instalações 2.0 não tinham scripts; inclua os utilitários e campos novos ao migrar para 2.1, mantendo as configurações reais.

Versione o snapshot e configurações sem segredos conforme a política do projeto. `.ai/` é estado local descartável. Não publique inventário privado, caminhos pessoais ou dados do sistema por acidente. O comando não modifica workflows, dependências, remotos ou proteções do repositório.
