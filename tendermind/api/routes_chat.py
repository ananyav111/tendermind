from fastapi import APIRouter, Body
from typing import Optional, Dict, Any
from pydantic import BaseModel
from tendermind.agents.orchestrator import orchestrator

router = APIRouter(prefix="/api/chat", tags=["Agent Chat & Assistant"])

class ChatRequest(BaseModel):
    query: str
    active_tender_id: Optional[str] = "GEM/2026/B/123456"
    company_id: Optional[str] = "comp_nexus_01"

@router.post("")
def chat_with_agent(req: ChatRequest = Body(...)):
    """
    Handles natural language questions with real evidence citations and next steps.
    """
    result = orchestrator.answer_user_query(
        query=req.query,
        active_tender_id=req.active_tender_id,
        company_id=req.company_id
    )
    return result
