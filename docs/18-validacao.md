# Validação e proveniência

Data: 2026-11-08. Esta página distingue o histórico publicado da verificação local da evolução 3.0. Alterações de conteúdo após uma verificação exigem repetir os checks afetados.

## Base publicada

O commit [d1c3ee0](https://github.com/matoslopes23/ai-dev-starter/commit/d1c3ee0aac1e5fbc50af34a0c591a5d9c2a90b6f) publicou o kit 2.1. A [CI correspondente](https://github.com/matoslopes23/ai-dev-starter/actions/runs/42532392797) passou em Ubuntu com Python 3.10, 3.12 e 3.14. O resultado não é atribuído automaticamente à versão posterior.

## Evolução 3.0

Ambiente local de validação: macOS, Python 3.14, Git e Node 24.21.0. Comando: `python -B scripts/verify.py` usando o Python 3.14 disponível. O gate executa 43 testes das automações/harness e 8 da demo, além de estrutura, JSON, links Markdown locais explícitos, sintaxe Python e metadados das 24 skills.

Os testes protegem adoção sem gravação, preservação de instruções/configuração, idiomas/arquiteturas livres, gravação atômica, conflitos entre base/local/nova origem, migração de manifesto 2.1, recusas de symlinks/caminhos inválidos, remoção de arquivo limpo, recuperação em falhas e restauração com integridade. Entradas nativas têm nome/descrição/link canônico verificados; o harness de evals separa checagem estrutural de revisão semântica e invalida scorecards após nova edição.

[Quatro avaliações comportamentais](25-resultados-evals.md) foram executadas por agentes independentes do revisor em fixtures sintéticos, com reprodução e revisão dos artefatos. Os resultados não comprovam acionamento automático de skills em ferramentas externas nem qualidade de todos os produtos consumidores.

Verificações complementares: whitespace de todos os arquivos do pacote; `git diff --check`; aplicabilidade do patch do workshop; ausência do nome do produto usado originalmente apenas como exemplo. Resultados finais e commit testado são registrados no handoff local e na entrega. As [execuções de CI](https://github.com/matoslopes23/ai-dev-starter/actions) devem ser consultadas pelo SHA da entrega.

A matriz 3.0 foi ampliada para Ubuntu (Python 3.10/3.12/3.14), macOS e Windows (Python 3.12). Declarar a matriz não comprova que ela passou: use o resultado remoto do commit correspondente.

## Limites

- Não foi feita inspeção visual/interação da demo no navegador nem diagnóstico de uma aplicação real nesta evolução.
- A ativação automática dos adaptadores requer smoke test na versão/modalidade de cada ferramenta utilizada.
- O validador externo quick_validate.py do skill-creator não foi executado por ausência de PyYAML; o gate local valida metadados e o parse YAML alternativo é verificado separadamente quando disponível.
- O scanner é heurístico: não audita histórico Git, binários, arquivos grandes, symlinks ou todos os formatos de segredo. Adoção do kit não é certificação de segurança ou conformidade.
- As avaliações com agentes são amostras pequenas, sem inferência estatística ou medição confiável de tokens/custo.
