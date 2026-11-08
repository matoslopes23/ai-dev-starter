"""Planeja ou grava configuração do kit; nunca executa comandos da aplicação."""
import argparse
from copy import deepcopy
import json
import os
from pathlib import Path
import stat
import sys
import tempfile

if __package__:
    from .project_config import FIELDS, WORKFLOWS, config_path, load, require, validate
else:
    from project_config import FIELDS, WORKFLOWS, config_path, load, require, validate


def configure(target, changes, apply=False):
    _, path = config_path(target)
    require(isinstance(changes, dict) and set(changes) <= FIELDS, "Patch contém campos não configuráveis.")
    original = path.read_bytes()
    config = load(path)
    updated = deepcopy(config)
    updated.update(deepcopy(changes))
    validate(updated)
    changed = sorted(key for key in changes if updated.get(key) != config.get(key))
    result = {"applied": False, "changed_fields": changed,
              "commands_executed": False, "status": "planned" if changed else "unchanged"}
    if not apply or not changed:
        return result
    content = (json.dumps(updated, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(dir=path.parent, prefix=".project-", suffix=".tmp", delete=False) as stream:
            temporary = Path(stream.name)
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        os.chmod(temporary, stat.S_IMODE(path.stat().st_mode))
        # Não substituir uma edição ocorrida durante a preparação.
        require(not path.is_symlink() and path.read_bytes() == original, "Configuração mudou durante o planejamento.")
        os.replace(temporary, path)
        temporary = None
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)
    result.update(applied=True, status="configured")
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", required=True, help="Raiz da aplicação ou workspace.")
    parser.add_argument("--config", help="Patch JSON com campos documentados; sem segredos.")
    parser.add_argument("--stack", action="append", help="Texto livre; repetir substitui a lista stack.")
    parser.add_argument("--architecture", help="Estilo livre; não altera a arquitetura do código.")
    parser.add_argument("--check", action="append", default=[], metavar="NOME=COMANDO")
    parser.add_argument("--base-branch")
    parser.add_argument("--git-workflow", choices=sorted(WORKFLOWS))
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    try:
        changes = {}
        if args.config:
            patch_path = Path(args.config)
            require(patch_path.suffix == ".json" and not patch_path.is_symlink(), "Patch deve ser arquivo .json sem symlink.")
            changes.update(load(patch_path))
        if args.stack is not None:
            changes["stack"] = args.stack
        for flag, key in ((args.base_branch, "base_branch"), (args.git_workflow, "git_workflow")):
            if flag is not None:
                changes[key] = flag
        # Flags complementam o patch sem eliminar outros contratos de arquitetura/checks.
        if args.architecture is not None or args.check:
            _, path = config_path(args.target)
            current = load(path)
            if args.architecture is not None:
                arch = deepcopy(changes.get("architecture", current.get("architecture", {})))
                require(isinstance(arch, dict), "architecture deve ser objeto.")
                arch["style"] = args.architecture
                changes["architecture"] = arch
            if args.check:
                checks = deepcopy(changes.get("checks", current.get("checks", {})))
                require(isinstance(checks, dict), "checks deve ser objeto.")
                for entry in args.check:
                    name, separator, command = entry.partition("=")
                    require(bool(separator and name.strip() and command.strip()), "Use --check NOME=COMANDO.")
                    checks[name.strip()] = command
                changes["checks"] = checks
        print(json.dumps(configure(args.target, changes, args.apply), ensure_ascii=False, indent=2))
        return 0
    except (OSError, ValueError) as error:
        print("Configuração não gravada: " + (str(error) if isinstance(error, ValueError) else type(error).__name__), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
