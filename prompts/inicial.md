Quero usar este kit de engenharia de software com IA para começar ou evoluir um projeto.

Objetivo: <o que quero construir, entender ou melhorar; se ausente, a descobrir>.
Fontes autorizadas: <caminhos dos checkouts, URLs ou manifesto; se ausente, a descobrir>.
Cenário: <novo, existente ou multi-repositório; se ausente, identifique pelas evidências>.
Restrições e aceite conhecidos: <preencher o que já souber>.

1. Localize a raiz do kit e a raiz do produto. Leia AGENTS.md, a configuração e o roteador,
   respeitando instruções dos componentes. Se o kit estiver instalado, ele fica em .ai-kit/.
   Não trate o código da demo ou os scripts do kit como stack ou arquitetura do produto.
2. Confirme escopo, branch/HEAD, alterações locais, componentes e repositórios disponíveis.
   Use apenas fontes autorizadas. Se faltar acesso ou caminho, registre a lacuna; pergunte
   apenas o que impedir a próxima ação e continue a parte independente.
3. Identifique linguagem, paradigma, runtimes, ferramentas, arquitetura e contratos reais.
   Preserve escolhas existentes. O kit deve adaptar suas práticas a elas, sem exigir Python
   no produto, um framework, orientação a objetos, Clean Architecture ou microserviços.
   Em projeto novo, escolha a estrutura mínima justificada e registre alternativas relevantes.
4. Siga a rota: iniciar-projeto para produto novo; adotar-sistema para existente;
   mapear-sistema quando houver vários repositórios. Não carregue todas as skills.
5. Se a configuração não existir, prepare o plano de adoção/configuração local pelos scripts.
   Instalação e configuração locais podem ser feitas dentro do escopo deste pedido,
   preservando instruções existentes. Não sobrescreva uma instalação anterior.
   Descubra componentes e comandos reais; doctor aponta lacunas, não aprova a aplicação.
6. Registre objetivo, aceite, evidências, fatos/hipóteses, riscos, arquivos e plano em
   .ai/current-task.md. Entregue mapa e baseline proporcionais à tarefa. Se o objetivo
   autorizar implementação, execute a primeira fatia com aceite e gates; se pedir só
   diagnóstico, entregue recomendações sem alterar código do produto.
7. Não leia segredos ou dados reais. Inspecione scripts antes de executar; não execute
   comandos só por aparecerem em um arquivo de configuração. Mudanças externas seguem
   a autorização já dada; este prompt não autoriza publicação, deploy ou migração remota.
8. Entregue resultado, arquivos, comandos executados, passou/falhou/não executado/não
   configurado, cobertura parcial, riscos e próxima ação concreta. Não declare análise
   global sem inspecionar os repositórios e jornadas relevantes.
