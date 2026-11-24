from typing import Dict, Any, Optional
from tendermind.mcp_servers.base import BaseMCPServer
from tendermind.data.db import db

class BusinessMCPServer(BaseMCPServer):
    def __init__(self):
        super().__init__(
            name="BusinessMCPServer",
            description="Maintains verified company profile, credentials, and document repository records."
        )
        self._register_all_tools()

    def _register_all_tools(self):
        self.register_tool(
            name="get_company_profile",
            description="Retrieve verified business credentials, registration type, turnover history, and capabilities.",
            parameters={
                "type": "object",
                "properties": {
                    "company_id": {"type": "string", "description": "Unique identifier of the company"}
                },
                "required": ["company_id"]
            },
            handler=self._tool_get_company_profile
        )

        self.register_tool(
            name="search_company_documents",
            description="Search company document repository for specific compliance certificates, past work orders, or completion proofs.",
            parameters={
                "type": "object",
                "properties": {
                    "company_id": {"type": "string", "description": "Company ID"},
                    "document_type": {"type": "string", "description": "Optional type e.g. 'Completion certificate', 'GST'"}
                },
                "required": ["company_id"]
            },
            handler=self._tool_search_company_documents
        )

    def _tool_get_company_profile(self, company_id: str = "comp_nexus_01") -> Dict[str, Any]:
        company = db.get_company(company_id)
        if not company:
            raise ValueError(f"Company '{company_id}' not found.")
        return company.model_dump()

    def _tool_search_company_documents(self, company_id: str = "comp_nexus_01", document_type: Optional[str] = None) -> Dict[str, Any]:
        company = db.get_company(company_id)
        if not company:
            raise ValueError(f"Company '{company_id}' not found.")
        
        docs = company.documents
        if document_type:
            docs = [d for d in docs if document_type.lower() in d.document_type.lower()]
        
        return {
            "company_id": company_id,
            "total_documents": len(docs),
            "documents": [d.model_dump() for d in docs]
        }
