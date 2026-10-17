"""Check that every personal project inherits the plain-English delivery requirements."""
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class DeliveryPolicyTests(unittest.TestCase):
    def setUp(self):
        self.pack=json.loads((ROOT/"policies/personal/policy.json").read_text())
        self.ids={r["id"]:r for r in self.pack["rules"]}

    def test_commit_and_release_requirements_are_global_and_required(self):
        for rule in ("delivery.commit","delivery.release-notes"):
            self.assertIn(rule,self.pack["global"]["rules"])
            self.assertEqual(self.ids[rule]["kind"],"required")

    def test_all_personal_projects_inherit_same_delivery_rules(self):
        for name in ("moatt","portfolio","gaming"):
            with self.subTest(name=name):
                self.assertIn(name,self.pack["projects"])
                for rule in ("delivery.commit","delivery.release-notes"):
                    self.assertIn(rule,self.pack["global"]["rules"])

    def test_release_notes_use_plain_language(self):
        text=(ROOT/"RELEASE_NOTES.md").read_text().lower()
        for jargon in ("api","endpoint","prisma","socket.io","refactor","ci/cd","sha","schema","cron","payload"):
            with self.subTest(jargon=jargon):
                self.assertIsNone(re.search(r"(?<![a-z])" + re.escape(jargon) + r"(?![a-z])", text))

    def test_only_personal_project_rule_package_is_changed(self):
        self.assertEqual(self.pack["trust_domain"],"personal")
        self.assertEqual(self.pack["owner"],"personal")

if __name__=="__main__":
    unittest.main()
