import unittest
from src.scorer import Lead, score_lead


class LeadScorerTests(unittest.TestCase):
    def test_high_intent_enterprise_is_p0(self):
        result = score_lead(Lead("Acme", "cto@acme.example", "AI automation", 150, 1_200_000, "this month", "Need CRM integration and a proposal"))
        self.assertEqual(result["priority"], "P0")
        self.assertGreaterEqual(result["score"], 65)
        self.assertTrue(result["score_explanation"])

    def test_sparse_lead_has_questions_and_no_rejection(self):
        result = score_lead(Lead("Student", "student@gmail.com"))
        self.assertEqual(result["priority"], "P2")
        self.assertGreaterEqual(len(result["missing_questions"]), 3)
        self.assertIn("human", result["safety_note"].lower())


if __name__ == "__main__":
    unittest.main()
