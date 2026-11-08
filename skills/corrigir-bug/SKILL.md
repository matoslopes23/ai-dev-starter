---
name: corrigir-bug
description: Reproduza e corrija um defeito com causa confirmada e proteção contra regressão.
---

# corrigir-bug

Entrada: esperado, observado, ambiente e escopo. Não solicite logs reais ou dados privados; use reprodução sintética.

1. Reproduza e reduza o caso. Separe fato, hipótese e condição ainda não reproduzida; confira versões e configuração sem segredos.
2. Trace origem e propagação, incluindo consumidor e contrato. Diferencie sintoma da causa; não esconda falhas com catch amplo ou fallback de sucesso.
3. Quando viável, crie regressão que falhe no estado antigo e registre a evidência. Para UI, inclua a interação que provoca o defeito.
4. Corrija a menor fronteira suficiente; preserve compatibilidade e valide casos adjacentes relevantes.
5. Execute gates, confira diff e relate causa confirmada, comportamento corrigido e limitações.

Saída: reprodução, causa/evidência, correção e verificação. Se a causa não puder ser confirmada, entregue o que foi isolado e o próximo experimento, sem afirmar resolução.
