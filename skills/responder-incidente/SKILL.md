---
name: responder-incidente
description: Investigue e coordene um incidente com mitigação autorizada, evidências e análise posterior.
---

# responder-incidente

Entrada: sintoma, ambiente, impacto conhecido e papel autorizado. Use [incident](../../templates/incident.md).

1. Confirme impacto e delimite sistemas/usuários afetados sem copiar dados pessoais. Registre horários, fontes e hipóteses separadas.
2. Identifique mudanças recentes e modos de falha com sinais sanitizados. Não confunda coincidência temporal com causa.
3. Priorize mitigação reversível e de menor blast radius dentro do runbook e da autorização. Não faça migração destrutiva ou reinício amplo por tentativa.
4. Verifique recuperação pelas jornadas e sinais, preservando evidência necessária. Coordenação ou envio de mensagens externas depende de autorização explícita.
5. Após estabilizar, registre causa confirmada, fatores contribuintes, lacunas e ações com dono e verificação; evite culpabilização individual.

Saída: impacto, linha do tempo, estado atual e ações verificáveis. Investigação local não autoriza atuação em produção.
