---
name: instrumentar-sistema
description: Defina e implemente sinais de observabilidade e objetivos de confiabilidade ligados a jornadas reais.
---

# instrumentar-sistema

Entrada: jornada, modos de falha e operação existente. Leia [operação](../../docs/13-operacao.md).

1. Escolha indicador, meta e janela com significado para o usuário; registre hipótese quando o negócio ainda não confirmou o objetivo.
2. Identifique fronteiras para logs estruturados, métricas e traces. Defina correlação entre serviços sem expor dados pessoais/segredos ou gerar labels de cardinalidade ilimitada.
3. Instrumente o mínimo para distinguir erro, latência, saturação e fila relevantes. Valide falha parcial, amostragem, retenção e custo.
4. Configure alertas acionáveis com responsável e [runbook](../../templates/runbook.md); evite notificação sem resposta definida.
5. Verifique emissão e diagnóstico em ambiente permitido; não ative coleta de dados reais ou serviços pagos por inferência.

Saída: sinais, objetivo, alertas/runbook e evidência. Dashboard sem ação ou meta não comprova confiabilidade.
