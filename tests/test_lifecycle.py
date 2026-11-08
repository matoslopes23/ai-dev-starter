import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from scripts import adopt, installation, update


class LifecycleTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="kit-lifecycle-")
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name).resolve()
        self.target = self.root / "product"
        self.target.mkdir()
        self.source = self.root / "source"
        self.source.mkdir()
        for file in installation.source_files(adopt.ROOT):
            dest = self.source / file.relative_to(adopt.ROOT)
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(file, dest)
        adopt.install(self.target, "Fixture", "existing", "undecided", True)

    def change_upstream(self, name="docs/02-arquitetura.md", suffix="\nUpstream revisado.\n"):
        path = self.source / name
        path.write_text(path.read_text(encoding="utf-8") + suffix, encoding="utf-8")

    def snapshot(self):
        return {p.relative_to(self.target).as_posix(): p.read_bytes()
                for p in self.target.rglob("*") if p.is_file() and ".ai" not in p.relative_to(self.target).parts}

    def test_native_wrappers_share_directory_and_link_to_canonical_skills(self):
        payload, origin = installation.build_payload(self.source, ["codex", "cursor", "copilot", "claude"])
        native = [key for key in payload if not key.startswith(".ai-kit/")]
        count = len(list((adopt.ROOT / "skills").glob("*/SKILL.md")))
        self.assertEqual(len(native), count * 2)
        before = self.snapshot()
        result = update.update(self.target, self.source, adapters=["codex", "cursor", "copilot", "claude"])
        self.assertEqual(self.snapshot(), before)
        self.assertFalse(result["applied"])
        applied = update.update(self.target, self.source, True, adapters=origin["adapters"])
        self.assertTrue(applied["applied"])
        from scripts.verify import local_links
        for relative in native:
            local_links(self.target / relative, (self.target / relative).read_text(encoding="utf-8"))

    def test_initial_install_refuses_adapter_collision(self):
        target = self.root / "collision"
        path = target / ".agents/skills/ai-kit-corrigir-bug/SKILL.md"
        path.parent.mkdir(parents=True)
        path.write_bytes(b"existing")
        with self.assertRaises(ValueError):
            adopt.install(target, "Test", "existing", "undecided", True, ["codex"])
        self.assertEqual(path.read_bytes(), b"existing")
        self.assertFalse((target / ".ai-kit").exists())

    def test_plan_has_no_side_effects_and_update_preserves_configs(self):
        self.change_upstream()
        config = self.target / ".ai-kit/project.json"
        config.write_text(config.read_text().replace('"stack": []', '"stack": ["Custom"]'), encoding="utf-8")
        before = self.snapshot()
        self.assertFalse(update.update(self.target, self.source)["applied"])
        self.assertEqual(before, self.snapshot())
        self.assertFalse((self.target / ".ai").exists())
        result = update.update(self.target, self.source, True)
        self.assertTrue(result["applied"])
        self.assertEqual(config.read_bytes(), before[".ai-kit/project.json"])
        self.assertEqual((self.target / ".ai-kit/system.json").read_bytes(), before[".ai-kit/system.json"])
        self.assertEqual((self.target / "AGENTS.md").read_bytes(), before["AGENTS.md"])
        update.restore(self.target, result["backup_id"], True)
        self.assertEqual(before, self.snapshot())

    def test_conflicts_block_every_write(self):
        local = self.target / ".ai-kit/docs/02-arquitetura.md"
        local.write_text("Custom local", encoding="utf-8")
        self.change_upstream()
        self.change_upstream("docs/03-fluxo-e-gates.md")
        before = self.snapshot()
        result = update.update(self.target, self.source, True)
        self.assertIn(".ai-kit/docs/02-arquitetura.md", result["conflicts"])
        self.assertFalse(result["applied"])
        self.assertEqual(before, self.snapshot())
        self.assertFalse((self.target / ".ai").exists())

    def test_local_changes_survive_when_upstream_unchanged(self):
        local = self.target / ".ai-kit/docs/02-arquitetura.md"
        local.write_text("Local policy", encoding="utf-8")
        result = update.update(self.target, self.source, True)
        self.assertIn(".ai-kit/docs/02-arquitetura.md", result["preserved_local"])
        self.assertEqual(local.read_text(), "Local policy")

    def test_removed_upstream_file_is_deleted_only_if_clean(self):
        name = "docs/16-adocao-pratica.md"
        (self.source / name).unlink()
        result = update.update(self.target, self.source, True)
        self.assertTrue(result["applied"])
        self.assertFalse((self.target / ".ai-kit" / name).exists())
        update.restore(self.target, result["backup_id"], True)
        self.assertTrue((self.target / ".ai-kit" / name).is_file())

    def test_restore_rejects_later_edit_and_corrupted_backup(self):
        self.change_upstream()
        result = update.update(self.target, self.source, True)
        local = self.target / ".ai-kit/docs/02-arquitetura.md"
        after = local.read_bytes()
        local.write_bytes(b"later edit")
        with self.assertRaises(ValueError):
            update.restore(self.target, result["backup_id"], True)
        self.assertEqual(local.read_bytes(), b"later edit")
        local.write_bytes(after)
        backup = self.target / ".ai/kit-backups" / result["backup_id"] / "before/.ai-kit/docs/02-arquitetura.md"
        backup.write_bytes(b"corrupt")
        with self.assertRaises(ValueError):
            update.restore(self.target, result["backup_id"], True)

    def test_write_failure_rolls_back_and_releases_lock(self):
        self.change_upstream()
        self.change_upstream("docs/03-fluxo-e-gates.md")
        before = self.snapshot()
        original = update.atomic_write
        failed = False
        def fail_once(path, content):
            nonlocal failed
            if path == self.target / ".ai-kit/docs/03-fluxo-e-gates.md" and not failed:
                failed = True
                raise OSError("simulated write failure")
            return original(path, content)
        with patch.object(update, "atomic_write", fail_once), self.assertRaises(OSError):
            update.update(self.target, self.source, True)
        self.assertEqual(before, self.snapshot())
        self.assertFalse((self.target / ".ai-kit/.update.lock").exists())

    def test_lock_symlinks_and_malicious_manifest_are_rejected(self):
        self.change_upstream()
        lock = self.target / ".ai-kit/.update.lock"
        lock.write_bytes(b"another process")
        with self.assertRaises(FileExistsError):
            update.update(self.target, self.source, True)
        lock.unlink()
        origin = self.target / ".ai-kit/origin.json"
        data = json.loads(origin.read_bytes())
        data["managed"]["../outside"] = "a" * 64
        origin.write_text(json.dumps(data), encoding="utf-8")
        with self.assertRaises(ValueError):
            update.update(self.target, self.source, True)
        data["managed"].pop("../outside")
        origin.write_text(json.dumps(data), encoding="utf-8")
        native = self.target / ".agents"
        native.symlink_to(self.root, target_is_directory=True)
        with self.assertRaises(ValueError):
            update.update(self.target, self.source, True, adapters=["codex"])

    def test_legacy_21_origin_migrates_with_known_readme(self):
        origin = self.target / ".ai-kit/origin.json"
        data = json.loads(origin.read_bytes())
        readme = self.target / ".ai-kit/README.md"
        readme.write_bytes(installation.LEGACY_README)
        data = {"kit_version": "2.1.0", "source_commit": data["source_commit"], "sha256": data["sha256"]}
        data["sha256"].pop("README.md")
        origin.write_text(json.dumps(data), encoding="utf-8")
        result = update.update(self.target, self.source, True)
        self.assertTrue(result["applied"])
        self.assertEqual(json.loads(origin.read_bytes())["format_version"], 2)

    def test_installed_update_cli_operates_without_central_imports(self):
        self.change_upstream()
        result = subprocess.run([sys.executable, "-B", str(self.target / ".ai-kit/scripts/update.py"),
                                 "--target", str(self.target), "--source", str(self.source)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse(json.loads(result.stdout)["applied"])

    def test_origin_write_failure_restores_payload_and_manifest(self):
        self.change_upstream()
        before = self.snapshot()
        original = update.atomic_write
        failed = False
        def fail_once(path, content):
            nonlocal failed
            if path == self.target / ".ai-kit/origin.json" and not failed:
                failed = True
                raise OSError("origin write failed")
            return original(path, content)
        with patch.object(update, "atomic_write", fail_once), self.assertRaises(OSError):
            update.update(self.target, self.source, True)
        self.assertEqual(before, self.snapshot())

    def test_prepared_backup_can_recover_fully_written_update(self):
        self.change_upstream()
        before = self.snapshot()
        original = update.atomic_write
        def fail_final_status(path, content):
            if path.name == "manifest.json" and b'"status": "completed"' in content:
                raise OSError("backup finalization failed")
            return original(path, content)
        with patch.object(update, "atomic_write", fail_final_status), self.assertRaises(OSError):
            update.update(self.target, self.source, True)
        folder = next((self.target / ".ai/kit-backups").iterdir())
        self.assertTrue(update.restore(self.target, folder.name, True)["applied"])
        self.assertEqual(before, self.snapshot())

    def test_modified_adapter_blocks_removal_then_clean_adapter_can_be_removed(self):
        update.update(self.target, self.source, True, adapters=["codex"])
        wrapper = self.target / ".agents/skills/ai-kit-corrigir-bug/SKILL.md"
        original = wrapper.read_bytes()
        wrapper.write_bytes(original + b"\nLocal change\n")
        result = update.update(self.target, self.source, True, adapters=[])
        self.assertIn(wrapper.relative_to(self.target).as_posix(), result["conflicts"])
        wrapper.write_bytes(original)
        result = update.update(self.target, self.source, True, adapters=[])
        self.assertTrue(result["applied"])
        self.assertFalse(wrapper.exists())


if __name__ == "__main__":
    unittest.main()
