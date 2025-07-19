from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime
from .base import PyObjectId, BaseSchema, TimestampSchema

class Education(BaseModel):
    degree: str = Field(..., description="Degree or qualification")
    institution: str = Field(..., description="Educational institution")
    year: Optional[int] = Field(None, description="Graduation year")
    gpa: Optional[float] = Field(None, description="Grade Point Average")

class Experience(BaseModel):
    title: str = Field(..., description="Job title")
    company: str = Field(..., description="Company name")
    start_date: Optional[str] = Field(None, description="Start date")
    end_date: Optional[str] = Field(None, description="End date (or 'Present')")
    description: Optional[str] = Field(None, description="Job description")

class ResumeBase(BaseModel):
    candidate_name: str = Field(..., description="Candidate's full name")
    email: EmailStr = Field(..., description="Candidate's email address")
    skills: List[str] = Field(default=[], description="List of skills")
    education: List[Education] = Field(default=[], description="Education history")
    experience: List[Experience] = Field(default=[], description="Work experience")
    raw_pdf_url: Optional[str] = Field(None, description="URL to the raw PDF file")
    raw_text: Optional[str] = Field(None, description="Extracted raw text from PDF")
    markdown_text: Optional[str] = None
    filename: Optional[str] = None
    links: Optional[List[Dict[str, str]]] = Field(default=None, description="List of extracted links (type, url)")

class ResumeCreate(ResumeBase):
    jd_ids: List[PyObjectId] = Field(default=[], description="List of job description IDs")

class ResumeUploadRequest(BaseModel):
    """Schema for resume upload request"""
    jd_id: str = Field(..., description="Selected job description ID")
    candidate_name: Optional[str] = Field(None, description="Candidate's full name (optional, can be extracted from PDF)")
    email: Optional[EmailStr] = Field(None, description="Candidate's email address (optional, can be extracted from PDF)")

class ResumeUpdate(BaseModel):
    candidate_name: Optional[str] = Field(None, description="Candidate's full name")
    email: Optional[EmailStr] = Field(None, description="Candidate's email address")
    skills: Optional[List[str]] = Field(None, description="List of skills")
    education: Optional[List[Education]] = Field(None, description="Education history")
    experience: Optional[List[Experience]] = Field(None, description="Work experience")
    raw_pdf_url: Optional[str] = Field(None, description="URL to the raw PDF file")
    raw_text: Optional[str] = Field(None, description="Extracted raw text from PDF")
    jd_ids: Optional[List[PyObjectId]] = Field(None, description="List of job description IDs")

class ResumeInDB(ResumeBase, TimestampSchema):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    jd_ids: List[PyObjectId] = Field(default=[], description="List of job description IDs")

class ResumeResponse(ResumeBase):
    id: str = Field(alias="_id")
    jd_ids: List[str] = Field(default=[], description="List of job description IDs")
    created_at: datetime
    updated_at: datetime
    evaluation: Optional[Dict[str, Any]] = None
    
    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True
    } 