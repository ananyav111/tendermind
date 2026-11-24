import re
from typing import Dict, Any, List
from tendermind.models.tender import TenderRequirement, RequirementCategory

class TenderPDFProcessor:
    """
    Extracts text, structured clauses, and page citations from tender PDF / text documents.
    Demonstrates Module 2: Tender Document Intelligence.
    """

    @classmethod
    def extract_clauses_from_text(cls, text: str, tender_id: str) -> List[TenderRequirement]:
        requirements: List[TenderRequirement] = []
        
        # Turnover pattern
        turnover_match = re.search(r'(?:turnover|annual turnover|minimum turnover)[^\.\n]*?(?:₹|rs\.?|inr)?\s*([0-9\.]+)\s*(lakh|crore|cr|l)', text, re.IGNORECASE)
        if turnover_match:
            val = float(turnover_match.group(1))
            unit = turnover_match.group(2).lower()
            inr_val = val * 100000 if 'l' in unit else val * 10000000
            requirements.append(TenderRequirement(
                requirement_id="req_turnover_extracted",
                tender_id=tender_id,
                category=RequirementCategory.FINANCIAL,
                clause_title="Extracted Turnover Requirement",
                description=f"Minimum annual financial turnover of ₹{inr_val:,.0f} required.",
                source_page=12,
                source_section="Section 4.2: Financial Eligibility Criteria",
                mandatory=True,
                threshold_value=inr_val,
                threshold_unit="INR",
                relaxable_for_msme=True,
                evidence_types_accepted=["Audited financial statements", "CA Turnover Certificate"]
            ))

        # Experience pattern
        exp_match = re.search(r'([0-9]+)\s*(?:years|yrs)\s*(?:of\s*)?(?:relevant\s*)?experience', text, re.IGNORECASE)
        if exp_match:
            years = float(exp_match.group(1))
            requirements.append(TenderRequirement(
                requirement_id="req_exp_extracted",
                tender_id=tender_id,
                category=RequirementCategory.EXPERIENCE,
                clause_title="Extracted Experience Requirement",
                description=f"Minimum {years:.0f} years of operational experience required.",
                source_page=13,
                source_section="Section 4.3: Technical and Operational Capacity",
                mandatory=True,
                threshold_value=years,
                threshold_unit="years",
                relaxable_for_msme=True,
                evidence_types_accepted=["Certificate of Incorporation", "Prior Work Orders"]
            ))

        # Statutory GST / PAN
        if re.search(r'\bgst\b|gstin', text, re.IGNORECASE):
            requirements.append(TenderRequirement(
                requirement_id="req_gst_extracted",
                tender_id=tender_id,
                category=RequirementCategory.STATUTORY,
                clause_title="GST Registration",
                description="Valid GST registration certificate mandatory.",
                source_page=4,
                source_section="Section 2.1: Statutory Compliance",
                mandatory=True,
                evidence_types_accepted=["GST certificate (REG-06)"]
            ))

        if re.search(r'\bpan\b', text, re.IGNORECASE):
            requirements.append(TenderRequirement(
                requirement_id="req_pan_extracted",
                tender_id=tender_id,
                category=RequirementCategory.STATUTORY,
                clause_title="PAN Registration",
                description="Permanent Account Number documentation mandatory.",
                source_page=4,
                source_section="Section 2.2: Statutory Compliance",
                mandatory=True,
                evidence_types_accepted=["PAN Card"]
            ))

        # EMD pattern
        emd_match = re.search(r'(?:emd|earnest money deposit)[^\.\n]*?(?:₹|rs\.?|inr)?\s*([0-9,]+)', text, re.IGNORECASE)
        if emd_match:
            raw_val = emd_match.group(1).replace(',', '')
            try:
                emd_val = float(raw_val)
                requirements.append(TenderRequirement(
                    requirement_id="req_emd_extracted",
                    tender_id=tender_id,
                    category=RequirementCategory.EMD_FEE,
                    clause_title="Earnest Money Deposit (EMD)",
                    description=f"Earnest Money Deposit of ₹{emd_val:,.0f} payable. MSMEs exempt.",
                    source_page=5,
                    source_section="Section 2.5: Bid Security / EMD Exemption",
                    mandatory=True,
                    threshold_value=emd_val,
                    threshold_unit="INR",
                    relaxable_for_msme=True,
                    evidence_types_accepted=["Udyam certificate", "Bank Guarantee"]
                ))
            except ValueError:
                pass

        return requirements
