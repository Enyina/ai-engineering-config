"""Isolated regression checks for rule discovery and safe managed-file restoration."""
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SOURCE = Path(__file__).resolve().parents[1] / "bin" / "codex-portable.py"

class SafetyTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        base = Path(self.temporary.name)
        self.project = base / "portable"
        self.project.mkdir()
        (self.project / "bin").mkdir()
        self.script = self.project / "bin" / "codex-portable.py"
        shutil.copy2(SOURCE, self.script)
        self.home = base / "home"
        self.home.mkdir()
        self.codex = self.home / ".codex"
        self.codex.mkdir()
        self.rules = self.codex / "rules"
        self.rules.mkdir()
        (self.rules / "default.rules").write_text("prefix_rule(pattern=[\"git\", \"status\"], decision=\"allow\")\n")
        self.env = dict(os.environ, HOME=str(self.home), CODEX_HOME=str(self.codex))

    def cli(self, *arguments):
        return subprocess.run([sys.executable, str(self.script), *arguments],
                              cwd=self.project, env=self.env, text=True, capture_output=True)

    def test_capture_omits_bundled_system_skills(self):
        sys_skill = self.codex / "skills" / ".system" / "skill-creator"
        sys_skill.mkdir(parents=True)
        (sys_skill / "SKILL.md").write_text("# Builtin\n")
        personal = self.codex / "skills" / "my-skill"
        personal.mkdir(parents=True)
        (personal / "SKILL.md").write_text("# Personal\n")
        r = self.cli("capture")
        self.assertEqual(r.returncode, 0, r.stderr)
        snapshot = self.project / "snapshot"
        self.assertFalse((snapshot / "codex" / "skills" / ".system").exists())
        self.assertTrue((snapshot / "codex" / "skills" / "my-skill" / "SKILL.md").exists())
        manifest = json.loads((snapshot / "manifest.json").read_text())
        self.assertFalse(any(".system" in item["path"] for item in manifest["files"]))

    def test_restore_dry_run_preserves_existing_files(self):
        self.assertEqual(self.cli("capture").returncode, 0)
        existing = self.rules / "unmanaged.rules"
        existing.write_text("# keep\n")
        result = self.cli("restore")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(existing.read_text(), "# keep\n")
        self.assertFalse((self.home / ".codex-portable-installed.json").exists())

    def test_restore_preserves_unmanaged_skills_and_keeps_backups(self):
        self.assertEqual(self.cli("capture").returncode, 0)
        extra = self.rules / "unmanaged.rules"
        extra.write_text("# keep\n")
        before = self.rules / "default.rules"
        before.write_text("# updated existing file\n")
        result = self.cli("restore", "--apply")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(extra.exists())
        self.assertIn("prefix_rule", before.read_text())
        receipt = json.loads((self.home / ".codex-portable-installed.json").read_text())
        self.assertTrue(receipt["files"][0]["backup"])
        self.assertTrue(Path(receipt["files"][0]["backup"]).exists())

    def test_restore_accepts_system_alias_before_trusted_home(self):
        # On macOS /var points to /private/var. The alias is above HOME.
        root = self.home.parent
        real = root / "real-var"
        real.mkdir()
        alias = root / "var"
        alias.symlink_to(real, target_is_directory=True)
        aliased_home = alias / "home"
        aliased_home.mkdir()
        aliased_rules = aliased_home / ".codex" / "rules"
        aliased_rules.mkdir(parents=True)
        (aliased_rules / "default.rules").write_text("# alias-safe test\\n")
        self.env["HOME"] = str(aliased_home)
        self.env["CODEX_HOME"] = str(aliased_home / ".codex")
        self.assertEqual(self.cli("capture").returncode, 0)
        result = self.cli("restore", "--apply")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual((aliased_rules / "default.rules").read_text(), "# alias-safe test\\n")

    def test_restore_refuses_symlink_in_managed_directory(self):
        self.assertEqual(self.cli("capture").returncode, 0)
        old_rules = self.codex / "real-rules"
        self.rules.rename(old_rules)
        self.rules.symlink_to(old_rules, target_is_directory=True)
        result = self.cli("restore", "--apply")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Symlink destination refused", result.stderr)
        self.assertFalse((self.home / ".codex-portable-installed.json").exists())

    def test_reset_without_receipt_cannot_delete_existing_files(self):
        result = self.cli("reset", "--apply", "--confirmed-remote")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((self.rules / "default.rules").exists())

    def test_tampered_snapshot_is_rejected(self):
        self.assertEqual(self.cli("capture").returncode, 0)
        (self.project / "snapshot" / "codex" / "rules" / "default.rules").write_text("# tampered\n")
        result = self.cli("restore", "--apply")
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse((self.home / ".codex-portable-installed.json").exists())

    def test_restore_is_not_repeatable_without_reset(self):
        self.assertEqual(self.cli("capture").returncode, 0)
        self.assertEqual(self.cli("restore", "--apply").returncode, 0)
        result = self.cli("restore", "--apply")
        self.assertNotEqual(result.returncode, 0)

if __name__ == "__main__":
    unittest.main()
