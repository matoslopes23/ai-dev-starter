# Comece aqui

Use a mesma entrada para qualquer linguagem, paradigma ou arquitetura, em projeto novo, existente ou multi-repositório. Python 3.10+ executa os utilitários; não é requisito da aplicação. Os procedimentos podem ser lidos e aplicados manualmente sem executar os scripts.

## 1. Abra o projeto e use o prompt inicial

Copie o conteúdo de [prompts/inicial.md](prompts/inicial.md) para o agente. Preencha o objetivo e os caminhos que já conhece; os demais campos podem permanecer “a descobrir”. Ele identifica a rota, levanta evidências e registra o plano antes da implementação dependente.

Para começar diretamente no chat do agente:

```text
Leia COMECE_AQUI.md e aplique prompts/inicial.md deste kit.
Meu objetivo é: <descreva o que pretende construir ou melhorar>.
O projeto está em: <caminho local, URLs autorizadas ou a descobrir>.
Preserve a linguagem, a arquitetura e o trabalho existente.
```

Se estiver na raiz de um projeto que já recebeu o kit, use `.ai-kit/COMECE_AQUI.md` e `.ai-kit/prompts/inicial.md`. Se abrir o checkout central do kit, informe o destino da aplicação para o agente não confundir produto e ferramenta.

## 2. Instale no projeto local quando desejar

Execute do checkout central do kit, com uma pasta de destino já existente:

```sh
python3 scripts/adopt.py --target ../produto --name Produto --mode existing
python3 scripts/adopt.py --target ../produto --name Produto --mode existing --apply
```

O primeiro comando mostra o plano; o segundo grava. Use `--mode new` para começar uma aplicação, ou `--mode multi-repo` para uma pasta central de contexto. A instalação preserva instruções anteriores e não cria a aplicação nem modifica seu histórico Git.

## 3. Configure e confira

Agora, da raiz da aplicação, com o kit instalado:

```sh
# Mostra o que falta configurar; pode retornar exit code 2 enquanto houver lacunas.
python3 .ai-kit/scripts/doctor.py --target .

# Campos livres; substitua pelos fatos e decisões do seu projeto.
python3 .ai-kit/scripts/configure.py --target . --stack "Minha linguagem" --architecture "Meu estilo"
# Acrescente --apply ao mesmo comando para gravar, depois de revisar o plano.
```

Para comandos, componentes e restrições, siga [configuração](docs/20-configuracao.md). Use somente comandos reais descobertos no projeto ou confirmados na documentação da stack. O diagnóstico confere configuração; os testes do produto são uma etapa separada.

## 4. Siga a rota do seu objetivo

- [Projeto novo](docs/08-projeto-novo.md): descubra requisitos e implemente a primeira fatia autorizada.
- [Sistema existente](docs/09-sistema-existente.md): estabeleça baseline, mapa e plano incremental.
- [Vários repositórios](docs/10-multi-repositorio.md): trace jornadas e contratos entre os componentes.
- [AgendaLu](docs/16-agendalu.md): roteiro específico de adoção, sem presumir sua stack.

Os [perfis](docs/14-perfis.md) e a [neutralidade de stack](docs/19-neutralidade.md) explicam como adaptar os gates. Listas de exemplos ajudam a começar; elas não limitam quais linguagens e arquiteturas podem usar o kit.
