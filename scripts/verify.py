"""Gate do kit: integridade, sintaxe, scanner heurístico e testes locais."""
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import unquote

if __package__:
    from .project_config import validate
else:
    from project_config import validate

ROOT = Path(__file__).resolve().parents[1]
EXCLUDED = {".git", ".ai", ".ai-kit", "__pycache__", ".venv", "venv", "node_modules",
            "vendor", "dist", "build", "target", ".tox", ".pytest_cache", ".mypy_cache",
            ".ruff_cache", "coverage", ".next"}
TEXT_SUFFIXES = {".md", ".py", ".json", ".yml", ".yaml", ".toml", ".ini", ".txt",
                 ".html", ".css", ".js", ".ts", ".tsx", ".jsx", ".xml", ".sh", ".csv", ".patch"}
TEXT_NAMES = {"LICENSE", ".gitignore", ".gitattributes", ".editorconfig", ".env.example", ".python-version"}
PATTERNS = [r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----",
            r"gh[pousr]_[A-Za-z0-9]{30,}", r"AKIA[0-9A-Z]{16}"]


def check(condition, message):
    if not condition:
        raise ValueError(message)


def iter_files(root):
    for directory, dirs, filenames in os.walk(root, followlinks=False):
        dirs[:] = sorted(d for d in dirs if d not in EXCLUDED and not (Path(directory) / d).is_symlink())
        for name in sorted(filenames):
            path = Path(directory) / name
            if not path.is_symlink() and name != ".DS_Store":
                yield path


def sensitive_name(path):
    return ((path.name == ".env" or path.name.startswith(".env.")) and path.name != ".env.example"
            or path.suffix.lower() in {".pem", ".p12", ".pfx", ".key", ".jks"})


def local_links(path, text):
    # Links inline explícitos; não interpreta HTML, anchors ou links por referência.
    # Remover blocos fenced evita tratar exemplos de sintaxe como navegação.
    clean = re.sub(r"^```.*?^```[^\n]*$", "", text, flags=re.M | re.S)
    for target in re.findall(r"\]\(([^\s)]+)\)", clean):
        if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", target) or target.startswith("#"):
            continue
        target = unquote(target.split("#", 1)[0])
        if target:
            check((path.parent / target).exists(), "Link local ausente em " + str(path) + ": " + target)


def validate_skills(root):
    skills = sorted((root / "skills").glob("*/SKILL.md"))
    check(bool(skills), "Catálogo de skills vazio")
    for path in skills:
        text = path.read_text(encoding="utf-8")
        header = re.match(r"\A---\n(.*?)\n---\n", text, re.S)
        check(header is not None, "Frontmatter ausente: " + str(path))
        fields = dict(re.findall(r"^(name|description): (.+)$", header.group(1), re.M))
        check(fields.get("name") == path.parent.name and re.fullmatch(r"[a-z0-9-]{1,63}", path.parent.name),
              "Nome de skill inválido: " + str(path))
        check(bool(fields.get("description", "").strip()), "Descrição ausente: " + str(path))
    return len(skills)


def inspect_tree(root):
    required = ["AGENTS.md", "README.md", "project.json", "kit-version.json", "ia-context/CONTEXT_ROUTER.md",
                "templates/task.md", "templates/handoff.md", "templates/system.example.json", "LICENSE"]
    for name in required:
        check((root / name).is_file(), "Arquivo ausente: " + name)
    config = json.loads((root / "project.json").read_text(encoding="utf-8"))
    validate(config)
    scanned = skipped = 0
    for path in iter_files(root):
        # Detectar por nome antes de ler evita abrir arquivos de credenciais conhecidos.
        check(not sensitive_name(path), "Arquivo sensível não permitido: " + str(path.relative_to(root)))
        if path.stat().st_size > 2 * 1024 * 1024 or (path.suffix not in TEXT_SUFFIXES and path.name not in TEXT_NAMES):
            skipped += 1
            continue
        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            check(path.suffix not in {".py", ".md", ".json", ".yml", ".yaml"}, "Texto inválido: " + str(path))
            skipped += 1
            continue
        check(not any(re.search(pattern, content) for pattern in PATTERNS),
              "Possível segredo: " + str(path.relative_to(root)))
        if path.suffix == ".py":
            compile(content, str(path), "exec")
        if path.suffix == ".json":
            json.loads(content)
        if path.suffix == ".md":
            local_links(path, content)
        scanned += 1
    return {"text_files": scanned, "skipped_files": skipped, "skills": validate_skills(root)}


def main():
    try:
        result = inspect_tree(ROOT)
        print("Integridade e scanner heurístico: " + json.dumps(result) +
              ". Binários, arquivos grandes, symlinks e diretórios excluídos não são auditados.", flush=True)
    except (OSError, ValueError, SyntaxError) as error:
        # Não reproduzir trechos de conteúdo que poderiam conter um segredo.
        print("FALHOU: " + (str(error) if not isinstance(error, (SyntaxError, json.JSONDecodeError))
                            else type(error).__name__), file=sys.stderr)
        return 1
    for directory in ("tests", "examples/taskboard"):
        result = subprocess.run([sys.executable, "-B", "-m", "unittest", "discover", "-s",
                                 str(ROOT / directory), "-p", "test_*.py", "-v"], cwd=ROOT)
        if result.returncode:
            return result.returncode
    print("PASSOU: gates do kit e demo. Não comprova UI manual, CI remota ou aplicação consumidora.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
