import unittest
from unittest.mock import patch
from cyberai.config import Settings
from cyberai.providers import ProviderError, complete

def settings(provider="ollama"):
    return Settings(provider=provider,model="test-model",base_url="http://localhost:11434" if provider=="ollama" else "https://example.test/v1",api_key="test",timeout=10,system_prompt="test")

class ProviderContractTests(unittest.TestCase):
    @patch("cyberai.providers._post")
    def test_ollama_contract(self,post):
        post.return_value={"message":{"content":" ok "}}
        self.assertEqual(complete(settings(),[{"role":"user","content":"hi"}]),"ok")

    @patch("cyberai.providers._post")
    def test_openai_compatible_contract(self,post):
        post.return_value={"choices":[{"message":{"content":" ok "}}]}
        self.assertEqual(complete(settings("openai"),[{"role":"user","content":"hi"}]),"ok")

    @patch("cyberai.providers._post")
    def test_invalid_provider_shape_is_normalized(self,post):
        post.return_value={}
        with self.assertRaises(ProviderError): complete(settings(),[])

if __name__=="__main__":
    unittest.main()
