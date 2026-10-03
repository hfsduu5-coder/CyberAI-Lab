import unittest
from unittest.mock import Mock, patch
from cyberai.providers import ProviderError, _post, MAX_RESPONSE_BYTES

class ProviderGuardTests(unittest.TestCase):
    @patch("cyberai.providers.requests.post")
    def test_rejects_large_content_length(self,post):
        response=Mock()
        response.raise_for_status.return_value=None
        response.headers={"Content-Length":str(MAX_RESPONSE_BYTES+1)}
        response.content=b"{}"
        post.return_value=response
        with self.assertRaises(ProviderError):
            _post("https://example.test",headers={},payload={},timeout=1)

    @patch("cyberai.providers.requests.post")
    def test_rejects_large_body_without_header(self,post):
        response=Mock()
        response.raise_for_status.return_value=None
        response.headers={}
        response.content=b"x"*(MAX_RESPONSE_BYTES+1)
        post.return_value=response
        with self.assertRaises(ProviderError):
            _post("https://example.test",headers={},payload={},timeout=1)

if __name__=="__main__":
    unittest.main()
