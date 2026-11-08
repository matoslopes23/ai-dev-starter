---
name: revisar-diff
description: Revise alterações de código ou documentação e relate defeitos concretos por impacto e reprodução.
---

# revisar-diff

Entrada: objetivo, aceite, diff autorizado e estado-base. Inclua arquivos novos; `git diff` sozinho não mostra não rastreados.

1. Confirme o escopo e leia instruções locais. Expanda leitura apenas para dependências e consumidores necessários para julgar o comportamento.
2. Confira invariantes, erros, compatibilidade, autorização, dados, concorrência, acessibilidade e operação conforme a mudança. Não confunda preferência estética com bug.
3. Avalie se os testes exercitam o comportamento e falhas relevantes; verifique os comandos realmente executados e o estado testado.
4. Relate achados em [review](../../templates/review.md): severidade, arquivo/linha/símbolo, gatilho, impacto, reprodução/evidência e recomendação mínima. Marque hipótese quando faltar confirmação.
5. Declare a cobertura e os limites. Ausência de achados não equivale a aprovação de segurança ou de todo o sistema.

Saída: achados acionáveis, riscos e gaps de validação. Uma revisão solicitada não autoriza corrigir ou publicar mudanças automaticamente.
