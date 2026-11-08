"""Payload e arquivos gerenciados: dados locais, sem execução do código de origem."""
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import subprocess
import tempfile

ADAPTERS = {"codex": ".agents/skills", "copilot": ".agents/skills",
            "cursor": ".agents/skills", "claude": ".claude/skills"}
SCRIPTS = ("configure.py", "doctor.py", "inventory.py", "project_config.py", "installation.py", "update.py")
EXCLUDED_CONFIG = {".ai-kit/project.json", ".ai-kit/system.json", ".ai-kit/origin.json"}
LEGACY_README = (
    "# Playbook instalado\n\nLeia [AGENTS.md](AGENTS.md), [a configuração](project.json) "
    "e [o roteador](ia-context/CONTEXT_ROUTER.md).\n\n"
    "Primeiro uso: [comece aqui](COMECE_AQUI.md). "
    "[Configuração e diagnóstico](docs/20-configuracao.md) usam scripts incluídos.\n\n"
    "Para configurar, veja [adaptação](docs/01-adaptacao.md); "
    "para atualizar, [portabilidade](docs/17-portabilidade.md).\n"
    "Gates vazios são não configurados. Código e .ai/ ficam na raiz da aplicação.\n"
).encode()
INSTALLED_README = (
    "# Playbook instalado\n\nComece em [COMECE_AQUI.md](COMECE_AQUI.md), "
    "leia [AGENTS.md](AGENTS.md) e [project.json](project.json).\n\n"
    "[Configuração](docs/20-configuracao.md), [integrações](docs/21-integracoes.md) "
    "e [atualização com recuperação](docs/22-atualizacao.md).\n"
    "Código e estado local ficam na raiz da aplicação. Checks vazios não são aprovação.\n"
).encode()


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(content):
    return hashlib.sha256(content).hexdigest() if content is not None else None


def safe_path(root, relative):
    require(isinstance(relative, str) and relative and "\\" not in relative and "\x00" not in relative,
            "Caminho gerenciado inválido.")
    parts = relative.split("/")
    require(not relative.startswith("/") and all(p not in {"", ".", ".."} and ":" not in p for p in parts),
            "Caminho fora da fronteira permitida.")
    path = Path(root)
    for part in parts:
        path /= part
        require(not path.is_symlink(), "Symlink em caminho gerenciado.")
    return path


def managed_path(root, relative):
    require(relative not in EXCLUDED_CONFIG, "Configuração local não pode ser gerenciada pelo update.")
    allowed = (relative.startswith(".ai-kit/") or
               re.fullmatch(r"\.(?:agents|claude)/skills/ai-kit-[a-z0-9-]+/SKILL\.md", relative))
    require(bool(allowed), "Arquivo fora do escopo do kit.")
    name = PurePosixPath(relative).name
    require(not name.startswith(".env") and PurePosixPath(name).suffix not in {".pem", ".key", ".p12", ".pfx"},
            "Arquivo sensível não pode ser gerenciado.")
    return safe_path(root, relative)


def read_optional(path):
    require(not path.is_symlink(), "Symlink não permitido.")
    require(not path.exists() or path.is_file(), "Colisão com diretório.")
    return path.read_bytes() if path.exists() else None


def atomic_write(path, content):
    require(not path.is_symlink(), "Symlink não permitido.")
    path.parent.mkdir(parents=True, exist_ok=True)
    if content is None:
        path.unlink(missing_ok=True)
        return
    mode = stat.S_IMODE(path.stat().st_mode) if path.exists() else 0o644
    temp = None
    try:
        with tempfile.NamedTemporaryFile(dir=path.parent, prefix=".kit-", delete=False) as stream:
            temp = Path(stream.name)
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        os.chmod(temp, mode)
        os.replace(temp, path)
        temp = None
    finally:
        if temp is not None:
            temp.unlink(missing_ok=True)


def git_value(source, args):
    try:
        result = subprocess.run(["git", "--no-optional-locks", "-c", "core.fsmonitor=false", "-C", str(source), *args],
                                capture_output=True, text=True, timeout=10, check=False)
        return result.stdout.strip() if result.returncode == 0 else None
    except (OSError, subprocess.TimeoutExpired):
        return None


def source_files(source):
    source = Path(source).resolve()
    names = ["AGENTS.md", "LICENSE", "COMECE_AQUI.md", "kit-version.json"]
    for name in ("CHANGELOG.md", "CONTRIBUTING.md", "SECURITY.md"):
        if (source / name).is_file():
            names.append(name)
    names += ["scripts/" + name for name in SCRIPTS]
    for directory in ("docs", "skills", "templates", "prompts", "ia-context"):
        folder = safe_path(source, directory)
        require(folder.is_dir(), "Diretório obrigatório ausente na origem.")
        # Não seguir diretórios symlink nem copiar extensões fora do contrato.
        for current, dirs, files in os.walk(folder, followlinks=False):
            require(not any((Path(current) / d).is_symlink() for d in dirs), "Symlink na origem.")
            for name in sorted(files):
                path = Path(current) / name
                if path.suffix in {".md", ".json", ".csv"}:
                    names.append(path.relative_to(source).as_posix())
    return [safe_path(source, name) for name in sorted(names)]


def build_payload(source, adapters=()):
    source = Path(source).expanduser().resolve()
    adapters = sorted(set(adapters))
    require(all(a in ADAPTERS for a in adapters), "Adaptador desconhecido.")
    version = json.loads(safe_path(source, "kit-version.json").read_text(encoding="utf-8"))["version"]
    require(isinstance(version, str) and re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+", version), "Versão inválida.")
    payload = {".ai-kit/" + p.relative_to(source).as_posix(): p.read_bytes() for p in source_files(source)}
    payload[".ai-kit/README.md"] = INSTALLED_README
    payload[".ai-kit/.gitattributes"] = b"* text eol=lf\n"
    for native_root in sorted({ADAPTERS[a] for a in adapters}):
        for path in sorted((source / "skills").glob("*/SKILL.md")):
            text = path.read_text(encoding="utf-8")
            name = re.search(r"^name: ([a-z0-9-]+)$", text, re.M)
            description = re.search(r"^description: (.+)$", text, re.M)
            require(name is not None and description is not None and name[1] == path.parent.name, "Skill sem metadados válidos.")
            require(len("ai-kit-" + name[1]) <= 64, "Nome de skill excede o limite do adaptador.")
            canonical = f"../../../.ai-kit/skills/{name[1]}/SKILL.md"
            wrapper = (f"---\nname: ai-kit-{name[1]}\ndescription: {json.dumps(description[1], ensure_ascii=False)}\n---\n\n"
                       "Leia o contrato na raiz da aplicação e `.ai-kit/AGENTS.md`. "
                       f"Aplique [o procedimento canônico]({canonical}) ao escopo autorizado. "
                       "Abra esse arquivo antes de agir; este adaptador não amplia permissões.\n")
            payload[f"{native_root}/ai-kit-{name[1]}/SKILL.md"] = wrapper.encode()
    status = git_value(source, ["status", "--porcelain"])
    origin = {"format_version": 2, "kit_version": version, "adapters": adapters,
              "source_commit": git_value(source, ["rev-parse", "HEAD"]),
              "source_dirty": bool(status) if status is not None else None,
              "managed": {key: digest(value) for key, value in sorted(payload.items())},
              "sha256": {key.removeprefix(".ai-kit/"): digest(value) for key, value in sorted(payload.items())
                         if key.startswith(".ai-kit/")}}
    return payload, origin
