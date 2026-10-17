"""Lightweight tests for the standalone personal Codex CLI."""
import os
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "bin" / "codex-portable.py"

class PortableCliTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.home = Path(self.temp.name)
        self.codex = self.home / ".codex"
        self.codex.mkdir()
        (self.codex / "AGENTS.md").write_text("# Personal test rule\n")
        self.env = dict(os.environ, HOME=str(self.home), CODEX_HOME=str(self.codex))

    def invoke(self, *args):
        return subprocess.run([sys.executable, str(SCRIPT), *args],
                              env=self.env, capture_output=True, text=True)

    def test_help(self):
        response = self.invoke("--help")
        self.assertEqual(response.returncode, 0, response.stderr)
        for name in ("audit", "capture", "restore", "reset"):
            self.assertIn(name, response.stdout)

    def test_audit_detects_user_rule(self):
        response = self.invoke("audit")
        self.assertEqual(response.returncode, 0, response.stderr)
        self.assertIn("AGENTS.md", response.stdout)

    def test_reset_is_dry_run_by_default(self):
        response = self.invoke("reset")
        self.assertEqual(response.returncode, 0, response.stderr)
        self.assertTrue((self.codex / "AGENTS.md").exists())

    def test_reset_requires_confirmed_remote_for_managed_install(self):
        rule = self.codex / "AGENTS.md"
        import hashlib
        checksum = hashlib.sha256(rule.read_bytes()).hexdigest()
        receipt = self.home / ".codex-portable-installed.json"
        receipt.write_text(json.dumps({"files": [
            {"path": str(rule), "sha256": checksum, "backup": None}
        ]}))
        response = self.invoke("reset", "--apply")
        self.assertNotEqual(response.returncode, 0)
        self.assertIn("--confirmed-remote", response.stderr)
        self.assertTrue(rule.exists())

if __name__ == "__main__":
    unittest.main()
