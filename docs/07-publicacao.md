# Publicar o kit ou uma aplicação

Publicar este kit, adotar em um produto e implantar uma aplicação são operações diferentes. Confirme qual destino está no pedido. Este documento não prova que o kit foi publicado nem que um consumidor está pronto para produção.

## Revisão local

1. Confira branch, HEAD, status e remoto sem expor credenciais. Se houver histórico herdado, confirme sua propriedade e destino; não reescreva nem apague histórico automaticamente.
2. Liste arquivos novos e alterações, confirme que pertencem à tarefa e revise cada um. Verifique licença, documentação, exemplos e conteúdo privado; inventários de sistemas podem exigir repositório privado.
3. Execute os gates do projeto e registre runtime e estado final. No kit: `python3 scripts/verify.py`; nos consumidores, use seus próprios comandos.
4. Complemente o scanner heurístico com revisão e ferramenta especializada quando pertinente, incluindo histórico, binários e metadados. Não abra segredos reais para confirmar um regex.
5. Prepare descrição e riscos. Se o checkout contém trabalho alheio, selecione explicitamente os arquivos do escopo; não use stage indiscriminado.

## Publicação autorizada

Confirme conta, URL exata, visibilidade e branch base antes de criar repositório ou enviar. Respeite autorização já presente no pedido; se faltar, entregue primeiro o diff e o plano concretos. Não force push, altere permissões ou contorne proteção para fazer um envio passar.

Commit, push, abertura de PR, merge, release e deploy têm efeitos diferentes. Execute somente o escopo autorizado e verifique o resultado remoto pelo commit/artefato correspondente. Autenticação existente não amplia o escopo; nunca copie tokens para arquivos ou prompts.

Ativar “Template repository” no GitHub é opcional e separado da publicação. Para produto novo, use remoto próprio; para produto existente, preserve seu remoto e sua política Git. Não envie código do produto ao repositório central do kit.

Para deploy, consulte a skill [preparar-release](../skills/preparar-release/SKILL.md), compatibilidade de dados, rollout e recuperação. Adoção do playbook não substitui validação operacional.
