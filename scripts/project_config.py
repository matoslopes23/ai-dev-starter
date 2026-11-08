"""Contrato de configuração do consumidor, sem catálogo fechado de stacks ou estilos."""
import json
from pathlib import Path

WORKFLOWS = {"undecided", "github-flow", "trunk-based", "gitflow"}
FIELDS = {"name", "purpose", "stack", "architecture", "profiles", "base_branch", "git_workflow",
          "components", "checks", "production", "risks"}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def strings(value, field):
    require(isinstance(value, list) and all(isinstance(x, str) and x.strip() and "\x00" not in x
            for x in value), field + " deve ser lista de textos não vazios.")


def validate(config):
    require(isinstance(config, dict) and config.get("schema_version") == 1, "schema_version deve ser 1.")
    for field in ("name", "purpose"):
        require(isinstance(config.get(field), str) and config[field].strip() and "\x00" not in config[field],
                field + " deve ser texto não vazio.")
    for field in ("stack", "profiles", "risks"):
        strings(config.get(field, []), field)
    architecture = config.get("architecture", {})
    require(isinstance(architecture, dict), "architecture deve ser objeto.")
    style = architecture.get("style")
    require(style is None or (isinstance(style, str) and style.strip()), "architecture.style deve ser texto ou null.")
    for field in ("boundaries", "constraints"):
        strings(architecture.get(field, []), "architecture." + field)
    base = config.get("base_branch")
    require(base is None or (isinstance(base, str) and base.strip()), "base_branch deve ser texto ou null.")
    workflow = config.get("git_workflow")
    require(isinstance(workflow, str) and workflow in WORKFLOWS, "git_workflow inválido.")
    require(config.get("production") is None or type(config["production"]) is bool, "production deve ser booleano ou null.")
    components = config.get("components")
    require(isinstance(components, list), "components deve ser lista.")
    names = set()
    for item in components:
        require(isinstance(item, dict), "Componente deve ser objeto.")
        name = item.get("name")
        require(isinstance(name, str) and name.strip() and name not in names, "Nome de componente vazio ou duplicado.")
        names.add(name)
        path = item.get("path")
        require(isinstance(path, str) and path.strip() and "\x00" not in path, "Componente requer path relativo.")
        # Usar / também no Windows mantém o manifesto compartilhável.
        require(not Path(path).is_absolute() and ".." not in path.replace("\\", "/").split("/")
                and not (len(path) >= 2 and path[1] == ":"), "Path deve ficar dentro da raiz do projeto.")
        require(isinstance(item.get("responsibility"), str) and item["responsibility"].strip(), "Responsabilidade ausente.")
    checks = config.get("checks")
    require(isinstance(checks, dict), "checks deve ser objeto.")
    require(all(isinstance(k, str) and k.strip() and isinstance(v, str) and v.strip() and "\x00" not in v
                for k, v in checks.items()), "Checks devem mapear nomes para comandos não vazios.")
    return config


def config_path(target):
    target = Path(target).expanduser().absolute()
    require(not target.is_symlink() and target.is_dir(), "Destino deve ser diretório existente sem symlink.")
    target = target.resolve()
    bundle = target / ".ai-kit"
    require(not bundle.is_symlink() and bundle.is_dir(), "Instale o kit no destino antes de configurar.")
    path = bundle / "project.json"
    require(not path.is_symlink() and path.is_file(), "project.json deve existir sem symlink.")
    return target, path


def load(path):
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        raise ValueError("JSON inválido; conteúdo omitido.") from None
    require(isinstance(data, dict), "Configuração deve ser objeto JSON.")
    return data
