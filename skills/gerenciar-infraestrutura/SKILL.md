---
name: gerenciar-infraestrutura
description: Revise ou altere infraestrutura como código com estado, permissões, custo e recuperação explícitos.
---

# gerenciar-infraestrutura

Entrada: recursos, ambiente, IaC e operação autorizada.

1. Identifique provedor, módulos, estado/lock, dependências e dono dos recursos. Não leia segredos ou despeje estado potencialmente sensível.
2. Separe validação estática, plan e apply. Inspecione scripts/providers antes de executar; plan também pode acessar rede e revelar valores.
3. Avalie privilégio mínimo, exposição de rede, dados, drift, substituições/destruição, custo e blast radius. Registre dependências e recuperação em ADR/runbook quando necessário.
4. Prepare diff e plan sanitizado vinculados ao estado e commit corretos. Um plan antigo não deve ser aplicado após mudança relevante.
5. Execute operações remotas somente dentro do escopo autorizado e verifique saúde, estado e custo observáveis; preserve logs sem segredos.

Saída: alteração revisável, impacto e evidência. IaC presente no repo não concede autorização para criar, destruir ou publicar recursos.
