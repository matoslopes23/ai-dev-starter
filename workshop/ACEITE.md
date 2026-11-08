# Aceite manual da demonstração

Baseline: adicionar tarefa válida; título em branco deve ser rejeitado; marcar/desmarcar; repetir cliques; servidor indisponível mostra erro e reabilita botão; recarregar limpa estado conforme documentado. Título com `<script>` deve aparecer como texto, nunca executar.

Feature filtro:
1. Adicionar “Estudar” e “Praticar”. Concluir “Estudar”.
2. Ativar “Somente pendentes”: mostrar somente “Praticar”.
3. Desativar: mostrar ambas, preservando checkbox concluído.
4. Ativar e concluir “Praticar”: lista vazia, mensagem “Nenhuma tarefa pendente.”
5. Desativar e reabrir uma tarefa: estado e contador corretos.
6. Usar Tab/Espaço/Enter sem mouse; foco visível e nomes acessíveis.
7. Repetir alternância e adição com filtro ativo. Verificar em janela estreita.

Registre navegador, data, passou/falhou/não executado e evidência. Testes HTTP não comprovam estes passos visuais.
