"""Local-only command review tests; use synthetic data, never private command text."""
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / 'bin' / 'review-codex-rules.py'

class RuleReviewTests(unittest.TestCase):
    def run_report(self, payload):
        with tempfile.TemporaryDirectory() as tmp:
            rules = Path(tmp) / 'default.rules'
            rules.write_text(payload)
            proc = subprocess.run([sys.executable, str(SCRIPT), '--input', str(rules), '--json'],
                                  capture_output=True, text=True, check=False)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            return json.loads(proc.stdout), rules.read_text()

    def test_classify_and_redact_all_content(self):
        secret_marker = 'PRIVATE-SAMPLE-NOT-A-REAL-TOKEN'
        text = '\n'.join([
            'prefix_rule(pattern=["git", "push"], decision="allow")',
            'prefix_rule(pattern=["git", "status"], decision="allow")',
            'prefix_rule(pattern=["node", "-e", "read patient jwt '+secret_marker+'"], decision="allow")',
            'prefix_rule(pattern=["npm", "run", "build"], decision="allow")'
        ])
        report, original = self.run_report(text)
        self.assertEqual(report['total_rules'], 4)
        self.assertEqual(report['decisions']['allow'], 4)
        self.assertEqual(report['categories']['project_or_sensitive'], 1)
        self.assertEqual(report['categories']['high_impact'], 1)
        self.assertEqual(report['categories']['read_oriented'], 1)
        self.assertEqual(report['categories']['task_specific'], 1)
        self.assertNotIn(secret_marker, json.dumps(report))
        self.assertEqual(original, text)

    def test_allows_no_config_changes_or_silently_installed_rules(self):
        report, _ = self.run_report('prefix_rule(pattern=["rm", "-rf"], decision="allow")')
        self.assertEqual(report['categories']['high_impact'], 1)

    def test_unrecognized_rule_is_not_treated_as_safe(self):
        report, _ = self.run_report('prefix_rule(pattern=[variable], decision="allow")')
        self.assertEqual(report['unparsed'], 1)
        self.assertEqual(report['categories']['unrecognized'], 1)

if __name__ == '__main__':
    unittest.main()
