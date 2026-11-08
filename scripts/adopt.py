"""Instala um snapshot local do playbook; sem rede, Git mutável ou dependências."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
KIT_VERSION = "2.1.0"
BLOCK = """<!-- ai-engineering-kit:start -->
## Engenharia de software com IA

Leia `.ai-kit/AGENTS.md`, `.ai-kit/project.json` e
`.ai-kit/ia-context/CONTEXT_ROUTER.md` antes de executar trabalho neste projeto.
Caminhos do playbook partem de `.ai-kit/`; componentes e `.ai/` partem desta raiz.
Preserve instruções específicas existentes; registre conflitos na fronteira afetada.
O kit não concede autorização para ações externas nem substitui gates do projeto.
<!-- ai-engineering-kit:end -->
"""


def git_value(args):
    try:
        result = subprocess.run(["git", "--no-optional-locks", "-c", "core.fsmonitor=false",
                                 "-C", str(ROOT), *args], capture_output=True,
                                text=True, timeout=10, check=False)
        return result.stdout.strip() if result.returncode == 0 else None
    except (OSError, subprocess.TimeoutExpired):
        return None


def source_files():
    paths = [ROOT / "AGENTS.md", ROOT / "LICENSE", ROOT / "COMECE_AQUI.md"]
    paths.extend(ROOT / "scripts" / name for name in
                 ("configure.py", "doctor.py", "inventory.py", "project_config.py"))
    for directory in ("docs", "skills", "templates", "prompts", "ia-context"):
        paths.extend(p for p in sorted((ROOT / directory).rglob("*"))
                     if p.suffix in {".md", ".json", ".csv"} and p.is_file())
    for path in paths:
        if path.is_symlink() or any((ROOT / parent).is_symlink()
                                    for parent in path.relative_to(ROOT).parents):
            raise ValueError("Fonte do kit não pode conter symlink.")
    return paths


def appended(original, addition):
    return original + (b"\n" if original and not original.endswith(b"\n") else b"") + addition


def plan_install(target, name, mode, workflow):
    if not name.strip() or any(ord(c) < 32 for c in name):
        raise ValueError("Nome vazio ou com caracteres de controle.")
    if mode not in {"new", "existing", "multi-repo"}:
        raise ValueError("Modo inválido.")
    if workflow not in {"undecided", "github-flow", "trunk-based", "gitflow"}:
        raise ValueError("Política Git inválida.")
    target = Path(target).expanduser().absolute()
    if target.is_symlink() or not target.is_dir():
        raise ValueError("Destino deve ser um diretório existente, sem symlink.")
    target = target.resolve()
    if target == ROOT or ROOT in target.parents:
        raise ValueError("Instale em uma pasta separada do checkout do kit.")
    bundle = target / ".ai-kit"
    if bundle.exists() or bundle.is_symlink():
        raise ValueError(".ai-kit já existe; use o fluxo de atualização revisada.")
    originals = {}
    for name_on_disk in ("AGENTS.md", ".gitignore"):
        path = target / name_on_disk
        if path.is_symlink() or (path.exists() and not path.is_file()):
            raise ValueError("Colisão ou symlink em " + name_on_disk)
        originals[name_on_disk] = path.read_bytes() if path.exists() else None
    original_agents = originals["AGENTS.md"] or b""
    if b"ai-engineering-kit:" in original_agents:
        raise ValueError("AGENTS.md já contém marcador de instalação; revise manualmente.")
    ignored = originals[".gitignore"] or b""
    # Bloco final prevalece inclusive se uma regra anterior designorava .ai/.
    additions = {
        "AGENTS.md": appended(original_agents, BLOCK.encode("utf-8")),
        ".gitignore": appended(ignored, b"\n# Estado local do kit de engenharia\n/.ai/\n"),
    }
    return target, originals, additions


def install(target, name, mode, workflow, apply=False):
    target, originals, additions = plan_install(target, name, mode, workflow)
    sources = source_files()
    planned = [".ai-kit/" + str(p.relative_to(ROOT)) for p in sources]
    planned += [".ai-kit/README.md", ".ai-kit/project.json", ".ai-kit/system.json",
                ".ai-kit/origin.json", "AGENTS.md (acrescentar)", ".gitignore (acrescentar)"]
    if not apply:
        return {"applied": False, "files": planned}
    config = {
        "schema_version": 1, "name": name.strip(),
        "purpose": "Definir a partir do diagnóstico ou descoberta do produto",
        "kind": "workspace" if mode == "multi-repo" else "application",
        "adoption_mode": mode, "stack": [], "base_branch": None,
        "architecture": {"style": None, "boundaries": [], "constraints": []}, "profiles": [],
        "git_workflow": workflow, "components": [], "checks": {},
        "production": None,
        "risks": ["Contexto e gates ainda não configurados; não representam aprovação"],
    }
    system = {"schema_version": 1, "name": name.strip(), "repositories": [],
              "journeys": [], "external_systems": [],
              "coverage": {"status": "not-started", "missing_repositories": []}}
    status = git_value(["status", "--porcelain"])
    origin = {"kit_version": KIT_VERSION, "source_commit": git_value(["rev-parse", "HEAD"]),
              "source_dirty": bool(status) if status is not None else None,
              "sha256": {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                         for p in sources}}
    # Stage fora do destino; só publicar após todos os arquivos estarem prontos.
    with tempfile.TemporaryDirectory(prefix="ai-kit-stage-") as tmp:
        staged = Path(tmp) / "bundle"
        staged.mkdir()
        for source in sources:
            output = staged / source.relative_to(ROOT)
            output.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, output)
        for filename, data in (("project.json", config), ("system.json", system), ("origin.json", origin)):
            (staged / filename).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        (staged / "README.md").write_text(
            "# Playbook instalado\n\nLeia [AGENTS.md](AGENTS.md), [a configuração](project.json) "
            "e [o roteador](ia-context/CONTEXT_ROUTER.md).\n\n"
            "Primeiro uso: [comece aqui](COMECE_AQUI.md). "
            "[Configuração e diagnóstico](docs/20-configuracao.md) usam scripts incluídos.\n\n"
            "Para configurar, veja [adaptação](docs/01-adaptacao.md); "
            "para atualizar, [portabilidade](docs/17-portabilidade.md).\n"
            "Gates vazios são não configurados. Código e .ai/ ficam na raiz da aplicação.\n",
            encoding="utf-8")
        # Reconfira o snapshot imediatamente antes de gravar. Uso concorrente não é suportado.
        _, current, _ = plan_install(target, name, mode, workflow)
        if current != originals:
            raise ValueError("Arquivos do destino mudaram durante o planejamento.")
        bundle = target / ".ai-kit"
        bundle.mkdir()  # Falha se outro instalador publicou no mesmo destino.
        written = []
        try:
            shutil.copytree(staged, bundle, dirs_exist_ok=True)
            for filename, data in additions.items():
                written.append(filename)
                (target / filename).write_bytes(data)
        except Exception:
            for filename in reversed(written):
                old = originals[filename]
                if old is None:
                    (target / filename).unlink(missing_ok=True)
                else:
                    (target / filename).write_bytes(old)
            shutil.rmtree(bundle)
            raise
    return {"applied": True, "files": planned}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", required=True)
    parser.add_argument("--name", required=True)
    parser.add_argument("--mode", choices=("new", "existing", "multi-repo"), default="existing")
    parser.add_argument("--git-workflow", choices=("undecided", "github-flow", "trunk-based", "gitflow"), default="undecided")
    parser.add_argument("--apply", action="store_true", help="Gravar o plano local; sem esta opção apenas inspeciona.")
    args = parser.parse_args()
    try:
        print(json.dumps(install(args.target, args.name, args.mode, args.git_workflow, args.apply),
                         ensure_ascii=False, indent=2))
    except (OSError, ValueError) as error:
        print("Não instalado: " + str(error), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
