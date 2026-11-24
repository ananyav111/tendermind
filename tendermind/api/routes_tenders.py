from fastapi import APIRouter, HTTPException, Body
from typing import Optional, List
from pydantic import BaseModel
from tendermind.data.db import db
from tendermind.models.tender import Tender
from tendermind.engine.pdf_processor import TenderPDFProcessor

router = APIRouter(prefix="/api/tenders", tags=["Tenders"])

class TenderUploadRequest(BaseModel):
    title: str
    department: str
    estimated_value: float
    submission_deadline: str
    text_content: Optional[str] = None
    portal_source: Optional[str] = "Manual Ingestion"

@router.get("", response_model=List[Tender])
def list_tenders(
    query: Optional[str] = None,
    category: Optional[str] = None,
    location: Optional[str] = None,
    max_value: Optional[float] = None
):
    return db.search_tenders(query=query, category=category, location=location, max_value=max_value)

@router.get("/{tender_id:path}")
def get_tender(tender_id: str):
    tender = db.get_tender(tender_id)
    if not tender:
        raise HTTPException(status_code=404, detail=f"Tender '{tender_id}' not found")
    return tender

@router.post("/upload")
def upload_tender_doc(req: TenderUploadRequest = Body(...)):
    tender_id = f"UPLOAD/2026/{req.title[:6].upper().replace(' ', '')}"
    extracted_text = req.text_content or f"{req.title} for {req.department}. Minimum turnover of ₹20 Lakh required. 3 years experience mandatory."

    requirements = TenderPDFProcessor.extract_clauses_from_text(extracted_text, tender_id)

    new_tender = Tender(
        tender_id=tender_id,
        title=req.title,
        reference_number=f"REF-{tender_id}",
        portal_source=req.portal_source or "Manual Ingestion",
        department=req.department,
        location="India",
        estimated_value_inr=req.estimated_value,
        earnest_money_deposit_inr=req.estimated_value * 0.02,
        publication_date="2026-11-24",
        submission_deadline=req.submission_deadline,
        category="IT Services" if "software" in req.title.lower() or "cloud" in req.title.lower() else "General Services",
        summary=f"Ingested tender notice: {req.title}. Processed {len(requirements)} requirement clauses with citation linking.",
        requirements=requirements,
        status="ACTIVE",
        suitability_score=85
    )
    db.save_tender(new_tender)
    return {"message": "Tender uploaded and structured successfully", "tender": new_tender}
