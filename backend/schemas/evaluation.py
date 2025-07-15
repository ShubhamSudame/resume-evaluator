from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from .base import PyObjectId, BaseSchema, TimestampSchema

class CategoryBreakdown(BaseModel):
    technical_skills: float = Field(..., description="Technical skills score (0-100)")
    experience: float = Field(..., description="Experience score (0-100)")
    education: float = Field(..., description="Education score (0-100)")
    communication: float = Field(..., description="Communication skills score (0-100)")

class EvaluationBase(BaseModel):
    jd_id: PyObjectId = Field(..., description="Job description ID")
    resume_id: PyObjectId = Field(..., description="Resume ID")
    score: float = Field(..., ge=0, le=100, description="Overall evaluation score (0-100)")
    verdict: str = Field(..., description="Evaluation verdict (e.g., 'Strong Match', 'Good Match', 'Weak Match')")
    category_breakdown: CategoryBreakdown = Field(..., description="Breakdown of scores by category")
    matched_skills: List[str] = Field(default=[], description="Skills that match the job description")
    missing_skills: List[str] = Field(default=[], description="Skills missing from the resume")
    pros: List[str] = Field(default=[], description="Positive aspects of the candidate")
    cons: List[str] = Field(default=[], description="Areas for improvement")
    feedback: str = Field(..., description="Detailed feedback and recommendations")

class EvaluationCreate(EvaluationBase):
    pass

class EvaluationUpdate(BaseModel):
    score: Optional[float] = Field(None, ge=0, le=100, description="Overall evaluation score (0-100)")
    verdict: Optional[str] = Field(None, description="Evaluation verdict")
    category_breakdown: Optional[CategoryBreakdown] = Field(None, description="Breakdown of scores by category")
    matched_skills: Optional[List[str]] = Field(None, description="Skills that match the job description")
    missing_skills: Optional[List[str]] = Field(None, description="Skills missing from the resume")
    pros: Optional[List[str]] = Field(None, description="Positive aspects of the candidate")
    cons: Optional[List[str]] = Field(None, description="Areas for improvement")
    feedback: Optional[str] = Field(None, description="Detailed feedback and recommendations")

class EvaluationInDB(EvaluationBase, TimestampSchema):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    evaluated_at: datetime = Field(default_factory=datetime.utcnow, description="When the evaluation was performed")

class EvaluationResponse(EvaluationBase):
    id: str = Field(alias="_id")
    jd_id: str = Field(..., description="Job description ID")
    resume_id: str = Field(..., description="Resume ID")
    evaluated_at: datetime
    created_at: datetime
    updated_at: datetime
    
    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True
    } 