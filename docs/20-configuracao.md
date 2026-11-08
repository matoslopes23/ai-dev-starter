# Scripts de configuração e diagnóstico

Python 3.10+ e biblioteca padrão executam as automações. Use `python` no lugar de `python3` se esse for o comando do seu ambiente, após conferir a versão. Caminhos com espaços devem ser colocados entre aspas no shell usado. Os scripts não dependem de Bash e não instalam ferramentas da aplicação.

## Instalação

No checkout central, `scripts/adopt.py --target <pasta> --name <nome> --mode new|existing|multi-repo` mostra um plano. `--apply` grava `.ai-kit/`, complementa `AGENTS.md` e ignora `.ai/`, preservando o conteúdo anterior. O destino deve existir. Veja [portabilidade](17-portabilidade.md).

A instalação inclui `configure.py`, `doctor.py`, `inventory.py` e seu módulo auxiliar. Os exemplos a seguir são executados **da raiz do consumidor instalado**. Pelo checkout central, use `scripts/<comando>.py --target <pasta-do-consumidor>`.

## Configuração por flags

```sh
python3 .ai-kit/scripts/configure.py --target . --stack "Linguagem e versão confirmadas" --architecture "Estilo observado ou decidido"
```

Sem `--apply`, o script informa os campos que mudariam sem escrever. `--stack` pode ser repetido, substituindo a lista de linguagens/runtimes. `--architecture` define somente o nome do estilo, preservando fronteiras e restrições. Não há catálogo fechado de estilos.

`--check 'nome=comando'` adiciona ou atualiza um check; não o executa. `--base-branch` e `--git-workflow` registram a política sem criar branches nem alterar o provedor. Exemplos de comandos, a conferir no projeto antes de configurar:

| Projeto | Exemplo de configuração de check |
|---|---|
| Go | `--check 'test=go test ./...'` |
| Rust | `--check 'test=cargo test'` |
| Java/Maven | `--check 'test=./mvnw test'` se o wrapper existir |
| C#/.NET | `--check 'test=dotnet test'` |
| Elixir | `--check 'test=mix test'` |
| Outra linguagem | `--check 'test=seu-comando-real'` |

Use aspas compatíveis com seu shell, e adapte os comandos à plataforma. Estes exemplos não são executados pelo kit nem constituem uma lista de linguagens suportadas.

## Configuração por JSON

Para propósito, componentes, restrições e comandos completos, prepare um patch a partir de [project-config.example.json](../templates/project-config.example.json). Substitua os textos de exemplo pelos dados confirmados, removendo os campos que ainda não quer alterar. Guarde o arquivo de entrada fora de `.ai-kit/project.json`; não inclua segredos.

```sh
python3 .ai-kit/scripts/configure.py --target . --config minha-configuracao.json
python3 .ai-kit/scripts/configure.py --target . --config minha-configuracao.json --apply
```

O patch aceita `name`, `purpose`, `stack`, `architecture`, `profiles`, `base_branch`, `git_workflow`, `components`, `checks`, `production` e `risks`. Campos do patch **substituem integralmente** os campos correspondentes: `checks: {}` limpa a lista e volta a indicar não configurado. Flags, quando fornecidas, complementam o patch: checks são adicionados/atualizados, arquitetura altera somente `style` e `--stack` substitui a lista.

Campos não mencionados e extensões já existentes são preservados. Campos desconhecidos no patch são recusados; para metadados específicos da equipe, edite o JSON diretamente mantendo o contrato comum. A arquitetura aceita extensões no objeto `architecture`. Componentes usam paths relativos à raiz do produto, sem sair dela. Workspace multi-repo usa `system.json` para checkouts externos.

A gravação de `project.json` é atômica e preserva permissões. JSON inválido, symlinks e configuração inconsistente são recusados. Sem uso concorrente: se o arquivo mudar durante a preparação, o script recusa a troca. O comando não modifica código, dependências, CI, branches ou arquitetura de fato.

## Diagnóstico

```sh
python3 .ai-kit/scripts/doctor.py --target .
```

Confere runtime da automação, disponibilidade de Git, entrada do agente, declaração de stack/arquitetura/política, componentes e checks. Em workspace, confere se há repositórios declarados. Não lê código, descobre stack, inspeciona segredos, chama rede ou executa comandos do produto. Não verifica se o comando configurado existe ou passa.

Exit codes: `0` significa configuração suficiente para iniciar o diagnóstico do projeto; `2` significa lacunas; `1` significa erro ou configuração inválida. Um projeto recém-adotado normalmente retorna `2`. “Ready for diagnosis” não significa pronto para produção nem aprovação de gates.

Para verificar disponibilidade dos repositórios de um workspace, execute `python3 .ai-kit/scripts/inventory.py --manifest .ai-kit/system.json`. Depois siga [o prompt inicial](../prompts/inicial.md), inspecione scripts e execute os gates reais dentro do escopo autorizado.
