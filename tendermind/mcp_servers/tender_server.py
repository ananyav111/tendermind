from typing import Dict, Any, Optional
from tendermind.mcp_servers.base import BaseMCPServer
from tendermind.data.db import db

class TenderMCPServer(BaseMCPServer):
    def __init__(self):
        super().__init__(
            name="TenderMCPServer",
            description="Manages government procurement portal tender discovery, notices, and corrigenda."
        )
        self._register_all_tools()

    def _register_all_tools(self):
        self.register_tool(
            name="search_tenders",
            description="Search active government tenders from GeM, CPPP, and state portals using filters.",
            parameters={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Keywords to search in title/summary"},
                    "category": {"type": "string", "description": "Business sector, e.g. 'IT Services'"},
                    "location": {"type": "string", "description": "State or city location"},
                    "max_value": {"type": "number", "description": "Maximum estimated contract value in INR"}
                }
            },
            handler=self._tool_search_tenders
        )

        self.register_tool(
            name="get_tender_details",
            description="Retrieve complete tender record, pre-qualification criteria, deadlines, and requirements.",
            parameters={
                "type": "object",
                "properties": {
                    "tender_id": {"type": "string", "description": "Unique identifier of tender"}
                },
                "required": ["tender_id"]
            },
            handler=self._tool_get_tender_details
        )

        self.register_tool(
            name="get_corrigenda",
            description="Retrieve official amendments, date extensions, or clause revisions for a tender.",
            parameters={
                "type": "object",
                "properties": {
                    "tender_id": {"type": "string", "description": "Unique identifier of tender"}
                },
                "required": ["tender_id"]
            },
            handler=self._tool_get_corrigenda
        )

        self.register_tool(
            name="get_tender_document",
            description="Fetch accessible PDF/specification URL or text contents for a tender.",
            parameters={
                "type": "object",
                "properties": {
                    "tender_id": {"type": "string", "description": "Unique identifier of tender"}
                },
                "required": ["tender_id"]
            },
            handler=self._tool_get_tender_document
        )

    def _tool_search_tenders(self, query: Optional[str] = None, category: Optional[str] = None,
                             location: Optional[str] = None, max_value: Optional[float] = None) -> Dict[str, Any]:
        results = db.search_tenders(query=query, category=category, location=location, max_value=max_value)
        return {
            "total_found": len(results),
            "tenders": [
                {
                    "tender_id": t.tender_id,
                    "title": t.title,
                    "department": t.department,
                    "estimated_value_inr": t.estimated_value_inr,
                    "submission_deadline": t.submission_deadline,
                    "suitability_score": t.suitability_score,
                    "status": t.status
                }
                for t in results
            ]
        }

    def _tool_get_tender_details(self, tender_id: str) -> Dict[str, Any]:
        tender = db.get_tender(tender_id)
        if not tender:
            raise ValueError(f"Tender with ID '{tender_id}' not found.")
        return tender.model_dump()

    def _tool_get_corrigenda(self, tender_id: str) -> Dict[str, Any]:
        tender = db.get_tender(tender_id)
        if not tender:
            raise ValueError(f"Tender with ID '{tender_id}' not found.")
        return {
            "tender_id": tender_id,
            "corrigenda_count": len(tender.corrigenda),
            "corrigenda": [c.model_dump() for c in tender.corrigenda]
        }

    def _tool_get_tender_document(self, tender_id: str) -> Dict[str, Any]:
        tender = db.get_tender(tender_id)
        if not tender:
            raise ValueError(f"Tender with ID '{tender_id}' not found.")
        return {
            "tender_id": tender_id,
            "document_url": tender.original_document_url,
            "title": tender.title,
            "portal": tender.portal_source,
            "summary": tender.summary
        }
