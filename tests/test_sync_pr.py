"""Opt-in PR sync safety: preview only, no remote writes or GH auth required."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/"bin"/"ai-rules-sync-pr"

class SafePrSync(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.workspace=Path(self.tmp.name)
        subprocess.run(["git","init","-q",str(self.workspace)],check=True)
        subprocess.run(["git","-C",str(self.workspace),"remote","add","origin",
                        "https://github.com/Enyina/moatt.git"],check=True)
        subprocess.run(["git","-C",str(self.workspace),"config","user.name","CI Fixture"],check=True)
        subprocess.run(["git","-C",str(self.workspace),"config","user.email","fixture@example.invalid"],check=True)
        (self.workspace/".ai-rules").mkdir()
        (self.workspace/".ai-rules"/"workspace.json").write_text(
            '{"schema_version":1,"trust_domain":"personal","policy_owner":"personal"}')
        subprocess.run(["git","-C",str(self.workspace),"add","-A"],check=True)
        subprocess.run(["git","-C",str(self.workspace),"commit","-q","-m","fixture"],check=True)

    def cmd(self,*args):
        return subprocess.run([sys.executable,str(SCRIPT),"--workspace",str(self.workspace),
                               "--project","moatt",*args],capture_output=True,text=True)

    def test_preview_does_not_create_branch_or_files(self):
        r=self.cmd()
        self.assertEqual(r.returncode,0,r.stderr)
        data=json.loads(r.stdout)
        self.assertFalse(data["applied"])
        self.assertFalse(data["external_write"])
        self.assertFalse((self.workspace/"AGENTS.md").exists())
        branch=subprocess.run(["git","-C",str(self.workspace),"branch","--show-current"],
                              capture_output=True,text=True).stdout.strip()
        self.assertNotIn("ai-rules/",branch)

    def test_unrelated_uncommitted_changes_refuse_pr(self):
        (self.workspace/"unrelated.txt").write_text("unrelated")
        self.assertEqual(self.cmd().returncode,2)

    def test_existing_unmanaged_agents_refuse_pr(self):
        (self.workspace/"AGENTS.md").write_text("Don't overwrite")
        subprocess.run(["git","-C",str(self.workspace),"add","AGENTS.md"],check=True)
        subprocess.run(["git","-C",str(self.workspace),"commit","-q","-m","existing"],check=True)
        r=self.cmd()
        self.assertEqual(r.returncode,2)
        self.assertEqual((self.workspace/"AGENTS.md").read_text(),"Don't overwrite")

    def test_invalid_branch_refuses(self):
        self.assertEqual(self.cmd("--branch","evil/name/../escape").returncode,2)

if __name__=="__main__":
    unittest.main()
