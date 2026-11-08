# Demonstração ao vivo: de pedido a evidência

## Preparação

Ensaie com a mesma ferramenta/modelo que usará na apresentação. Rode `python3 scripts/verify.py` e `python3 examples/taskboard/server.py`. Abra http://127.0.0.1:8000. Não dependa de instalação, cloud ou chaves. O agente de IA precisa estar disponível separadamente: a aplicação não chama IA.

## 1. Mostrar o contrato (3 min)

Abra README, AGENTS e o roteador. Explique que o método independe do Python. Mostre uma skill, sem carregar todas. Rode o gate e mostre o baseline.

## 2. Pedido e plano (4 min)

Cole em seu agente:

“Leia AGENTS.md e ia-context/CONTEXT_ROUTER.md. Na demo taskboard, adicione um checkbox ‘Somente pendentes’. Ao ativar, esconda concluídas; ao desativar, mostre todas sem perder estado. Concluir a última pendente deve mostrar estado vazio correto. Deve funcionar por teclado. Não adicionar dependências, backend, persistência ou mudanças visuais fora do controle. Registre plano e aceite antes de editar. Não leia workshop/reference/ para resolver.”

Mostre os arquivos selecionados, o plano e os critérios. Pergunte à turma qual é o caso de borda antes de implementar.

## 3. Implementar e testar (10–15 min)

Deixe o agente implementar a mudança pequena. A validação de domínio/API não cobre o filtro do navegador: peça teste de comportamento apropriado à ferramenta disponível e execute também `ACEITE.md` manualmente. Mostre o diff e peça ao agente para encontrar defeitos concretos.

## 4. Entrega (3 min)

Rode gates, demonstre teclado/estado vazio e mostre o handoff com o que foi ou não testado. Explique por que contexto menor ajuda foco, sem alegar percentual de tokens.

## Plano B (5 min)

Uma solução de referência revisável está em `workshop/reference/filter.patch`. Ela não está aplicada no baseline. Se o agente/Internet falhar, pare o servidor e aplique:

```sh
git apply --check workshop/reference/filter.patch
git apply workshop/reference/filter.patch
python3 scripts/verify.py
python3 examples/taskboard/server.py
```

Confira antes `git diff`: se já houve edição no mesmo arquivo, não force o patch. Use um clone limpo separado para o plano B. A demonstração da solução de referência é leitura guiada, não prova de implementação ao vivo pelo agente.

## Comparação honesta

Registre tempo e telemetria real em templates/medicao.csv. Uma execução ao vivo mede somente aquela execução. Testes passados, tamanho do diff e ausência de dependências novas são observáveis; redução de tokens exige medição.
