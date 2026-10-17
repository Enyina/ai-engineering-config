"""Friendly one-sentence UX/UI and coding advisor, with strict workspace isolation."""
import subprocess
import sys
import tempfile
import unittest
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
ASK=ROOT/"bin"/"ask"

class FriendlyAskTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.workspace=Path(self.tmp.name)/"project"
        self.workspace.mkdir()
        subprocess.run(["git","init","-q",str(self.workspace)],check=True)
        subprocess.run(["git","-C",str(self.workspace),"remote","add","origin",
                        "https://github.com/Enyina/moatt.git"],check=True)
        self.marker("personal")

    def marker(self,kind):
        d=self.workspace/".ai-rules"
        d.mkdir(exist_ok=True)
        (d/"workspace.json").write_text(json.dumps({
            "schema_version":1,"trust_domain":kind,
            "policy_owner":"personal" if kind=="personal" else "organization"}))

    def ask(self,*words,cwd=None):
        return subprocess.run([sys.executable,str(ASK),*words],cwd=cwd or self.workspace,
                              capture_output=True,text=True,timeout=25)

    def test_one_sentence_autodetects_personal_project_and_design(self):
        out=self.ask("make the clothing editor easier to use")
        self.assertEqual(out.returncode,0,out.stderr)
        self.assertIn("Personal project advice",out.stdout)
        self.assertIn("Rules selected for: moatt",out.stdout)
        self.assertIn("Research to check",out.stdout)
        self.assertIn("Watch out:",out.stdout)
        self.assertNotIn('"trust_domain"',out.stdout)
        self.assertFalse((self.workspace/"CLAUDE.md").exists())

    def test_automatic_engineering_detection(self):
        out=self.ask("make the webhook retry more reliable")
        self.assertEqual(out.returncode,0,out.stderr)
        self.assertIn("Retry safely",out.stdout)
        self.assertNotIn("studio-panels",out.stdout)

    def test_project_inside_git_subdirectory_is_detected(self):
        child=self.workspace/"deep"/"screen"
        child.mkdir(parents=True)
        out=self.ask("improve the mannequin layout",cwd=child)
        self.assertEqual(out.returncode,0,out.stderr)
        self.assertIn("moatt",out.stdout)

    def test_unknown_git_origin_must_not_inherit_moatt_rules(self):
        subprocess.run(["git","-C",str(self.workspace),"remote","set-url","origin",
                        "https://github.com/another-org/secret.git"],check=True)
        out=self.ask("improve the garment editor")
        self.assertEqual(out.returncode,2)
        self.assertNotIn("Rules selected for: moatt",out.stdout)

    def test_missing_origin_is_not_silently_assigned(self):
        subprocess.run(["git","-C",str(self.workspace),"remote","remove","origin"],check=True)
        out=self.ask("improve the garment editor")
        self.assertEqual(out.returncode,2)
        self.assertIn("connection is missing",out.stderr)
        self.assertFalse((self.workspace/"AGENTS.md").exists())

    def test_employer_marker_only_returns_advice_not_active_rules(self):
        self.marker("employer")
        out=self.ask("improve accessible dashboard navigation")
        self.assertEqual(out.returncode,0,out.stderr)
        self.assertIn("Workplace advice",out.stdout)
        self.assertIn("NOT employer rules",out.stdout)
        self.assertNotIn("Rules selected for: moatt",out.stdout)

    def test_unknown_marker_does_not_guess_employer(self):
        (self.workspace/".ai-rules"/"workspace.json").unlink()
        out=self.ask("improve accessible dashboard navigation")
        self.assertEqual(out.returncode,2)
        self.assertIn("verified owner marker",out.stderr)

    def test_explicit_work_mode_without_project_does_not_require_config(self):
        out=self.ask("--work","improve accessible dashboard navigation",cwd=Path(self.tmp.name))
        self.assertEqual(out.returncode,0,out.stderr)
        self.assertIn("NOT employer rules",out.stdout)
        self.assertNotIn("moatt",out.stdout.lower())
    
    def test_force_engineering_works_for_ambiguous_words(self):
        out=self.ask("--code","improve editor state")
        self.assertEqual(out.returncode,0,out.stderr)
        self.assertIn("Personal project advice",out.stdout)
        self.assertIn("state",out.stdout.lower())

    def test_simple_help(self):
        out=subprocess.run([sys.executable,str(ASK),"--help"],capture_output=True,text=True)
        self.assertEqual(out.returncode,0)
        self.assertIn("ordinary language",out.stdout)

if __name__=="__main__":
    unittest.main()
