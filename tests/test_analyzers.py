import unittest

from cyberai.analyzers import http_report, parse_http_request, recon_report


class AnalyzerTests(unittest.TestCase):
    def test_http_request(self):
        raw = (
            "POST /login?next=%2Fadmin HTTP/1.1\r\n"
            "Host: example.test\r\n"
            "Content-Type: application/json\r\n\r\n"
            '{"username":"student"}'
        )
        result = parse_http_request(raw)
        self.assertEqual(result["method"], "POST")
        self.assertEqual(result["host"], "example.test")
        self.assertEqual(result["query_parameter_names"], ["next"])
        self.assertEqual(result["content_type"], "application/json")

    def test_http_report(self):
        report = http_report("GET / HTTP/1.1\nHost: lab.test\n\n")
        self.assertIn('"host": "lab.test"', report)

    def test_recon_report_is_offline(self):
        report = recon_report(
            "https://lab.test/login [200]\n"
            "https://lab.test/admin [403]\n"
            "10.10.10.10"
        )
        self.assertIn("URLs found: 2", report)
        self.assertIn("Unique URL hosts: 1", report)
        self.assertIn("does not scan or contact targets", report)


if __name__ == "__main__":
    unittest.main()
