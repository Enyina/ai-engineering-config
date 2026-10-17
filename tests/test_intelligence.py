"""Personal design/engineering intelligence regression and isolation tests."""
import copy
import json
import runpy
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INTELLIGENCE = ROOT / "bin" / "ai-intelligence"
WATCH = ROOT / "bin" / "ai-source-watch"

class IntelligenceTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.workspace = self.root / "moatt"
        self.workspace.mkdir()
        (self.workspace / ".ai-rules").mkdir()
        self.marker("personal")
        subprocess.run(["git","init","-q",str(self.workspace)],check=True)
        subprocess.run(["git","-C",str(self.workspace),"remote","add","origin",
                        "https://github.com/Enyina/moatt.git"],check=True)

    def marker(self, domain):
        (self.workspace/".ai-rules"/"workspace.json").write_text(json.dumps({
            "schema_version":1,"trust_domain":domain,
            "policy_owner":"personal" if domain=="personal" else "organization"}))

    def cli(self, command, project="moatt", domain="design", task="garment editor layout",
            feature="garment-editor", extra=()):
        argv=[sys.executable,str(INTELLIGENCE),command]
        if command=="suggest":
            argv+=["--workspace",str(self.workspace),"--project",project,
                   "--domain",domain,"--task",task]
            if feature:
                argv+=["--feature",feature]
            argv+=list(extra)
        return subprocess.run(argv,text=True,capture_output=True,timeout=15)

    def test_canonical_source_and_option_catalogs_are_valid(self):
        r=self.cli("validate")
        self.assertEqual(r.returncode,0,r.stderr)
        parsed=json.loads(r.stdout)
        self.assertGreaterEqual(parsed["sources"],12)
        self.assertGreaterEqual(parsed["patterns"],6)
        self.assertEqual(parsed["trust_domain"],"personal")

    def test_moatt_editor_gets_distinct_explainable_options(self):
        r=self.cli("suggest")
        self.assertEqual(r.returncode,0,r.stderr)
        data=json.loads(r.stdout)
        ids=[x["id"] for x in data["matches"]]
        self.assertIn("editor-layout",ids)
        layout=next(x for x in data["matches"] if x["id"]=="editor-layout")
        self.assertGreaterEqual(len(layout["alternatives"]),3)
        self.assertGreaterEqual(len(layout["evidence"]),2)
        self.assertEqual(layout["selection"],"none_preselected")
        self.assertTrue(all(x.get("tradeoff") and x.get("verify")
                            for x in layout["alternatives"]))
        self.assertFalse(data["changes_applied"])

    def test_moatt_cannot_get_portfolio_only_pattern(self):
        r=self.cli("suggest",task="portfolio homepage hero",feature=None)
        self.assertEqual(r.returncode,0,r.stderr)
        self.assertNotIn("product-home",[x["id"] for x in json.loads(r.stdout)["matches"]])

    def test_portfolio_gets_portfolio_not_moatt(self):
        subprocess.run(["git","-C",str(self.workspace),"remote","set-url","origin",
                        "git@github.com:Enyina/newPortfolio.git"],check=True)
        r=self.cli("suggest",project="portfolio",task="portfolio homepage hero",
                   feature="admin-dashboard")
        self.assertEqual(r.returncode,0,r.stderr)
        ids=[x["id"] for x in json.loads(r.stdout)["matches"]]
        self.assertIn("product-home",ids)
        self.assertNotIn("editor-layout",ids)

    def test_engineering_options_are_separate_from_design(self):
        r=self.cli("suggest",domain="engineering",task="integration webhook retry reliability")
        self.assertEqual(r.returncode,0,r.stderr)
        ids=[x["id"] for x in json.loads(r.stdout)["matches"]]
        self.assertIn("service-recovery",ids)
        self.assertNotIn("editor-layout",ids)

    def test_employer_workspace_is_refused_even_for_generic_question(self):
        self.marker("employer")
        r=self.cli("suggest",task="forms")
        self.assertEqual(r.returncode,2)
        self.assertIn("not authorized",r.stderr)
        self.assertNotIn("Enyina",r.stderr)

    def test_wrong_git_origin_refuses_personal_recommendations(self):
        subprocess.run(["git","-C",str(self.workspace),"remote","set-url","origin",
                        "https://github.com/ExampleCompany/private.git"],check=True)
        self.assertEqual(self.cli("suggest").returncode,2)

    def test_no_matching_topic_creates_gap_not_fabricated_rule(self):
        r=self.cli("suggest",task="quantum hyperdrive calibration",feature=None)
        self.assertEqual(r.returncode,0,r.stderr)
        data=json.loads(r.stdout)
        self.assertTrue(data["unmatched"])
        self.assertEqual(data["matches"],[])
        self.assertFalse(data["changes_applied"])

    def test_personal_rule_fallback(self):
        pack=json.loads((ROOT/"policies/personal/policy.json").read_text())
        for id in ("moatt","portfolio","gaming"):
            self.assertIn(id,pack["projects"])
        for id in ("research.options","engineering.source-evidence"):
            self.assertIn(id,pack["global"]["rules"])
        self.assertIn("design.accessibility",pack["categories"]["web-product"]["rules"])
        self.assertNotIn("design.accessibility",pack["categories"]["games"]["rules"])

    def test_rule_provenance_links_existing_sources(self):
        catalog=json.loads((ROOT/"knowledge/sources/catalog.json").read_text())
        refs={source["id"] for source in catalog["sources"]}
        evidence=json.loads((ROOT/"knowledge/rule-evidence.json").read_text())
        for rule,meta in evidence["rule_sources"].items():
            self.assertTrue(meta["sources"],rule)
            self.assertTrue(all(src in refs for src in meta["sources"]),rule)

class SourceWatchTests(unittest.TestCase):
    def setUp(self):
        self.mod=runpy.run_path(str(WATCH))
        self.catalog=json.loads((ROOT/"knowledge/sources/catalog.json").read_text())
        self.baseline={"schema_version":1,"owner":"personal","sources":{}}

    def test_no_network_default_only_reports_unknown_freshness(self):
        items=self.mod["validate"](self.catalog,self.baseline)
        out=self.mod["evaluate"](items[:3],self.baseline,False,1)
        self.assertTrue(all(x["state"]=="unchecked" for x in out["sources"]))
        self.assertTrue(all(not x["rule_automatically_changed"] for x in out["sources"]))

    def test_nonofficial_host_refused(self):
        evil=copy.deepcopy(self.catalog)
        evil["sources"][0]["url"]="https://localhost:9999/private"
        with self.assertRaises(ValueError):
            self.mod["validate"](evil,self.baseline)

    def test_source_revision_becomes_review_candidate_not_rule(self):
        items=self.mod["validate"](self.catalog,self.baseline)
        one=items[:1]
        self.baseline["sources"][one[0]["id"]]={"etag":"previous"}
        original=self.mod["fetch_metadata"]
        self.mod["fetch_metadata"]=lambda url,timeout: {
            "status":"observed","http_code":200,"etag":"next","last_modified":""}
        try:
            # evaluate's globals belong to its own namespace, so change them there.
            self.mod["evaluate"].__globals__["fetch_metadata"]=self.mod["fetch_metadata"]
            report=self.mod["evaluate"](one,self.baseline,True,1)
        finally:
            self.mod["evaluate"].__globals__["fetch_metadata"]=original
        self.assertEqual(report["sources"][0]["state"],"source_change_candidate")
        self.assertFalse(report["sources"][0]["rule_automatically_changed"])

if __name__ == "__main__":
    unittest.main()
