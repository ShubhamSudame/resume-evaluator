from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List, Optional
from services.job_description_service import JobDescriptionService
from schemas.job_description import JobDescriptionCreate, JobDescriptionUpdate, JobDescriptionResponse

router = APIRouter(prefix="/api/job-descriptions", tags=["Job Descriptions"])

def get_job_description_service():
    return JobDescriptionService()

@router.post("/", response_model=JobDescriptionResponse)
async def create_job_description(
    job_description: JobDescriptionCreate,
    service: JobDescriptionService = Depends(get_job_description_service)
):
    """Create a new job description with title and JD text"""
    try:
        return service.create_job_description(job_description)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[JobDescriptionResponse])
async def get_all_job_descriptions(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    service: JobDescriptionService = Depends(get_job_description_service)
):
    """Get all job descriptions with pagination"""
    return service.get_all_job_descriptions(skip=skip, limit=limit)

@router.get("/{jd_id}", response_model=JobDescriptionResponse)
async def get_job_description(
    jd_id: str,
    service: JobDescriptionService = Depends(get_job_description_service)
):
    """Get a job description by ID"""
    result = service.get_job_description(jd_id)
    if not result:
        raise HTTPException(status_code=404, detail="Job description not found")
    return result

@router.put("/{jd_id}", response_model=JobDescriptionResponse)
async def update_job_description(
    jd_id: str,
    job_description: JobDescriptionUpdate,
    service: JobDescriptionService = Depends(get_job_description_service)
):
    """Update a job description"""
    result = service.update_job_description(jd_id, job_description)
    if not result:
        raise HTTPException(status_code=404, detail="Job description not found")
    return result

@router.delete("/{jd_id}")
async def delete_job_description(
    jd_id: str,
    service: JobDescriptionService = Depends(get_job_description_service)
):
    """Delete a job description"""
    success = service.delete_job_description(jd_id)
    if not success:
        raise HTTPException(status_code=404, detail="Job description not found")
    return {"message": "Job description deleted successfully"}

@router.get("/search/", response_model=List[JobDescriptionResponse])
async def search_job_descriptions(
    title: str = Query(..., description="Title to search for"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    service: JobDescriptionService = Depends(get_job_description_service)
):
    """Search job descriptions by title"""
    return service.search_job_descriptions(title, skip=skip, limit=limit)

@router.get("/stats/count")
async def get_job_description_count(
    service: JobDescriptionService = Depends(get_job_description_service)
):
    """Get total count of job descriptions"""
    count = service.get_job_description_count()
    return {"count": count} 