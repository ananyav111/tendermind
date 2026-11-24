import unittest
from tendermind.agents.orchestrator import orchestrator

class TestOrchestrator(unittest.TestCase):
    def test_full_pipeline(self):
        result = orchestrator.run_full_pipeline("GEM/2026/B/123456")
        self.assertIn("tender", result)
        self.assertIn("eligibility_report", result)
        self.assertIn("bid_package", result)
        self.assertIn("msme_benefits", result)

    def test_killer_moment_query(self):
        query = "Can my company apply for this tender? What exactly is preventing us from being submission-ready?"
        response = orchestrator.answer_user_query(query, active_tender_id="GEM/2026/B/123456")
        self.assertIn("answer", response)
        # Should cite the missing completion certificate
        self.assertIn("Client Completion Certificate", response["answer"])
        self.assertIn("Page 14", response["answer"])
        # Should cite EMD exemption
        self.assertIn("EMD Exemption", response["answer"])

if __name__ == "__main__":
    unittest.main()
