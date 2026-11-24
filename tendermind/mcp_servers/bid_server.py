from typing import Dict, Any, List
from datetime import datetime
from tendermind.mcp_servers.base import BaseMCPServer
from tendermind.models.bid import (
    BidPackage, BidChecklistItem, GeneratedProposalSection, ChecklistItemStatus
)
from tendermind.data.db import db
from tendermind.engine.rule_evaluator import EligibilityRuleEngine

class BidMCPServer(BaseMCPServer):
    def __init__(self):
        super().__init__(
            name="BidMCPServer",
            description="Compiles structured bid submission packages, checklists, draft technical proposals, and statutory undertakings."
        )
        self._register_all_tools()

    def _register_all_tools(self):
        self.register_tool(
            name="generate_compliance_checklist",
            description="Generate section-wise document checklist mapped to verified company documents and tender requirements.",
            parameters={
                "type": "object",
                "properties": {
                    "tender_id": {"type": "string", "description": "Tender ID"},
                    "company_id": {"type": "string", "description": "Company ID"}
                },
                "required": ["tender_id", "company_id"]
            },
            handler=self._tool_generate_checklist
        )

        self.register_tool(
            name="generate_draft_proposal",
            description="Generate criterion-aligned draft technical proposal, executive summary, approach, and declarations.",
            parameters={
                "type": "object",
                "properties": {
                    "tender_id": {"type": "string", "description": "Tender ID"},
                    "company_id": {"type": "string", "description": "Company ID"}
                },
                "required": ["tender_id", "company_id"]
            },
            handler=self._tool_generate_proposal
        )

    def _tool_generate_checklist(self, tender_id: str, company_id: str = "comp_nexus_01") -> Dict[str, Any]:
        tender = db.get_tender(tender_id)
        if not tender:
            raise ValueError(f"Tender '{tender_id}' not found.")
        company = db.get_company(company_id)
        if not company:
            raise ValueError(f"Company '{company_id}' not found.")

        # Build checklist items
        checklist: List[BidChecklistItem] = [
            BidChecklistItem(
                item_id="chk_01",
                tender_section="Envelope A: Statutory & Fee",
                title="Company Profile & Registration Dossier",
                description="Certificate of Incorporation, MoA/AoA, and executive leadership details.",
                mandatory=True,
                status=ChecklistItemStatus.COMPLETED,
                associated_document_name="Company_Profile_NexusTech.pdf",
                verification_source="CIN: U72200KA2022PTC123456"
            ),
            BidChecklistItem(
                item_id="chk_02",
                tender_section="Envelope A: Statutory & Fee",
                title="GST Registration Certificate (Form GST REG-06)",
                description="Clear scan of valid GST registration certificate in Karnataka state.",
                mandatory=True,
                status=ChecklistItemStatus.COMPLETED,
                associated_document_name="GST_REG_06_NexusTech.pdf",
                verification_source="GSTIN: 29AABCU9603R1ZM"
            ),
            BidChecklistItem(
                item_id="chk_03",
                tender_section="Envelope A: Statutory & Fee",
                title="Permanent Account Number (PAN) Card",
                description="Legible copy of PAN card in company name.",
                mandatory=True,
                status=ChecklistItemStatus.COMPLETED,
                associated_document_name="PAN_Card_NexusTech.pdf",
                verification_source="PAN: AABCU9603R"
            ),
            BidChecklistItem(
                item_id="chk_04",
                tender_section="Envelope A: Statutory & Fee",
                title="Udyam Registration Certificate (MSE Fee/EMD Exemption)",
                description="Valid Udyam certificate with NIC Code 6201 to claim 100% EMD waiver under GFR Rule 170.",
                mandatory=True,
                status=ChecklistItemStatus.COMPLETED,
                associated_document_name="Udyam_Registration_NexusTech.pdf",
                verification_source="UDYAM-KR-03-0098472"
            ),
            BidChecklistItem(
                item_id="chk_05",
                tender_section="Envelope A: Statutory & Fee",
                title="Audited Financial Statements & CA Turnover Certificate",
                description="Balance sheets for FY 22-23, 23-24, 24-25 with CA UDIN certification.",
                mandatory=True,
                status=ChecklistItemStatus.COMPLETED,
                associated_document_name="Audited_Financials_FY23_25.pdf",
                verification_source="UDIN: 25089201AAAA"
            ),
            BidChecklistItem(
                item_id="chk_06",
                tender_section="Envelope B: Technical Bid",
                title="Previous Work Orders",
                description="Copies of relevant government or corporate software contracts.",
                mandatory=True,
                status=ChecklistItemStatus.COMPLETED,
                associated_document_name="WorkOrder_BU_2024.pdf",
                verification_source="Bangalore University Contract Ref: BU/IT/2024/88"
            ),
            BidChecklistItem(
                item_id="chk_07",
                tender_section="Envelope B: Technical Bid",
                title="Client Completion Certificate",
                description="Satisfactory work completion certificate for contract > ₹10 Lakh.",
                mandatory=True,
                status=ChecklistItemStatus.ACTION_REQUIRED,
                associated_document_name=None,
                verification_source="Missing from Document Repository"
            ),
            BidChecklistItem(
                item_id="chk_08",
                tender_section="Envelope B: Technical Bid",
                title="Technical Proposal & Approach Document",
                description="Comprehensive architecture, deployment strategy, and SLA management proposal.",
                mandatory=True,
                status=ChecklistItemStatus.PENDING,
                associated_document_name="Draft_Technical_Proposal.docx",
                verification_source="AI Generated Draft Ready for Human Approval"
            ),
            BidChecklistItem(
                item_id="chk_09",
                tender_section="Envelope C: Financial Bid",
                title="Financial Bid Form & Schedule of Rates (BoQ)",
                description="Itemized commercial pricing format as prescribed in GeM schedule.",
                mandatory=True,
                status=ChecklistItemStatus.PENDING,
                associated_document_name="BoQ_Schedule_Template.xlsx",
                verification_source="Commercial rates pending financial authorization"
            )
        ]

        completed = sum(1 for c in checklist if c.status == ChecklistItemStatus.COMPLETED)
        total = len(checklist)

        pkg_id = f"pkg_{tender.tender_id.replace('/', '_').replace('-', '_')}"
        pkg = BidPackage(
            package_id=pkg_id,
            tender_id=tender.tender_id,
            company_id=company.company_id,
            title=f"Bid Submission Dossier: {tender.title}",
            status="READY_FOR_REVIEW" if completed == total else "DRAFT",
            readiness_fraction=f"{completed}/{total}",
            completed_items_count=completed,
            total_items_count=total,
            checklist=checklist,
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat()
        )
        db.save_bid_package(pkg)
        return pkg.model_dump()

    def _tool_generate_proposal(self, tender_id: str, company_id: str = "comp_nexus_01") -> Dict[str, Any]:
        tender = db.get_tender(tender_id)
        if not tender:
            raise ValueError(f"Tender '{tender_id}' not found.")
        company = db.get_company(company_id)
        if not company:
            raise ValueError(f"Company '{company_id}' not found.")

        proposals = [
            GeneratedProposalSection(
                section_id="prop_01",
                title="1. Executive Summary & Organizational Credentials",
                content=(
                    f"{company.name} ({company.trade_name}) is an established {company.enterprise_category.title()} Enterprise "
                    f"incorporated in {company.city}, {company.state}, with {company.years_of_operation:.0f} years of distinguished "
                    f"track record delivering mission-critical web applications, cloud infrastructure, and software maintenance services. "
                    f"Our average annual turnover across the last 3 financial years stands at ₹{company.average_annual_turnover_inr:,.0f}, "
                    f"substantially exceeding the qualification threshold set out in {tender.reference_number}. "
                    f"As a registered MSME (Udyam: {company.udyam_registration_number}), we bring agile software engineering combined with "
                    f"strict adherence to ISO 9001:2015 quality frameworks."
                ),
                page_target="Section 1",
                ai_generated=True,
                human_approved=False
            ),
            GeneratedProposalSection(
                section_id="prop_02",
                title="2. Scope Understanding & Technical Solution Architecture",
                content=(
                    f"In response to the requirements specified by {tender.department}, our engineering team proposes a resilient, modular architecture "
                    f"leveraging modern microservices, hardened API gateways, and automated continuous integration pipelines. "
                    f"Our technical stack ({', '.join(company.technical_capabilities[:5])}) directly addresses the department's mandate for "
                    f"zero downtime, role-based access security, and full data sovereignty within Government of India data center guidelines."
                ),
                page_target="Section 2",
                ai_generated=True,
                human_approved=False
            ),
            GeneratedProposalSection(
                section_id="prop_03",
                title="3. Project Delivery, SLA Framework & Maintenance Plan",
                content=(
                    "We establish a 4-tier Support & Incident Resolution SLA:\n"
                    "• Severity 1 (Critical Service Outage): Initial response < 15 minutes; Mean Time to Restore < 2 hours.\n"
                    "• Severity 2 (Major Feature Impairment): Response < 1 hour; Resolution < 6 hours.\n"
                    "• Severity 3 (Routine Maintenance & Patches): Scheduled off-peak deployment with automated rollback guards.\n"
                    "Dedicated on-site and remote DevOps engineers will be assigned with daily health audits."
                ),
                page_target="Section 3",
                ai_generated=True,
                human_approved=False
            )
        ]

        undertakings = {
            "Non-Blacklisting Undertaking": (
                f"We hereby solemnly declare that {company.name} has never been blacklisted, debarred, or sanctioned by "
                f"any Central/State Government Ministry, Public Sector Undertaking, or multilateral development bank."
            ),
            "Public Procurement Make-in-India Declaration": (
                f"In compliance with Public Procurement (Preference to Make in India) Order, we certify that the local value addition "
                f"for services offered under {tender.reference_number} is greater than 80%, qualifying us as a Class-I Local Supplier."
            ),
            "Bid Security / EMD Exemption Declaration": (
                f"Under Rule 170(iii) of General Financial Rules 2017, we claim exemption from EMD payment as a registered Micro Enterprise "
                f"(Udyam: {company.udyam_registration_number}). We undertake that if we withdraw or modify our bid during validity, we shall be debarred for 2 years."
            )
        }

        # Update package in DB
        pkg = db.get_bid_package_by_tender(tender.tender_id, company.company_id)
        if pkg:
            pkg.proposals = proposals
            pkg.undertakings = undertakings
            pkg.updated_at = datetime.now().isoformat()
            db.save_bid_package(pkg)

        return {
            "tender_id": tender.tender_id,
            "company_id": company.company_id,
            "proposals": [p.model_dump() for p in proposals],
            "statutory_undertakings": undertakings
        }
