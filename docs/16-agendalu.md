# Aplicar no AgendaLu

Este roteiro não presume stack, regras de negócio, serviços, URLs ou acesso ao AgendaLu. Esses fatos precisam vir dos repositórios e do responsável pelo produto. Nenhum repositório do AgendaLu foi analisado para escrever este guia.

## Preparar o contexto central

1. Clone este kit para uma pasta própria. Liste os repositórios que realmente compõem o AgendaLu, incluindo infra, bibliotecas, aplicativos e jobs quando existirem.
2. Abra checkouts autorizados sem misturar históricos; confira acesso e instruções de cada um. Registre URLs sem credenciais e os caminhos locais. Não importe bancos, `.env` ou dados de clientes.
3. Crie uma pasta de contexto e adote o kit nela:

Execute os comandos abaixo do checkout central original deste kit, não de uma instalação `.ai-kit/`:

```sh
mkdir -p ../agendalu-contexto
python3 scripts/adopt.py --target ../agendalu-contexto --name AgendaLu --mode multi-repo
python3 scripts/adopt.py --target ../agendalu-contexto --name AgendaLu --mode multi-repo --apply
```

4. Preencha `../agendalu-contexto/.ai-kit/system.json` com os repositórios confirmados. Paths são relativos a esse manifesto; para um checkout em `trabalho/repos/api`, partindo de `trabalho/agendalu-contexto/.ai-kit/`, o path seria `../../repos/api`. É apenas um exemplo de caminho, não um serviço presumido.
5. Execute `python3 scripts/inventory.py --manifest ../agendalu-contexto/.ai-kit/system.json`. Inventário vazio ou inacessível é lacuna, não análise concluída.

Da raiz de `agendalu-contexto`, instalações 2.1 também permitem `python3 .ai-kit/scripts/inventory.py --manifest .ai-kit/system.json`. Use [o prompt inicial único](../prompts/inicial.md) se quiser começar sem conhecer ainda o cenário; [configure.py e doctor.py](20-configuracao.md) registram linguagens, arquitetura e comandos reais sem executá-los.

## Primeiro pedido ao agente

Abra a pasta central e use este texto, preenchendo as fontes reais:

```text
Leia AGENTS.md e siga a rota de adoção em .ai-kit/ia-context/CONTEXT_ROUTER.md.
Quero aplicar o kit ao AgendaLu. Os repositórios autorizados estão em
.ai-kit/system.json. Analise o contexto do sistema por jornadas, repositórios,
contratos e dados. Confirme runtimes, branches, HEADs e alterações existentes.
Não leia segredos nem dados reais. Nesta etapa, faça diagnóstico e documentação;
não altere o código do produto nem publique nada.
Entregue mapa do sistema, baseline de checks, riscos priorizados, lacunas de
cobertura e um plano incremental com a primeira melhoria verificável.
Use evidências repo@commit:caminho:símbolo e marque fatos versus hipóteses.
```

Registre o resultado com os templates de mapa, diagnóstico e adoção em `docs/engineering/` da pasta central, observando a confidencialidade. Defina quais jornadas são críticas com quem conhece o produto; o agente não deve inventá-las pelo nome do sistema.

## Levar as práticas aos repositórios

Após o diagnóstico, use `scripts/adopt.py --mode existing` em cada checkout que precisa operar independentemente, sempre inspecionando o plano antes de `--apply`. Preserve instruções locais. Configure stack e gates específicos de cada repo; centralize apenas as decisões e contratos compartilhados. Registre uma versão de kit por consumidor para atualizar de modo controlado.

Escolha a política Git pelo modo atual de entrega do AgendaLu. Se Gitflow fizer sentido, documente bases de feature/release/hotfix, retorno das correções e gates de cada branch. Não crie `develop` apenas para “adotar boas práticas”.

O próximo pedido pode autorizar uma primeira melhoria do plano com aceite e repositório definidos. Mudanças entre repos usam o template de alteração coordenada e verificam consumidores antes de remover contratos antigos.
