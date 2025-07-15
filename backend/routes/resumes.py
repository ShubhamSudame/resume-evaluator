from fastapi import APIRouter, HTTPException, Query, Depends, UploadFile, File, Form
from typing import List, Optional
import os
import tempfile
import shutil
from bson import ObjectId
from services.resume_service import ResumeService
from schemas.resume import ResumeCreate, ResumeUpdate, ResumeResponse, ResumeUploadRequest
from utils.pdf_parser import PDFTextExtractor
import markitdown
from markitdown import MarkItDown
import time
import re

router = APIRouter(prefix="/api/resumes", tags=["Resumes"])

def get_resume_service():
    return ResumeService()

def sanitize_filename(filename: str, fallback: str) -> str:
    # Remove path separators and non-printable characters
    filename = os.path.basename(filename)
    filename = re.sub(r'[^\w\-. ]', '', filename)
    # Limit length
    max_length = 100
    if len(filename) > max_length or not filename:
        filename = fallback
    return filename

@router.post("/upload", response_model=ResumeResponse)
async def upload_resume(
    file: UploadFile = File(..., description="PDF resume file"),
    jd_id: str = Form(..., description="Selected job description ID"),
    candidate_name: Optional[str] = Form(None, description="Candidate's full name (optional)"),
    email: Optional[str] = Form(None, description="Candidate's email address (optional)"),
    service: ResumeService = Depends(get_resume_service)
):
    """Upload a PDF resume with job description association"""
    try:
        # Validate file type
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Only PDF files are allowed")
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
            shutil.copyfileobj(file.file, temp_file)
            temp_file_path = temp_file.name
        
        try:
            # Validate PDF file
            if not PDFTextExtractor.validate_pdf_file(temp_file_path):
                raise HTTPException(status_code=400, detail="Invalid PDF file")
            
            # Extract text from PDF
            raw_text = PDFTextExtractor.extract_text(temp_file_path)
            if not raw_text:
                raise HTTPException(status_code=400, detail="Could not extract text from PDF")
            
            # Convert PDF to markdown using markitdown (pass file path, not raw text)
            md = MarkItDown()
            result = md.convert(temp_file_path)
            markdown_text = result.text_content
            
            # Extract basic info if not provided
            extracted_name, extracted_email = PDFTextExtractor.extract_basic_info(raw_text)
            
            # Use provided values or extracted values
            final_name = candidate_name or extracted_name or "Unknown Candidate"
            final_email = email or extracted_email or "unknown@example.com"
            
            # Determine filename
            fallback_name = f"{final_name.replace(' ', '_')}_{int(time.time())}.pdf"
            safe_filename = sanitize_filename(file.filename, fallback_name) if file.filename else fallback_name
            
            # Create resume data
            resume_data = ResumeCreate(
                candidate_name=final_name,
                email=final_email,
                skills=[],  # Empty for now as requested
                education=[],
                experience=[],
                raw_text=raw_text,
                markdown_text=markdown_text,
                jd_ids=[ObjectId(jd_id)],
                filename=safe_filename
            )
            
            # Save resume
            result = service.create_resume(resume_data)
            
            return result
            
        finally:
            # Clean up temporary file
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
                
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process resume: {str(e)}")

@router.post("/", response_model=ResumeResponse)
async def create_resume(
    resume: ResumeCreate,
    service: ResumeService = Depends(get_resume_service)
):
    """Create a new resume"""
    try:
        return service.create_resume(resume)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{resume_id}", response_model=ResumeResponse)
async def get_resume(
    resume_id: str,
    service: ResumeService = Depends(get_resume_service)
):
    """Get a resume by ID"""
    result = service.get_resume(resume_id)
    if not result:
        raise HTTPException(status_code=404, detail="Resume not found")
    return result

@router.get("/", response_model=List[ResumeResponse])
async def get_all_resumes(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    service: ResumeService = Depends(get_resume_service)
):
    """Get all resumes with pagination"""
    return service.get_all_resumes(skip=skip, limit=limit)

@router.put("/{resume_id}", response_model=ResumeResponse)
async def update_resume(
    resume_id: str,
    resume: ResumeUpdate,
    service: ResumeService = Depends(get_resume_service)
):
    """Update a resume"""
    result = service.update_resume(resume_id, resume)
    if not result:
        raise HTTPException(status_code=404, detail="Resume not found")
    return result

@router.delete("/{resume_id}")
async def delete_resume(
    resume_id: str,
    service: ResumeService = Depends(get_resume_service)
):
    """Delete a resume"""
    success = service.delete_resume(resume_id)
    if not success:
        raise HTTPException(status_code=404, detail="Resume not found")
    return {"message": "Resume deleted successfully"}

@router.get("/search/name", response_model=List[ResumeResponse])
async def search_resumes_by_name(
    name: str = Query(..., description="Candidate name to search for"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    service: ResumeService = Depends(get_resume_service)
):
    """Search resumes by candidate name"""
    return service.search_by_candidate_name(name, skip=skip, limit=limit)

@router.get("/by-jd/{jd_id}", response_model=List[ResumeResponse])
async def get_resumes_by_jd(
    jd_id: str,
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    service: ResumeService = Depends(get_resume_service)
):
    """Get resumes associated with a specific job description"""
    return service.get_resumes_by_jd_id(jd_id, skip=skip, limit=limit)

@router.post("/{resume_id}/associate-jd/{jd_id}")
async def add_jd_association(
    resume_id: str,
    jd_id: str,
    service: ResumeService = Depends(get_resume_service)
):
    """Add a job description association to a resume"""
    success = service.add_jd_association(resume_id, jd_id)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to add association")
    return {"message": "Association added successfully"}

@router.delete("/{resume_id}/associate-jd/{jd_id}")
async def remove_jd_association(
    resume_id: str,
    jd_id: str,
    service: ResumeService = Depends(get_resume_service)
):
    """Remove a job description association from a resume"""
    success = service.remove_jd_association(resume_id, jd_id)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to remove association")
    return {"message": "Association removed successfully"}

@router.get("/stats/count")
async def get_resume_count(
    service: ResumeService = Depends(get_resume_service)
):
    """Get total count of resumes"""
    count = service.get_resume_count()
    return {"count": count} 