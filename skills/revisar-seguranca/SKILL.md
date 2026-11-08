---
name: revisar-seguranca
description: Avalie ameaças e controles de uma mudança ou aplicação com evidências e escopo de segurança explícito.
---

# revisar-seguranca

Entrada: ativos, dados, fronteiras e escopo de revisão. Leia [segurança](../../docs/05-seguranca.md).

1. Faça [threat-model](../../templates/threat-model.md): ator, ativo, ação abusiva, impacto e controle esperado. Priorize superfícies realmente expostas.
2. Trace autenticação e autorização até o objeto/tenant, validação, encoding, consultas, arquivos, URLs externas, sessões, webhooks e segredos conforme o sistema.
3. Verifique dependências, execução de código não confiável e permissões de pipeline. Selecione requisitos ASVS aplicáveis e consulte a versão oficial; não alegue cobertura total do padrão.
4. Reproduza riscos com dados sintéticos em ambiente autorizado. Auditoria estática não autoriza probes remotos, exfiltração ou acesso a dados reais.
5. Registre gravidade, evidência sanitizada, impacto, correção e teste negativo. Para exposição de segredo, evite reproduzir o valor e acione o processo de rotação do responsável.

Saída: riscos verificados, controles, lacunas e plano. Correções e operações remotas seguem o escopo já autorizado; não declare certificação.
