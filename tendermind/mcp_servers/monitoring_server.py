from typing import Dict, Any, List
from tendermind.mcp_servers.base import BaseMCPServer
from tendermind.data.db import db

class MonitoringMCPServer(BaseMCPServer):
    def __init__(self):
        super().__init__(
            name="MonitoringMCPServer",
            description="Continuously tracks tender updates, deadline amendments, corrigenda, and analyzes impact on prepared bids."
        )
        self._register_all_tools()

    def _register_all_tools(self):
        self.register_tool(
            name="monitor_tender_updates",
            description="Scan active tenders for newly published corrigenda, retendering notices, or deadline extensions.",
            parameters={
                "type": "object",
                "properties": {
                    "tender_id": {"type": "string", "description": "Optional tender ID, or scans all active if omitted"}
                }
            },
            handler=self._tool_monitor_updates
        )

        self.register_tool(
            name="check_corrigenda_impact",
            description="Analyze how a specific corrigendum alters bid compliance, checklist items, and submission readiness.",
            parameters={
                "type": "object",
                "properties": {
                    "tender_id": {"type": "string", "description": "Tender ID"},
                    "corrigendum_id": {"type": "string", "description": "Corrigendum identifier"}
                },
                "required": ["tender_id", "corrigendum_id"]
            },
            handler=self._tool_check_impact
        )

    def _tool_monitor_updates(self, tender_id: str = "") -> Dict[str, Any]:
        if tender_id:
            tenders = [db.get_tender(tender_id)]
            tenders = [t for t in tenders if t]
        else:
            tenders = db.get_all_tenders()

        active_corrigenda = []
        for t in tenders:
            for c in t.corrigenda:
                active_corrigenda.append({
                    "tender_id": t.tender_id,
                    "tender_title": t.title,
                    "corrigendum_number": c.corrigendum_number,
                    "title": c.title,
                    "issue_date": c.issue_date,
                    "impact_type": c.impact_type,
                    "old_value": c.old_value,
                    "new_value": c.new_value,
                    "action_required": c.action_required
                })

        return {
            "total_amendments_detected": len(active_corrigenda),
            "corrigenda": active_corrigenda
        }

    def _tool_check_impact(self, tender_id: str, corrigendum_id: str) -> Dict[str, Any]:
        tender = db.get_tender(tender_id)
        if not tender:
            raise ValueError(f"Tender '{tender_id}' not found.")
        
        target_corr = next((c for c in tender.corrigenda if c.corrigendum_id == corrigendum_id), None)
        if not target_corr:
            raise ValueError(f"Corrigendum '{corrigendum_id}' not found on tender '{tender_id}'.")

        return {
            "tender_id": tender_id,
            "corrigendum_id": corrigendum_id,
            "title": target_corr.title,
            "affected_sections": target_corr.affected_sections,
            "old_value": target_corr.old_value,
            "new_value": target_corr.new_value,
            "impact_level": "ACTION_REQUIRED",
            "checklist_impact": f"Updates required: {target_corr.action_required}",
            "recommendation": "Review bid checklist and update statutory undertakings before final submission sign-off."
        }
