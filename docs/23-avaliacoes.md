# Avaliar comportamento das skills

Os testes unitários do kit validam scripts e invariantes. As avaliações aqui exercitam decisões de um agente em tarefas reais pequenas: reprodução, respeito ao escopo, cobertura parcial e resistência a instruções externas. Não tratam a presença de uma palavra no texto como prova de qualidade.

O checkout central contém `evals/cases/` e `scripts/evaluate.py`. Eles não são instalados na aplicação. Use uma pasta temporária nova por execução:

```sh
python3 scripts/evaluate.py --prepare legacy-contract --output /caminho/temporario/avaliacao-1
```

O comando copia somente dados sintéticos para `workspace/` e cria `REQUEST.md` e `state.json`. Ele não chama modelos nem executa código do fixture. Entregue somente `REQUEST.md` ao agente avaliado, em uma sessão separada, com acesso ao kit como leitura. Não forneça a resposta esperada nem os resultados de outra execução. A execução de comandos pelo agente continua sujeita à revisão e às permissões normais do ambiente.

Casos iniciais: `legacy-contract`, `bug-regression`, `multi-repo-gap` e `untrusted-note`. Cada caso tem objetivo, fronteira editável, artefatos obrigatórios e critérios semânticos versionados. Adicione casos pelas falhas observadas, sem gerar um catálogo de cenários redundantes.

## Dois níveis de resultado

```sh
python3 scripts/evaluate.py --check /caminho/temporario/avaliacao-1
```

A checagem determinística compara os arquivos com o fixture versionado, aponta mudanças fora do escopo e exige artefatos. Ela retorna `behavioral_status: needs-review`: isso **não aprova o conteúdo da resposta**.

Um avaliador independente deve ler o pedido, a skill, o diff, a resposta e as evidências dos comandos. Para cada item da rubric retornada, registra `passed` booleano e `evidence` textual em um scorecard. Exemplo de formato (substitua todos os valores e inclua todos os critérios):

```json
{
  "case": "legacy-contract",
  "fingerprint": "valor retornado pelo checker",
  "reviewer": "identificação do avaliador e ambiente/modelo quando aplicável",
  "criteria": [{"passed": true, "evidence": "Evidência verificada, não apenas alegada pelo agente"}]
}
```

```sh
python3 scripts/evaluate.py --check /caminho/temporario/avaliacao-1 --review /caminho/scorecard.json
```

O scorecard precisa corresponder ao fingerprint dos arquivos e da resposta atuais. Nova edição invalida a revisão anterior. O harness valida o formato e o vínculo, não a honestidade ou a independência declarada do avaliador. A decisão semântica continua sendo responsabilidade desse avaliador.

Exit codes do check: `0` com checagem estrutural e revisão semântica aprovadas; `2` quando ainda precisa de revisão; `1` para falha ou entrada inválida. Resultados sem modelo/ambiente/data ou sem evidências suficientes não devem ser apresentados como benchmark generalizável. Registre custo e repetição quando a ferramenta os informar; não invente economia de tokens.

## Gate e limites

A CI executa os testes determinísticos do harness; ela não contrata APIs ou modelos automaticamente. Avaliações com agentes são opt-in e precisam de ambiente, custo e acesso autorizados. Registre execuções reais em `.ai/eval-results/` ou em relatório sanitizado específico, sem transcrições privadas. Compare resultados por versão da skill e do caso.

Consulte [os resultados iniciais e seus limites](25-resultados-evals.md).
