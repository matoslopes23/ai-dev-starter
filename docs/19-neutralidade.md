# Qualquer linguagem, paradigma ou arquitetura

O contrato do kit é sobre engenharia: objetivos, fronteiras, comportamento, contratos, evidências e operação. Sintaxe, compilação, distribuição, estrutura física e testes pertencem ao projeto. Os campos `stack`, `architecture.style` e os comandos de `checks` são livres; nenhuma linguagem ou estilo é requisito ou precisa ser adicionado a uma lista de suporte.

## O que é comum e o que se adapta

| Núcleo comum | Adaptação no produto |
|---|---|
| Aceite e invariantes | Tipos, regras, representação e mecanismos de erro da linguagem |
| Coesão e dependências explícitas | Funções, módulos, objetos, atores, entidades ou outros mecanismos apropriados |
| Contratos e isolamento de efeitos | Protocolos, APIs, interfaces ou convenções próprias do paradigma |
| Gates reproduzíveis | Ferramentas e comandos reais de build, análise, teste e empacotamento |
| Entrega e recuperação | Distribuição, ambiente, dados e requisitos operacionais concretos |

Código limpo se traduz em intenção clara, invariantes protegidas, efeitos compreensíveis e mudança testável. Isso se aplica a código procedural, funcional, orientado a objetos, orientado a dados, declarativo ou misto. Não é necessário converter tudo em classes, entidades, repositories ou casos de uso.

Arquitetura limpa e hexagonal são opções. MVC, monólito modular, serviços, eventos, atores, serverless, pipelines e arquiteturas específicas de domínio também podem usar o kit. Avalie as fronteiras no estilo observado. Em aplicação nova, justifique a escolha pelos requisitos; em existente, registre problemas concretos antes de propor migração.

## Linguagem sem detector ou receita

1. Registre nomes e versões confirmados em `stack`.
2. Identifique módulos, executáveis, bibliotecas e contratos em `components` e no mapa.
3. Consulte ferramentas e comandos oficiais do projeto; configure `checks` sem executá-los automaticamente.
4. Adapte os testes aos comportamentos e riscos. Ausência de lint/tipos/build deve ter justificativa ou tarefa de configuração.
5. Documente limitações do agente e ambientes que exigem hardware, compilador proprietário ou revisão especializada.

A presença de manifests conhecidos no inventário é somente uma pista. Não detectar um manifesto não significa que a linguagem é incompatível. Sistemas com várias linguagens podem registrar todas no mesmo projeto, ou manter configurações por repositório e mapa compartilhado.

## Ferramenta versus produto

As automações usam Python 3.10+ com biblioteca padrão e caminhos via `pathlib`; os procedimentos em Markdown podem ser aplicados sem elas. Isso não adiciona Python às dependências, ao build ou ao runtime do produto. Comandos da aplicação são texto opaco para os scripts de configuração e diagnóstico: podem ser de qualquer ferramenta ou linguagem.

O kit não gera código correto para todo domínio automaticamente nem comprova suporte a todas as plataformas. Os gates e as decisões precisam de evidências no ambiente real da aplicação. Consulte [configuração](20-configuracao.md).
