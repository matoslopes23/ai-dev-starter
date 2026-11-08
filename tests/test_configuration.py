import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from scripts import adopt, configure, doctor


class ConfigurationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="configuration-test-")
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name).resolve()
        adopt.install(self.root, "Produto", "existing", "undecided", True)
        self.config = self.root / ".ai-kit/project.json"

    def read(self):
        return json.loads(self.config.read_text(encoding="utf-8"))

    def command(self, script, *args):
        return subprocess.run([sys.executable, "-B", str(self.root / ".ai-kit/scripts" / script),
                               "--target", str(self.root), *args], capture_output=True, text=True)

    def test_dry_run_preserves_configuration_and_project(self):
        before = self.config.read_bytes()
        app = self.root / "custom.lang"
        app.write_text("original", encoding="utf-8")
        result = configure.configure(self.root, {"stack": ["Linguagem própria"],
                                               "architecture": {"style": "Arquitetura própria"}})
        self.assertFalse(result["applied"])
        self.assertEqual(set(result["changed_fields"]), {"stack", "architecture"})
        self.assertEqual(self.config.read_bytes(), before)
        self.assertEqual(app.read_text(), "original")

    def test_arbitrary_languages_and_architectures_are_accepted(self):
        for stack, style in ((["Elixir", "Erlang/OTP"], "Atores"),
                             (["C", "Assembly"], "Orientada a dados / ECS"),
                             (["Clojure"], "Funcional com núcleo puro"),
                             (["Linguagem interna vX"], "Estilo interno sem receita")):
            with self.subTest(stack=stack, style=style):
                configure.configure(self.root, {"stack": stack, "architecture": {"style": style}}, True)
                self.assertEqual(self.read()["stack"], stack)
                self.assertEqual(self.read()["architecture"]["style"], style)

    def test_installed_cli_merges_flags_without_executing_commands(self):
        marker = self.root / "must-not-exist"
        command = sys.executable + ' -c "open(' + repr(str(marker)) + ', \'w\').write(\'executed\')"'
        config_patch = self.root / "settings.json"
        config_patch.write_text(json.dumps({
            "purpose": "Objetivo confirmado", "architecture": {"style": "Anterior", "constraints": ["Preservar API"]},
            "checks": {"existing": "custom-build --verify"},
            "components": [{"name": "core", "path": ".", "responsibility": "Aplicação"}],
        }), encoding="utf-8")
        result = self.command("configure.py", "--config", str(config_patch), "--stack", "F#",
                              "--stack", "C#", "--architecture", "Funcional e serviços",
                              "--check", "test=" + command, "--base-branch", "main",
                              "--git-workflow", "trunk-based", "--apply")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse(json.loads(result.stdout)["commands_executed"])
        data = self.read()
        self.assertEqual(data["stack"], ["F#", "C#"])
        self.assertEqual(data["architecture"]["constraints"], ["Preservar API"])
        self.assertEqual(set(data["checks"]), {"existing", "test"})
        self.assertFalse(marker.exists())
        check = self.command("doctor.py")
        self.assertEqual(check.returncode, 0, check.stderr)
        self.assertEqual(json.loads(check.stdout)["status"], "ready-for-diagnosis")
        self.assertFalse(marker.exists())

    def test_invalid_patch_does_not_write(self):
        before = self.config.read_bytes()
        patches = [{"schema_version": 2}, {"stack": "Java"}, {"git_workflow": []},
                   {"architecture": "MVC"}, {"checks": {"test": ""}},
                   {"components": [{"name": "outside", "path": "../other", "responsibility": "Outside"}]}]
        for changes in patches:
            with self.subTest(changes=changes), self.assertRaises(ValueError):
                configure.configure(self.root, changes, True)
            self.assertEqual(self.config.read_bytes(), before)

    def test_atomic_failure_leaves_original_and_no_temp_files(self):
        before = self.config.read_bytes()
        with patch.object(configure.os, "replace", side_effect=OSError("simulated failure")):
            with self.assertRaises(OSError):
                configure.configure(self.root, {"stack": ["Rust"]}, True)
        self.assertEqual(self.config.read_bytes(), before)
        self.assertEqual(list(self.config.parent.glob(".project-*.tmp")), [])

    def test_unknown_existing_metadata_and_permissions_survive(self):
        data = self.read()
        data["team_extension"] = {"contract": "preserve"}
        self.config.write_text(json.dumps(data), encoding="utf-8")
        self.config.chmod(0o640)
        mode = self.config.stat().st_mode & 0o777
        configure.configure(self.root, {"stack": ["Ruby"]}, True)
        self.assertEqual(self.read()["team_extension"], {"contract": "preserve"})
        self.assertEqual(self.config.stat().st_mode & 0o777, mode)

    def test_symlink_configuration_is_refused(self):
        external = self.root / "external.json"
        external.write_bytes(self.config.read_bytes())
        self.config.unlink()
        self.config.symlink_to(external)
        before = external.read_bytes()
        with self.assertRaises(ValueError):
            configure.configure(self.root, {"stack": ["PHP"]}, True)
        with self.assertRaises(ValueError):
            doctor.diagnose(self.root)
        self.assertEqual(external.read_bytes(), before)

    def test_initial_doctor_and_workspace_report_gaps(self):
        result = self.command("doctor.py")
        self.assertEqual(result.returncode, 2, result.stderr)
        gaps = {r["check"] for r in json.loads(result.stdout)["checks"] if r["status"] == "gap"}
        self.assertTrue({"stack", "architecture", "checks", "components"} <= gaps)
        data = self.read()
        data["kind"] = "workspace"
        self.config.write_text(json.dumps(data), encoding="utf-8")
        result = doctor.diagnose(self.root)
        self.assertIn("repositories", {r["check"] for r in result["checks"] if r["status"] == "gap"})


if __name__ == "__main__":
    unittest.main()
