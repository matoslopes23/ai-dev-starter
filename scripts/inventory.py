"""Inventário explícito e somente leitura; não clona nem busca remotos."""
import argparse
import json
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import urlsplit

MANIFESTS = ("package.json", "pyproject.toml", "requirements.txt", "go.mod", "Cargo.toml",
             "pom.xml", "build.gradle", "build.gradle.kts", "composer.json", "Gemfile",
             "pubspec.yaml", "Dockerfile", "CMakeLists.txt", "global.json")


def load_manifest(path):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, dict) or data.get("schema_version") != 1 or not isinstance(data.get("name"), str):
        raise ValueError("Manifesto requer schema_version=1 e name em texto.")
    repos = data.get("repositories")
    if not isinstance(repos, list):
        raise ValueError("repositories deve ser uma lista.")
    ids = set()
    for item in repos:
        if not isinstance(item, dict):
            raise ValueError("Cada repositório deve ser um objeto.")
        repo_id = item.get("id", "")
        if not isinstance(repo_id, str) or not re.fullmatch(r"[a-zA-Z0-9][a-zA-Z0-9_-]*", repo_id) or repo_id in ids:
            raise ValueError("ID inválido ou duplicado no manifesto.")
        ids.add(repo_id)
        local = item.get("path")
        if local is not None and (not isinstance(local, str) or not local.strip() or any(ord(c) < 32 for c in local)):
            raise ValueError("path deve ser texto não vazio ou null.")
        url = item.get("url")
        if url is not None:
            if not isinstance(url, str):
                raise ValueError("url deve ser texto ou null.")
            parsed = urlsplit(url)
            if (parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password
                    or parsed.query or parsed.fragment or any(ord(c) < 32 for c in url)):
                raise ValueError("Use URL HTTPS sem credenciais, query ou fragmento.")
        deps = item.get("depends_on", [])
        if not isinstance(deps, list) or any(not isinstance(x, str) for x in deps):
            raise ValueError("depends_on deve ser lista de IDs.")
    for item in repos:
        if any(dep not in ids or dep == item["id"] for dep in item.get("depends_on", [])):
            raise ValueError("Dependência desconhecida ou autorreferência.")
    return data


def git(path, *args):
    try:
        result = subprocess.run(["git", "--no-optional-locks", "-c", "core.fsmonitor=false",
                                 "-C", str(path), *args], capture_output=True,
                                text=True, timeout=10, check=False)
        return result.stdout.strip() if result.returncode == 0 else None
    except (OSError, subprocess.TimeoutExpired):
        return None


def inventory(manifest):
    manifest = Path(manifest).resolve()
    data = load_manifest(manifest)
    output = {"schema_version": 1, "name": data["name"], "repositories": [],
              "coverage": "partial", "gaps": [],
              "scope": "Metadados locais; sem rede, leitura de código ou validação funcional"}
    seen = set()
    for item in data["repositories"]:
        row = {"id": item["id"], "depends_on": item.get("depends_on", [])}
        local = item.get("path")
        if local is None:
            row["status"] = "path-not-configured"
        else:
            candidate = Path(local).expanduser()
            path = (candidate if candidate.is_absolute() else manifest.parent / candidate).resolve()
            if not path.is_dir():
                row["status"] = "unavailable"
            elif path in seen:
                row["status"] = "duplicate-path"
            else:
                seen.add(path)
                top = git(path, "rev-parse", "--show-toplevel")
                if top is None or Path(top).resolve() != path:
                    row["status"] = "not-repository-root"
                else:
                    head = git(path, "rev-parse", "HEAD")
                    branch = git(path, "symbolic-ref", "--quiet", "--short", "HEAD")
                    status = git(path, "status", "--porcelain", "--untracked-files=normal")
                    state = "git-error" if status is None else "inspected" if head else "unborn"
                    row.update(status=state,
                               head=head, branch=branch, detached=bool(head and branch is None),
                               changes=len(status.splitlines()) if status else 0,
                               manifests=[name for name in MANIFESTS if (path / name).is_file()])
                    # Sem conteúdo, remotos ou nomes de arquivos modificados na saída.
        output["repositories"].append(row)
        if row["status"] != "inspected":
            output["gaps"].append(item["id"] + ":" + row["status"])
    if not output["repositories"]:
        output["gaps"].append("no-repositories-configured")
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", required=True)
    args = parser.parse_args()
    try:
        result = inventory(args.manifest)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 2 if result["gaps"] else 0
    except (ValueError, OSError) as error:
        # Erros de parse não reproduzem conteúdo do manifesto.
        print("Inventário não concluído: " + type(error).__name__, file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
