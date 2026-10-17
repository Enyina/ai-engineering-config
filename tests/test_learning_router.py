import importlib.util
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("learning_router", ROOT / "learning" / "router.py")
router = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = router
spec.loader.exec_module(router)

class LearningRouterTests(unittest.TestCase):
    def test_youtube_routes(self):
        self.assertEqual(router.route("https://youtu.be/abc")["pipelines"], ["video-to-skill"])

    def test_github_routes(self):
        self.assertEqual(router.route("https://github.com/example/repo")["pipelines"], ["repository-to-skill"])

    def test_unknown_website_is_gap(self):
        output = router.route("https://example.com/page")
        self.assertEqual(output["status"], "capability_gap")
        self.assertEqual(output["proposal"]["status"], "proposed")

    def test_manual_type(self):
        self.assertEqual(router.route("feedback", "experience")["pipelines"], ["experience-to-rule"])

    def test_lookalike_domain_not_youtube(self):
        self.assertEqual(router.route("https://youtube.com.evil.test/x")["status"], "capability_gap")

    def test_no_automatic_execution(self):
        self.assertEqual(router.route("https://youtu.be/abc")["execution"], "not_started")

if __name__ == "__main__":
    unittest.main()
