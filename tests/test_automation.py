import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from scripts import adopt, inventory, verify
from scripts.installation import digest


class AdoptionTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="ai-kit-test-")
        self.addCleanup(self.tmp.cleanup)
        self.target = (Path(self.tmp.name) / "product").resolve()
        self.target.mkdir()

    def install(self, apply=True, mode="existing"):
        return adopt.install(self.target, "Produto de teste", mode, "undecided", apply)

    def test_dry_run_preserves_every_byte(self):
        original = b"# Existing instructions\r\nKeep this."
        (self.target / "AGENTS.md").write_bytes(original)
        result = self.install(apply=False)
        self.assertFalse(result["applied"])
        self.assertEqual(list(self.target.iterdir()), [self.target / "AGENTS.md"])
        self.assertEqual((self.target / "AGENTS.md").read_bytes(), original)

    def test_install_preserves_project_and_has_self_contained_links(self):
        agents = b"# Existing contract\nDo not replace me."
        ignored = b"cache/\n!/.ai/\n"
        (self.target / "AGENTS.md").write_bytes(agents)
        (self.target / ".gitignore").write_bytes(ignored)
        (self.target / "app.py").write_text("original", encoding="utf-8")
        self.assertTrue(self.install()["applied"])
        self.assertTrue((self.target / "AGENTS.md").read_bytes().startswith(agents))
        self.assertTrue((self.target / ".gitignore").read_bytes().startswith(ignored))
        self.assertEqual((self.target / "app.py").read_text(), "original")
        kit = self.target / ".ai-kit"
        config = json.loads((kit / "project.json").read_text())
        self.assertEqual(config["checks"], {})
        self.assertEqual(config["git_workflow"], "undecided")
        self.assertIsNone(config["production"])
        self.assertFalse((kit / "examples").exists())
        self.assertFalse((self.target / ".github").exists())
        self.assertTrue((kit / "scripts/configure.py").is_file())
        self.assertTrue((kit / "scripts/doctor.py").is_file())
        self.assertFalse((kit / "scripts/verify.py").exists())
        for path in kit.rglob("*.md"):
            verify.local_links(path, path.read_text(encoding="utf-8"))
        origin = json.loads((kit / "origin.json").read_text())
        self.assertEqual(origin["kit_version"], adopt.KIT_VERSION)
        self.assertIn("AGENTS.md", origin["sha256"])
        for relative, expected in origin["managed"].items():
            self.assertEqual(digest((self.target / relative).read_bytes()), expected)
        self.assertEqual(json.loads((kit / "system.json").read_text())["repositories"], [])

    def test_repeat_install_refuses_without_changes(self):
        self.install()
        before = {str(p): p.read_bytes() for p in self.target.rglob("*") if p.is_file()}
        with self.assertRaises(ValueError):
            self.install()
        self.assertEqual(before, {str(p): p.read_bytes() for p in self.target.rglob("*") if p.is_file()})

    def test_all_modes_generate_correct_kind(self):
        for mode in ("new", "existing", "multi-repo"):
            with self.subTest(mode=mode):
                target = self.target / mode
                target.mkdir()
                adopt.install(target, "Test", mode, "gitflow", True)
                config = json.loads((target / ".ai-kit/project.json").read_text())
                self.assertEqual(config["adoption_mode"], mode)
                self.assertEqual(config["kind"], "workspace" if mode == "multi-repo" else "application")
                self.assertEqual(config["git_workflow"], "gitflow")

    def test_symlink_destination_and_files_are_refused(self):
        external = Path(self.tmp.name) / "outside.md"
        external.write_text("unchanged", encoding="utf-8")
        for name in ("AGENTS.md", ".gitignore", ".ai-kit"):
            with self.subTest(name=name):
                destination = self.target / name
                destination.symlink_to(external)
                with self.assertRaises(ValueError):
                    self.install()
                destination.unlink()
        self.assertEqual(external.read_text(), "unchanged")
        linked = Path(self.tmp.name) / "linked"
        linked.symlink_to(self.target, target_is_directory=True)
        with self.assertRaises(ValueError):
            adopt.install(linked, "Test", "existing", "undecided", True)

    def test_collision_incomplete_marker_and_invalid_name(self):
        for name in ("", " \n", "Test\x00"):
            with self.subTest(name=repr(name)), self.assertRaises(ValueError):
                adopt.install(self.target, name, "existing", "undecided")
        (self.target / "AGENTS.md").write_text("<!-- ai-engineering-kit:start -->", encoding="utf-8")
        with self.assertRaises(ValueError):
            self.install()
        self.assertFalse((self.target / ".ai-kit").exists())

    def test_copy_failure_restores_target(self):
        (self.target / "AGENTS.md").write_bytes(b"original")
        with patch.object(adopt.shutil, "copytree", side_effect=OSError("simulated copy failure")):
            with self.assertRaises(OSError):
                self.install()
        self.assertEqual((self.target / "AGENTS.md").read_bytes(), b"original")
        self.assertFalse((self.target / ".gitignore").exists())
        self.assertFalse((self.target / ".ai-kit").exists())

    def test_failure_after_root_write_restores_original_files(self):
        (self.target / "AGENTS.md").write_bytes(b"original agents")
        (self.target / ".gitignore").write_bytes(b"original ignore")
        write_bytes = Path.write_bytes
        failed = False
        def simulated_write(path, data):
            nonlocal failed
            if path == self.target / ".gitignore" and not failed:
                failed = True
                raise OSError("simulated write failure")
            return write_bytes(path, data)
        with patch.object(Path, "write_bytes", simulated_write):
            with self.assertRaises(OSError):
                self.install()
        self.assertEqual((self.target / "AGENTS.md").read_bytes(), b"original agents")
        self.assertEqual((self.target / ".gitignore").read_bytes(), b"original ignore")
        self.assertFalse((self.target / ".ai-kit").exists())


class InventoryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="inventory-test-")
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.manifest = self.root / "system.json"

    def write(self, repos):
        self.manifest.write_text(json.dumps({"schema_version": 1, "name": "System", "repositories": repos}), encoding="utf-8")

    def repo(self, name="api"):
        path = self.root / name
        hooks = self.root / "empty-hooks"
        hooks.mkdir(exist_ok=True)
        subprocess.run(["git", "init", "-q", "-b", "main", str(path)], check=True)
        subprocess.run(["git", "-C", str(path), "-c", "user.name=Kit Test",
                        "-c", "user.email=test@example.invalid", "-c", "commit.gpgsign=false",
                        "-c", "core.hooksPath=" + str(hooks), "commit", "-q", "--allow-empty", "-m", "fixture"], check=True)
        return path

    def test_empty_and_missing_paths_are_gaps(self):
        self.write([])
        self.assertIn("no-repositories-configured", inventory.inventory(self.manifest)["gaps"])
        self.write([{"id": "remote", "url": "https://github.com/example/repo"}, {"id": "missing", "path": "absent"}])
        result = inventory.inventory(self.manifest)
        self.assertEqual([r["status"] for r in result["repositories"]], ["path-not-configured", "unavailable"])
        self.assertEqual(result["coverage"], "partial")

    def test_real_git_metadata_without_opening_files_or_remotes(self):
        path = self.repo()
        (path / "package.json").write_text("not read by inventory", encoding="utf-8")
        # Nome sensível e conteúdo sintético: inventário não deve abrir este arquivo.
        (path / ".env").write_text("synthetic-test-data", encoding="utf-8")
        self.write([{"id": "api", "path": "api", "depends_on": []}])
        manifest_text = self.manifest.read_text(encoding="utf-8")
        with patch.object(Path, "read_text", autospec=True, side_effect=lambda p, **kw: manifest_text
                          if p == self.manifest.resolve() else self.fail("Unexpected file read")):
            result = inventory.inventory(self.manifest)
        row = result["repositories"][0]
        self.assertEqual(row["status"], "inspected")
        self.assertEqual(row["branch"], "main")
        self.assertEqual(len(row["head"]), 40)
        self.assertIn("package.json", row["manifests"])
        self.assertNotIn("synthetic-test-data", json.dumps(result))
        self.assertNotIn(".env", json.dumps(result))
        self.assertFalse(result["gaps"])

    def test_subdirectory_duplicate_and_unborn_are_not_silent_success(self):
        path = self.repo()
        (path / "nested").mkdir()
        subprocess.run(["git", "init", "-q", "-b", "main", str(self.root / "unborn")], check=True)
        self.write([{"id": "a", "path": "api"}, {"id": "b", "path": "api"},
                    {"id": "nested", "path": "api/nested"}, {"id": "unborn", "path": "unborn"}])
        result = inventory.inventory(self.manifest)
        self.assertEqual([r["status"] for r in result["repositories"]],
                         ["inspected", "duplicate-path", "not-repository-root", "unborn"])
        self.assertEqual(len(result["gaps"]), 3)

    def test_manifest_validation(self):
        invalid = [
            [{"id": "a"}, {"id": "a"}],
            [{"id": "a", "depends_on": ["missing"]}],
            [{"id": "a", "depends_on": ["a"]}],
            [{"id": "a", "path": ""}],
            [{"id": "a", "url": "https://user:synthetic@github.com/example/repo"}],
            [{"id": "a", "url": "https://github.com/example/repo?token=synthetic"}],
        ]
        for repos in invalid:
            with self.subTest(repos=repos):
                self.write(repos)
                with self.assertRaises(ValueError):
                    inventory.load_manifest(self.manifest)


class VerificationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="verify-test-")
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)

    def test_binary_and_dependencies_do_not_break_gate(self):
        adopt.install(self.root, "Fixture", "new", "undecided", True)
        kit = self.root / ".ai-kit"
        before = verify.inspect_tree(kit)
        (kit / "node_modules").mkdir()
        (kit / "node_modules/bad.py").write_text("not python!", encoding="utf-8")
        (kit / "image.png").write_bytes(b"\x89PNG\r\n\x1a\n")
        (kit / "alias").symlink_to(kit, target_is_directory=True)
        after = verify.inspect_tree(kit)
        self.assertEqual(after["text_files"], before["text_files"])
        self.assertEqual(after["skipped_files"], before["skipped_files"] + 1)

    def test_sensitive_name_detected_before_read(self):
        for name in (".env", ".env.production", "key.pem", "cert.p12", "key.pfx"):
            self.assertTrue(verify.sensitive_name(Path(name)))
        self.assertFalse(verify.sensitive_name(Path(".env.example")))
        adopt.install(self.root, "Fixture", "new", "undecided", True)
        kit = self.root / ".ai-kit"
        (kit / ".env").write_text("synthetic-only", encoding="utf-8")
        original_read = Path.read_text
        def guarded_read(path, *args, **kwargs):
            self.assertNotEqual(path.name, ".env", "Scanner opened forbidden file")
            return original_read(path, *args, **kwargs)
        with patch.object(Path, "read_text", guarded_read):
            with self.assertRaisesRegex(ValueError, "Arquivo sensível"):
                verify.inspect_tree(kit)

    def test_broken_link_is_rejected_and_external_link_is_not_fetched(self):
        doc = self.root / "doc.md"
        with self.assertRaises(ValueError):
            verify.local_links(doc, "[missing](missing.md)")
        verify.local_links(doc, "[external](https://example.invalid/private) [anchor](#title)")


if __name__ == "__main__":
    unittest.main()
