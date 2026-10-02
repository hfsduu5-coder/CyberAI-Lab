import tempfile
import unittest
from pathlib import Path
from cyberai.dashboard import build_dashboard, save_dashboard
from cyberai.workspace import create_workspace

class DashboardTests(unittest.TestCase):
    def test_dashboard_lists_workspace_and_modules(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)/"labs"
            create_workspace("demo",str(root))
            page=build_dashboard(str(root))
            self.assertIn("CyberAI-Lab Dashboard",page)
            self.assertIn("demo",page)
            self.assertIn("http",page)
            self.assertIn("headers",page)

    def test_dashboard_file(self):
        with tempfile.TemporaryDirectory() as temp:
            output=Path(temp)/"dashboard.html"
            save_dashboard(str(output),str(Path(temp)/"missing"))
            self.assertTrue(output.is_file())
            self.assertIn("No local workspaces found.",output.read_text())

if __name__=="__main__":
    unittest.main()
