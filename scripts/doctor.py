"""Diagnóstico local da configuração; não instala, não executa checks e não usa rede."""
import argparse
import json
from pathlib import Path
import shutil
import sys

if __package__:
    from .project_config import config_path, load, validate
    from .inventory import load_manifest
else:
    from project_config import config_path, load, validate
    from inventory import load_manifest


def diagnose(target):
    root, path = config_path(target)
    config = validate(load(path))
    results = []
    def report(name, passed, detail):
        results.append({"check": name, "status": "pass" if passed else "gap", "detail": detail})
    report("python", sys.version_info >= (3, 10), "Runtime das automações: " + sys.version.split()[0])
    report("git", shutil.which("git") is not None, "Disponibilidade local; nenhuma operação Git executada.")
    agents = root / "AGENTS.md"
    report("entrypoint", agents.is_file() and not agents.is_symlink(), "AGENTS.md na raiz do consumidor.")
    report("stack", bool(config.get("stack")), "Linguagens/runtimes livres, declarados pelo projeto.")
    report("architecture", bool(config.get("architecture", {}).get("style")), "Estilo identificado ou decidido; sem valor padrão imposto.")
    report("base_branch", bool(config.get("base_branch")), "Branch base declarada; existência remota não verificada.")
    report("git_workflow", config.get("git_workflow") != "undecided", "Política Git declarada; proteção remota não verificada.")
    components = config["components"]
    if config.get("kind") != "workspace":
        report("components", bool(components), "Mapa de componentes da aplicação.")
    for index, component in enumerate(components):
        candidate = (root / component["path"]).resolve()
        inside = candidate == root or root in candidate.parents
        report("component-" + str(index), inside and candidate.is_dir(), "Diretório deve existir dentro da raiz do consumidor.")
    report("checks", bool(config["checks"]), "Comandos declarados; não executados nem aprovados por este diagnóstico.")
    if config.get("kind") == "workspace":
        manifest = path.parent / "system.json"
        if manifest.is_symlink() or not manifest.is_file():
            report("repositories", False, "system.json deve existir sem symlink.")
        else:
            system = load_manifest(manifest)
            report("repositories", bool(system["repositories"]), "Inventário declarado; rode inventory.py para verificar disponibilidade.")
    return {"status": "ready-for-diagnosis" if all(r["status"] == "pass" for r in results) else "incomplete",
            "scope": "Configuração local; não comprova testes, segurança, arquitetura ou operação do produto.",
            "checks": results, "commands_executed": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", required=True)
    args = parser.parse_args()
    try:
        result = diagnose(args.target)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if result["status"] == "ready-for-diagnosis" else 2
    except (ValueError, OSError) as error:
        print("Diagnóstico inválido: " + type(error).__name__, file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
