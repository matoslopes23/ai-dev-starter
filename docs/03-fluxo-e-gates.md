# Fluxo de trabalho e gates

## Da intenção à entrega

1. **Entender:** usuário, comportamento esperado, aceite mensurável, escopo e riscos. Use [feature](../templates/feature.md) quando o pedido ainda não estiver especificado.
2. **Localizar:** comportamento existente, dependências e contratos. Em primeira adoção, estabeleça baseline antes de editar.
3. **Planejar:** fronteiras, menor entrega, validações e recuperação. Mudanças difíceis de reverter pedem ADR/plano de migração.
4. **Implementar:** uma fatia vertical. Cubra regressões e regras importantes; preserve mudanças alheias.
5. **Verificar:** gates locais e do CI, consumidores afetados e aceite manual pertinente. Registre falhas preexistentes separadamente.
6. **Revisar:** diff integral do escopo, contratos, segurança, acessibilidade, dados e operação conforme risco.
7. **Entregar:** evidências, limites, documentação e próxima ação. Publicação é uma operação com destino e autorização próprios.

## Definição de pronto

Aceite atendido e demonstrável; código revisado; checks obrigatórios aprovados para o estado final; contratos compatíveis ou migração coordenada; documentação necessária atualizada; sem novos segredos; risco de rollout e recuperação conhecidos. Exceção precisa de responsável, motivo e prazo. Um gate obrigatório bloqueado impede declarar entrega pronta para merge, mesmo que a edição local esteja concluída.

## Matriz de risco

| Mudança | Evidência adicional |
|---|---|
| Documentação | Links/comandos, consistência e whitespace do diff |
| Regra de negócio | Limites, erro, invariantes e regressão |
| UI/mobile | Teclado, foco, estados vazio/erro/carregamento, navegação e visual |
| API/evento | Schema, erros, autorização, idempotência e consumidores |
| Banco | Ensaio com dados sintéticos, compatibilidade e recuperação |
| Concorrência/filas | Duplicação, corrida, ordenação e falhas parciais |
| Segurança/pagamento | Modelo de ameaça, abuso e validação especializada quando necessária |
| Infra/deploy | Plan, blast radius, permissões, rollout e rollback |

## Evidência reproduzível

Registre runtime, diretório, comando exato, status, contagem quando disponível, commit e diff testado. Se falta ferramenta ou credencial, reporte **não executado**. Se falta configuração, reporte **não configurado**. Não instale dependências ou contorne controles sem avaliar escopo e efeitos.

O gate deste kit é `python3 scripts/verify.py`. Ele executa testes da automação e da demo, integridade documental e scanner heurístico. Os projetos consumidores mantêm seus próprios gates em sua configuração. A demo e o kit não provam acessibilidade, segurança ou confiabilidade de outro sistema.
