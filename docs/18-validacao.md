# Validação da evolução do kit

Data: 2026-11-08. Ambiente local: macOS, Python 3.14 via `/opt/homebrew/bin/python3`, Git e Node 24.21.0. Branch `main`, HEAD-base `76c8b61f6922ee5cfb7377842128b437a6522ca3`, alterações locais sem commit. O repositório tinha apenas README rastreado antes da tarefa; os demais arquivos preexistentes foram preservados e os arquivos novos fazem parte da entrega local.

## Evidências automatizadas

- PASSOU: `/opt/homebrew/bin/python3 -B scripts/verify.py`: 23 testes de adoção/inventário/configuração/verificação e 8 testes de domínio/HTTP da demo. Os sockets HTTP usam loopback; a execução completa foi autorizada fora do sandbox.
- PASSOU: estrutura, JSON, links Markdown locais explícitos, metadados de 24 skills e sintaxe Python no mesmo gate. O verificador não valida URLs remotas, anchors ou links por referência.
- PASSOU: parse YAML dos frontmatters das 24 skills com Ruby/Psych, disponível no ambiente, sem instalar dependências.
- PASSOU: sintaxe do workflow com Ruby/Psych; matriz declarada para Python 3.10, 3.12 e 3.14. A declaração não comprova execução remota.
- PASSOU: `git apply --check workshop/reference/filter.patch`; o exercício continua aplicável à demo preservada.
- PASSOU: revisão de whitespace de todos os arquivos textuais do pacote, incluindo não rastreados; não apenas `git diff --check`.

Os testes da automação verificam plano sem gravação, preservação de arquivos existentes, os três modos de adoção, recusa de instalação repetida/symlinks, recuperação após falha de cópia ou escrita, links do snapshot, manifesto inválido, repositórios ausentes/duplicados/sem commit, metadados reais de fixture Git e ausência de leitura de arquivos sensíveis pelo inventário. O scanner tem reprodução com PNG e dependências ignoradas; nomes conhecidos de credenciais são rejeitados antes de leitura.

A evolução 2.1 inclui prompt inicial único e scripts de configuração/diagnóstico no snapshot. Oito testes adicionais verificam linguagens e arquiteturas livres, dry-run, substituição atômica, preservação de extensões/permissões, recusas de configuração inválida e execução das CLIs instaladas. Um comando que criaria um arquivo foi registrado como check; configure e doctor não o executaram. O diagnóstico de configuração distingue lacunas de prontidão para começar a análise, sem aprovar testes do produto.

## Exercício independente das skills

Foi usado um fixture temporário com API Python, cliente JavaScript, contrato compartilhado e um terceiro repositório conhecido sem checkout. A aplicação das skills de adoção e mapeamento produziu mapa, baseline, diagnóstico e plano sem alterar os dois produtos. Os testes locais dos componentes passavam; a reprodução entre produtor e consumidor expôs incompatibilidade de contrato, priorizada no diagnóstico. A lacuna permaneceu como cobertura parcial.

O exercício da versão 2.0 revelou ambiguidade entre checkout central e snapshot instalado, inicialmente corrigida nos guias. A versão 2.1 passou a incluir configuração, diagnóstico e inventário no snapshot; instalação/atualização e gate do kit continuam no checkout central. É uma avaliação sintética pequena, não comprovação de adoção em um sistema real.

## Limites e pendências

- NÃO EXECUTADO: CI remota, matriz local em Python 3.10/3.12, inspeção visual ou interação da demo em navegador.
- NÃO EXECUTADO: `quick_validate.py` do skill-creator, pois PyYAML não está instalado nos runtimes disponíveis. A validação local de metadados e o parse YAML alternativo passaram; não se declara execução daquele comando.
- NÃO EXECUTADO: diagnóstico dos repositórios reais do AgendaLu, pois não foram fornecidos neste escopo. O guia e o manifesto começam sem inferir sua arquitetura.
- NÃO REALIZADO: commit, push, merge, publicação ou deploy. Proteções de branch e gates de consumidores devem ser configurados no projeto real.

O scanner é heurístico, ignora binários/arquivos grandes/symlinks e diretórios de dependências, e não verifica histórico Git. Adoção de documentação não equivale a certificação de segurança, conformidade ou escalabilidade.
