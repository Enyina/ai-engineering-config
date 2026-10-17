"""Isolated trust-domain preflight regression tests, no real employer data."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "bin" / "workspace-boundary.py"

class WorkspaceBoundaries(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)

    def marker(self, data, filename="workspace.json"):
        path = self.root / ".ai-rules" / filename
        path.parent.mkdir(exist_ok=True)
        path.write_text(json.dumps(data))

    def check(self, op):
        result = subprocess.run([sys.executable, str(SCRIPT), "--workspace",
                                 str(self.root), "--operation", op, "--json"],
                                text=True, capture_output=True)
        return result, json.loads(result.stdout)

    def test_unclassified_is_inspect_only(self):
        r, d = self.check("personal-rules")
        self.assertEqual(r.returncode, 2)
        self.assertEqual(d["reason"], "missing_declaration")
        r, d = self.check("inspect")
        self.assertEqual(r.returncode, 0)

    def test_personal_allows_personal_mode(self):
        self.marker({"schema_version": 1, "trust_domain": "personal", "policy_owner": "personal"})
        for op in ("personal-rules", "personal-export", "personal-onboard"):
            r, d = self.check(op)
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertTrue(d["allowed"])

    def test_employer_denies_all_personal_operations(self):
        self.marker({"schema_version": 1, "trust_domain": "employer", "policy_owner": "organization"})
        for op in ("personal-rules", "personal-export", "personal-onboard"):
            r, d = self.check(op)
            self.assertEqual(r.returncode, 2)
            self.assertFalse(d["allowed"])
            self.assertEqual(d["reason"], "employer_boundary")
        self.assertEqual(self.check("inspect")[0].returncode, 0)

    def test_owner_mismatch_denies(self):
        self.marker({"schema_version": 1, "trust_domain": "personal", "policy_owner": "organization"})
        self.assertEqual(self.check("personal-onboard")[0].returncode, 2)

    def test_dual_declaration_denies(self):
        self.marker({"schema_version": 1, "trust_domain": "personal", "policy_owner": "personal"})
        self.marker({"schema_version": 1, "trust_domain": "employer", "policy_owner": "organization"}, "workspace.local.json")
        self.assertEqual(self.check("personal-rules")[1]["reason"], "multiple_declarations")

    def test_symlinked_declaration_denies(self):
        outside = self.root / "marker.txt"
        outside.write_text('{"schema_version":1,"trust_domain":"personal","policy_owner":"personal"}')
        marker = self.root / ".ai-rules" / "workspace.json"
        marker.parent.mkdir()
        marker.symlink_to(outside)
        self.assertEqual(self.check("personal-onboard")[0].returncode, 2)

    def test_excess_keys_are_rejected(self):
        self.marker({"schema_version": 1, "trust_domain": "personal", "policy_owner": "personal",
                     "company_specific_rules": ["private"]})
        r, d = self.check("personal-export")
        self.assertEqual(r.returncode, 2)
        self.assertNotIn("private", r.stdout)

if __name__ == "__main__":
    unittest.main()
