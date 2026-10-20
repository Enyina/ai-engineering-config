"""Synthetic community users cannot rewrite the owner's rules."""
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
LEARN=ROOT/"bin/rule-learn"
USE=ROOT/"bin/use"

class PublicProductTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base=Path(self.tmp.name)
        self.bin=self.base/"bin"
        self.bin.mkdir()
        self.workspace=self.base/"project"
        self.workspace.mkdir()
        subprocess.run(["git","init","-q",str(self.workspace)],check=True)
        self.event=self.base/"proposal.json"
        self.event.write_text(json.dumps({
            "schema_version":1,
            "title":"Confirm why retries can repeat payment results",
            "problem":"A retried action might be executed twice after a timeout.",
            "lesson":"Verify the external result before repeating irreversible operations.",
            "scope":"general","category":None,
            "evidence":[{"kind":"test","reference":"public synthetic fixture",
                         "finding":"Repeated simulated calls trigger a duplicate outcome.",
                         "checked":True}],
            "limitations":"One isolated simulation; other implementations may differ.",
            "verification":"Run duplicate and ambiguous-timeout regression checks.",
            "privacy_review":True,"sharing_consent":False
        }))
        self.storage=self.base/"storage"
        self.set_identity(445566,"OtherBuilder")
        self.remote("OtherBuilder/project")

    def set_identity(self,user_id,login):
        # Fake the actual GitHub CLI protocol; production uses GitHub API.
        path=self.bin/"gh"
        data=json.dumps({"id":user_id,"login":login})
        path.write_text("#!/bin/sh\nprintf '%s\\n' '"+data+"'\n")
        path.chmod(0o755)

    def remote(self,github_path):
        subprocess.run(["git","-C",str(self.workspace),"remote","remove","origin"],
                       capture_output=True)
        subprocess.run(["git","-C",str(self.workspace),"remote","add","origin",
                        "https://github.com/"+github_path+".git"],check=True)

    def invoke(self,script,*args):
        env=dict(os.environ,PATH=str(self.bin)+os.pathsep+os.environ.get("PATH",""),
                 HOME=str(self.base))
        return subprocess.run([sys.executable,str(script),*args],env=env,
                              cwd=self.workspace,capture_output=True,text=True,timeout=30)

    def test_other_user_gets_only_local_user_proposal(self):
        result=self.invoke(LEARN,"--event",str(self.event),"--apply",
                           "--storage",str(self.storage))
        self.assertEqual(result.returncode,0,result.stderr)
        obj=json.loads(result.stdout)
        self.assertEqual(obj["authenticated_role"],"contributor")
        self.assertEqual(obj["destination"],"user_private")
        self.assertFalse(obj["personal_rules_changed"])
        self.assertFalse(obj["shared_rules_changed"])
        self.assertFalse(obj["saved_locally"] is False)
        self.assertEqual(len(list((self.storage/"users/445566/proposals").glob("*.json"))),1)
        self.assertFalse((self.storage/"owner-private").exists())

    def test_only_verified_owner_routes_to_owner_private(self):
        self.set_identity(91235626,"Enyina")
        r=self.invoke(LEARN,"--event",str(self.event),"--apply",
                      "--storage",str(self.storage))
        self.assertEqual(r.returncode,0,r.stderr)
        data=json.loads(r.stdout)
        self.assertEqual(data["destination"],"owner_private")
        self.assertTrue(list((self.storage/"owner-private/proposals").glob("*.json")))
        self.assertFalse((ROOT/"policies/personal/proposals").exists())

    def test_lookalike_git_name_is_not_owner(self):
        self.set_identity(445566,"Enyina")
        r=self.invoke(LEARN,"--event",str(self.event))
        self.assertEqual(r.returncode,0,r.stderr)
        self.assertEqual(json.loads(r.stdout)["authenticated_role"],"contributor")

    def test_git_commit_author_is_not_identity(self):
        subprocess.run(["git","-C",str(self.workspace),"config","user.name","Enyina"],check=True)
        subprocess.run(["git","-C",str(self.workspace),"config","user.email",
                        "enyina@example.com"],check=True)
        r=self.invoke(LEARN,"--event",str(self.event))
        self.assertEqual(json.loads(r.stdout)["authenticated_role"],"contributor")

    def test_poor_evidence_stays_unpromoted(self):
        data=json.loads(self.event.read_text())
        data["evidence"][0]["checked"]=False
        self.event.write_text(json.dumps(data))
        r=self.invoke(LEARN,"--event",str(self.event),"--apply",
                      "--storage",str(self.storage))
        self.assertEqual(r.returncode,0,r.stderr)
        self.assertEqual(json.loads(r.stdout)["status"],"needs_more_evidence")

    def test_secrets_fail_privacy_screen(self):
        data=json.loads(self.event.read_text())
        data["lesson"]="Don't copy API_KEY=secret_secret_value_12345 into reports"
        self.event.write_text(json.dumps(data))
        r=self.invoke(LEARN,"--event",str(self.event),"--apply",
                      "--storage",str(self.storage))
        self.assertEqual(r.returncode,2)
        self.assertFalse(self.storage.exists())

    def test_dry_run_does_not_write(self):
        r=self.invoke(LEARN,"--event",str(self.event),"--storage",str(self.storage))
        self.assertEqual(r.returncode,0,r.stderr)
        self.assertFalse(self.storage.exists())

    def test_external_user_can_use_shared_rules_without_owner_pack(self):
        r=self.invoke(USE,"--workspace",str(self.workspace),"--apply")
        self.assertEqual(r.returncode,0,r.stderr)
        agents=(self.workspace/"AGENTS.md").read_text()
        self.assertIn("Shared engineering guidance",agents)
        self.assertNotIn("Moatt",agents)
        self.assertNotIn("garment-workbench",agents)
        self.assertNotIn("Enyina",agents)
        self.assertTrue((self.workspace/"CLAUDE.md").exists())
        self.assertTrue((self.workspace/".cursor/rules/shared-engineering.mdc").exists())
        self.assertEqual((self.workspace/".ai-rules/workspace.json").exists(),True)

    def test_shared_setup_preserves_existing_instruction(self):
        path=self.workspace/"AGENTS.md"
        path.write_text("# My existing rules\n")
        r=self.invoke(USE,"--workspace",str(self.workspace),"--apply")
        self.assertEqual(r.returncode,0,r.stderr)
        self.assertTrue(path.read_text().startswith("# My existing rules"))
        again=self.invoke(USE,"--workspace",str(self.workspace),"--apply")
        self.assertEqual(again.returncode,0,again.stderr)
        self.assertEqual(path.read_text().count("<!-- shared-ai-rules:begin -->"),1)

    def test_shared_setup_does_not_touch_other_users_repo(self):
        self.remote("Enyina/moatt")
        r=self.invoke(USE,"--workspace",str(self.workspace),"--apply")
        self.assertEqual(r.returncode,2)
        self.assertFalse((self.workspace/"AGENTS.md").exists())

    def test_employer_marker_denied_even_with_matching_login(self):
        marker=self.workspace/".ai-rules/workspace.json"
        marker.parent.mkdir()
        marker.write_text(json.dumps({"schema_version":1,"trust_domain":"employer",
                                       "policy_owner":"organization"}))
        r=self.invoke(USE,"--workspace",str(self.workspace),"--apply")
        self.assertEqual(r.returncode,2)
        self.assertFalse((self.workspace/"AGENTS.md").exists())

    def test_no_unauthenticated_owner_promotion(self):
        (self.bin/"gh").unlink()
        r=self.invoke(LEARN,"--event",str(self.event))
        self.assertEqual(r.returncode,0)
        self.assertEqual(json.loads(r.stdout)["authenticated_role"],"unverified")

    def test_public_shared_rule_is_not_owner_only(self):
        self.assertIn("Shared engineering guidance",
                      (ROOT/"rules/shared/BASE.md").read_text())

if __name__=="__main__":
    unittest.main()
