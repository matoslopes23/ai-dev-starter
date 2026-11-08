# Qualidade e estratégia de testes

O teste deve proteger uma regra, risco ou contrato observável. Se um teste falha apenas porque uma função privada foi renomeada, reavalie seu acoplamento. Nem toda mudança reversível precisa de um teste novo; valide na fronteira onde uma regressão importa.

## Escolha a fronteira

| Tipo | Protege | Atenção |
|---|---|---|
| Unitário | Invariantes e decisões puras | Limites, tabelas de casos e mensagens/erros relevantes |
| Integração | Banco, adaptador, fila, filesystem | Semântica real, concorrência e recursos isolados |
| Contrato | Produtor/consumidor e schemas | Compatibilidade entre versões coexistentes |
| E2E | Jornadas críticas | Poucos fluxos estáveis, estado controlado e diagnóstico |
| Acessibilidade/visual | Uso e apresentação | Ferramentas automáticas mais teclado e inspeção humana |
| Carga/resiliência | Limites e modos de falha | Ambiente isolado, metas e orçamento explícitos |

Mocks são úteis em fronteiras controladas; não substituem a verificação de protocolos, SQL ou comportamento do serviço real. Para legado sem testes, primeiro caracterize o comportamento importante, inclusive decisões controversas que o produto ainda depende.

## Gates da stack

Descubra instalação reprodutível, formatador, lint, tipos, teste, build e análise de dependências a partir do projeto. Inclua análise de segurança conforme risco e ferramenta disponível. Use versões e lockfiles controlados. Não execute package manager de outra stack nem substitua CI existente para uniformizar o kit.

Cobertura ajuda a encontrar lacunas; uma porcentagem isolada não prova qualidade. Defina metas pela criticidade e evolução. Flaky tests precisam de responsável e correção; retry não transforma instabilidade em confiança. Snapshots amplos e testes que apenas repetem a implementação costumam esconder intenção.

## Evidência

Use [test-plan](../templates/test-plan.md): requisito/risco → cenário → fronteira → comando/ambiente → resultado. Para bug, quando viável demonstre o teste falhando antes e passando depois. Registre falha preexistente separadamente. Após edição relevante, rode os checks afetados novamente; amplie apenas quando o risco ou uma falha justificar.

Contratos críticos pedem casos negativos: autorização, concorrência, duplicação, falha de rede, cancelamento, timeout, dados inválidos e migração parcial. Se um gate obrigatório não puder rodar, explique o bloqueio e mantenha a limitação visível no handoff e PR.
