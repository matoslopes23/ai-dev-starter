---
name: implementar-interface
description: Implemente ou ajuste interfaces web/mobile com estados, acessibilidade e navegação verificáveis.
---

# implementar-interface

Entrada: jornada, plataforma, referência visual quando houver e aceite. Preserve componentes e design system existentes.

1. Mapeie estado, ações e contrato de rede; preveja carregamento, vazio, erro, indisponibilidade, interrupção e repetição.
2. Use semântica nativa e nomes acessíveis, associe erros a campos e mantenha foco previsível. Evite recriar controles focados sem restauração intencional.
3. Separe regras de negócio de apresentação quando necessário. Renderize texto não confiável de forma segura e valide no servidor as regras e permissões.
4. Valide responsividade e teclado; em mobile inclua ciclo de vida, retorno, permissões e offline conforme impacto. Consulte [perfis](../../docs/14-perfis.md).
5. Execute checks e inspeção de UI em ambiente suportado. Registre navegador/dispositivo e evidência; DOM simulado não comprova layout nem acessibilidade.

Saída: interação implementada, estados cobertos e limites da validação. Não declare validação visual quando somente sintaxe ou testes de backend foram executados.
