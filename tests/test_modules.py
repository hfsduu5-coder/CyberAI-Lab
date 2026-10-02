import unittest
from cyberai.modules import get_module, list_modules

class ModuleRegistryTests(unittest.TestCase):
    def test_builtin_modules_exist(self):
        names=[m.name for m in list_modules()]
        for name in ("http","recon","headers","logs"):
            self.assertIn(name,names)

    def test_http_module(self):
        result=get_module("http").analyzer("GET / HTTP/1.1\nHost: lab.test\n\n")
        self.assertEqual(result["host"],"lab.test")

    def test_headers_module(self):
        result=get_module("headers").analyzer("Content-Type: text/html\nX-Content-Type-Options: nosniff")
        self.assertIn("x-content-type-options",result["present_security_headers"])
        self.assertIn("content-security-policy",result["missing_security_headers"])

    def test_logs_module(self):
        result=get_module("logs").analyzer("INFO started\nERROR failed\nWARN retry")
        self.assertEqual(result["lines"],3)
        self.assertEqual(result["level_counts"]["ERROR"],1)

    def test_unknown_module(self):
        with self.assertRaises(ValueError): get_module("missing")

if __name__=="__main__":
    unittest.main()
