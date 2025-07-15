from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from services.evaluation_service import EvaluationService
from schemas.evaluation import EvaluationCreate, EvaluationUpdate, EvaluationResponse

router = APIRouter(prefix="/api/evaluations", tags=["Evaluations"])

class EvaluateResumeRequest(BaseModel):
    resume_id: str
    jd_id: str

def get_evaluation_service():
    return EvaluationService()

@router.post("/evaluate", response_model=EvaluationResponse)
async def evaluate_resume_with_ai(
    request: EvaluateResumeRequest,
    service: EvaluationService = Depends(get_evaluation_service)
):
    """
    Evaluate a resume against a job description using AI (Gemini 2.5 Flash)
    
    This endpoint:
    1. Fetches the resume and job description from the database
    2. Uses Google Gemini AI to evaluate the resume against the JD
    3. Stores the evaluation results in the database
    4. Returns the evaluation with detailed breakdown
    """
    try:
        result = service.evaluate_resume_with_ai(request.resume_id, request.jd_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/test-gemini")
async def test_gemini_connection(
    service: EvaluationService = Depends(get_evaluation_service)
):
    """Test the Gemini AI connection"""
    result = service.test_gemini_connection()
    return result

@router.post("/", response_model=EvaluationResponse)
async def create_evaluation(
    evaluation: EvaluationCreate,
    service: EvaluationService = Depends(get_evaluation_service)
):
    """Create a new evaluation"""
    try:
        return service.create_evaluation(evaluation)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{evaluation_id}", response_model=EvaluationResponse)
async def get_evaluation(
    evaluation_id: str,
    service: EvaluationService = Depends(get_evaluation_service)
):
    """Get an evaluation by ID"""
    result = service.get_evaluation(evaluation_id)
    if not result:
        raise HTTPException(status_code=404, detail="Evaluation not found")
    return result

@router.get("/", response_model=List[EvaluationResponse])
async def get_all_evaluations(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    service: EvaluationService = Depends(get_evaluation_service)
):
    """Get all evaluations with pagination"""
    return service.get_all_evaluations(skip=skip, limit=limit)

@router.put("/{evaluation_id}", response_model=EvaluationResponse)
async def update_evaluation(
    evaluation_id: str,
    evaluation: EvaluationUpdate,
    service: EvaluationService = Depends(get_evaluation_service)
):
    """Update an evaluation"""
    result = service.update_evaluation(evaluation_id, evaluation)
    if not result:
        raise HTTPException(status_code=404, detail="Evaluation not found")
    return result

@router.delete("/{evaluation_id}")
async def delete_evaluation(
    evaluation_id: str,
    service: EvaluationService = Depends(get_evaluation_service)
):
    """Delete an evaluation"""
    success = service.delete_evaluation(evaluation_id)
    if not success:
        raise HTTPException(status_code=404, detail="Evaluation not found")
    return {"message": "Evaluation deleted successfully"}

@router.get("/by-jd/{jd_id}", response_model=List[EvaluationResponse])
async def get_evaluations_by_jd(
    jd_id: str,
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    service: EvaluationService = Depends(get_evaluation_service)
):
    """Get evaluations for a specific job description"""
    return service.get_evaluations_by_jd(jd_id, skip=skip, limit=limit)

@router.get("/by-resume/{resume_id}", response_model=List[EvaluationResponse])
async def get_evaluations_by_resume(
    resume_id: str,
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    service: EvaluationService = Depends(get_evaluation_service)
):
    """Get evaluations for a specific resume"""
    return service.get_evaluations_by_resume_id(resume_id, skip=skip, limit=limit)

@router.get("/by-jd-and-resume/{jd_id}/{resume_id}", response_model=EvaluationResponse)
async def get_evaluation_by_jd_and_resume(
    jd_id: str,
    resume_id: str,
    service: EvaluationService = Depends(get_evaluation_service)
):
    """Get evaluation for a specific job description and resume combination"""
    result = service.get_evaluation_by_jd_and_resume(jd_id, resume_id)
    if not result:
        raise HTTPException(status_code=404, detail="Evaluation not found")
    return result

@router.get("/search/score-range", response_model=List[EvaluationResponse])
async def get_evaluations_by_score_range(
    min_score: float = Query(..., ge=0, le=100, description="Minimum score"),
    max_score: float = Query(..., ge=0, le=100, description="Maximum score"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    service: EvaluationService = Depends(get_evaluation_service)
):
    """Get evaluations within a score range"""
    if min_score > max_score:
        raise HTTPException(status_code=400, detail="min_score cannot be greater than max_score")
    return service.get_evaluations_by_score_range(min_score, max_score, skip=skip, limit=limit)

@router.get("/search/verdict/{verdict}", response_model=List[EvaluationResponse])
async def get_evaluations_by_verdict(
    verdict: str,
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    service: EvaluationService = Depends(get_evaluation_service)
):
    """Get evaluations by verdict"""
    return service.get_evaluations_by_verdict(verdict, skip=skip, limit=limit)

@router.get("/top/{jd_id}", response_model=List[EvaluationResponse])
async def get_top_evaluations(
    jd_id: str,
    limit: int = Query(10, ge=1, le=100, description="Number of top evaluations to return"),
    service: EvaluationService = Depends(get_evaluation_service)
):
    """Get top evaluations for a job description by score"""
    return service.get_top_evaluations(jd_id, limit=limit)

@router.get("/stats/count")
async def get_evaluation_count(
    service: EvaluationService = Depends(get_evaluation_service)
):
    """Get total count of evaluations"""
    count = service.get_evaluation_count()
    return {"count": count}

@router.get("/stats/count-by-jd/{jd_id}")
async def get_evaluation_count_by_jd(
    jd_id: str,
    service: EvaluationService = Depends(get_evaluation_service)
):
    """Get count of evaluations for a specific job description"""
    count = service.get_evaluation_count_by_jd(jd_id)
    return {"count": count}

@router.get("/stats/count-by-resume/{resume_id}")
async def get_evaluation_count_by_resume(
    resume_id: str,
    service: EvaluationService = Depends(get_evaluation_service)
):
    """Get count of evaluations for a specific resume"""
    count = service.get_evaluation_count_by_resume(resume_id)
    return {"count": count} 