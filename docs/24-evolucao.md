# Evolução orientada por evidências

A comparação com [Spec Kit](https://github.com/github/spec-kit), [OpenSpec](https://github.com/Fission-AI/OpenSpec), [Superpowers](https://github.com/obra/superpowers), [BMAD](https://github.com/bmad-code-org/BMAD-METHOD) e [Awesome Copilot](https://github.com/github/awesome-copilot) identificou prioridades operacionais. Recursos não são incorporados apenas porque existem em outro kit; preservar neutralidade, segurança e proporcionalidade continua sendo requisito.

| Frente | Estado na versão 3.0 | Critério para avançar |
|---|---|---|
| Integração de skills | Entradas nativas opcionais, fonte canônica e testes de colisões/links | Smoke de descoberta/ativação em cada ferramenta e modalidade usada |
| Avaliações de comportamento | Quatro casos versionados, harness estrutural e scorecard semântico vinculado ao resultado | Repetir cenários em ambientes/modelos relevantes, registrar falhas e regressões |
| Atualização | Comparação base/local/nova, conflitos, backups e restore com verificação de integridade | Avaliar ciclos reais de adoção e atualizar política de migrações conforme falhas observadas |
| Portabilidade | Matriz CI proposta para Ubuntu/macOS/Windows; resultados no relatório de validação | Manter gates aprovados em todos os ambientes declarados |
| Rastreabilidade de features | Templates e revisão manual | IDs estáveis e validação entre requisito, plano, tarefa e teste |
| Contexto incremental multi-repo | Inventário Git e mapa com evidências; atualização manual | Detectar mudanças que invalidam evidências, mantendo fallback para stacks sem analisador |
| Gates do consumidor | Comandos configuráveis; execução pelo operador/agente autorizado | Descritores com diretório/timeout/obrigatoriedade e relatório opt-in por commit/diff |
| Packs de stack/arquitetura | Núcleo livre e perfis documentais | Fixtures de consumo real e referências de versões para necessidades comprovadas |
| Distribuição e segurança | Versionamento local, changelog, contribuição e política de relatos | Releases reproduzíveis e ferramentas de análise especializadas segundo o risco |

Não há promessa de economia de tokens ou qualidade superior a partir de número de skills. Resultados devem ser comparados por tarefas, ambiente, critérios e custo observados. Os próximos packs devem partir de aplicações reais autorizadas, sem personalizar o núcleo para uma marca ou produto.
