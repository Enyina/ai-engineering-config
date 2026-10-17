"""Contract tests for hierarchical, domain-isolated rule resolution and safe rendering."""
import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BIN = ROOT / "bin" / "ai-rules"
PERSONAL = ROOT / "policies" / "personal" / "policy.json"

class HierarchyTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
        self.workspace = self.base / "workspace"
        self.workspace.mkdir()
        self.pack = self.base / "pack"
        self.pack.mkdir()
        self.policy = json.loads(PERSONAL.read_text())
        self.save()
        self.make_repo("Enyina/moatt")
        self.marker("personal")

    def save(self):
        (self.pack / "policy.json").write_text(json.dumps(self.policy))

    def marker(self, domain):
        d = self.workspace / ".ai-rules"
        d.mkdir(exist_ok=True)
        (d / "workspace.json").write_text(json.dumps({
            "schema_version":1, "trust_domain":domain,
            "policy_owner":"personal" if domain == "personal" else "organization"}))

    def make_repo(self, repo):
        subprocess.run(["git","init","-q",str(self.workspace)], check=True)
        subprocess.run(["git","-C",str(self.workspace),"remote","remove","origin"],capture_output=True)
        subprocess.run(["git","-C",str(self.workspace),"remote","add","origin",
                        "https://github.com/"+repo+".git"],check=True)

    def invoke(self, command, project="moatt", *args, json_output=True):
        argv = [sys.executable,str(BIN),command,"--policy-root",str(self.pack),
                "--workspace",str(self.workspace),"--project",project,*args]
        result = subprocess.run(argv,capture_output=True,text=True,timeout=10)
        return result, json.loads(result.stdout) if result.returncode in (0,1) and result.stdout.strip() else {}

    def test_validate_succeeds(self):
        result,_ = self.invoke("validate")
        self.assertEqual(result.returncode,0,result.stderr)

    def test_moatt_inherits_parent_system_and_overrides_preference(self):
        r,body = self.invoke("resolve","moatt","--feature","garment-editor")
        self.assertEqual(r.returncode,0,r.stderr)
        self.assertIn("system/web-foundation",body["layers"])
        self.assertIn("system/garment-workbench",body["layers"])
        self.assertEqual(body["preferences"]["test_focus"]["source"],"project/moatt")
        self.assertEqual(body["preferences"]["interaction_mode"]["source"],"feature/garment-editor")
        self.assertIn("editor.pointer",[x["id"] for x in body["guidance"]])
        self.assertNotIn("game.frame",[x["id"] for x in body["guidance"]])
        self.assertIn("security.privacy",[x["id"] for x in body["required"]])

    def test_portfolio_does_not_get_moatt_or_game_rules(self):
        self.make_repo("Enyina/newPortfolio")
        r,body = self.invoke("resolve","portfolio","--feature","admin-dashboard")
        self.assertEqual(r.returncode,0,r.stderr)
        ids = [x["id"] for x in body["required"]+body["guidance"]]
        self.assertIn("web.admin",ids)
        self.assertNotIn("editor.pointer",ids)
        self.assertNotIn("game.frame",ids)

    def test_gaming_does_not_get_product_rules(self):
        self.make_repo("Enyina/game-reverse-engineering-lab")
        r,body = self.invoke("resolve","gaming","--feature","time-arena")
        self.assertEqual(r.returncode,0,r.stderr)
        ids = [x["id"] for x in body["required"]+body["guidance"]]
        self.assertIn("game.frame",ids)
        self.assertNotIn("web.admin",ids)
        self.assertNotIn("editor.pointer",ids)

    def test_missing_marker_shows_update_hint(self):
        (self.workspace / ".ai-rules" / "workspace.json").unlink()
        r, _ = self.invoke("resolve")
        self.assertEqual(r.returncode, 2)
        self.assertIn("Missing trust-domain marker", r.stderr)
        self.assertIn("git -C <workspace> pull --ff-only", r.stderr)

    def test_conflicting_markers_are_not_silently_accepted(self):
        existing = (self.workspace / ".ai-rules" / "workspace.json").read_text()
        (self.workspace / ".ai-rules" / "workspace.local.json").write_text(existing)
        r, _ = self.invoke("resolve")
        self.assertEqual(r.returncode, 2)
        self.assertIn("Conflicting trust-domain markers", r.stderr)

    def test_wrong_origin_detected_before_missing_marker(self):
        (self.workspace / ".ai-rules" / "workspace.json").unlink()
        self.make_repo("OtherOwner/otherRepo")
        r, _ = self.invoke("resolve")
        self.assertEqual(r.returncode, 2)
        self.assertIn("Git origin differs", r.stderr)
        self.assertNotIn("Missing trust-domain marker", r.stderr)

    def test_other_employer_denies_personal_policy(self):
        self.marker("employer")
        r,_ = self.invoke("resolve")
        self.assertEqual(r.returncode,2)
        self.assertIn("trust domain",r.stderr)

    def employer(self,org):
        self.policy["trust_domain"]="employer"
        self.policy["owner"]=org
        self.policy["organizations"]={org:{"rules":[],"preferences":{"review_style":"organization-owned review"}}}
        self.policy["systems"]={"shared-platform":{"organization":org,"parents":[],"rules":["crosssystem.contracts"],"preferences":{"test_focus":"shared integration"}}}
        self.policy["projects"]={
            "api":{"organization":org,"repository":org+"/api","systems":["shared-platform"],
                   "categories":[],"rules":[],"preferences":{"test_focus":"API contract tests"},
                   "features":{"payments":{"rules":[],"preferences":{"test_focus":"idempotent payment tests"}}}},
            "mobile":{"organization":org,"repository":org+"/mobile","systems":["shared-platform"],
                      "categories":[],"rules":[],"preferences":{},"features":{}}
        }
        self.save()
        self.marker("employer")

    def test_employer_policy_multiple_projects_shared_system(self):
        self.employer("companya")
        self.make_repo("companya/api")
        r,body = self.invoke("resolve","api","--feature","payments")
        self.assertEqual(r.returncode,0,r.stderr)
        self.assertIn("system/shared-platform",body["layers"])
        self.assertEqual(body["preferences"]["test_focus"]["value"],"idempotent payment tests")
        self.make_repo("companya/mobile")
        r,body = self.invoke("resolve","mobile")
        self.assertEqual(r.returncode,0,r.stderr)
        self.assertEqual(body["preferences"]["test_focus"]["source"],"system/shared-platform")

    def test_cross_employer_policy_cannot_target_other_employer_repo(self):
        self.employer("companya")
        self.make_repo("companyb/api")
        r,_ = self.invoke("resolve","api")
        self.assertEqual(r.returncode,2)
        self.assertIn("Repository mismatch",r.stderr)

    def test_employer_policy_not_allowed_inside_personal_repo(self):
        self.employer("companya")
        r = subprocess.run([sys.executable,str(BIN),"validate","--policy-root",str(ROOT),
                           "--project","api"],capture_output=True,text=True)
        self.assertNotEqual(r.returncode,0)

    def test_system_cycle_is_rejected(self):
        self.policy["systems"]["web-foundation"]["parents"]=["garment-workbench"]
        self.save()
        r,_ = self.invoke("validate")
        self.assertEqual(r.returncode,2)
        self.assertIn("cycle",r.stderr)

    def test_conflicting_system_preferences_fail_without_project_resolution(self):
        self.policy["systems"]["another"]={"organization":"personal","parents":[],"rules":[],
                                            "preferences":{"rendering":"other system"}}
        p=self.policy["projects"]["moatt"]
        p["systems"]=["garment-workbench","another"]
        self.save()
        r,_ = self.invoke("resolve")
        self.assertEqual(r.returncode,2)
        self.assertIn("Conflicting",r.stderr)

    def test_cross_system_preference_explicitly_resolved(self):
        self.policy["systems"]["another"]={"organization":"personal","parents":[],"rules":[],
                                            "preferences":{"rendering":"other system"}}
        p=self.policy["projects"]["moatt"]
        p["systems"]=["garment-workbench","another"]
        p["preferences"]["rendering"]="user-approved final renderer"
        self.save()
        r,body=self.invoke("resolve")
        self.assertEqual(r.returncode,0,r.stderr)
        self.assertEqual(body["preferences"]["rendering"]["source"],"project/moatt")

    def test_multi_agent_render_is_preview_only_by_default(self):
        r,body=self.invoke("render")
        self.assertEqual(r.returncode,0,r.stderr)
        self.assertEqual(len(body["actions"]),4)
        self.assertFalse((self.workspace/"AGENTS.md").exists())
        self.assertEqual(body["applied"],False)

    def test_all_agents_render_managed_files(self):
        r,body=self.invoke("onboard","moatt","--apply")
        self.assertEqual(r.returncode,0,r.stderr)
        self.assertTrue(body["applied"])
        self.assertIn("Mandatory requirements",(self.workspace/"AGENTS.md").read_text())
        self.assertIn("Mandatory requirements",(self.workspace/"CLAUDE.md").read_text())
        self.assertIn("alwaysApply: true",(self.workspace/".cursor/rules/ai-engineering-managed.mdc").read_text())
        self.assertTrue((self.workspace/".ai-rules/INSTRUCTIONS.md").is_file())
        self.assertFalse((self.workspace/"GEMINI.md").exists(),
                         "Antigravity shares AGENTS.md to avoid duplicated project rules")
        r,body=self.invoke("sync")
        self.assertEqual(r.returncode,0,r.stderr)
        self.assertTrue(body["in_sync"])

    def test_write_refuses_preexisting_manually_edited_agent_file(self):
        (self.workspace/"AGENTS.md").write_text("personal instructions\n")
        r,_=self.invoke("onboard","moatt","--apply")
        self.assertEqual(r.returncode,2)
        self.assertEqual((self.workspace/"AGENTS.md").read_text(),"personal instructions\n")

    def test_managed_edit_is_not_overwritten(self):
        self.assertEqual(self.invoke("onboard","moatt","--apply")[0].returncode,0)
        (self.workspace/"AGENTS.md").write_text("hand-edited text")
        r,_=self.invoke("render","moatt","--apply")
        self.assertEqual(r.returncode,2)
        self.assertEqual((self.workspace/"AGENTS.md").read_text(),"hand-edited text")

    def test_sync_detects_drift_without_writing(self):
        self.assertEqual(self.invoke("onboard","moatt","--apply")[0].returncode,0)
        (self.workspace/"CLAUDE.md").write_text("manual edit")
        r,body=self.invoke("sync")
        self.assertEqual(r.returncode,1)
        self.assertFalse(body["in_sync"])
        self.assertEqual((self.workspace/"CLAUDE.md").read_text(),"manual edit")

    def test_invalid_feature_rejected(self):
        self.assertEqual(self.invoke("resolve","moatt","--feature","not-real")[0].returncode,2)

    def test_policy_path_directory_escape_is_not_allowed(self):
        target = self.workspace/".cursor"
        target.symlink_to(self.base, target_is_directory=True)
        r,_=self.invoke("onboard","moatt","--apply")
        self.assertEqual(r.returncode,2)

if __name__=="__main__":
    unittest.main()
