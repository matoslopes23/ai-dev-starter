# Adotar sem substituir o projeto

Escolha [projeto novo](08-projeto-novo.md), [sistema existente](09-sistema-existente.md) ou [multi-repositório](10-multi-repositorio.md). Para instalação local, consulte [portabilidade](17-portabilidade.md). Não clone o kit por cima de uma aplicação nem reutilize seu remoto como destino do produto.

## Configure o contrato da aplicação

Em instalação local, edite `.ai-kit/project.json`. Ao desenvolver o kit, use o `project.json` da raiz. Registre:

- Identidade, propósito e tipo (`application` ou `workspace`).
- Stack e runtimes comprovados em manifests, lockfiles, imagens ou CI.
- Estilo arquitetural, fronteiras e restrições em `architecture`, com nomes livres; preserve o desenho existente até decisão justificada.
- Componentes e responsabilidades, com caminhos relativos à raiz da aplicação.
- Branch base e política Git **observadas**, ou `undecided` enquanto não confirmadas.
- Checks com comandos reais, diretório de execução e requisitos sanitizados. O objeto `checks` contém nomes e comandos; condições e diretórios ficam no diagnóstico/plano de testes.
- Restrições de dados, produção, segurança, escala e compatibilidade.

Configuração gerada começa sem stack nem gates inventados. Não use os testes da demo para aprovar um produto. Se o projeto não tem um gate, registre a falta e introduza o menor check útil na primeira mudança autorizada.

Para planejar/gravar esses campos e conferir lacunas sem executar comandos do produto, use [os scripts de configuração](20-configuracao.md). No primeiro contato, use [o prompt inicial](../prompts/inicial.md).

## Onde guardar informação

| Informação | Local sugerido | Versionar? |
|---|---|---|
| Práticas compartilhadas | `.ai-kit/` ou este repositório central | Sim, após revisão |
| Arquitetura comprovada e ADRs | `docs/engineering/` na aplicação | Sim, sem dados privados |
| Tarefa ativa e evidência local | `.ai/` na aplicação | Não |
| Mapa de vários repositórios | Workspace de engenharia privado adequado ao sistema | Conforme confidencialidade |
| Segredos / dados reais | Gerenciador autorizado de segredos/dados | Nunca no kit |

## Compatibilidade com agentes

Markdown é portável; descoberta automática de skills e de `AGENTS.md` depende da ferramenta. O caminho manual é sempre válido: indique o arquivo `SKILL.md` no prompt. Crie adaptadores nativos apenas após conferir a documentação da ferramenta utilizada, mantendo uma fonte de verdade e sem sobrescrever instruções existentes. O kit não exige instalar skills globalmente.

Atualizações do kit entram como alterações revisáveis: preserve decisões do projeto, registre a origem e valide links e gates. Um manifesto atualizado não significa adoção concluída.
