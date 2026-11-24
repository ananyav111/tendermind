import unittest
from tendermind.mcp_servers.registry import mcp_registry

class TestMCPServers(unittest.TestCase):
    def test_registered_tools_count(self):
        tools = mcp_registry.list_all_tools()
        # Should have at least 10 tools across 7 servers
        self.assertGreaterEqual(len(tools), 10)
        tool_names = [t.name for t in tools]
        self.assertIn("search_tenders", tool_names)
        self.assertIn("extract_requirements", tool_names)
        self.assertIn("get_company_profile", tool_names)
        self.assertIn("evaluate_eligibility", tool_names)
        self.assertIn("generate_compliance_checklist", tool_names)
        self.assertIn("monitor_tender_updates", tool_names)

    def test_tender_search_tool(self):
        resp = mcp_registry.execute_tool(
            server_name="TenderMCPServer",
            tool_name="search_tenders",
            arguments={"category": "IT Services"}
        )
        self.assertTrue(resp.success)
        self.assertGreaterEqual(resp.result["total_found"], 1)

    def test_corrigenda_tool(self):
        resp = mcp_registry.execute_tool(
            server_name="TenderMCPServer",
            tool_name="get_corrigenda",
            arguments={"tender_id": "GEM/2026/B/123456"}
        )
        self.assertTrue(resp.success)
        self.assertEqual(resp.result["corrigenda_count"], 2)

if __name__ == "__main__":
    unittest.main()
