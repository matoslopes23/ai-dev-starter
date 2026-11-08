# Continuidade sem recomeçar do zero

O estado ativo fica em `.ai/current-task.md` (ignorado pelo Git); o template público fica em `templates/task.md`. Cada checkpoint registra fatos, hipóteses, arquivos, validações e uma próxima ação. Não guarde segredos ou transcrições.

Antes de transferir: termine a edição atual, registre branch/HEAD e mudanças não commitadas, a última validação e seus limites. Use `templates/handoff.md`. Ao retomar, confira o checkout e reconcilie divergências; não confie cegamente no estado antigo.

Trocar de máquina não transfere código. Use branch ou patch revisado quando autorizado e confirme aplicação. Não faça commit/push só porque precisa encerrar a sessão.

Em paralelo: atribua arquivos distintos, saída esperada, dependências e responsável por integrar. Se dois agentes precisam do mesmo arquivo, serialize. Revisor deve procurar defeitos concretos, não aumentar escopo.
