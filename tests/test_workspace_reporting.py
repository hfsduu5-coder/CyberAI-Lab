import json
import tempfile
import unittest
from pathlib import Path
from cyberai.reporting import build_report, save_report
from cyberai.workspace import create_workspace, workspace_status

class WorkspaceReportingTests(unittest.TestCase):
    def test_workspace_creation(self):
        with tempfile.TemporaryDirectory() as temp:
            path = create_workspace("demo-lab", str(Path(temp) / "labs"))
            self.assertTrue((path / "workspace.json").is_file())
            self.assertEqual(workspace_status(str(path))["inputs"], 0)

    def test_json_report(self):
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / "report.json"
            save_report(build_report("http", "request.txt", {"method": "GET"}), str(output), "json")
            self.assertEqual(json.loads(output.read_text())["data"]["method"], "GET")

    def test_markdown_report(self):
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / "report.md"
            save_report(build_report("recon", "recon.txt", "Recon Summary"), str(output), "md")
            self.assertIn("# CyberAI-Lab Report", output.read_text())

if __name__ == "__main__":
    unittest.main()
