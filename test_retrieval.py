import unittest
from src.retrieval import retrieve


class RetrievalTests(unittest.TestCase):
    def test_service_match_is_ranked_first(self):
        results = retrieve("AI Automation", "invoice extraction CRM workflow")
        self.assertEqual(results[0]["id"], "svc-ai-automation")
        self.assertLessEqual(len(results), 2)


if __name__ == "__main__":
    unittest.main()
