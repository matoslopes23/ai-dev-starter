# Entender um sistema com vários repositórios

Um workspace de engenharia reúne contexto; ele não precisa fundir históricos nem transformar o sistema em monorepo. Mantenha o kit e os repositórios do produto em pastas separadas. A topologia abaixo é ilustrativa, não pressupõe que seu sistema tenha estes componentes:

```text
trabalho/
  template-ia-desenvolvimento/
  sistema-contexto/          # mapa e decisões do sistema
  repos/                    # checkouts autorizados, estrutura livre
```

Crie `sistema-contexto`, adote com `--mode multi-repo` e edite `.ai-kit/system.json`. Cada item de `repositories` tem `id`, `path` (relativo ao manifesto ou absoluto), `url` opcional sem credenciais, `role`, `owner` e `depends_on` (IDs existentes). Caminhos locais podem ficar apenas em uma cópia privada; não publique a topologia privada sem revisão.

Exemplo de um item, a substituir pelos dados confirmados do sistema. `path: null` registra um repo conhecido ainda sem checkout; ele não será clonado pelo inventário.

```json
{
  "id": "componente-a",
  "path": null,
  "url": null,
  "role": "Responsabilidade a confirmar",
  "owner": "Responsável a confirmar",
  "depends_on": []
}
```

```sh
# Execute do checkout central original; o comando é somente leitura, sem rede.
python3 scripts/inventory.py --manifest ../sistema-contexto/.ai-kit/system.json
```

Na raiz de um consumidor instalado com kit 2.1 ou posterior, use `python3 .ai-kit/scripts/inventory.py --manifest .ai-kit/system.json`. Instalações 2.0 não incluíam scripts e precisam do checkout central ou de atualização revisada. Consulte [portabilidade](17-portabilidade.md).

O inventário inspeciona metadados Git e a presença de manifests conhecidos nos caminhos explicitamente listados. Não clona, busca remotos, abre arquivos de segredos, executa builds nem descobre repositórios de uma organização. Checkouts ausentes ficam como lacunas. Branch, HEAD e estado são uma fotografia local, não prova do estado de produção.

Exit codes: `0` para metadados coletados sem lacunas locais, `2` para inventário parcial/vazio e `1` para manifesto inválido ou erro de leitura. Mesmo com `0`, a cobertura funcional continua parcial: código, jornadas e contratos ainda precisam ser analisados.

## Cobertura do contexto

Faça primeiro uma visão de contexto (atores e sistemas externos), depois de unidades executáveis/dados e depois de componentes nas áreas de risco. Diagramas no estilo C4 ajudam a comunicar, mas não substituem contratos e evidência de código. Em cada jornada, registre chamadas síncronas, eventos, armazenamentos, limites de confiança, dono de dados e falhas parciais.

Mantenha [system-map](../templates/system-map.md), [diagnóstico](../templates/diagnostic.md) e uma tabela de contratos: produtor, consumidor, schema/versão, autenticação, invariantes, compatibilidade e responsável. Use o mesmo ID de tarefa quando uma alteração atravessar repositórios; cada um mantém branch, HEAD, diff e checks próprios.

## Entrega entre repositórios

Use [cross-repo-change](../templates/cross-repo-change.md). Planeje ordem de implantação e estados intermediários: produtor antigo/novo com consumidor antigo/novo. Prefira adição compatível, migração gradual de consumidores e remoção posterior após evidência de desuso. Um merge em dois repositórios não é atômico.

Registre flags, compatibilidade de dados, versão de contratos, rollback e responsável por cada etapa. Testes de contrato e integração devem cobrir as versões que coexistirão. Atualize o mapa quando contratos ou dependências mudarem; valide novamente os commits utilizados ao retomar.
