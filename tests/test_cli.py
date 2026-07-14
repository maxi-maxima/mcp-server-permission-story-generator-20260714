import json
import os
import subprocess
import sys
import tempfile
import unittest

SCRIPT = "mcp-server-permission-story-generator-20260714.py"


class T(unittest.TestCase):
    def write_manifest(self, manifest):
        fd, path = tempfile.mkstemp(text=True)
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(manifest, handle)
        self.addCleanup(lambda: os.path.exists(path) and os.remove(path))
        return path

    def run_cli(self, *args):
        return subprocess.check_output([sys.executable, SCRIPT, *args], text=True)

    def test_story(self):
        path = self.write_manifest({"tools": [{"name": "run", "description": "run command", "permissions": ["shell"]}]})
        out = self.run_cli(path)
        self.assertIn("Can execute local commands", out)
        self.assertIn("high", out)

    def test_capabilities_alias_and_min_level_filter(self):
        path = self.write_manifest(
            {
                "tools": [
                    {"name": "search", "description": "web search", "capabilities": ["network"]},
                    {"name": "note", "description": "local summary", "permissions": []},
                ]
            }
        )
        out = self.run_cli(path, "--min-level", "medium")
        self.assertIn("search", out)
        self.assertIn("Can contact external services", out)
        self.assertNotIn("note", out)

    def test_json_summary(self):
        path = self.write_manifest(
            {
                "tools": [
                    {"name": "run", "permissions": ["shell", "filesystem"]},
                    {"name": "browse", "permissions": "network"},
                    {"name": "noop", "permissions": []},
                ]
            }
        )
        summary = json.loads(self.run_cli(path, "--format", "json-summary"))
        self.assertEqual(summary["tools"], 3)
        self.assertEqual(summary["levels"]["high"], 1)
        self.assertEqual(summary["levels"]["medium"], 1)
        self.assertEqual(summary["levels"]["low"], 1)
        self.assertEqual(summary["permissions"]["filesystem"], 1)


if __name__ == "__main__":
    unittest.main()
