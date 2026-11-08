# Perfis por tipo de aplicação

O núcleo do kit é comum. Acrescente gates da plataforma, domínio e regulamentação relevantes; ele não contém todos os detalhes de cada ecossistema. Em primeira adoção, selecione perfis aplicáveis e registre lacunas e fontes oficiais no projeto.

| Perfil | Fronteiras e riscos a investigar | Evidência típica |
|---|---|---|
| Web/frontend | Estado, sessão, acessibilidade, rede, bundle, browser support | Teclado/foco, estados de UI, integração e jornadas |
| API/backend | Autorização por objeto/tenant, schema, concorrência, limites | Contrato, integração, abuso e idempotência |
| Mobile | Ciclo de vida, offline, sincronização, permissões, armazenamento local | Dispositivo/emulador, interrupção e compatibilidade de versões |
| Desktop/CLI | Filesystem, argumentos, permissões, distribuição e atualização | Entradas inválidas, exit codes e instalação suportada |
| Dados/ETL | Schema, qualidade, linhagem, replay, retenção e custo | Idempotência, validação, reprocessamento e dados sintéticos |
| Bibliotecas/SDK | API pública, compatibilidade e matriz de consumidores | Testes por runtime, exemplos executáveis e versionamento |
| Jobs/filas | Duplicação, ordenação, retry, DLQ e agendamento | Falhas parciais, replay e cancelamento |
| IA/LLM no produto | Dados enviados, prompt injection, ferramentas, avaliação e custo | Evals versionados, limites de ação e regressões de qualidade |
| Infra/serverless/edge | Estado, cold start, quotas, permissões e distribuição | Plan, smoke, recuperação e limites do provedor |
| Embarcado/tempo real | Hardware, deadlines, atualização e falha física | Simulação e validação especializada de hardware/segurança |

Perfis financeiros, de saúde ou outros ambientes regulados exigem responsáveis e revisão especializada. Não transforme este catálogo em afirmação de conformidade legal ou certificação de segurança.

Para interfaces: use semântica nativa, nomes acessíveis, erros associados ao campo, foco previsível, responsividade e contraste. Preserve estado durante rede lenta e interrupções. Para mobile, inclua navegação de retorno, permissões negadas e sincronização conflitante. Consulte WCAG e guias oficiais da plataforma aplicáveis.

Para produtos com IA: diferencie o agente que desenvolve o software do modelo que faz parte do produto. Versione evals com dados permitidos e critérios de sucesso/falha; defina comportamento de indisponibilidade, validação de saída e autorização fora do modelo. Não use somente exemplos felizes nem confunda respostas plausíveis com correção.
