from fastapi import APIRouter, HTTPException, Query, Body
from tendermind.data.db import db
from tendermind.models.bid import BidPackage, ChecklistItemStatus
from tendermind.mcp_servers.registry import mcp_registry

router = APIRouter(prefix="/api/bids", tags=["Bid Preparation"])

@router.get("/{tender_id:path}", response_model=BidPackage)
def get_or_generate_bid_package(tender_id: str, company_id: str = "comp_nexus_01"):
    tender = db.get_tender(tender_id)
    if not tender:
        raise HTTPException(status_code=404, detail=f"Tender '{tender_id}' not found")
    
    pkg = db.get_bid_package_by_tender(tender_id, company_id)
    if not pkg:
        # Trigger MCP Bid Server to generate
        res = mcp_registry.execute_tool(
            server_name="BidMCPServer",
            tool_name="generate_compliance_checklist",
            arguments={"tender_id": tender_id, "company_id": company_id},
            agent_name="Bid Preparation Agent"
        )
        # Also generate initial draft proposals
        mcp_registry.execute_tool(
            server_name="BidMCPServer",
            tool_name="generate_draft_proposal",
            arguments={"tender_id": tender_id, "company_id": company_id},
            agent_name="Bid Preparation Agent"
        )
        pkg = db.get_bid_package_by_tender(tender_id, company_id)

    return pkg

@router.post("/{tender_id:path}/checklist/{item_id}/toggle")
def toggle_checklist_item(tender_id: str, item_id: str, company_id: str = "comp_nexus_01"):
    pkg = db.get_bid_package_by_tender(tender_id, company_id)
    if not pkg:
        raise HTTPException(status_code=404, detail="Bid package not found")

    target = next((item for item in pkg.checklist if item.item_id == item_id), None)
    if not target:
        raise HTTPException(status_code=404, detail=f"Checklist item '{item_id}' not found")

    if target.status == ChecklistItemStatus.COMPLETED:
        target.status = ChecklistItemStatus.PENDING
    else:
        target.status = ChecklistItemStatus.COMPLETED

    completed = sum(1 for c in pkg.checklist if c.status == ChecklistItemStatus.COMPLETED)
    pkg.completed_items_count = completed
    pkg.readiness_fraction = f"{completed}/{pkg.total_items_count}"
    if completed == pkg.total_items_count:
        pkg.status = "READY_FOR_REVIEW"
    
    db.save_bid_package(pkg)
    return pkg

@router.post("/{tender_id:path}/proposal/{section_id}/approve")
def approve_proposal_section(tender_id: str, section_id: str, company_id: str = "comp_nexus_01"):
    pkg = db.get_bid_package_by_tender(tender_id, company_id)
    if not pkg:
        raise HTTPException(status_code=404, detail="Bid package not found")

    sec = next((s for s in pkg.proposals if s.section_id == section_id), None)
    if not sec:
        raise HTTPException(status_code=404, detail=f"Proposal section '{section_id}' not found")

    sec.human_approved = not sec.human_approved
    db.save_bid_package(pkg)
    return {"success": True, "approved": sec.human_approved, "section": sec}
