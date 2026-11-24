from enum import Enum
from typing import List, Optional, Dict
from pydantic import BaseModel, Field

class ChecklistItemStatus(str, Enum):
    COMPLETED = "COMPLETED"
    PENDING = "PENDING"
    ACTION_REQUIRED = "ACTION_REQUIRED"

class BidChecklistItem(BaseModel):
    item_id: str
    tender_section: str  # e.g., "Envelope A: Fee & Statutory", "Envelope B: Technical Bid", "Envelope C: Financial Bid"
    title: str
    description: str
    mandatory: bool = True
    status: ChecklistItemStatus
    associated_document_name: Optional[str] = None
    verification_source: Optional[str] = None
    action_url: Optional[str] = None

class GeneratedProposalSection(BaseModel):
    section_id: str
    title: str
    content: str
    page_target: Optional[str] = None
    ai_generated: bool = True
    human_approved: bool = False

class BidPackage(BaseModel):
    package_id: str
    tender_id: str
    company_id: str
    title: str
    status: str = "DRAFT"  # "DRAFT", "READY_FOR_REVIEW", "APPROVED"
    readiness_fraction: str = "0/0"
    completed_items_count: int = 0
    total_items_count: int = 0
    checklist: List[BidChecklistItem] = Field(default_factory=list)
    proposals: List[GeneratedProposalSection] = Field(default_factory=list)
    undertakings: Dict[str, str] = Field(default_factory=dict)
    created_at: str
    updated_at: str
