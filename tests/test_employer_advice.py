"""External advice may borrow public/personal guidance but never company policies."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
CLI=ROOT/"bin"/"ai-intelligence"

class EmployerAdvisoryTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name)

    def call(self,*args):
        return subprocess.run([sys.executable,str(CLI),"suggest",
            "--advisory-for-employer","--domain","design",
            "--task","improve accessible dashboard navigation",*args],
            capture_output=True,text=True,timeout=15)

    def test_employer_suggestions_work_before_policy_onboarding(self):
        out=self.call()
        self.assertEqual(out.returncode,0,out.stderr)
        data=json.loads(out.stdout)
        self.assertEqual(data["mode"],"external_suggestions_only")
        self.assertEqual(data["employer_policy_check"],
                         "not_checked_no_employer_context_provided")
        self.assertFalse(data["policy_conflicts_checked"])
        self.assertFalse(data["changes_applied"])
        self.assertFalse(data["employer_rules_modified"])
        self.assertNotIn("task",data)
        self.assertNotIn("ExampleCo",out.stdout)
        self.assertTrue(data["matches"])
        for item in data["matches"]:
            self.assertFalse(item["origin"]["status"].startswith("approved"))
            self.assertTrue(item["evidence"])
            self.assertTrue(all(x["url"].startswith("https://") for x in item["evidence"]))
            self.assertNotIn(item["id"],("editor-layout","product-home"))
        for rule in data["candidate_personal_guidance"]:
            self.assertEqual(rule["status"],"candidate_only_not_employer_policy")
            self.assertEqual(rule["source"]["type"],"personal_generic_rule")
            self.assertIn("ai-engineering-config",rule["source"]["url"])
            self.assertTrue(rule["references"])

    def test_no_company_details_are_ever_echoed(self):
        text="confidential-q7-tenant-identity dashboard"
        r=self.call("--task",text)
        self.assertEqual(r.returncode,0,r.stderr)
        self.assertNotIn(text,r.stdout)
        self.assertNotIn(text,r.stderr)

    def test_no_project_specific_personal_patterns_for_employer(self):
        r=self.call("--task","portfolio homepage or garment editor layout")
        self.assertEqual(r.returncode,0,r.stderr)
        ids=[x["id"] for x in json.loads(r.stdout)["matches"]]
        self.assertNotIn("editor-layout",ids)
        self.assertNotIn("product-home",ids)

    def test_engineering_suggestions_have_provenance(self):
        r=self.call("--domain","engineering","--task","reliability retry webhook")
        self.assertEqual(r.returncode,0,r.stderr)
        out=json.loads(r.stdout)
        self.assertIn("service-recovery",[x["id"] for x in out["matches"]])
        self.assertTrue(all(rule["source"]["type"]=="personal_generic_rule"
                            for rule in out["candidate_personal_guidance"]))
        self.assertNotIn("editor.pointer",str(out))

    def employer(self,valid_marker=True):
        pack=self.root/"exampleco-policy"
        pack.mkdir()
        payload={"schema_version":1,"trust_domain":"employer","owner":"exampleco",
          "rules":[{"id":"org.privacy","kind":"required",
                    "text":"Use approved organizational access controls."}],
          "global":{"rules":["org.privacy"],"preferences":{}},
          "organizations":{"exampleco":{"rules":[],"preferences":{}}},
          "categories":{},"systems":{},
          "projects":{"backend":{"organization":"exampleco",
             "repository":"ExampleCo/backend","systems":[],"categories":[],
             "rules":[],"preferences":{},"features":{}}}}
        (pack/"policy.json").write_text(json.dumps(payload))
        work=self.root/"workspace"
        work.mkdir()
        (work/".ai-rules").mkdir()
        marker={"schema_version":1,
                "trust_domain":"employer" if valid_marker else "personal",
                "policy_owner":"organization" if valid_marker else "personal"}
        (work/".ai-rules"/"workspace.json").write_text(json.dumps(marker))
        subprocess.run(["git","init","-q",str(work)],check=True)
        subprocess.run(["git","-C",str(work),"remote","add","origin",
                        "https://github.com/ExampleCo/backend.git"],check=True)
        return work,pack

    def test_explicit_employer_pack_verified_no_company_rules_exported(self):
        work,pack=self.employer()
        r=self.call("--workspace",str(work),"--project","backend",
                    "--policy-root",str(pack))
        self.assertEqual(r.returncode,0,r.stderr)
        body=json.loads(r.stdout)
        self.assertEqual(body["employer_policy_check"],
                         "employer_pack_workspace_and_origin_checked")
        self.assertFalse(body["policy_conflicts_checked"])
        self.assertNotIn("org.privacy",r.stdout)
        self.assertNotIn("exampleco",r.stdout.lower())
        self.assertFalse(body["employer_rules_modified"])
        self.assertFalse((work/"AGENTS.md").exists())

    def test_mismatched_employer_workspace_rejected(self):
        work,pack=self.employer(False)
        r=self.call("--workspace",str(work),"--project","backend",
                    "--policy-root",str(pack))
        self.assertEqual(r.returncode,2)
        self.assertFalse((work/"AGENTS.md").exists())

    def test_employer_mode_cannot_pass_personal_pack_for_verification(self):
        work,pack=self.employer()
        r=self.call("--workspace",str(work),"--project","backend",
                    "--policy-root",str(ROOT/"policies"/"personal"))
        self.assertEqual(r.returncode,2)

    def test_partial_context_fails_closed(self):
        r=self.call("--workspace",str(self.root))
        self.assertEqual(r.returncode,2)

    def test_old_personal_mode_still_rejects_employer_workspace(self):
        work,pack=self.employer()
        r=subprocess.run([sys.executable,str(CLI),"suggest","--workspace",str(work),
                          "--project","backend","--domain","engineering",
                          "--task","reliability"],capture_output=True,text=True)
        self.assertEqual(r.returncode,2)

    def test_no_employer_advice_unless_explicitly_requested(self):
        r=subprocess.run([sys.executable,str(CLI),"suggest","--domain","design",
                          "--task","dashboard"],capture_output=True,text=True)
        self.assertEqual(r.returncode,2)

    def test_twice_daily_schedule_is_at_eight_and_twenty_wat(self):
        s=(ROOT/".github/workflows/knowledge-source-review.yml").read_text()
        self.assertIn("cron: '0 7,19 * * *'",s)
        self.assertNotIn("cron: '0 9 * * 1'",s)
        self.assertIn("workflow_dispatch",s)

if __name__=="__main__":
    unittest.main()
