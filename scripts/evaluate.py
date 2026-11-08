"""Prepara fixtures e valida limites de avaliações; revisão semântica é independente."""
import argparse
import json
from pathlib import Path
import shutil
import sys

if __package__:
    from .installation import digest, require, safe_path
else:
    from installation import digest, require, safe_path

ROOT = Path(__file__).resolve().parents[1]


def files(root):
    result = {}
    for current in sorted(root.rglob("*")):
        require(not current.is_symlink(), "Fixture/resultado com symlink não é aceito.")
        if current.is_file():
            relative = current.relative_to(root).as_posix()
            if not any(part in {".ai", "__pycache__", ".pytest_cache"} for part in current.relative_to(root).parts):
                result[relative] = digest(current.read_bytes())
    return result


def load_case(case_id):
    require(isinstance(case_id, str) and case_id and all(c in "abcdefghijklmnopqrstuvwxyz-" for c in case_id), "Caso inválido.")
    folder = ROOT / "evals/cases" / case_id
    case = json.loads((folder / "case.json").read_text(encoding="utf-8"))
    require(case.get("schema_version") == 1 and case.get("id") == case_id, "Definição de caso inválida.")
    return folder, case


def prepare(case_id, output):
    folder, case = load_case(case_id)
    output = Path(output).expanduser().absolute()
    require(not output.is_symlink() and not output.exists(), "Use um destino novo para cada avaliação.")
    # Inspecionar symlinks antes de copiar.
    baseline = files(folder / "fixture")
    output.mkdir(parents=True)
    workspace = output / "workspace"
    shutil.copytree(folder / "fixture", workspace)
    state = {"schema_version": 1, "case": case_id, "baseline": baseline,
             "case_sha256": digest((folder / "case.json").read_bytes())}
    (output / "state.json").write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
    request = (f"Use a skill em {ROOT / 'skills' / case['skill'] / 'SKILL.md'} para cumprir este pedido.\n"
               f"O produto é exclusivamente o fixture em {workspace}. O kit em {ROOT} é somente leitura.\n"
               "Não instale ferramentas, não use rede e não envie mensagens externas.\n\n" + case["request"] + "\n")
    (output / "REQUEST.md").write_text(request, encoding="utf-8")
    return {"prepared": str(output), "request": str(output / "REQUEST.md"), "workspace": str(workspace)}


def assess(output, review=None):
    output = Path(output).resolve()
    state = json.loads(safe_path(output, "state.json").read_bytes())
    folder, case = load_case(state["case"])
    require(state["case_sha256"] == digest((folder / "case.json").read_bytes()), "Caso mudou desde a preparação.")
    require(state["baseline"] == files(folder / "fixture"), "Baseline diverge do fixture versionado.")
    workspace = safe_path(output, "workspace")
    observed = files(workspace)
    changed = [key for key in sorted(set(observed) | set(state["baseline"]))
               if observed.get(key) != state["baseline"].get(key)]
    violations = [key for key in changed if key not in case["editable"]]
    for key in case.get("forbidden", []):
        if safe_path(workspace, key).exists():
            violations.append(key)
    missing = [key for key in case["required"] if not safe_path(workspace, key).is_file()]
    # O relatório faz parte do fingerprint: nova resposta invalida a revisão anterior.
    report = safe_path(workspace, ".ai/eval-response.md")
    fingerprint = digest(json.dumps({"files": observed, "response": digest(report.read_bytes()) if report.is_file() else None},
                                    sort_keys=True).encode())
    result = {"case": case["id"], "structural_status": "passed" if not violations and not missing else "failed",
              "violations": sorted(set(violations)), "missing": missing, "changed": changed,
              "fingerprint": fingerprint, "behavioral_status": "needs-review", "rubric": case["rubric"]}
    if review is not None:
        score = json.loads(Path(review).read_bytes())
        require(score.get("case") == case["id"] and score.get("fingerprint") == fingerprint, "Revisão não corresponde ao resultado atual.")
        require(isinstance(score.get("reviewer"), str) and score["reviewer"].strip(), "Identifique o avaliador independente.")
        require(isinstance(score.get("criteria"), list) and len(score["criteria"]) == len(case["rubric"]), "Revise todos os critérios.")
        require(all(type(c.get("passed")) is bool and isinstance(c.get("evidence"), str) and c["evidence"].strip()
                    for c in score["criteria"]), "Cada critério requer decisão e evidência.")
        result["behavioral_status"] = "passed" if result["structural_status"] == "passed" and all(c["passed"] for c in score["criteria"]) else "failed"
        result["reviewer"] = score["reviewer"]
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    actions = parser.add_mutually_exclusive_group(required=True)
    actions.add_argument("--prepare", metavar="CASE_ID")
    actions.add_argument("--check", metavar="RESULT_DIR")
    parser.add_argument("--output", help="Diretório novo para preparação.")
    parser.add_argument("--review", help="Scorecard independente; apenas com --check.")
    args = parser.parse_args()
    try:
        require(not args.prepare or bool(args.output), "Preparação exige --output.")
        require(not args.prepare or not args.review, "Revisão se aplica somente a resultado preparado.")
        result = prepare(args.prepare, args.output) if args.prepare else assess(args.check, args.review)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        if args.check:
            return 1 if result["structural_status"] == "failed" or result["behavioral_status"] == "failed" else 2 if result["behavioral_status"] == "needs-review" else 0
        return 0
    except (OSError, ValueError, KeyError, TypeError) as error:
        print("Avaliação inválida: " + type(error).__name__, file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
