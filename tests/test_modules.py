import unittest

from cyberai.modules import get_module, list_modules


class ModuleRegistryTests(unittest.TestCase):
    def test_builtin_modules_exist(self):
        names = [module.name for module in list_modules()]
        self.assertIn("http", names)
        self.assertIn("recon", names)

    def test_get_module(self):
        module = get_module("http")
        result = module.analyzer("GET / HTTP/1.1\nHost: lab.test\n\n")
        self.assertEqual(result["host"], "lab.test")

    def test_unknown_module(self):
        with self.assertRaises(ValueError):
            get_module("missing")


if __name__ == "__main__":
    unittest.main()
