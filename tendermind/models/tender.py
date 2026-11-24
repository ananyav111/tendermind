from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class RequirementCategory(str, Enum):
    FINANCIAL = "FINANCIAL"
    EXPERIENCE = "EXPERIENCE"
    STATUTORY = "STATUTORY"
    TECHNICAL = "TECHNICAL"
    CERTIFICATION = "CERTIFICATION"
    EMD_FEE = "EMD_FEE"
    MSME_STARTUP = "MSME_STARTUP"

class TenderRequirement(BaseModel):
    requirement_id: str
    tender_id: str
    category: RequirementCategory
    clause_title: str
    description: str
    source_page: int
    source_section: str
    mandatory: bool = True
    threshold_value: Optional[float] = None  # e.g., 2000000 (20 Lakhs)
    threshold_unit: Optional[str] = None    # e.g., "INR" or "years"
    relaxable_for_msme: bool = False
    evidence_types_accepted: List[str] = Field(default_factory=list)

class Corrigendum(BaseModel):
    corrigendum_id: str
    tender_id: str
    corrigendum_number: int
    issue_date: str
    title: str
    description: str
    affected_sections: List[str]
    old_value: Optional[str] = None
    new_value: Optional[str] = None
    impact_type: str  # "DEADLINE_EXTENSION", "EMD_REDUCTION", "CRITERIA_RELAXATION", "NEW_DOCUMENT_REQUIRED"
    action_required: str

class Tender(BaseModel):
    tender_id: str
    title: str
    reference_number: str
    portal_source: str  # e.g. "GeM", "CPPP", "KPPP"
    department: str
    location: str
    estimated_value_inr: float
    earnest_money_deposit_inr: float
    tender_fee_inr: float = 0.0
    publication_date: str
    submission_deadline: str
    pre_bid_meeting_date: Optional[str] = None
    category: str
    summary: str
    original_document_url: Optional[str] = None
    requirements: List[TenderRequirement] = Field(default_factory=list)
    corrigenda: List[Corrigendum] = Field(default_factory=list)
    msme_exemption_clause: Optional[str] = None
    status: str = "ACTIVE"  # "ACTIVE", "AMENDED", "CLOSED"
    suitability_score: Optional[int] = None
