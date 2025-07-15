from pydantic import BaseModel, Field, field_validator
from typing import Optional, Any, Union, Annotated
from datetime import datetime
from bson import ObjectId
from pydantic_core import core_schema

class PyObjectId:
    """Custom ObjectId type for Pydantic v2"""
    
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type: Any, handler) -> core_schema.CoreSchema:
        return core_schema.union_schema([
            core_schema.is_instance_schema(ObjectId),
            core_schema.chain_schema([
                core_schema.str_schema(),
                core_schema.no_info_plain_validator_function(cls.validate)
            ])
        ])
    
    @classmethod
    def validate(cls, v: Any) -> ObjectId:
        if isinstance(v, ObjectId):
            return v
        if isinstance(v, str):
            if ObjectId.is_valid(v):
                return ObjectId(v)
        raise ValueError("Invalid ObjectId")
    
    @classmethod
    def __get_pydantic_json_schema__(cls, core_schema: core_schema.CoreSchema, handler) -> dict[str, Any]:
        return {"type": "string", "format": "objectid"}

class BaseSchema(BaseModel):
    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
        "json_encoders": {
            ObjectId: str,
            PyObjectId: str
        }
    }

class TimestampSchema(BaseSchema):
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow) 