from enum import Enum
from typing import List, Optional, Dict
from pydantic import BaseModel, Field

class DocumentStatus(str, Enum):
    UPLOADED = "Uploaded"
    MISSING = "Missing"
    NOT_PROVIDED = "Not provided"
    EXPIRED = "Expired"

class BusinessDocument(BaseModel):
    document_id: str
    company_id: str
    document_type: str  # e.g., "GST certificate", "PAN", "Udyam certificate", "Audited balance sheet", "Work order", "Completion certificate"
    title: str
    file_name: str
    status: DocumentStatus = DocumentStatus.UPLOADED
    upload_date: Optional[str] = None
    expiry_date: Optional[str] = None
    financial_year: Optional[str] = None
    issuing_authority: Optional[str] = None
    verification_hash: Optional[str] = None
    is_verified: bool = True

class BusinessCredential(BaseModel):
    credential_id: str
    company_id: str
    credential_type: str  # e.g., "PAN", "GSTIN", "UDYAM", "INCORPORATION"
    identifier_value: str
    valid_from: str
    valid_until: Optional[str] = None
    status: str = "ACTIVE"

class CompanyProfile(BaseModel):
    company_id: str
    name: str
    trade_name: Optional[str] = None
    business_type: str  # "Private Limited", "Partnership", "Proprietorship", "LLP"
    state: str
    city: str
    pincode: str
    udyam_registration_number: Optional[str] = None
    enterprise_category: str = "MICRO"  # "MICRO", "SMALL", "MEDIUM", "LARGE"
    incorporation_date: str
    years_of_operation: float
    pan_number: str
    gstin: str
    annual_turnover_fy: Dict[str, float] = Field(default_factory=dict) # e.g. {"2022-23": 2800000, "2023-24": 3500000, "2024-25": 4100000}
    average_annual_turnover_inr: float
    net_worth_inr: float
    core_services: List[str] = Field(default_factory=list)
    technical_capabilities: List[str] = Field(default_factory=list)
    past_projects_count: int = 0
    completed_contracts_value_inr: float = 0.0
    certifications: List[str] = Field(default_factory=list) # e.g. ["ISO 9001:2015", "ISO 27001"]
    documents: List[BusinessDocument] = Field(default_factory=list)
    credentials: List[BusinessCredential] = Field(default_factory=list)
