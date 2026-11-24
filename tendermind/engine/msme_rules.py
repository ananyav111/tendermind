from typing import Dict, Any, Optional
from tendermind.models.tender import Tender
from tendermind.models.company import CompanyProfile
from tendermind.models.eligibility import MSMEBenefitAssessment

class MSMERuleEngine:
    """
    Evaluates Public Procurement Policy for Micro and Small Enterprises (MSEs) Order, 2012
    and Rule 170 of General Financial Rules (GFR), 2017.
    """

    @staticmethod
    def evaluate_benefits(company: CompanyProfile, tender: Tender) -> MSMEBenefitAssessment:
        is_mse = company.enterprise_category.upper() in ["MICRO", "SMALL"]
        has_udyam = bool(company.udyam_registration_number and len(company.udyam_registration_number) > 5)

        # Check if tender belongs to civil infrastructure mega contracts with explicit non-applicability
        is_civil_mega = tender.estimated_value_inr > 500000000 and "civil" in tender.category.lower()

        if is_mse and has_udyam and not is_civil_mega:
            qualifies = True
            policy_ref = "Public Procurement Policy for MSEs Order 2012 / GFR 2017 Rule 170 (iii)"
            emd_exempt = True
            emd_savings = tender.earnest_money_deposit_inr
            fee_exempt = True
            
            # Turnover relaxation: Permitted for MSEs subject to meeting quality & technical standards
            turnover_relax = True
            turnover_notes = "Relaxation of prior turnover permissible under Ministry of MSME OM No. F.20/2/2014-PPD dated 20.09.2016."
            
            # Experience relaxation: Startups/MSEs eligible for prior experience relaxation unless safety/critical
            exp_relax = True
            exp_notes = "Prior experience criteria relaxed subject to meeting technical capability and quality standards."
            
            doc_req = "Valid Udyam Registration Certificate (NIC 6201/6202 matching services)"
            summary = (
                f"Eligible for 100% EMD Exemption (Saving ₹{emd_savings:,.0f}), "
                f"Tender Fee Exemption (Saving ₹{tender.tender_fee_inr:,.0f}), "
                f"and statutory turnover/experience relaxation under MSE Procurement Policy."
            )
        elif is_civil_mega:
            qualifies = False
            policy_ref = "Mega EPC Contract Exemption Policy"
            emd_exempt = False
            emd_savings = 0.0
            fee_exempt = False
            turnover_relax = False
            turnover_notes = "Relaxations not applicable for major heavy infrastructure packages exceeding ₹50 Crore."
            exp_relax = False
            exp_notes = "Not applicable."
            doc_req = "Standard commercial guarantees required."
            summary = "Not eligible: High-value civil EPC tender excludes general MSE relaxations."
        else:
            qualifies = False
            policy_ref = "Public Procurement Policy for MSEs Order 2012"
            emd_exempt = False
            emd_savings = 0.0
            fee_exempt = False
            turnover_relax = False
            turnover_notes = "Requires valid Udyam Registration Certificate under Micro/Small category."
            exp_relax = False
            exp_notes = "Requires valid Udyam Registration Certificate under Micro/Small category."
            doc_req = "Register for Udyam certificate at udyamregistration.gov.in"
            summary = "Ineligible for MSME concessions: Active Udyam registration missing or entity categorized as Medium/Large."

        return MSMEBenefitAssessment(
            qualifies_for_msme_policy=qualifies,
            policy_reference=policy_ref,
            emd_exemption_eligible=emd_exempt,
            emd_exemption_savings_inr=emd_savings,
            tender_fee_exemption_eligible=fee_exempt,
            turnover_relaxation_eligible=turnover_relax,
            turnover_relaxation_notes=turnover_notes,
            experience_relaxation_eligible=exp_relax,
            experience_relaxation_notes=exp_notes,
            mandatory_document_required=doc_req,
            status_summary=summary
        )
