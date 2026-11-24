from fastapi import APIRouter, HTTPException, Query, UploadFile, File, Form
from datetime import datetime
from tendermind.data.db import db
from tendermind.models.company import CompanyProfile, BusinessDocument, DocumentStatus

router = APIRouter(prefix="/api/company", tags=["Company Profile"])

@router.get("", response_model=CompanyProfile)
def get_company_profile(company_id: str = "comp_nexus_01"):
    company = db.get_company(company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company profile not found")
    return company

@router.post("/documents/resolve-gap")
def resolve_missing_document(
    company_id: str = "comp_nexus_01",
    document_type: str = "Completion certificate",
    title: str = "Client Completion Certificate - Bangalore University"
):
    """
    Simulates uploading the missing document (e.g., Client Completion Certificate)
    to demonstrate real-time eligibility resolution and readiness transformation.
    """
    company = db.get_company(company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    # Look for existing missing doc or add
    updated = False
    for doc in company.documents:
        if document_type.lower() in doc.document_type.lower():
            doc.status = DocumentStatus.UPLOADED
            doc.title = title
            doc.file_name = f"{document_type.replace(' ', '_')}_Verified.pdf"
            doc.upload_date = datetime.now().strftime("%Y-%m-%d")
            doc.is_verified = True
            doc.issuing_authority = "Bangalore University Registrar"
            doc.verification_hash = "sha256_verified_resolution_891e"
            updated = True
            break

    if not updated:
        company.documents.append(BusinessDocument(
            document_id=f"doc_{len(company.documents)+1}",
            company_id=company_id,
            document_type=document_type,
            title=title,
            file_name=f"{document_type.replace(' ', '_')}_Verified.pdf",
            status=DocumentStatus.UPLOADED,
            upload_date=datetime.now().strftime("%Y-%m-%d"),
            issuing_authority="Client Authority",
            verification_hash="sha256_verified_resolution_891e",
            is_verified=True
        ))

    db.update_company(company)
    return {
        "success": True,
        "message": f"Successfully uploaded and verified '{document_type}' in company document repository.",
        "company": company
    }
