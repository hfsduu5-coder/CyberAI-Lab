import tempfile
import unittest
from pathlib import Path
from cyberai.reporting import build_report, save_report

class ReportingTests(unittest.TestCase):
    def test_source_is_minimized(self):
        report=build_report("indicators","folder/evidence.log",{"ok":True})
        self.assertEqual(report["source"],"evidence.log")

    def test_empty_kind_rejected(self):
        with self.assertRaises(ValueError):
            build_report(" ","x",{})

    def test_html_escapes_markup(self):
        with tempfile.TemporaryDirectory() as d:
            report=build_report("test","x.txt",{"value":"<b>unsafe</b>"})
            out=save_report(report,str(Path(d)/"r.html"),"html")
            text=out.read_text(encoding="utf-8")
            self.assertNotIn("<b>unsafe</b>",text)
            self.assertIn("&lt;b&gt;",text)

    def test_directory_output_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(ValueError):
                save_report(build_report("test","x",{}),d,"json")

if __name__=="__main__":
    unittest.main()
