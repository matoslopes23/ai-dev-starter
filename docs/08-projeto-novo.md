# Começar uma aplicação do zero

Use [iniciar-projeto](../skills/iniciar-projeto/SKILL.md) e o prompt [projeto novo](../prompts/projeto-novo.md). Se quiser separar o produto do kit, crie uma pasta para o produto e execute `scripts/adopt.py --mode new` conforme [portabilidade](17-portabilidade.md). Não herde a demo como arquitetura obrigatória.

## Descoberta mínima

Registre usuário, problema, jornada prioritária, restrições e o que fica fora. Torne explícitos dados sensíveis, integrações, canais (web/mobile/API/etc.), distribuição, disponibilidade, desempenho e orçamento. Diferencie requisito confirmado de hipótese; não transforme uma preferência de framework em requisito de negócio.

Escolha uma stack compatível com a equipe, ecossistema, suporte e operação. Consulte documentação oficial para comandos e versões. Registre runtimes, instalação e lockfiles. Defina estrutura mínima; uma decisão com custo relevante vai para [ADR](../templates/adr.md).

## Primeira entrega vertical

Escolha uma jornada que atravesse as fronteiras reais: entrada, caso de uso, dados/integração quando necessários e retorno observável. Especifique sucesso, falha, autorização e aceite em [feature](../templates/feature.md). Evite meses de infraestrutura sem comportamento verificável.

Antes de ampliar o produto, obtenha um ambiente reproduzível com dados sintéticos, README de execução, política Git escolhida e gates de lint/tipos/teste/build compatíveis com a stack. A dispensa de um gate precisa de motivo, não de um comando fictício.

Defina uma forma de observar falhas e uma estratégia de release adequada. Persistência exige migrações; integrações exigem timeout e contrato; autenticação exige autorização; UI exige fluxo de erro e acessibilidade. Introduza cada capacidade junto da primeira jornada que a necessita.

## Saída esperada

`project.json` configurado, primeira especificação, arquitetura inicial com decisões justificadas, comandos reproduzíveis, plano da primeira fatia e riscos abertos com próximo responsável. O agente pode implementar a primeira fatia quando isso estiver no pedido; diagnóstico não é autorização para publicar.
