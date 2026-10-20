"""Evidence claims must have contradictory checks and a verified mechanism."""
import copy
import json
import runpy
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/"bin/evidence-check"
class EvidenceGates(unittest.TestCase):
    def setUp(self):
        self.fn=runpy.run_path(str(SCRIPT))["analyze"]
        self.note={"schema_version":1,
          "problem":{"observed":"Approval fails","expected":"Approval succeeds","scope":"Synthetic test"},
          "evidence":[
             {"id":"e1","kind":"test","finding":"Transition fails under one condition","reference":"test fixture","confidence":"direct"},
             {"id":"e2","kind":"trace","finding":"Alternative path did execute","reference":"trace fixture","confidence":"direct"}],
          "hypotheses":[
             {"id":"h1","explanation":"A state guard rejects the request","status":"supported","supports":["e1"],"contradicts":[]},
             {"id":"h2","explanation":"The request never reached the guard","status":"ruled_out","supports":[],"contradicts":["e2"]}],
          "verification":{"method":"Reproduce the transition","evidence_ids":["e1"],"outcome":"passed"},
          "decision":{"confidence":"confirmed","cause_id":"h1","recommendation":"Fix only with authorization"},
          "learning":{"status":"candidate","scope":"project","reviewed":False}}
    def test_evidence_gate_and_human_review_only(self):
        r=self.fn(self.note)
        self.assertEqual(r["confirmation_gate"],"passed")
        self.assertFalse(r["active_rules_changed"])
    def test_open_alternative_blocks_confirmed(self):
        self.note["hypotheses"][1]["status"]="open"
        with self.assertRaisesRegex(Exception,"Confirmed cause"):
            self.fn(self.note)
    def test_unexecuted_verification_blocks_confirmed(self):
        self.note["verification"]["outcome"]="not_run"
        with self.assertRaisesRegex(Exception,"Confirmed cause"):
            self.fn(self.note)
    def test_report_is_not_direct_evidence(self):
        self.note["evidence"][0]["confidence"]="reported"
        with self.assertRaisesRegex(Exception,"direct evidence"):
            self.fn(self.note)
    def test_missing_contradiction_does_not_rule_out(self):
        self.note["hypotheses"][1]["contradicts"]=[]
        with self.assertRaisesRegex(Exception,"not ruled out"):
            self.fn(self.note)
    def test_wrong_check_cannot_confirm(self):
        self.note["verification"]["evidence_ids"]=["e2"]
        with self.assertRaises(Exception):
            self.fn(self.note)

    def test_unresolved_is_legitimate(self):
        self.note["decision"]["confidence"]="unresolved"
        self.note["hypotheses"][1]["status"]="open"
        self.assertEqual(self.fn(self.note)["confirmation_gate"],"not_met")
    def test_invalid_reference_fails(self):
        self.note["verification"]["evidence_ids"]=["nonexistent"]
        with self.assertRaises(Exception):
            self.fn(self.note)
    def test_process_is_a_required_shared_personal_rule(self):
        pack=json.loads((ROOT/"policies/personal/policy.json").read_text())
        self.assertIn("investigation.evidence-gate",pack["global"]["rules"])
        item=next(x for x in pack["rules"] if x["id"]=="investigation.evidence-gate")
        self.assertEqual(item["kind"],"required")
        self.assertIn("Eliminate possibilities",item["text"])

    def test_anywhere_file_is_self_contained(self):
        process=(ROOT/"USE-ANYWHERE.md").read_text()
        for phase in ("Understand","Investigate","Gather evidence","Eliminate possibilities",
                      "Verify","Recommend","Learn"):
            self.assertIn(phase,process)
        self.assertIn("diagnosis only",process)
        self.assertIn("private",process.lower())

    def test_sample_is_read_only(self):
        with tempfile.TemporaryDirectory() as folder:
            r=subprocess.run([sys.executable,str(SCRIPT),"--sample"],cwd=folder,capture_output=True,text=True)
            self.assertEqual(r.returncode,0,r.stderr)
            self.assertEqual(json.loads(r.stdout)["decision"]["confidence"],"unresolved")
            self.assertEqual(list(Path(folder).iterdir()),[])
    def test_file_check_does_not_echo_observation(self):
        with tempfile.TemporaryDirectory() as folder:
            self.note["problem"]["observed"]="nonpublic-incident-data"
            path=Path(folder)/"local.json"
            original=json.dumps(self.note)
            path.write_text(original)
            r=subprocess.run([sys.executable,str(SCRIPT),str(path)],capture_output=True,text=True)
            self.assertEqual(r.returncode,0,r.stderr)
            self.assertNotIn("nonpublic-incident-data",r.stdout)
            self.assertEqual(path.read_text(),original)
    def test_symlink_is_refused(self):
        with tempfile.TemporaryDirectory() as folder:
            p=Path(folder)/"record.json"
            p.write_text(json.dumps(self.note))
            link=Path(folder)/"link.json"
            link.symlink_to(p)
            r=subprocess.run([sys.executable,str(SCRIPT),str(link)],capture_output=True,text=True)
            self.assertEqual(r.returncode,2)
if __name__=="__main__":
    unittest.main()
