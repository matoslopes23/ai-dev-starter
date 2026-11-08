---
name: mapear-sistema
description: Mapeie jornadas, dados, contratos e dependências de um sistema, inclusive distribuído por vários repositórios.
---

# mapear-sistema

Entrada: inventário autorizado e jornadas de interesse. Leia [multi-repositório](../../docs/10-multi-repositorio.md).

1. Confirme fronteira do sistema, atores, integrações e repositórios conhecidos. Use `system.json`; paths ausentes permanecem lacunas. Não trate convenção de nome como prova de responsabilidade.
2. Registre repo@commit e rastreie entrada → autorização → caso de uso → escrita/leitura → evento/integração → retorno. Inclua jobs, bibliotecas e infra que realmente participam.
3. Identifique invariantes, donos de dados, transações, contratos e consumidores, versões coexistentes, sincronismo e falhas parciais.
4. Produza [system-map](../../templates/system-map.md), com evidência por símbolo e cobertura por jornada/repo. Use diagramas para comunicação; mantenha contratos e incertezas explícitos.
5. Para mudança transversal, identifique a menor fronteira e preencha [cross-repo-change](../../templates/cross-repo-change.md), com ordem e recuperação.

Saída: mapa verificável, tabela de contratos e áreas não cobertas. Não leia tudo em uma conversa nem declare completude sem fontes.
