from fastapi import APIRouter, HTTPException, Query
from tendermind.data.db import db
from tendermind.mcp_servers.registry import mcp_registry

router = APIRouter(prefix="/api/corrigenda", tags=["Deadline & Corrigendum Intelligence"])

@router.get("")
def list_all_corrigenda():
    res = mcp_registry.execute_tool(
        server_name="MonitoringMCPServer",
        tool_name="monitor_tender_updates",
        arguments={},
        agent_name="Monitoring Agent"
    )
    return res.result

@router.get("/{tender_id:path}")
def get_tender_corrigenda(tender_id: str):
    tender = db.get_tender(tender_id)
    if not tender:
        raise HTTPException(status_code=404, detail=f"Tender '{tender_id}' not found")
    return {
        "tender_id": tender.tender_id,
        "tender_title": tender.title,
        "corrigenda": [c.model_dump() for c in tender.corrigenda]
    }
