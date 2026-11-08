# Contexto útil e custo verificável

Tokens não são sinônimo de qualidade. O objetivo é evitar leitura e repetição sem perder evidências. Não existe percentual de economia garantido por este template.

## Práticas

- Entrada pequena e estável: contrato + roteador + tarefa.
- Busca por símbolo/rota antes de leitura integral. Leia trechos e amplie se houver dependência.
- Use referências a arquivos e fatos, não recopie diretórios ou conversas.
- Carregue uma skill por necessidade. Não injete todo o catálogo.
- Checkpoint ao concluir uma etapa, confirmar causa ou encontrar bloqueio.
- Handoff curto aponta ao estado principal e inclui próxima ação executável.
- Paralelize somente fronteiras independentes. Cada agente extra tem custo de contexto e integração.
- Use modelo/ferramenta conforme risco e capacidade, não apenas menor preço.

## Experimento honesto

Escolha a mesma tarefa e condições, registre modelo/versão/data, prompt, contexto fornecido, tokens de entrada/saída quando a ferramenta informar, chamadas, tempo, testes passados e retrabalho. Compare baseline e fluxo roteado em execuções independentes. Cache, raciocínio e preços variam; bytes/caracteres não equivalem exatamente a tokens. Sem telemetria real, reporte apenas arquivos/linhas lidos e tempo, sem convertê-los em “economia de tokens”.

Use `templates/medicao.csv`. Nunca apresente um resultado de uma única demonstração como benchmark generalizável.
