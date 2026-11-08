# Contribuir

Leia AGENTS.md, identifique a fronteira e registre objetivo/aceite. Mudanças devem manter o núcleo independente de linguagem e arquitetura. Uma nova skill precisa de gatilho distinto, decisão útil, saída verificável e referências carregadas por necessidade.

Execute `python -B scripts/verify.py`, revise o diff e adicione testes somente onde protegem comportamento ou risco real. Mudanças em instalação/update precisam de fixtures de preservação, conflitos e falhas; alterações relevantes de skills devem ter avaliações comportamentais adequadas. Não apresente checker estrutural como validação semântica.

Use exemplos sintéticos e genéricos. Não inclua credenciais, dados de clientes, cópias de logs ou transcrições privadas. Indique fonte/licença quando incorporar material externo; não copie regras ou scripts de outros kits sem revisão de adequação.

Descreva o problema e o resultado da mudança no PR, comandos/resultados e limitações. Mudanças incompatíveis precisam de migração documentada, atualização da versão em kit-version.json e entrada no CHANGELOG.md. Não atualize a versão só para alterar documentação.
