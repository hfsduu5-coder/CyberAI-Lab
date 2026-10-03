import os
import unittest
from unittest.mock import patch
from cyberai.config import load_settings

class ConfigTests(unittest.TestCase):
    def test_rejects_invalid_base_url(self):
        with patch.dict(os.environ,{"CYBERAI_PROVIDER":"ollama","CYBERAI_BASE_URL":"not-a-url"},clear=True):
            with self.assertRaises(ValueError): load_settings()

    def test_rejects_timeout_above_bound(self):
        with patch.dict(os.environ,{"CYBERAI_PROVIDER":"ollama","CYBERAI_TIMEOUT":"301"},clear=True):
            with self.assertRaises(ValueError): load_settings()

    def test_accepts_local_ollama_defaults(self):
        with patch.dict(os.environ,{"CYBERAI_PROVIDER":"ollama"},clear=True):
            settings=load_settings()
            self.assertEqual(settings.provider,"ollama")
            self.assertTrue(settings.base_url.startswith("http://"))

if __name__=="__main__":
    unittest.main()
