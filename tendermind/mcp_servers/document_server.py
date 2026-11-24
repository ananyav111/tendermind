from typing import Dict, Any, List
from tendermind.mcp_servers.base import BaseMCPServer
from tendermind.engine.pdf_processor import TenderPDFProcessor
from tendermind.data.db import db

class DocumentMCPServer(BaseMCPServer):
    def __init__(self):
        super().__init__(
            name="DocumentMCPServer",
            description="Parses tender PDFs, extracts structured requirement clauses, and links source citations."
        )
        self._register_all_tools()

    def _register_all_tools(self):
        self.register_tool(
            name="extract_pdf_text",
            description="Extract text content and page breaks from a tender PDF document or URL.",
            parameters={
                "type": "object",
                "properties": {
                    "tender_id": {"type": "string", "description": "Tender ID"},
                    "raw_text": {"type": "string", "description": "Optional raw text if PDF is already decoded"}
                },
                "required": ["tender_id"]
            },
            handler=self._tool_extract_pdf_text
        )

        self.register_tool(
            name="extract_requirements",
            description="Extract structured financial, technical, and statutory requirement clauses with exact page citations.",
            parameters={
                "type": "object",
                "properties": {
                    "tender_id": {"type": "string", "description": "Tender ID to analyze"}
                },
                "required": ["tender_id"]
            },
            handler=self._tool_extract_requirements
        )

    def _tool_extract_pdf_text(self, tender_id: str, raw_text: str = "") -> Dict[str, Any]:
        tender = db.get_tender(tender_id)
        if not tender:
            raise ValueError(f"Tender '{tender_id}' not found.")
        text_content = raw_text if raw_text else f"Tender Specifications for {tender.title}\n{tender.summary}"
        return {
            "tender_id": tender_id,
            "document_url": tender.original_document_url,
            "character_count": len(text_content),
            "sample_snippet": text_content[:300]
        }

    def _tool_extract_requirements(self, tender_id: str) -> Dict[str, Any]:
        tender = db.get_tender(tender_id)
        if not tender:
            raise ValueError(f"Tender '{tender_id}' not found.")
        return {
            "tender_id": tender_id,
            "total_requirements": len(tender.requirements),
            "requirements": [
                {
                    "requirement_id": r.requirement_id,
                    "category": r.category.value,
                    "clause_title": r.clause_title,
                    "description": r.description,
                    "citation": f"Page {r.source_page}, {r.source_section}",
                    "mandatory": r.mandatory,
                    "relaxable_for_msme": r.relaxable_for_msme
                }
                for r in tender.requirements
            ]
        }
