---
name: atualizar-dependencias
description: Atualize bibliotecas, runtimes ou imagens com análise de compatibilidade, vulnerabilidade e licença.
---

# atualizar-dependencias

Entrada: dependência/alvo, motivo e escopo. Não combine atualização ampla com correção não relacionada.

1. Descubra manifesto, lockfile, runtime e consumidores reais. Consulte advisories, changelog e guia de migração oficiais para as versões envolvidas.
2. Confirme aplicabilidade do problema e alterações incompatíveis; registre APIs removidas, licença e suporte. Um aviso de scanner não comprova exploração na aplicação.
3. Escolha a menor atualização suficiente ou justifique salto maior. Revise scripts de instalação e origem; não exponha tokens de registry.
4. Atualize por mecanismo da stack e lockfile consistente. Valide compile/build, integração e jornadas afetadas; inclua matriz de runtimes quando necessária.
5. Registre diferença de versões, riscos residuais e plano de rollout/recuperação.

Saída: atualização reproduzível e evidência. Não aplique “fix --force” indiscriminado nem desative check para ocultar um alerta.
