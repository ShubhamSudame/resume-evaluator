from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from .base import PyObjectId, BaseSchema, TimestampSchema

class JobDescriptionBase(BaseModel):
    title: str = Field(..., description="Job title")
    jd_text: str = Field(..., description="Full job description text")

class JobDescriptionCreate(JobDescriptionBase):
    pass

class JobDescriptionUpdate(BaseModel):
    title: Optional[str] = Field(None, description="Job title")
    jd_text: Optional[str] = Field(None, description="Full job description text")

class JobDescriptionInDB(JobDescriptionBase, TimestampSchema):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

class JobDescriptionResponse(JobDescriptionBase):
    id: str = Field(alias="_id")
    created_at: datetime
    updated_at: datetime
    
    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True
    } 