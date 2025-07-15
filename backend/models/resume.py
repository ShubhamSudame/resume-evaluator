from datetime import datetime
from typing import List, Optional
from bson import ObjectId
from pymongo import ASCENDING, DESCENDING
from utils.db import get_database

class ResumeModel:
    def __init__(self):
        self.db = get_database()
        self.collection = self.db.resumes
        
        # Create indexes
        self._create_indexes()
    
    def _create_indexes(self):
        """Create database indexes for better performance"""
        self.collection.create_index([("candidate_name", ASCENDING)])
        self.collection.create_index([("email", ASCENDING)])
        self.collection.create_index([("skills", ASCENDING)])
        self.collection.create_index([("created_at", DESCENDING)])
        self.collection.create_index([("jd_ids", ASCENDING)])
    
    def create(self, resume_data: dict) -> dict:
        """Create a new resume"""
        now = datetime.utcnow()
        resume_data["created_at"] = now
        resume_data["updated_at"] = now
        result = self.collection.insert_one(resume_data)
        return self.get_by_id(result.inserted_id)
    
    def get_by_id(self, resume_id: ObjectId) -> Optional[dict]:
        """Get resume by ID"""
        return self.collection.find_one({"_id": resume_id})
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[dict]:
        """Get all resumes with pagination"""
        cursor = self.collection.find().sort("created_at", DESCENDING).skip(skip).limit(limit)
        return list(cursor)
    
    def update(self, resume_id: ObjectId, update_data: dict) -> Optional[dict]:
        """Update a resume"""
        update_data["updated_at"] = datetime.utcnow()
        result = self.collection.update_one(
            {"_id": resume_id},
            {"$set": update_data}
        )
        if result.modified_count:
            return self.get_by_id(resume_id)
        return None
    
    def delete(self, resume_id: ObjectId) -> bool:
        """Delete a resume"""
        result = self.collection.delete_one({"_id": resume_id})
        return result.deleted_count > 0
    
    def search_by_candidate_name(self, name: str, skip: int = 0, limit: int = 100) -> List[dict]:
        """Search resumes by candidate name"""
        cursor = self.collection.find(
            {"candidate_name": {"$regex": name, "$options": "i"}}
        ).sort("created_at", DESCENDING).skip(skip).limit(limit)
        return list(cursor)
    
    def search_by_email(self, email: str) -> Optional[dict]:
        """Search resume by email"""
        return self.collection.find_one({"email": email})
    
    def search_by_skills(self, skills: List[str], skip: int = 0, limit: int = 100) -> List[dict]:
        """Search resumes by skills"""
        cursor = self.collection.find(
            {"skills": {"$in": skills}}
        ).sort("created_at", DESCENDING).skip(skip).limit(limit)
        return list(cursor)
    
    def get_by_jd_id(self, jd_id: ObjectId, skip: int = 0, limit: int = 100) -> List[dict]:
        """Get resumes associated with a specific job description"""
        cursor = self.collection.find(
            {"jd_ids": jd_id}
        ).sort("created_at", DESCENDING).skip(skip).limit(limit)
        return list(cursor)
    
    def add_jd_association(self, resume_id: ObjectId, jd_id: ObjectId) -> bool:
        """Add a job description association to a resume"""
        result = self.collection.update_one(
            {"_id": resume_id},
            {"$addToSet": {"jd_ids": jd_id}}
        )
        return result.modified_count > 0
    
    def remove_jd_association(self, resume_id: ObjectId, jd_id: ObjectId) -> bool:
        """Remove a job description association from a resume"""
        result = self.collection.update_one(
            {"_id": resume_id},
            {"$pull": {"jd_ids": jd_id}}
        )
        return result.modified_count > 0
    
    def count(self) -> int:
        """Get total count of resumes"""
        return self.collection.count_documents({}) 