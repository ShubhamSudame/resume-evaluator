from datetime import datetime
from typing import List, Optional
from bson import ObjectId
from pymongo import ASCENDING, DESCENDING
from utils.db import get_database

class JobDescriptionModel:
    def __init__(self):
        self.db = get_database()
        self.collection = self.db.job_descriptions
        
        # Create indexes
        self._create_indexes()
    
    def _create_indexes(self):
        """Create database indexes for better performance"""
        self.collection.create_index([("title", ASCENDING)])
        self.collection.create_index([("created_at", DESCENDING)])
    
    def create(self, job_description_data: dict) -> dict:
        """Create a new job description"""
        now = datetime.utcnow()
        job_description_data["created_at"] = now
        job_description_data["updated_at"] = now
        result = self.collection.insert_one(job_description_data)
        return self.get_by_id(result.inserted_id)
    
    def get_by_id(self, jd_id: ObjectId) -> Optional[dict]:
        """Get job description by ID"""
        return self.collection.find_one({"_id": jd_id})
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[dict]:
        """Get all job descriptions with pagination"""
        cursor = self.collection.find().sort("created_at", DESCENDING).skip(skip).limit(limit)
        return list(cursor)
    
    def update(self, jd_id: ObjectId, update_data: dict) -> Optional[dict]:
        """Update a job description"""
        update_data["updated_at"] = datetime.utcnow()
        result = self.collection.update_one(
            {"_id": jd_id},
            {"$set": update_data}
        )
        if result.modified_count:
            return self.get_by_id(jd_id)
        return None
    
    def delete(self, jd_id: ObjectId) -> bool:
        """Delete a job description"""
        result = self.collection.delete_one({"_id": jd_id})
        return result.deleted_count > 0
    
    def search_by_title(self, title: str, skip: int = 0, limit: int = 100) -> List[dict]:
        """Search job descriptions by title"""
        cursor = self.collection.find(
            {"title": {"$regex": title, "$options": "i"}}
        ).sort("created_at", DESCENDING).skip(skip).limit(limit)
        return list(cursor)
    
    def count(self) -> int:
        """Get total count of job descriptions"""
        return self.collection.count_documents({}) 