"""Regras puras: nenhuma dependência de HTTP ou armazenamento."""
from uuid import uuid4


def create_task(title):
    if not isinstance(title, str):
        raise ValueError("Informe um título em texto.")
    title = title.strip()
    if not title or len(title) > 80:
        raise ValueError("O título deve ter de 1 a 80 caracteres.")
    return {"id": str(uuid4()), "title": title, "done": False}
