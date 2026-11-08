# Validação da entrega

Registro histórico da demo original. A evolução do kit tem [validação própria](../docs/18-validacao.md); não reutilize os resultados abaixo como evidência do código atual.

Data: 2026-11-08. Ambiente: Linux, Python 3.12.14, Node 24.22.1 para verificação complementar de sintaxe.

- PASSOU: 8 testes de domínio e HTTP com `python3 -B scripts/verify.py`.
- PASSOU: compilação sintática Python, estrutura/JSON e scanner heurístico de segredos.
- PASSOU: `git diff --cached --check` e `git apply --check workshop/reference/filter.patch`.
- PASSOU: sintaxe do JavaScript extraído da página com `node --check`.
- PASSOU: patch aplicado em cópia isolada, gates novamente verdes; lógica de filtro, vazio e preservação de estado avaliada com DOM simulado em Node.
- PASSOU: revisão de marcadores de projetos de origem, nomes privados e caminhos locais; nenhum encontrado no pacote.
- NÃO EXECUTADO: inspeção visual e interação em navegador real. Chromium headless não pôde iniciar neste ambiente por restrição de socket. DOM simulado não comprova layout, teclado ou acessibilidade.
- NÃO EXECUTADO: CI remota, pois o repositório ainda não foi publicado.

Antes do evento, execute workshop/ACEITE.md em navegador real. As verificações não constituem auditoria de segurança nem garantia de ausência de dados sensíveis.
