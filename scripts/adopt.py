"""Instala um snapshot local do playbook; sem rede, Git mutável ou dependências."""
import argparse
import json
from pathlib import Path
import shutil
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
if __package__:
    from .installation import build_payload, source_files as kit_files, safe_path, read_optional
else:
    from installation import build_payload, source_files as kit_files, safe_path, read_optional

KIT_VERSION = json.loads((ROOT / "kit-version.json").read_text(encoding="utf-8"))["version"]
BLOCK = """<!-- ai-engineering-kit:start -->
## Engenharia de software com IA

Leia `.ai-kit/AGENTS.md`, `.ai-kit/project.json` e
`.ai-kit/ia-context/CONTEXT_ROUTER.md` antes de executar trabalho neste projeto.
Caminhos do playbook partem de `.ai-kit/`; componentes e `.ai/` partem desta raiz.
Preserve instruções específicas existentes; registre conflitos na fronteira afetada.
O kit não concede autorização para ações externas nem substitui gates do projeto.
<!-- ai-engineering-kit:end -->
"""


def source_files():
    return kit_files(ROOT)


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


def install(target, name, mode, workflow, apply=False, adapters=()):
    target, originals, additions = plan_install(target, name, mode, workflow)
    payload, origin = build_payload(ROOT, adapters)
    adapter_files = {key: value for key, value in payload.items() if not key.startswith(".ai-kit/")}
    for relative in adapter_files:
        if read_optional(safe_path(target, relative)) is not None:
            raise ValueError("Adaptador já existe; instalação não pode sobrescrevê-lo.")
    planned = [key for key in payload if key.startswith(".ai-kit/")]
    planned += [".ai-kit/project.json", ".ai-kit/system.json",
                ".ai-kit/origin.json", "AGENTS.md (acrescentar)", ".gitignore (acrescentar)"]
    planned += list(adapter_files)
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
    # Stage fora do destino; só publicar após todos os arquivos estarem prontos.
    with tempfile.TemporaryDirectory(prefix="ai-kit-stage-") as tmp:
        staged = Path(tmp) / "bundle"
        staged.mkdir()
        for relative, content in payload.items():
            if not relative.startswith(".ai-kit/"):
                continue
            output = staged / relative.removeprefix(".ai-kit/")
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_bytes(content)
        for filename, data in (("project.json", config), ("system.json", system), ("origin.json", origin)):
            (staged / filename).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        (staged / "README.md").write_bytes(payload[".ai-kit/README.md"])
        # Reconfira o snapshot imediatamente antes de gravar. Uso concorrente não é suportado.
        _, current, _ = plan_install(target, name, mode, workflow)
        if current != originals:
            raise ValueError("Arquivos do destino mudaram durante o planejamento.")
        bundle = target / ".ai-kit"
        bundle.mkdir()  # Falha se outro instalador publicou no mesmo destino.
        written = []
        try:
            shutil.copytree(staged, bundle, dirs_exist_ok=True)
            for filename, data in {**additions, **adapter_files}.items():
                path = safe_path(target, filename)
                if filename in adapter_files and path.exists():
                    raise ValueError("Adaptador mudou durante a preparação.")
                path.parent.mkdir(parents=True, exist_ok=True)
                written.append(filename)
                path.write_bytes(data)
        except Exception:
            for filename in reversed(written):
                old = originals.get(filename)
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
    parser.add_argument("--adapter", action="append", choices=("codex", "claude", "copilot", "cursor"), default=[])
    parser.add_argument("--apply", action="store_true", help="Gravar o plano local; sem esta opção apenas inspeciona.")
    args = parser.parse_args()
    try:
        print(json.dumps(install(args.target, args.name, args.mode, args.git_workflow, args.apply, args.adapter),
                         ensure_ascii=False, indent=2))
    except (OSError, ValueError) as error:
        print("Não instalado: " + str(error), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
