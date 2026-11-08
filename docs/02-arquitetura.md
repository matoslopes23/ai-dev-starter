# Código limpo, arquitetura e crescimento

Arquitetura deve proteger regras e permitir mudanças com custo conhecido. Escolha fronteiras a partir de domínio, consumidores, dados, requisitos não funcionais e operação. Não escolha microserviços, CQRS, eventos ou camadas apenas porque aparecem neste kit.

## Direção das dependências

Regras de domínio e casos de uso não devem precisar de detalhes de HTTP, UI, banco ou provedor externo. Adaptadores traduzem contratos e efeitos. Introduza portas/interfaces quando isolarem uma dependência real, sustentarem testes úteis ou permitirem alternativas necessárias. Uma função pura pode ser suficiente para uma regra pequena.

Em um sistema existente, identifique primeiro o fluxo atual. Extraia fronteiras em passos com comportamento preservado; não converta o sistema inteiro em uma entrega. DTO de transporte, modelo de persistência e entidade podem ser separados quando suas regras divergem; duplicá-los sem motivo também tem custo.

## Decisões que afetam o código

- Organize por capacidade de negócio quando ajudar a manter mudanças relacionadas próximas. Módulos expõem contratos pequenos; detalhes internos não viram API por acidente.
- Nomeie conceitos do domínio; funções devem ter intenção clara, dependências explícitas e efeitos previsíveis. Reduza aninhamento, estado mutável compartilhado e booleanos com significados ambíguos.
- Aplique responsabilidade única e inversão de dependência a pontos com motivos reais de mudança. SOLID, DRY, KISS e YAGNI são critérios de decisão, não metas de contagem de classes. Extraia duplicação de conhecimento, não toda semelhança textual.
- Modele invariantes no domínio, valide entrada nas fronteiras e preserve restrições no banco quando aplicável. Evite usar exceções ou valores nulos como protocolo implícito de sucesso.
- Trate falhas esperadas com contratos claros; preserve causa para diagnóstico sanitizado. Defina timeout, cancelamento e comportamento de falha de integrações. Retry exige idempotência e limite.
- Tipagem e análise estática devem acompanhar a stack. Não simule garantias de tipo ignorando erros indiscriminadamente.
- Dependências novas precisam de benefício, manutenção, licença, custo operacional e estratégia de atualização considerados.

## Escolha de topologia

| Opção | Considere quando | Custo a validar |
|---|---|---|
| Aplicação simples | Poucas regras e um deploy | Acoplamento e limite de crescimento |
| Monólito modular | Domínios distintos com operação compartilhada | Fronteiras e acesso indevido entre módulos |
| Serviços separados | Necessidade concreta de autonomia, isolamento ou escala | Contratos, consistência, rede, observabilidade e operação |
| Eventos / processamento assíncrono | Trabalho desacoplado ou absorção de picos | Entrega duplicada, ordenação, replay e consistência eventual |

Uma base compartilhada de dados pode impedir autonomia mesmo com vários repositórios. Registre dono de cada escrita e restrição de consistência. Evite transação distribuída introduzida por acidente.

## Escalabilidade verificável

Declare volume, concorrência, latência, disponibilidade e limites de custo esperados. Meça antes de distribuir. Verifique consultas e índices, contenção, pools, filas, particionamento, cardinalidade, payloads e backpressure conforme o gargalo. Cache exige validade, invalidação, isolamento e comportamento de indisponibilidade. Escalar réplicas não resolve um banco saturado nem uma operação não idempotente.

Use [ADR](../templates/adr.md) para decisões com alternativas e custo de reversão relevantes. Inclua resultado de medição ou hipótese, consequência operacional e condição de revisão.

A demo mantém uma regra pura, um adaptador HTTP e estado no navegador. É uma ilustração mínima; não estabelece uma estrutura física universal.
