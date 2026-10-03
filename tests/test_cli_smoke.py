import subprocess, sys, unittest

class CLISmokeTests(unittest.TestCase):
    def run_cli(self,*args):
        return subprocess.run([sys.executable,"-m","cyberai",*args],capture_output=True,text=True,timeout=15)

    def test_help(self):
        self.assertEqual(self.run_cli("--help").returncode,0)

    def test_version(self):
        result=self.run_cli("--version")
        self.assertEqual(result.returncode,0)
        self.assertIn("cyberai",result.stdout.lower())

    def test_module_list(self):
        result=self.run_cli("module","list")
        self.assertEqual(result.returncode,0)

if __name__=="__main__":
    unittest.main()
