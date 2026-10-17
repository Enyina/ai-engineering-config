"""One-time setup is reversible, project-scoped and refuses unknown employers."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/"bin"/"setup"
BEGIN="<!-- ai-engineering-setup:begin -->"

class FreshComputerSetupTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base=Path(self.tmp.name)
        self.projects=self.base/"Projects"
        self.projects.mkdir()
        self.personal=self.make_repo("moatt","Enyina/moatt","personal")
        self.work=self.make_repo("company","ExampleCo/work","employer")
        self.state=self.base/"setup-state"

    def make_repo(self,name,origin,domain):
        folder=self.projects/name
        folder.mkdir()
        subprocess.run(["git","init","-q",str(folder)],check=True)
        subprocess.run(["git","-C",str(folder),"remote","add","origin",
                        "https://github.com/"+origin+".git"],check=True)
        rules=folder/".ai-rules"
        rules.mkdir()
        (rules/"workspace.json").write_text(json.dumps({
            "schema_version":1,"trust_domain":domain,
            "policy_owner":"personal" if domain=="personal" else "organization"}))
        return folder

    def call(self,*arguments):
        return subprocess.run([sys.executable,str(SCRIPT),"--projects-root",
            str(self.projects),"--state-dir",str(self.state),*arguments],
            capture_output=True,text=True,timeout=30)

    def test_first_run_offers_download_but_decline_writes_nothing(self):
        import runpy
        mod=runpy.run_path(str(SCRIPT))
        fn=mod["get_personal_projects"]
        globals_=fn.__globals__
        old=globals_.get("input")
        globals_["input"]=lambda prompt: "n"
        try:
            fn(self.projects,{"moatt":"enyina/moatt","portfolio":"enyina/newPortfolio"})
        finally:
            if old is None:
                globals_.pop("input",None)
            else:
                globals_["input"]=old
        self.assertFalse((self.projects/"portfolio").exists())

    def test_first_run_uses_only_approved_project_urls(self):
        import runpy
        from types import SimpleNamespace
        mod=runpy.run_path(str(SCRIPT))
        fn=mod["get_personal_projects"]
        globals_=fn.__globals__
        old_input=globals_.get("input")
        old_command=globals_["command"]
        calls=[]
        globals_["input"]=lambda prompt: "y"
        def fake_git(argv,timeout=15):
            calls.append(argv)
            return SimpleNamespace(returncode=0)
        globals_["command"]=fake_git
        try:
            fn(self.projects,{"moatt":"enyina/moatt","portfolio":"enyina/newPortfolio",
                              "gaming":"enyina/unverified-game"})
        finally:
            if old_input is None:
                globals_.pop("input",None)
            else:
                globals_["input"]=old_input
            globals_["command"]=old_command
        self.assertEqual(len(calls),1)
        self.assertEqual(calls[0][0:3],["git","clone","--quiet"])
        self.assertEqual(calls[0][3],"https://github.com/enyina/newPortfolio.git")
        self.assertNotIn("unverified-game",str(calls))

    def test_one_command_default_is_preview_without_terminal_confirmation(self):
        (self.personal/"AGENTS.md").write_text("# My project rules\n")
        r=self.call()
        self.assertEqual(r.returncode,0,r.stderr)
        self.assertIn("Proposed changes:",r.stdout)
        self.assertIn("Verified personal projects: 1",r.stdout)
        self.assertNotIn("ExampleCo",r.stdout)
        self.assertEqual((self.personal/"AGENTS.md").read_text(),"# My project rules\n")
        self.assertFalse(self.state.exists())

    def test_apply_keeps_existing_instructions_and_creates_supported_adapters(self):
        original="# My own project rules\n\nNever erase this guidance.\n"
        (self.personal/"AGENTS.md").write_text(original)
        (self.personal/"CLAUDE.md").write_text("# Claude instructions\n\n@AGENTS.md\n")
        r=self.call("--apply")
        self.assertEqual(r.returncode,0,r.stderr)
        text=(self.personal/"AGENTS.md").read_text()
        self.assertTrue(text.startswith(original.rstrip("\n")))
        self.assertEqual(text.count(BEGIN),1)
        self.assertIn("Approved shared personal guidance",text)
        self.assertIn("Do not copy credentials",text)
        self.assertNotIn("game.frame",text)
        self.assertEqual((self.personal/"CLAUDE.md").read_text(),
                         "# Claude instructions\n\n@AGENTS.md\n")
        cursor=self.personal/".cursor/rules/ai-engineering-setup.mdc"
        self.assertTrue(cursor.is_file())
        self.assertIn("alwaysApply: true",cursor.read_text())
        self.assertFalse((self.work/"AGENTS.md").exists())
        self.assertFalse((self.work/"CLAUDE.md").exists())
        self.assertTrue((self.state/"setup-state.json").is_file())

    def test_double_install_is_idempotent_and_check_succeeds(self):
        self.assertEqual(self.call("--apply").returncode,0)
        first=(self.personal/"AGENTS.md").read_bytes()
        second=self.call("--apply")
        self.assertEqual(second.returncode,0,second.stderr)
        self.assertIn("Already set up",second.stdout)
        self.assertEqual(first,(self.personal/"AGENTS.md").read_bytes())
        check=self.call("--check")
        self.assertEqual(check.returncode,0,check.stderr)
        self.assertIn("up to date",check.stdout)

    def test_rollback_restores_originals_and_removes_generated_files(self):
        original=b"# Personal design instructions\n"
        (self.personal/"AGENTS.md").write_bytes(original)
        self.assertEqual(self.call("--apply").returncode,0)
        roll=self.call("--rollback")
        self.assertEqual(roll.returncode,0,roll.stderr)
        self.assertEqual((self.personal/"AGENTS.md").read_bytes(),original)
        self.assertFalse((self.personal/"CLAUDE.md").exists())
        self.assertFalse((self.personal/".cursor/rules/ai-engineering-setup.mdc").exists())
        self.assertFalse((self.work/"AGENTS.md").exists())

    def test_rollback_refuses_modified_managed_instructions(self):
        self.assertEqual(self.call("--apply").returncode,0)
        file=self.personal/"CLAUDE.md"
        file.write_text(file.read_text()+"Human changes\n")
        r=self.call("--rollback")
        self.assertEqual(r.returncode,2)
        self.assertIn("changed since setup",r.stderr)
        self.assertIn("Human changes",file.read_text())

    def test_rerun_does_not_overwrite_personal_edits(self):
        self.assertEqual(self.call("--apply").returncode, 0)
        path = self.personal / "AGENTS.md"
        path.write_text(path.read_text() + "\nKeep my later edits.\n")
        result = self.call("--apply")
        self.assertEqual(result.returncode, 2)
        self.assertIn("changed since setup", result.stderr)
        self.assertIn("Keep my later edits", path.read_text())

    def test_no_trust_marker_means_no_personal_changes(self):
        (self.personal/".ai-rules/workspace.json").unlink()
        r=self.call("--apply")
        self.assertEqual(r.returncode,0,r.stderr)
        self.assertIn("Verified personal projects: 0",r.stdout)
        self.assertFalse((self.personal/"AGENTS.md").exists())

    def test_missing_git_origin_is_not_guessed_from_folder_name(self):
        subprocess.run(["git","-C",str(self.personal),"remote","remove","origin"],check=True)
        r=self.call("--apply")
        self.assertEqual(r.returncode,0,r.stderr)
        self.assertIn("Verified personal projects: 0",r.stdout)
        self.assertFalse((self.personal/"AGENTS.md").exists())

    def test_unmanaged_generated_filename_is_not_overwritten(self):
        path=self.personal/".cursor/rules/ai-engineering-setup.mdc"
        path.parent.mkdir(parents=True)
        path.write_text("Hand-written team rules\n")
        r=self.call("--apply")
        self.assertEqual(r.returncode,2)
        self.assertIn("unmanaged Cursor",r.stderr)
        self.assertEqual(path.read_text(),"Hand-written team rules\n")
        self.assertFalse((self.personal/"AGENTS.md").exists())

    def test_project_symlinks_are_refused_before_writing(self):
        other=self.base/"other.txt"
        other.write_text("Do not touch")
        (self.personal/"AGENTS.md").symlink_to(other)
        r=self.call("--apply")
        self.assertEqual(r.returncode,2)
        self.assertEqual(other.read_text(),"Do not touch")
        self.assertFalse(self.state.exists())

    def test_existing_claude_rules_get_readable_reference_not_replaced(self):
        path=self.personal/"CLAUDE.md"
        path.write_text("# Special Claude rules\n\nKeep this context\n")
        r=self.call("--apply")
        self.assertEqual(r.returncode,0,r.stderr)
        self.assertTrue(path.read_text().startswith("# Special Claude rules"))
        self.assertIn("@AGENTS.md",path.read_text())
        self.assertEqual(path.read_text().count(BEGIN),1)

    def test_check_reports_needs_setup_before_install(self):
        r=self.call("--check")
        self.assertEqual(r.returncode,1)
        self.assertIn("needs setup",r.stdout)

if __name__=="__main__":
    unittest.main()
