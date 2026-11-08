"""Plano/update/restore de arquivos gerenciados, sem rede ou execução da origem."""
from contextlib import contextmanager
import argparse
import json
import os
from pathlib import Path
import re
import sys
import uuid

if __package__:
    from .installation import (LEGACY_README, atomic_write, build_payload, digest,
                               managed_path, read_optional, require, safe_path)
else:
    from installation import (LEGACY_README, atomic_write, build_payload, digest,
                              managed_path, read_optional, require, safe_path)


def encode(data):
    return (json.dumps(data, ensure_ascii=False, indent=2) + "\n").encode()


def root_path(target):
    target = Path(target).expanduser().absolute()
    require(target.is_dir() and not target.is_symlink(), "Destino deve ser diretório existente sem symlink.")
    root = target.resolve()
    require(safe_path(root, ".ai-kit").is_dir(), "Instalação ausente.")
    return root


def load_origin(root):
    raw = read_optional(safe_path(root, ".ai-kit/origin.json"))
    require(raw is not None, "Manifesto de origem ausente.")
    origin = json.loads(raw)
    require(isinstance(origin, dict), "Manifesto de origem inválido.")
    if origin.get("format_version") == 2:
        base = origin.get("managed")
    else:
        require(origin.get("format_version") in {None, 1}, "Formato de origem desconhecido.")
        legacy = origin.get("sha256")
        require(isinstance(legacy, dict), "Sem hashes-base; migração manual necessária.")
        base = {".ai-kit/" + key: value for key, value in legacy.items()}
        # 2.1 gerava README mas não o incluía nos hashes. Reconhecer somente os bytes conhecidos.
        readme = read_optional(safe_path(root, ".ai-kit/README.md"))
        if readme == LEGACY_README:
            base[".ai-kit/README.md"] = digest(readme)
    require(isinstance(base, dict) and base, "Manifesto sem arquivos gerenciados.")
    for key, value in base.items():
        managed_path(root, key)
        require(isinstance(value, str) and re.fullmatch(r"[a-f0-9]{64}", value), "Hash-base inválido.")
    return raw, origin, base


def prepare(target, source, adapters=None):
    root = root_path(target)
    raw, previous, base = load_origin(root)
    chosen = previous.get("adapters", []) if adapters is None else adapters
    payload, origin = build_payload(source, chosen)
    rows, before, after = [], {}, {}
    for key in sorted(set(base) | set(payload)):
        local = read_optional(managed_path(root, key))
        old_hash, local_hash, new_hash = base.get(key), digest(local), digest(payload.get(key))
        if local_hash == new_hash:
            action = "unchanged"
        elif local_hash == old_hash:
            action = "write" if new_hash is not None else "delete"
        elif new_hash == old_hash:
            action = "keep-local"
        else:
            action = "conflict"
        rows.append({"path": key, "action": action})
        if action in {"write", "delete"}:
            before[key], after[key] = local, payload.get(key)
    plan = {"applied": False, "from_version": previous.get("kit_version"), "to_version": origin["kit_version"],
            "adapters": chosen, "files": rows, "conflicts": [r["path"] for r in rows if r["action"] == "conflict"],
            "preserved_local": [r["path"] for r in rows if r["action"] == "keep-local"]}
    # Não renovar a origem quando a árvore e os adaptadores são idênticos.
    same = (previous.get("format_version") == 2 and previous.get("managed") == origin["managed"]
            and previous.get("adapters", []) == origin["adapters"] and previous.get("kit_version") == origin["kit_version"])
    metadata = raw if same else encode(origin)
    return root, raw, metadata, before, after, plan


@contextmanager
def lock(root):
    path = safe_path(root, ".ai-kit/.update.lock")
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    os.close(fd)
    try:
        yield
    finally:
        path.unlink(missing_ok=True)


def apply_files(root, expected_origin, origin_content, before, after):
    origin_path = safe_path(root, ".ai-kit/origin.json")
    require(read_optional(origin_path) == expected_origin, "Origem mudou durante o planejamento.")
    for key, value in before.items():
        require(read_optional(managed_path(root, key)) == value, "Arquivo mudou durante o planejamento.")
    written = []
    try:
        for key, value in after.items():
            written.append(key)
            atomic_write(managed_path(root, key), value)
        atomic_write(origin_path, origin_content)
    except Exception:
        for key in reversed(written):
            atomic_write(managed_path(root, key), before[key])
        # Atomicidade do origin: se não trocou, manter; se trocou, restaurar.
        if read_optional(origin_path) != expected_origin:
            atomic_write(origin_path, expected_origin)
        raise


