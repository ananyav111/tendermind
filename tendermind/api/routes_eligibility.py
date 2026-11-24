from fastapi import APIRouter, HTTPException, Query
from tendermind.data.db import db
from tendermind.engine.rule_evaluator import EligibilityRuleEngine
from tendermind.engine.msme_rules import MSMERuleEngine
from tendermind.models.eligibility import EligibilityReport, MSMEBenefitAssessment

router = APIRouter(prefix="/api/eligibility", tags=["Eligibility & Gap Analysis"])

@router.get("/{tender_id:path}", response_model=EligibilityReport)
def get_eligibility(tender_id: str, company_id: str = "comp_nexus_01"):
    tender = db.get_tender(tender_id)
    if not tender:
        raise HTTPException(status_code=404, detail=f"Tender '{tender_id}' not found")
    company = db.get_company(company_id)
    if not company:
        raise HTTPException(status_code=404, detail=f"Company '{company_id}' not found")

    report = EligibilityRuleEngine.evaluate(company, tender)
    return report

@router.get("/msme-benefits/{tender_id:path}", response_model=MSMEBenefitAssessment)
def get_msme_benefits(tender_id: str, company_id: str = "comp_nexus_01"):
    tender = db.get_tender(tender_id)
    if not tender:
        raise HTTPException(status_code=404, detail=f"Tender '{tender_id}' not found")
    company = db.get_company(company_id)
    if not company:
        raise HTTPException(status_code=404, detail=f"Company '{company_id}' not found")

    assessment = MSMERuleEngine.evaluate_benefits(company, tender)
    return assessment
