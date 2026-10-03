import unittest
from cyberai.analyzers import http_report, indicators_summary, parse_http_request, recon_report, url_inventory

class AnalyzerTests(unittest.TestCase):
    def test_http_request(self):
        raw="POST /login?next=%2Fadmin HTTP/1.1\r\nHost: example.test\r\nContent-Type: application/json\r\n\r\n{\"username\":\"student\"}"
        result=parse_http_request(raw)
        self.assertEqual(result["method"],"POST")
        self.assertEqual(result["host"],"example.test")
        self.assertEqual(result["query_parameter_names"],["next"])
        self.assertEqual(result["content_type"],"application/json")

    def test_http_report(self):
        self.assertIn('"host": "lab.test"',http_report("GET / HTTP/1.1\nHost: lab.test\n\n"))

    def test_recon_report_is_offline(self):
        report=recon_report("https://lab.test/login [200]\nhttps://lab.test/admin [403]\n10.10.10.10")
        self.assertIn("URLs found: 2",report)
        self.assertIn("Unique URL hosts: 1",report)
        self.assertIn("does not scan or contact targets",report)

    def test_url_inventory(self):
        result=url_inventory("https://lab.example/a.js\nhttp://lab.example/b.css")
        self.assertEqual(result["urls_found"],2)
        self.assertEqual(result["unique_hosts"],1)
        self.assertEqual(result["file_extensions"][".js"],1)

    def test_indicator_summary(self):
        text="192.0.2.10 example.org "+"a"*64
        result=indicators_summary(text)
        self.assertEqual(result["ipv4_values"],1)
        self.assertEqual(result["domain_like_values"],1)
        self.assertEqual(result["sha256_like_values"],1)

    def test_invalid_ipv4_is_excluded(self):
        result=indicators_summary("valid=192.0.2.10 invalid=999.999.999.999")
        self.assertEqual(result["ipv4_values"],1)

if __name__=="__main__":
    unittest.main()