def backup(root, previous_origin, new_origin, before, after):
    backup_id = uuid.uuid4().hex
    folder = safe_path(root, ".ai/kit-backups/" + backup_id)
    folder.mkdir(parents=True, exist_ok=False)
    for key, value in before.items():
        if value is not None:
            atomic_write(safe_path(folder, "before/" + key), value)
    atomic_write(folder / "origin.before.json", previous_origin)
    manifest = {"format_version": 1, "status": "prepared", "before": {k: digest(v) for k, v in before.items()},
                "after": {k: digest(v) for k, v in after.items()},
                "origin_before": digest(previous_origin), "origin_after": digest(new_origin)}
    atomic_write(folder / "manifest.json", encode(manifest))
    return backup_id, folder, manifest


def update(target, source, apply=False, adapters=None):
    root, raw, metadata, before, after, plan = prepare(target, source, adapters)
    if not apply or plan["conflicts"]:
        return plan
    if not after and metadata == raw:
        return plan
    with lock(root):
        # Conferir hashes novamente depois de adquirir o lock.
        current = prepare(target, source, adapters)
        require(current[1:5] == (raw, metadata, before, after), "Plano mudou; gere novamente.")
        backup_id, folder, manifest = backup(root, raw, metadata, before, after)
        try:
            apply_files(root, raw, metadata, before, after)
        except Exception:
            manifest["status"] = "rolled-back"
            atomic_write(folder / "manifest.json", encode(manifest))
            raise
        manifest["status"] = "completed"
        atomic_write(folder / "manifest.json", encode(manifest))
        plan.update(applied=True, backup_id=backup_id)
    return plan


def restore(target, backup_id, apply=False):
    root = root_path(target)
    require(bool(re.fullmatch(r"[a-f0-9]{32}", backup_id)), "ID de backup inválido.")
    folder = safe_path(root, ".ai/kit-backups/" + backup_id)
    manifest_path = safe_path(folder, "manifest.json")
    manifest = json.loads(manifest_path.read_bytes())
    require(manifest.get("format_version") == 1 and manifest.get("status") in {"completed", "prepared"}, "Backup não restaurável.")
    require(isinstance(manifest.get("before"), dict) and isinstance(manifest.get("after"), dict)
            and manifest["before"].keys() == manifest["after"].keys(), "Manifesto de backup inválido.")
    previous_origin = safe_path(folder, "origin.before.json").read_bytes()
    require(digest(previous_origin) == manifest["origin_before"], "Backup de origem corrompido.")
    current_origin = read_optional(safe_path(root, ".ai-kit/origin.json"))
    require(digest(current_origin) == manifest["origin_after"], "Instalação mudou após o update; restauração recusada.")
    before, after = {}, {}
    for key, value in manifest["before"].items():
        current = read_optional(managed_path(root, key))
        require(digest(current) == manifest["after"][key], "Arquivo mudou após update; restauração recusada.")
        saved = safe_path(folder, "before/" + key).read_bytes() if value is not None else None
        require(digest(saved) == value, "Backup de arquivo corrompido.")
        before[key], after[key] = current, saved
    result = {"applied": False, "backup_id": backup_id, "restore_files": sorted(after)}
    if apply:
        with lock(root):
            apply_files(root, current_origin, previous_origin, before, after)
            manifest["status"] = "restored"
            atomic_write(manifest_path, encode(manifest))
        result["applied"] = True
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", required=True)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--source", help="Checkout/snapshot local revisado; nenhum download é feito.")
    mode.add_argument("--restore", metavar="BACKUP_ID")
    parser.add_argument("--adapter", action="append", choices=("codex", "claude", "copilot", "cursor"))
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    try:
        require(not (args.restore and args.adapter), "Restore não altera seleção de adaptadores.")
        result = restore(args.target, args.restore, args.apply) if args.restore else update(args.target, args.source, args.apply, args.adapter)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 2 if result.get("conflicts") else 0
    except (OSError, ValueError, KeyError, TypeError) as error:
        print("Operação não concluída: " + (str(error) if isinstance(error, ValueError) and not isinstance(error, json.JSONDecodeError)
                                           else type(error).__name__), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
