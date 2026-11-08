# Adotar em um sistema existente

Use [adotar-sistema](../skills/adotar-sistema/SKILL.md) e [mapear-sistema](../skills/mapear-sistema/SKILL.md). Não reestruture a aplicação antes de entender seu funcionamento. O resultado inicial é um diagnóstico com evidências e um plano, seguido de melhorias pequenas autorizadas.

## 1. Inventário e limites

Liste os repositórios autorizados e seus papéis: aplicações, APIs, jobs, bibliotecas, infra e integrações. Registre os ausentes e quem pode confirmar. URLs não significam acesso nem checkout local; se o projeto está apenas no GitHub, use leitura conectada autorizada ou clone para uma pasta própria após confirmar destino. Nunca imprima URLs com credenciais embutidas.

Confirme instruções locais, branch, HEAD e alterações de cada checkout. Não troque branches nem faça stash sobre trabalho alheio. Use [system.example.json](../templates/system.example.json) para o manifesto, e [system-map](../templates/system-map.md) para evidências.

## 2. Baseline reproduzível

Descubra runtimes e comandos em manifests, lockfiles, CI e README, sem ler segredos. Inspecione scripts antes de executá-los. Registre quais checks já passam, falham ou dependem de recursos indisponíveis. Não corrija toda falha histórica incidentalmente; registre dívida separada e escopo do trabalho atual.

## 3. Percorra jornadas completas

Escolha as jornadas centrais confirmadas pelo produto. Trace entrada → autenticação/autorização → caso de uso → dados → integrações/eventos → retorno. Para cada passo, aponte repositório, commit e símbolo. Inclua consumidores móveis, jobs e infra quando existirem. APIs não revelam sozinhas toda regra de negócio.

Registre entidades, invariantes, dono de escrita, contratos, dependências, modos de falha e ambiente de execução. Documentação desatualizada é hipótese até confrontar com código. Liste áreas não inspecionadas e motivos.

## 4. Diagnóstico e plano incremental

Use [diagnóstico](../templates/diagnostic.md) e [plano de adoção](../templates/adoption-plan.md). Separe defeito comprovado, risco, dívida técnica e preferência. Classifique impacto, probabilidade, evidência, custo e dependências. Evite uma pontuação de maturidade sem critério observável.

Priorize recuperar build/testes e falhas críticas, depois reduzir risco nas áreas que serão alteradas. Introduza testes de caracterização antes de refatorações frágeis. Evolua arquitetura por fronteiras reais; um rewrite precisa de justificativa, custo, coexistência e migração.

## 5. Primeira melhoria

Escolha uma mudança pequena com ganho claro e verificação antes/depois: uma regressão, um contrato sem proteção, um check ausente ou uma dependência insegura confirmada. Registre aceite e, quando a implementação estiver autorizada, execute a skill adequada. Em pedido apenas de diagnóstico, entregue essa melhoria como recomendação. Mantenha baseline histórico separado do resultado da mudança.

Não declare “sistema todo analisado” enquanto faltarem repositórios, jornadas ou componentes relevantes. Informe exatamente o que foi coberto e o que depende de acesso ou confirmação.
