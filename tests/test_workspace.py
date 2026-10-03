import json
import tempfile
import unittest
from pathlib import Path
from cyberai.workspace import create_workspace, workspace_status

class WorkspaceTests(unittest.TestCase):
    def test_create_and_status(self):
        with tempfile.TemporaryDirectory() as d:
            ws=create_workspace("case-01",d)
            status=workspace_status(str(ws))
            self.assertEqual(status["name"],"case-01")
            self.assertEqual(status["notes"],1)
            self.assertTrue((ws/"workspace.json").is_file())

    def test_duplicate_workspace_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            create_workspace("demo",d)
            with self.assertRaises(ValueError):
                create_workspace("demo",d)

    def test_non_workspace_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(ValueError):
                workspace_status(d)

    def test_invalid_metadata_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            ws=Path(d)/"broken"; ws.mkdir()
            (ws/"workspace.json").write_text("{bad",encoding="utf-8")
            with self.assertRaises(ValueError):
                workspace_status(str(ws))

if __name__=="__main__":
    unittest.main()
