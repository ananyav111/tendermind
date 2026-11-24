from typing import Dict, Any
from tendermind.models.tender import Tender
from tendermind.models.company import CompanyProfile

class OpportunityScorer:
    """
    Two-way business-to-tender matching engine.
    Ranks opportunities based on capability, sector, financial band, and location.
    """

    @classmethod
    def calculate_suitability(cls, company: CompanyProfile, tender: Tender) -> int:
        score = 0
        
        # 1. Category relevance (Max 35 points)
        tender_cat = tender.category.lower()
        is_it_tender = any(k in tender_cat for k in ["it", "software", "cloud", "technology", "digital", "data"])
        is_civil_tender = any(k in tender_cat for k in ["civil", "road", "construction", "bridge", "asphalt"])
        
        if is_it_tender:
            score += 35
        elif is_civil_tender:
            # Major mismatch for an IT software company
            score += 5
        else:
            score += 15

        # 2. Financial Band Feasibility (Max 25 points)
        # Ideal tender value for MSME is between 20% and 150% of annual turnover
        ratio = tender.estimated_value_inr / max(company.average_annual_turnover_inr, 100000.0)
        if 0.2 <= ratio <= 1.5:
            score += 25
        elif 1.5 < ratio <= 3.0:
            score += 18
        elif ratio < 0.2:
            score += 15
        else:
            # Over 10x company turnover - excessive bonding and risk
            score += 2

        # 3. Location preference (Max 15 points)
        loc_lower = tender.location.lower()
        if company.state.lower() in loc_lower or company.city.lower() in loc_lower:
            score += 15
        elif "pan-india" in loc_lower or "india" in loc_lower:
            score += 12
        else:
            score += 8

        # 4. Technical keywords match (Max 15 points)
        summary_lower = (tender.summary + " " + tender.title).lower()
        matches = sum(1 for cap in company.technical_capabilities if cap.lower() in summary_lower)
        service_matches = sum(1 for s in company.core_services if any(w in summary_lower for w in s.lower().split()))
        total_matches = matches + service_matches
        score += min(15, total_matches * 3)

        # 5. MSME policy benefit availability (Max 10 points)
        if tender.msme_exemption_clause and company.udyam_registration_number:
            score += 10
        else:
            score += 3

        return min(99, max(10, score))
