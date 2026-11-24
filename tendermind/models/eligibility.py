from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class ConditionStatus(str, Enum):
    SATISFIED = "Satisfied"
    NOT_SATISFIED = "Not satisfied"
    NEEDS_VERIFICATION = "Needs verification"

class ConditionAssessment(BaseModel):
    requirement_id: str
    clause_title: str
    category: str
    tender_condition: str
    source_citation: str  # e.g., "Page 12, Section 4.2"
    status: ConditionStatus
    company_value_or_evidence: str
    missing_evidence: Optional[str] = None
    audit_notes: str
    msme_benefit_applied: bool = False
    msme_benefit_notes: Optional[str] = None

class GapItem(BaseModel):
    gap_id: str
    severity: str  # "BLOCKING", "WARNING", "OPPORTUNITY"
    requirement_title: str
    description: str
    resolution_step: str
    suggested_action: str

class MSMEBenefitAssessment(BaseModel):
    qualifies_for_msme_policy: bool
    policy_reference: str  # e.g. "Public Procurement Policy for MSEs Order, 2012 / GFR Rule 170"
    emd_exemption_eligible: bool
    emd_exemption_savings_inr: float
    tender_fee_exemption_eligible: bool
    turnover_relaxation_eligible: bool
    turnover_relaxation_notes: str
    experience_relaxation_eligible: bool
    experience_relaxation_notes: str
    mandatory_document_required: str  # "Valid Udyam Registration Certificate with matching NIC Code"
    status_summary: str

class EligibilityReport(BaseModel):
    tender_id: str
    company_id: str
    overall_status: str  # "SUBMISSION_READY", "POTENTIAL_GAP", "DISQUALIFIED"
    readiness_percentage: int
    satisfied_count: int
    not_satisfied_count: int
    needs_verification_count: int
    assessments: List[ConditionAssessment] = Field(default_factory=list)
    gaps: List[GapItem] = Field(default_factory=list)
    msme_benefits: MSMEBenefitAssessment
    executive_verdict: str
    next_recommended_actions: List[str] = Field(default_factory=list)
