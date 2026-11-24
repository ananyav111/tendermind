import unittest
from tendermind.api.routes_tenders import list_tenders, get_tender
from tendermind.api.routes_company import get_company_profile, resolve_missing_document
from tendermind.api.routes_eligibility import get_eligibility, get_msme_benefits
from tendermind.api.routes_bids import get_or_generate_bid_package, toggle_checklist_item
from tendermind.api.routes_corrigenda import list_all_corrigenda
from tendermind.api.routes_mcp import list_mcp_tools, get_agent_traces
from tendermind.api.routes_chat import chat_with_agent, ChatRequest

class TestAPIHandlers(unittest.TestCase):
    def test_list_tenders(self):
        tenders = list_tenders()
        self.assertGreaterEqual(len(tenders), 3)

    def test_get_tender(self):
        t = get_tender("GEM/2026/B/123456")
        self.assertEqual(t.tender_id, "GEM/2026/B/123456")
        self.assertEqual(len(t.requirements), 7)

    def test_get_company(self):
        comp = get_company_profile("comp_nexus_01")
        self.assertEqual(comp.company_id, "comp_nexus_01")
        self.assertIn("Nexus", comp.name)

    def test_eligibility(self):
        report = get_eligibility("GEM/2026/B/123456", "comp_nexus_01")
        # Prior to resolving gap, completion certificate is missing
        self.assertIn(report.overall_status, ["POTENTIAL_GAP", "SUBMISSION_READY"])
        self.assertGreater(report.satisfied_count, 0)

    def test_msme_benefits(self):
        benefits = get_msme_benefits("GEM/2026/B/123456", "comp_nexus_01")
        self.assertTrue(benefits.qualifies_for_msme_policy)
        self.assertEqual(benefits.emd_exemption_savings_inr, 50000.0)

    def test_bids_package(self):
        pkg = get_or_generate_bid_package("GEM/2026/B/123456", "comp_nexus_01")
        self.assertEqual(len(pkg.checklist), 9)
        self.assertTrue(pkg.readiness_fraction.endswith("/9"))

    def test_mcp_tools_and_traces(self):
        tools = list_mcp_tools()
        self.assertGreaterEqual(len(tools), 10)
        traces = get_agent_traces()
        self.assertIsInstance(traces, list)

    def test_chat_killer_moment(self):
        req = ChatRequest(
            query="Can my company apply for this tender? What exactly is preventing us from being submission-ready?",
            active_tender_id="GEM/2026/B/123456"
        )
        resp = chat_with_agent(req)
        self.assertIn("answer", resp)
        self.assertIn("Tender Readiness Assessment", resp["answer"])
        self.assertIn("Page 12", resp["answer"])

    def test_gap_resolution_flow(self):
        # Resolve the missing document
        res = resolve_missing_document(company_id="comp_nexus_01")
        self.assertTrue(res["success"])

        # Check eligibility: now it becomes SUBMISSION_READY!
        report = get_eligibility("GEM/2026/B/123456", "comp_nexus_01")
        self.assertEqual(report.overall_status, "SUBMISSION_READY")
        self.assertEqual(report.readiness_percentage, 100)
        self.assertEqual(report.not_satisfied_count, 0)

if __name__ == "__main__":
    unittest.main()
