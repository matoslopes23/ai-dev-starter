# Engenharia de software com IA

Kit de práticas, skills e automações locais para desenvolver aplicações do zero e evoluir sistemas existentes. Funciona como um playbook versionado, independente de linguagem, framework, IDE ou provedor de IA. A aplicação continua usando sua própria stack e seus próprios testes.

O kit cobre descoberta do sistema, requisitos, arquitetura, implementação, revisão, testes, segurança, dados, Git, CI/CD e operação. Os procedimentos são adaptáveis: o catálogo cobre um ciclo de desenvolvimento, sem prometer substituir especialização de domínio ou conter toda prática possível.

**Primeiro uso:** abra [COMECE_AQUI.md](COMECE_AQUI.md) e copie o [prompt inicial](prompts/inicial.md) no agente. A mesma entrada atende projetos novos, existentes e multi-repositório. Linguagem, paradigma e arquitetura são campos livres: [como adaptar](docs/19-neutralidade.md).

## Escolha sua entrada

| Situação | Comece aqui | Resultado inicial |
|---|---|---|
| Criar uma aplicação | [Projeto novo](docs/08-projeto-novo.md) | Escopo, decisões e primeira entrega vertical |
| Melhorar um projeto no GitHub | [Sistema existente](docs/09-sistema-existente.md) | Baseline, mapa do sistema e plano incremental |
| Entender vários repositórios | [Contexto multi-repositório](docs/10-multi-repositorio.md) | Inventário, contratos e jornadas entre serviços |
| Aplicar no AgendaLu | [Guia AgendaLu](docs/16-agendalu.md) | Roteiro executável sem presumir stack ou repositórios |
| Executar trabalho cotidiano | [Catálogo de skills](skills/README.md) | Procedimento escolhido pelo objetivo da tarefa |

## Comece pelo diagnóstico

Clone este kit e seus projetos em pastas separadas. Abra o kit no seu agente e use o prompt de [adoção](prompts/adotar-sistema.md), informando os caminhos ou URLs dos repositórios autorizados. O agente deve descobrir contexto, registrar lacunas e propor uma primeira fatia verificável antes de alterar o produto.

Para levar o playbook a um projeto local, Python 3.10+ e Git são os únicos requisitos da automação:

```sh
# Execute na raiz deste kit. O destino deve existir.
python3 scripts/adopt.py --target ../meu-projeto --name MeuProjeto --mode existing
# O primeiro comando somente mostra o plano. Para aplicar:
python3 scripts/adopt.py --target ../meu-projeto --name MeuProjeto --mode existing --apply
```

Isso cria `.ai-kit/` com o playbook e configurações iniciais, acrescenta um bloco ao `AGENTS.md` e ignora `.ai/`. Preserva instruções preexistentes, sem copiar demo, CI ou dependências. Não clona, instala pacotes, cria branches ou publica. Se `.ai-kit/` já existir, recusa substituir: [atualização e portabilidade](docs/17-portabilidade.md).

Para um projeto novo use `--mode new`; para uma pasta central de contexto de vários repositórios use `--mode multi-repo`. O comando não gera a aplicação. Após adoção, configure `.ai-kit/project.json` e o manifesto quando houver vários repos. Checks vazios significam **não configurado**, nunca aprovação.

Os [scripts de configuração](docs/20-configuracao.md) acompanham a instalação. Da raiz do produto:

```sh
python3 .ai-kit/scripts/doctor.py --target .
python3 .ai-kit/scripts/configure.py --target . --stack "Sua linguagem" --architecture "Seu estilo"
# Revise o plano; repita o configure com --apply para gravar.
```

Python é o runtime dessas automações, sem virar dependência do produto. Elas aceitam comandos de qualquer linguagem e não os executam automaticamente. O diagnóstico retorna `2` enquanto houver lacunas de configuração.

## Como o agente trabalha

1. Lê [AGENTS.md](AGENTS.md), [project.json](project.json) e o [roteador](ia-context/CONTEXT_ROUTER.md).
2. Confere branch, HEAD e alterações locais; identifica componentes e o comportamento existente.
3. Registra objetivo, aceite, limites e plano em `.ai/current-task.md` usando [o pacote de trabalho](templates/task.md).
4. Carrega somente a skill pertinente; implementa uma fatia e valida contratos e consumidores afetados.
5. Revisa o diff e entrega comandos, resultados, riscos e próxima ação. Commit, push, merge e deploy dependem do escopo autorizado.

Em sistemas grandes, analisar o todo significa cobrir repositórios, jornadas, contratos e riscos com evidências. Não significa carregar todos os arquivos em uma conversa. Consulte [contexto e tokens](docs/04-contexto-e-tokens.md).

## Práticas e escolhas

[Código e arquitetura](docs/02-arquitetura.md) orientam coesão, separação de responsabilidades e dependências em direção às regras de negócio. Monólito modular, serviços e outros estilos são opções justificadas por contexto. [Git](docs/11-git-e-colaboracao.md) inclui GitHub Flow, trunk-based e Gitflow completo; a escolha depende de entregas e versões mantidas.

[Qualidade](docs/12-qualidade.md), [segurança](docs/05-seguranca.md), [operação](docs/13-operacao.md) e [perfis de aplicação](docs/14-perfis.md) definem evidências e gates proporcionais ao risco. As [fontes primárias](docs/15-referencias.md) orientam o método; adotar este kit não certifica conformidade.

## Validar este kit

```sh
python3 scripts/verify.py
```

O gate valida estrutura, links locais, JSON, metadados das skills, sintaxe Python e testes das automações e da demo. O scanner de segredos é heurístico e limitado. O gate do kit **não valida a qualidade de uma aplicação consumidora**. A versão de referência está em `.python-version`; a matriz do CI cobre Python 3.10, 3.12 e 3.14. Consulte [a validação desta entrega](docs/18-validacao.md) para distinguir configuração e execução comprovada.

A [demo opcional](examples/taskboard/index.html) continua disponível com `python3 examples/taskboard/server.py` em `http://127.0.0.1:8000`: dados fictícios, estado apenas no navegador, sem autenticação. O [workshop](workshop/ROTEIRO.md) é um exercício, não a estrutura exigida para seus projetos.

Licença MIT. Não há dependência de API de IA ou serviço pago para ler e usar o kit.
