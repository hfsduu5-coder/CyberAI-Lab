import unittest
from cyberai.doctor import format_checks, run_checks

class DoctorTests(unittest.TestCase):
    def test_doctor_returns_checks(self):
        checks,ok=run_checks()
        self.assertTrue(checks)
        self.assertIsInstance(ok,bool)
        self.assertIn("python",[item["name"] for item in checks])

    def test_format_checks(self):
        text=format_checks([{"name":"demo","ok":True,"detail":"ready"}])
        self.assertIn("[OK] demo: ready",text)

if __name__=="__main__":
    unittest.main()
