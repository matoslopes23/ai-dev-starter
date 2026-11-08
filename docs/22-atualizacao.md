# Atualizar e recuperar uma instalação

As atualizações usam uma origem local revisada: o script não busca versões na rede nem executa o código da origem. Confirme sua versão em `kit-version.json`. Gere o plano antes de aplicar:

```sh
# Da raiz de uma aplicação que recebeu o kit:
python3 .ai-kit/scripts/update.py --target . --source ../kit
python3 .ai-kit/scripts/update.py --target . --source ../kit --apply
```

O checkout central também oferece `python3 scripts/update.py --target ../produto --source .`. Um snapshot completo pode ser usado como origem. Não use diretórios obtidos de fontes não revisadas.

## Comparação entre três estados

A base é o conjunto de hashes em `.ai-kit/origin.json`. Ele é comparado com os bytes locais e os bytes da origem desejada.

| Situação | Resultado |
|---|---|
| Local e origem nova iguais | Nenhuma gravação necessária |
| Local igual à base; origem alterada | Atualizar ou remover arquivo gerenciado |
| Local personalizado; origem igual à base | Preservar personalização local |
| Local e origem mudaram de maneiras diferentes | Conflito; recusar toda a aplicação do plano |
| Arquivo novo colide com conteúdo local | Conflito; preservar conteúdo local |

`project.json` e `system.json` da instalação são sempre preservados. Instruções na raiz, código do produto e arquivos fora da lista gerenciada não são atualizados. A seleção de adaptadores pode ser alterada com flags documentadas em [integrações](21-integracoes.md).

Os hashes comparam bytes, inclusive finais de linha. O payload inclui `.ai-kit/.gitattributes` com LF para manter snapshots consistentes entre sistemas. Se versionar entradas nativas, preserve suas regras existentes e configure LF também nesses diretórios no `.gitattributes` do projeto. Conversões de EOL ou filtros Git podem aparecer como personalizações/conflitos; o update não normaliza conteúdo local automaticamente.

Instalações 2.1 são reconhecidas pelos hashes legados. O README gerado conhecido também é reconhecido; arquivos sem uma base confiável causam conflito ou exigem migração manual. Ausência de manifesto/hash-base não autoriza sobrescrever o destino. Não há opção de force.

## Backup e restauração

Aplicações efetivas criam `.ai/kit-backups/<id>/` com os bytes dos arquivos que mudarão, hashes antes/depois e a origem anterior. O ID é retornado no resultado. Esses backups são locais e não devem ser publicados. O ignore de `.ai/` já é configurado na adoção.

```sh
python3 .ai-kit/scripts/update.py --target . --restore ID_DO_BACKUP
python3 .ai-kit/scripts/update.py --target . --restore ID_DO_BACKUP --apply
```

A restauração verifica a integridade do backup e recusa alterações se os arquivos afetados ou o manifesto da instalação mudaram desde o update. Ela não restaura código/configuração do produto, que não participaram da atualização.

Se a gravação do status final do backup falhar, um backup `prepared` só pode ser restaurado quando todos os hashes do estado após update coincidirem. Estado parcialmente gravado ou arquivos modificados exigem investigação; não são sobrescritos pelo restore.

Cada gravação é atômica; a transação entre vários arquivos usa backup e reversão em falhas capturadas. O lock `.ai-kit/.update.lock` impede dois updates simultâneos. Não execute configure, edição manual ou outro instalador ao mesmo tempo. Uma interrupção abrupta do processo pode deixar lock/estado intermediário: preserve o backup, confira hashes e investigue antes de remover manualmente um lock. O script não apaga locks existentes para prosseguir.

Exit codes: `0` para plano/aplicação sem conflitos, `2` para conflitos e `1` para entrada inválida, erro de I/O ou lock existente. Plano sem `--apply` não cria backup, lock ou arquivos. Após atualizar, execute doctor, revise instruções e rode os gates reais do consumidor.
