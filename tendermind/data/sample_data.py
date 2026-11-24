from tendermind.models.tender import Tender, TenderRequirement, Corrigendum, RequirementCategory
from tendermind.models.company import CompanyProfile, BusinessCredential, BusinessDocument, DocumentStatus

SAMPLE_COMPANY: CompanyProfile = CompanyProfile(
    company_id="comp_nexus_01",
    name="Nexus Technology Solutions Pvt Ltd",
    trade_name="NexusTech",
    business_type="Private Limited",
    state="Karnataka",
    city="Bengaluru",
    pincode="560001",
    udyam_registration_number="UDYAM-KR-03-0098472",
    enterprise_category="MICRO",
    incorporation_date="2022-04-15",
    years_of_operation=4.0,
    pan_number="AABCU9603R",
    gstin="29AABCU9603R1ZM",
    annual_turnover_fy={
        "2022-23": 2800000.0,
        "2023-24": 3500000.0,
        "2024-25": 4100000.0
    },
    average_annual_turnover_inr=3466666.67,
    net_worth_inr=4500000.0,
    core_services=[
        "Web development",
        "Software maintenance",
        "Cloud solutions",
        "API integration",
        "DevOps consulting"
    ],
    technical_capabilities=[
        "Python", "FastAPI", "React", "PostgreSQL", "Docker", "AWS", "GovStack"
    ],
    past_projects_count=5,
    completed_contracts_value_inr=8200000.0,
    certifications=["ISO 9001:2015"],
    credentials=[
        BusinessCredential(
            credential_id="cred_01",
            company_id="comp_nexus_01",
            credential_type="UDYAM",
            identifier_value="UDYAM-KR-03-0098472",
            valid_from="2022-05-10",
            valid_until=None,
            status="ACTIVE"
        ),
        BusinessCredential(
            credential_id="cred_02",
            company_id="comp_nexus_01",
            credential_type="GSTIN",
            identifier_value="29AABCU9603R1ZM",
            valid_from="2022-04-20",
            valid_until=None,
            status="ACTIVE"
        ),
        BusinessCredential(
            credential_id="cred_03",
            company_id="comp_nexus_01",
            credential_type="PAN",
            identifier_value="AABCU9603R",
            valid_from="2022-04-16",
            valid_until=None,
            status="ACTIVE"
        )
    ],
    documents=[
        BusinessDocument(
            document_id="doc_gst_01",
            company_id="comp_nexus_01",
            document_type="GST certificate",
            title="GST Registration Certificate (Form GST REG-06)",
            file_name="GST_REG_06_NexusTech.pdf",
            status=DocumentStatus.UPLOADED,
            upload_date="2026-01-10",
            expiry_date=None,
            issuing_authority="Government of India - GSTN",
            verification_hash="sha256_gst_981a2f",
            is_verified=True
        ),
        BusinessDocument(
            document_id="doc_pan_01",
            company_id="comp_nexus_01",
            document_type="PAN",
            title="Permanent Account Number Card",
            file_name="PAN_Card_NexusTech.pdf",
            status=DocumentStatus.UPLOADED,
            upload_date="2026-01-10",
            expiry_date=None,
            issuing_authority="Income Tax Department",
            verification_hash="sha256_pan_224b1c",
            is_verified=True
        ),
        BusinessDocument(
            document_id="doc_udyam_01",
            company_id="comp_nexus_01",
            document_type="Udyam certificate",
            title="Udyam Registration Certificate (MSE)",
            file_name="Udyam_Registration_NexusTech.pdf",
            status=DocumentStatus.UPLOADED,
            upload_date="2026-01-12",
            expiry_date=None,
            issuing_authority="Ministry of MSME, Govt of India",
            verification_hash="sha256_udyam_449c0d",
            is_verified=True
        ),
        BusinessDocument(
            document_id="doc_ca_01",
            company_id="comp_nexus_01",
            document_type="Audited financial statements",
            title="Audited Financial Statements & CA Turnover Certificate FY 2022-25",
            file_name="Audited_Financials_FY23_25.pdf",
            status=DocumentStatus.UPLOADED,
            upload_date="2026-02-01",
            financial_year="2024-25",
            issuing_authority="M/s R.K. & Associates Chartered Accountants (UDIN: 25089201AAAA)",
            verification_hash="sha256_ca_1098ef",
            is_verified=True
        ),
        BusinessDocument(
            document_id="doc_wo_01",
            company_id="comp_nexus_01",
            document_type="Previous work orders",
            title="Work Order - Bangalore University Web Portal Revamp",
            file_name="WorkOrder_BU_2024.pdf",
            status=DocumentStatus.UPLOADED,
            upload_date="2026-02-15",
            issuing_authority="Bangalore University",
            verification_hash="sha256_wo_7718de",
            is_verified=True
        ),
        BusinessDocument(
            document_id="doc_iso_01",
            company_id="comp_nexus_01",
            document_type="Technical certifications",
            title="ISO 9001:2015 Quality Management Certificate",
            file_name="ISO_9001_Certificate_NexusTech.pdf",
            status=DocumentStatus.UPLOADED,
            upload_date="2026-01-15",
            expiry_date="2027-01-14",
            issuing_authority="Bureau Veritas Certification",
            verification_hash="sha256_iso_6654ab",
            is_verified=True
        ),
        BusinessDocument(
            document_id="doc_comp_cert_missing",
            company_id="comp_nexus_01",
            document_type="Completion certificate",
            title="Formal Client Completion & Satisfactory Service Certificate",
            file_name="",
            status=DocumentStatus.MISSING,
            upload_date=None,
            is_verified=False
        )
    ]
)

