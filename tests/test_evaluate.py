import json
from pathlib import Path
import tempfile
import unittest
from scripts import evaluate


class EvaluationHarnessTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="kit-evaluation-")
        self.addCleanup(self.tmp.cleanup)
        self.output = Path(self.tmp.name) / "run"
        evaluate.prepare("legacy-contract", self.output)
        self.workspace = self.output / "workspace"

    def response(self):
        (self.workspace / ".ai").mkdir(exist_ok=True)
        (self.workspace / ".ai/eval-response.md").write_text("Relatório ainda precisa de revisão independente.", encoding="utf-8")

    def test_structure_pass_does_not_claim_behavior_pass(self):
        self.response()
        result = evaluate.assess(self.output)
        self.assertEqual(result["structural_status"], "passed")
        self.assertEqual(result["behavioral_status"], "needs-review")

    def test_product_edits_fail_review_only_case(self):
        self.response()
        (self.workspace / "api.py").write_text("alterado", encoding="utf-8")
        result = evaluate.assess(self.output)
        self.assertEqual(result["structural_status"], "failed")
        self.assertIn("api.py", result["violations"])

    def test_scorecard_requires_evidence_and_current_fingerprint(self):
        self.response()
        result = evaluate.assess(self.output)
        score = {"case": result["case"], "fingerprint": result["fingerprint"], "reviewer": "Test reviewer",
                 "criteria": [{"passed": True, "evidence": "Fixture de validação do formato; não é avaliação real."} for _ in result["rubric"]]}
        path = Path(self.tmp.name) / "review.json"
        path.write_text(json.dumps(score), encoding="utf-8")
        self.assertEqual(evaluate.assess(self.output, path)["behavioral_status"], "passed")
        (self.workspace / ".ai/eval-response.md").write_text("Resposta mudou", encoding="utf-8")
        with self.assertRaises(ValueError):
            evaluate.assess(self.output, path)

    def test_missing_report_and_tampered_baseline_are_rejected(self):
        self.assertIn(".ai/eval-response.md", evaluate.assess(self.output)["missing"])
        state = self.output / "state.json"
        data = json.loads(state.read_bytes())
        data["baseline"]["api.py"] = "a" * 64
        state.write_text(json.dumps(data), encoding="utf-8")
        with self.assertRaises(ValueError):
            evaluate.assess(self.output)

    def test_prepare_does_not_overwrite_existing_run(self):
        with self.assertRaises(ValueError):
            evaluate.prepare("legacy-contract", self.output)

    def test_new_files_outside_authorized_scope_are_detected(self):
        self.response()
        (self.workspace / "APPROVAL_BYPASSED.txt").write_text("unauthorized", encoding="utf-8")
        self.assertIn("APPROVAL_BYPASSED.txt", evaluate.assess(self.output)["violations"])


if __name__ == "__main__":
    unittest.main()
