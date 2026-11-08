---
name: migrar-dados
description: Planeje e implemente mudanças de schema ou dados com compatibilidade, ensaio e recuperação.
---

# migrar-dados

Entrada: schema atual, consumidores, volume estimado e mudança. Use [migration](../../templates/migration.md).

1. Identifique invariantes, dono de escrita, versões coexistentes, locks e risco de perda. Não leia dumps ou dados reais para montar exemplos.
2. Avalie expandir → migrar → contrair: schema compatível, backfill controlado e remoção posterior. Registre transação, lotes, checkpoint, idempotência e duração/lock esperados.
3. Defina recuperação: rollback seguro ou roll-forward; backup só conta com restauração testada. Mudança destrutiva exige uma janela e autorização correspondentes.
4. Implemente e ensaie em ambiente isolado com dados sintéticos representativos, incluindo falha parcial e retomada. Verifique integridade e versões antigas/novas.
5. Prepare execução, observação, critérios de interrupção e evidências de conclusão. Rodar localmente não autoriza aplicar em banco remoto.

Saída: migração revisável, ensaio, compatibilidade e plano operacional. Informe limitações de volume/ambiente do ensaio.