SAMPLE_TENDERS = [
    Tender(
        tender_id="GEM/2026/B/123456",
        title="Comprehensive Annual Maintenance, Software Enhancement and Cloud Solutions",
        reference_number="GEM-2026-IT-123456",
        portal_source="GeM (Government e-Marketplace)",
        department="Department of Administrative Reforms & Public Grievances",
        location="New Delhi / Karnataka",
        estimated_value_inr=2500000.0,  # 25 Lakh
        earnest_money_deposit_inr=50000.0,
        tender_fee_inr=0.0,
        publication_date="2026-11-15",
        submission_deadline="2026-12-15T15:00:00",
        pre_bid_meeting_date="2026-12-05T11:00:00",
        category="IT Services",
        summary="Procurement of application support, cloud maintenance, automated API integration and bug fixes for central grievance management portal.",
        original_document_url="https://gem.gov.in/tenders/GEM-2026-B-123456.pdf",
        msme_exemption_clause="As per Public Procurement Policy for MSEs Order 2012 and Rule 170 of GFR 2017, eligible Micro and Small Enterprises registered with Udyam are exempted from payment of EMD and Tender Fee. Prior experience and turnover criteria are relaxed subject to meeting quality and technical specifications.",
        status="AMENDED",
        suitability_score=92,
        requirements=[
            TenderRequirement(
                requirement_id="req_turnover",
                tender_id="GEM/2026/B/123456",
                category=RequirementCategory.FINANCIAL,
                clause_title="Minimum Annual Turnover",
                description="Bidder must have minimum average annual financial turnover of ₹20.00 Lakh over the last 3 financial years (FY 2022-23, 2023-24, 2024-25).",
                source_page=12,
                source_section="Section 4.2: Financial Eligibility Criteria",
                mandatory=True,
                threshold_value=2000000.0,
                threshold_unit="INR",
                relaxable_for_msme=True,
                evidence_types_accepted=["Audited financial statements", "CA Turnover certificate with UDIN"]
            ),
            TenderRequirement(
                requirement_id="req_experience",
                tender_id="GEM/2026/B/123456",
                category=RequirementCategory.EXPERIENCE,
                clause_title="Years of Business Experience",
                description="Bidder must have at least 3 completed years of commercial operations in software development and maintenance.",
                source_page=13,
                source_section="Section 4.3: Technical and Operational Capacity",
                mandatory=True,
                threshold_value=3.0,
                threshold_unit="years",
                relaxable_for_msme=True,
                evidence_types_accepted=["Certificate of Incorporation", "First commercial invoice / Work Order"]
            ),
            TenderRequirement(
                requirement_id="req_gst",
                tender_id="GEM/2026/B/123456",
                category=RequirementCategory.STATUTORY,
                clause_title="GST Registration Certificate",
                description="Bidder must possess a valid Goods and Services Tax (GST) registration certificate issued by the competent tax authority.",
                source_page=4,
                source_section="Section 2.1: Mandatory Statutory Compliances",
                mandatory=True,
                relaxable_for_msme=False,
                evidence_types_accepted=["GST certificate (REG-06)"]
            ),
            TenderRequirement(
                requirement_id="req_pan",
                tender_id="GEM/2026/B/123456",
                category=RequirementCategory.STATUTORY,
                clause_title="PAN Registration",
                description="Copy of valid Permanent Account Number (PAN) card of the enterprise/entity.",
                source_page=4,
                source_section="Section 2.2: Mandatory Statutory Compliances",
                mandatory=True,
                relaxable_for_msme=False,
                evidence_types_accepted=["PAN"]
            ),
            TenderRequirement(
                requirement_id="req_emd",
                tender_id="GEM/2026/B/123456",
                category=RequirementCategory.EMD_FEE,
                clause_title="Earnest Money Deposit (EMD)",
                description="Earnest Money Deposit of ₹50,000 via online bank guarantee or demand draft. MSMEs with valid Udyam certificate are 100% exempt under GFR Rule 170.",
                source_page=5,
                source_section="Section 2.5: Bid Security / EMD Exemption",
                mandatory=True,
                threshold_value=50000.0,
                threshold_unit="INR",
                relaxable_for_msme=True,
                evidence_types_accepted=["Udyam certificate", "EMD Bank Guarantee", "Bid Security Declaration"]
            ),
            TenderRequirement(
                requirement_id="req_completion_cert",
                tender_id="GEM/2026/B/123456",
                category=RequirementCategory.TECHNICAL,
                clause_title="Client Completion Certificate",
                description="Satisfactory work completion certificate from client for at least one completed software development contract of value not less than ₹10 Lakh.",
                source_page=14,
                source_section="Section 5.1: Past Performance Credentials",
                mandatory=True,
                threshold_value=1000000.0,
                threshold_unit="INR",
                relaxable_for_msme=False,
                evidence_types_accepted=["Completion certificate signed by client competent authority"]
            ),
            TenderRequirement(
                requirement_id="req_iso",
                tender_id="GEM/2026/B/123456",
                category=RequirementCategory.CERTIFICATION,
                clause_title="ISO 9001:2015 Certification",
                description="Bidder must hold a valid ISO 9001:2015 Quality Management System accreditation at the date of bid opening.",
                source_page=15,
                source_section="Section 5.3: Quality Certifications",
                mandatory=False,
                relaxable_for_msme=False,
                evidence_types_accepted=["ISO 9001:2015 certificate"]
            )
        ],
        corrigenda=[
            Corrigendum(
                corrigendum_id="corrigendum_gem_01",
                tender_id="GEM/2026/B/123456",
                corrigendum_number=1,
                issue_date="2026-11-20",
                title="Corrigendum #1: Extension of Submission Date & Make-in-India Declaration",
                description="Revised submission deadline extended by 5 days. Added mandatory declaration under Public Procurement (Preference to Make in India) Order.",
                affected_sections=["Section 1: Critical Dates", "Section 7: Declarations"],
                old_value="Submission Deadline: 10 December 2026, 15:00 IST",
                new_value="Submission Deadline: 15 December 2026, 15:00 IST",
                impact_type="DEADLINE_EXTENSION",
                action_required="Bid submission timeline updated. Make-in-India local content undertaking must be attached in Envelope A."
            ),
            Corrigendum(
                corrigendum_id="corrigendum_gem_02",
                tender_id="GEM/2026/B/123456",
                corrigendum_number=2,
                issue_date="2026-11-22",
                title="Corrigendum #2: Clarification on MSME EMD Relaxation",
                description="Clarified that Micro and Small Enterprises holding valid Udyam Registration are fully exempted from EMD deposit regardless of enterprise turnover.",
                affected_sections=["Section 2.5: EMD Exemption Clause"],
                old_value="EMD exemption required CA net worth certificate",
                new_value="Only valid Udyam Registration Certificate required",
                impact_type="EMD_REDUCTION",
                action_required="Ensure Udyam Certificate is uploaded in the EMD Exemption slot. No demand draft needed."
            )
        ]
    ),
    Tender(
        tender_id="CPPP/2026/NIC/9821",
        title="Design, Development and Cloud Hosting of Citizen Grievance Web Portal",
        reference_number="NIC-HQ-2026-9821",
        portal_source="CPPP (Central Public Procurement Portal)",
        department="National Informatics Centre (NIC), Ministry of Electronics & IT",
        location="Pan-India / Karnataka Hub",
        estimated_value_inr=1800000.0,  # 18 Lakh
        earnest_money_deposit_inr=36000.0,
        tender_fee_inr=500.0,
        publication_date="2026-11-18",
        submission_deadline="2026-12-22T17:00:00",
        pre_bid_meeting_date="2026-12-08T14:30:00",
        category="IT Services",
        summary="Turnkey software development, responsive citizen dashboard, multilingual UI and Postgres cloud database for public grievance redressal.",
        original_document_url="https://eprocure.gov.in/eprocure/app?page=NIC9821.pdf",
        msme_exemption_clause="MSEs are exempted from tender fee and EMD. Relaxations under Startups and MSE Policy applicable.",
        status="ACTIVE",
        suitability_score=95,
        requirements=[
            TenderRequirement(
                requirement_id="req_nic_01",
                tender_id="CPPP/2026/NIC/9821",
                category=RequirementCategory.FINANCIAL,
                clause_title="Minimum Turnover",
                description="Minimum ₹15 Lakh average annual turnover in preceding 2 financial years.",
                source_page=8,
                source_section="Clause 3.1: Commercial Pre-qualification",
                mandatory=True,
                threshold_value=1500000.0,
                threshold_unit="INR",
                relaxable_for_msme=True,
                evidence_types_accepted=["Audited financial statements"]
            ),
            TenderRequirement(
                requirement_id="req_nic_02",
                tender_id="CPPP/2026/NIC/9821",
                category=RequirementCategory.EXPERIENCE,
                clause_title="Operational Experience",
                description="Minimum 2 years experience in web application development.",
                source_page=9,
                source_section="Clause 3.2: Technical Experience",
                mandatory=True,
                threshold_value=2.0,
                threshold_unit="years",
                relaxable_for_msme=True,
                evidence_types_accepted=["Certificate of Incorporation", "Previous work orders"]
            ),
            TenderRequirement(
                requirement_id="req_nic_03",
                tender_id="CPPP/2026/NIC/9821",
                category=RequirementCategory.STATUTORY,
                clause_title="GST and PAN",
                description="Valid GST and PAN registrations.",
                source_page=4,
                source_section="Clause 2: Statutory",
                mandatory=True,
                relaxable_for_msme=False,
                evidence_types_accepted=["GST certificate", "PAN"]
            )
        ],
        corrigenda=[]
    ),
    Tender(
        tender_id="KPPP/2026/BBMP/0042",
        title="Smart Waste Logistics IoT Dashboard & Real-Time Fleet Tracking App",
        reference_number="BBMP-SW-2026-0042",
        portal_source="Karnataka Public Procurement Portal (KPPP)",
        department="Bruhat Bengaluru Mahanagara Palike (BBMP)",
        location="Bengaluru, Karnataka",
        estimated_value_inr=4500000.0,  # 45 Lakh
        earnest_money_deposit_inr=90000.0,
        tender_fee_inr=2000.0,
        publication_date="2026-11-21",
        submission_deadline="2026-12-28T16:00:00",
        pre_bid_meeting_date="2026-12-10T11:00:00",
        category="IT Services",
        summary="Real-time telemetry aggregation, geofencing API and responsive mobile UI for municipal waste vehicle tracking.",
        original_document_url="https://kppp.karnataka.gov.in/tender/BBMP-0042.pdf",
        msme_exemption_clause="Karnataka state MSME policy provisions for EMD relaxation applicable.",
        status="ACTIVE",
        suitability_score=85,
        requirements=[
            TenderRequirement(
                requirement_id="req_bbmp_01",
                tender_id="KPPP/2026/BBMP/0042",
                category=RequirementCategory.FINANCIAL,
                clause_title="Minimum Turnover Requirement",
                description="Minimum average annual turnover of ₹30 Lakh in last 3 financial years.",
                source_page=10,
                source_section="Section 3.1: Financial Turnover",
                mandatory=True,
                threshold_value=3000000.0,
                threshold_unit="INR",
                relaxable_for_msme=True,
                evidence_types_accepted=["Audited financial statements"]
            ),
            TenderRequirement(
                requirement_id="req_bbmp_02",
                tender_id="KPPP/2026/BBMP/0042",
                category=RequirementCategory.EXPERIENCE,
                clause_title="Experience in IoT / GPS tracking systems",
                description="Bidder must have completed at least 2 software projects involving live telemetry or maps integration.",
                source_page=11,
                source_section="Section 3.4: Technical Domain Experience",
                mandatory=True,
                threshold_value=2.0,
                threshold_unit="projects",
                relaxable_for_msme=False,
                evidence_types_accepted=["Previous work orders"]
            )
        ],
        corrigenda=[]
    ),
    Tender(
        tender_id="CPPP/2026/NHAI/7710",
        title="Four-Laning & Rigid Pavement Construction of Hyderabad-Warangal Highway",
        reference_number="NHAI-RO-HYD-2026-7710",
        portal_source="CPPP (Central Public Procurement Portal)",
        department="National Highways Authority of India (NHAI)",
        location="Telangana",
        estimated_value_inr=750000000.0,  # 75 Crore
        earnest_money_deposit_inr=15000000.0,  # 1.5 Crore
        tender_fee_inr=50000.0,
        publication_date="2026-11-10",
        submission_deadline="2026-12-18T11:00:00",
        pre_bid_meeting_date="2026-11-25T11:00:00",
        category="Civil Construction & Infrastructure",
        summary="Civil construction of multi-lane bituminous asphalt highway, concrete bridges and road drainage works.",
        original_document_url="https://eprocure.gov.in/nhai/7710.pdf",
        msme_exemption_clause="No MSME relaxation for major EPC highway construction packages exceeding ₹50 Crore.",
        status="ACTIVE",
        suitability_score=18,
        requirements=[
            TenderRequirement(
                requirement_id="req_nhai_01",
                tender_id="CPPP/2026/NHAI/7710",
                category=RequirementCategory.FINANCIAL,
                clause_title="Heavy Infrastructure Turnover",
                description="Minimum average annual turnover of ₹50 Crore in civil infrastructure works.",
                source_page=16,
                source_section="Section 4: Technical & Financial Prequalification",
                mandatory=True,
                threshold_value=500000000.0,
                threshold_unit="INR",
                relaxable_for_msme=False,
                evidence_types_accepted=["Audited financial statements"]
            )
        ],
        corrigenda=[]
    )
]
