"""Isolated lesson approval test: no live customer/employer data."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
LESSON=ROOT/"bin"/"ai-lessons"
BASE=json.loads((ROOT/"policies"/"personal"/"policy.json").read_text())

class LearningProposals(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.folder=Path(self.tmp.name)
        self.pack=self.folder/"pack"
        self.pack.mkdir()
        (self.pack/"policy.json").write_text(json.dumps(BASE))
        self.workspace=self.folder/"repo"
        self.workspace.mkdir()
        (self.workspace/".ai-rules").mkdir()
        (self.workspace/".ai-rules"/"workspace.json").write_text(
            '{"schema_version":1,"trust_domain":"personal","policy_owner":"personal"}')
        subprocess.run(["git","init","-q",str(self.workspace)],check=True)
        subprocess.run(["git","-C",str(self.workspace),"remote","add","origin",
                        "git@github.com:Enyina/moatt.git"],check=True)
        self.event_file=self.folder/"input.json"
        self.data={"schema_version":1,"project":"moatt",
                   "title":"Interaction exclusivity","observation":"One gesture was interpreted twice.",
                   "evidence":"Isolated pointer interaction test with synthetic fixture.",
                   "candidate_rule":"Viewport tools need explicit exclusive interaction modes.",
                   "scope":"category","affected_projects":["moatt"],
                   "regression_test":"Pointer test confirms draw action does not orbit.",
                   "privacy_review":"sanitized_and_authorized"}
        self.save()

    def save(self):
        self.event_file.write_text(json.dumps(self.data))

    def call(self,*extra):
        r=subprocess.run([sys.executable,str(LESSON),"--event",str(self.event_file),
                          "--policy-root",str(self.pack),"--workspace",str(self.workspace),
                          *extra],text=True,capture_output=True,timeout=10)
        return r

    def test_dry_run_never_creates_rule_or_proposal(self):
        r=self.call()
        self.assertEqual(r.returncode,0,r.stderr)
        self.assertFalse((self.pack/"proposals").exists())
        self.assertFalse((self.pack/"rules").exists())

    def test_proposal_is_not_active_policy_rule(self):
        r=self.call("--apply")
        self.assertEqual(r.returncode,0,r.stderr)
        result=json.loads(r.stdout)
        self.assertFalse(result["active_rule_changed"])
        self.assertEqual(len(list((self.pack/"proposals").glob("*.json"))),1)
        self.assertEqual(BASE,json.loads((self.pack/"policy.json").read_text()))
        self.assertEqual(self.call("--apply").returncode,2)

    def test_cross_domain_affected_project_rejected(self):
        self.data["affected_projects"]=["othercompany"]
        self.save()
        r=self.call("--apply")
        self.assertEqual(r.returncode,2)
        self.assertFalse((self.pack/"proposals").exists())

    def test_privacy_review_required(self):
        self.data["privacy_review"]="pending"
        self.save()
        self.assertEqual(self.call("--apply").returncode,2)

    def test_token_shaped_secret_rejected(self):
        self.data["evidence"]="Bearer "+"ab" * 18
        self.save()
        self.assertEqual(self.call("--apply").returncode,2)

    def test_employer_workspace_rejected_from_personal_pack(self):
        (self.workspace/".ai-rules"/"workspace.json").write_text(
            '{"schema_version":1,"trust_domain":"employer","policy_owner":"organization"}')
        self.assertEqual(self.call("--apply").returncode,2)

if __name__=="__main__":
    unittest.main()
