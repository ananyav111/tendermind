from typing import Dict, Any
from tendermind.mcp_servers.base import BaseMCPServer
from tendermind.engine.rule_evaluator import EligibilityRuleEngine
from tendermind.engine.msme_rules import MSMERuleEngine
from tendermind.data.db import db

class EligibilityMCPServer(BaseMCPServer):
    def __init__(self):
        super().__init__(
            name="EligibilityMCPServer",
            description="Performs deterministic 3-state eligibility analysis and MSME policy exemption matching."
        )
        self._register_all_tools()

    def _register_all_tools(self):
        self.register_tool(
            name="evaluate_eligibility",
            description="Run audit-grade comparison between tender requirements and business documents, outputting Satisfied, Not satisfied, or Needs verification.",
            parameters={
                "type": "object",
                "properties": {
                    "tender_id": {"type": "string", "description": "Tender ID"},
                    "company_id": {"type": "string", "description": "Company ID"}
                },
                "required": ["tender_id", "company_id"]
            },
            handler=self._tool_evaluate_eligibility
        )

        self.register_tool(
            name="check_msme_benefits",
            description="Evaluate applicable MSME exemptions including EMD waiver, tender fee waiver, and relaxation clauses under Indian procurement law.",
            parameters={
                "type": "object",
                "properties": {
                    "tender_id": {"type": "string", "description": "Tender ID"},
                    "company_id": {"type": "string", "description": "Company ID"}
                },
                "required": ["tender_id", "company_id"]
            },
            handler=self._tool_check_msme_benefits
        )

    def _tool_evaluate_eligibility(self, tender_id: str, company_id: str = "comp_nexus_01") -> Dict[str, Any]:
        tender = db.get_tender(tender_id)
        if not tender:
            raise ValueError(f"Tender '{tender_id}' not found.")
        company = db.get_company(company_id)
        if not company:
            raise ValueError(f"Company '{company_id}' not found.")
        
        report = EligibilityRuleEngine.evaluate(company, tender)
        return report.model_dump()

    def _tool_check_msme_benefits(self, tender_id: str, company_id: str = "comp_nexus_01") -> Dict[str, Any]:
        tender = db.get_tender(tender_id)
        if not tender:
            raise ValueError(f"Tender '{tender_id}' not found.")
        company = db.get_company(company_id)
        if not company:
            raise ValueError(f"Company '{company_id}' not found.")

        assessment = MSMERuleEngine.evaluate_benefits(company, tender)
        return assessment.model_dump()
