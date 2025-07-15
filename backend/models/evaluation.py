from datetime import datetime
from typing import List, Optional
from bson import ObjectId
from pymongo import ASCENDING, DESCENDING
from utils.db import get_database

class EvaluationModel:
    def __init__(self):
        self.db = get_database()
        self.collection = self.db.evaluations
        
        # Create indexes
        self._create_indexes()
    
    def _create_indexes(self):
        """Create database indexes for better performance"""
        self.collection.create_index([("jd_id", ASCENDING)])
        self.collection.create_index([("resume_id", ASCENDING)])
        self.collection.create_index([("score", DESCENDING)])
        self.collection.create_index([("verdict", ASCENDING)])
        self.collection.create_index([("evaluated_at", DESCENDING)])
        # Compound index for jd_id and resume_id
        self.collection.create_index([("jd_id", ASCENDING), ("resume_id", ASCENDING)], unique=True)
    
    def create(self, evaluation_data: dict) -> dict:
        """Create a new evaluation"""
        now = datetime.utcnow()
        evaluation_data["evaluated_at"] = now
        evaluation_data["created_at"] = now
        evaluation_data["updated_at"] = now
        result = self.collection.insert_one(evaluation_data)
        return self.get_by_id(result.inserted_id)
    
    def get_by_id(self, evaluation_id: ObjectId) -> Optional[dict]:
        """Get evaluation by ID"""
        return self.collection.find_one({"_id": evaluation_id})
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[dict]:
        """Get all evaluations with pagination"""
        cursor = self.collection.find().sort("evaluated_at", DESCENDING).skip(skip).limit(limit)
        return list(cursor)
    
    def update(self, evaluation_id: ObjectId, update_data: dict) -> Optional[dict]:
        """Update an evaluation"""
        update_data["updated_at"] = datetime.utcnow()
        result = self.collection.update_one(
            {"_id": evaluation_id},
            {"$set": update_data}
        )
        if result.modified_count:
            return self.get_by_id(evaluation_id)
        return None
    
    def delete(self, evaluation_id: ObjectId) -> bool:
        """Delete an evaluation"""
        result = self.collection.delete_one({"_id": evaluation_id})
        return result.deleted_count > 0
    
    def get_by_jd_id(self, jd_id: ObjectId, skip: int = 0, limit: int = 100) -> List[dict]:
        """Get evaluations for a specific job description"""
        cursor = self.collection.find(
            {"jd_id": jd_id}
        ).sort("evaluated_at", DESCENDING).skip(skip).limit(limit)
        return list(cursor)
    
    def get_by_resume_id(self, resume_id: ObjectId, skip: int = 0, limit: int = 100) -> List[dict]:
        """Get evaluations for a specific resume"""
        cursor = self.collection.find(
            {"resume_id": resume_id}
        ).sort("evaluated_at", DESCENDING).skip(skip).limit(limit)
        return list(cursor)
    
    def get_by_jd_and_resume(self, jd_id: ObjectId, resume_id: ObjectId) -> Optional[dict]:
        """Get evaluation for a specific job description and resume combination"""
        return self.collection.find_one({"jd_id": jd_id, "resume_id": resume_id})
    
    def get_by_score_range(self, min_score: float, max_score: float, skip: int = 0, limit: int = 100) -> List[dict]:
        """Get evaluations within a score range"""
        cursor = self.collection.find(
            {"score": {"$gte": min_score, "$lte": max_score}}
        ).sort("evaluated_at", DESCENDING).skip(skip).limit(limit)
        return list(cursor)
    
    def get_by_verdict(self, verdict: str, skip: int = 0, limit: int = 100) -> List[dict]:
        """Get evaluations by verdict"""
        cursor = self.collection.find(
            {"verdict": verdict}
        ).sort("evaluated_at", DESCENDING).skip(skip).limit(limit)
        return list(cursor)
    
    def get_top_evaluations(self, jd_id: ObjectId, limit: int = 10) -> List[dict]:
        """Get top evaluations for a job description by score"""
        cursor = self.collection.find(
            {"jd_id": jd_id}
        ).sort("score", DESCENDING).limit(limit)
        return list(cursor)
    
    def count(self) -> int:
        """Get total count of evaluations"""
        return self.collection.count_documents({})
    
    def count_by_jd_id(self, jd_id: ObjectId) -> int:
        """Get count of evaluations for a specific job description"""
        return self.collection.count_documents({"jd_id": jd_id})
    
    def count_by_resume_id(self, resume_id: ObjectId) -> int:
        """Get count of evaluations for a specific resume"""
        return self.collection.count_documents({"resume_id": resume_id}) 