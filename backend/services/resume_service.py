from typing import List, Optional, Dict, Any
from bson import ObjectId
from models.resume import ResumeModel
from schemas.resume import ResumeCreate, ResumeUpdate, ResumeResponse, ResumeUploadRequest
from services.evaluation_service import EvaluationService

class ResumeService:
    def __init__(self):
        self.model = ResumeModel()
    
    def _convert_objectids_to_strings(self, data: dict) -> dict:
        """Convert ObjectIds to strings in the data dictionary"""
        converted = {}
        for key, value in data.items():
            if isinstance(value, ObjectId):
                converted[key] = str(value)
            elif isinstance(value, list):
                converted[key] = [str(item) if isinstance(item, ObjectId) else item for item in value]
            else:
                converted[key] = value
        return converted
    
    def create_resume(self, resume: ResumeCreate) -> ResumeResponse:
        """Create a new resume"""
        resume_data = resume.dict()
        result = self.model.create(resume_data)
        # Convert ObjectIds to strings
        result = self._convert_objectids_to_strings(result)
        return ResumeResponse(**result)
    
    def get_resume(self, resume_id: str) -> Optional[ResumeResponse]:
        """Get a resume by ID"""
        try:
            object_id = ObjectId(resume_id)
            result = self.model.get_by_id(object_id)
            if result:
                # Convert ObjectIds to strings
                result = self._convert_objectids_to_strings(result)
                return ResumeResponse(**result)
            return None
        except Exception:
            return None
    
    def get_all_resumes(self, skip: int = 0, limit: int = 100) -> List[ResumeResponse]:
        """Get all resumes with pagination"""
        results = self.model.get_all(skip=skip, limit=limit)
        # Convert ObjectIds to strings for each result
        converted_results = []
        for result in results:
            converted_result = self._convert_objectids_to_strings(result)
            converted_results.append(ResumeResponse(**converted_result))
        return converted_results
    
    def update_resume(self, resume_id: str, resume: ResumeUpdate) -> Optional[ResumeResponse]:
        """Update a resume"""
        try:
            object_id = ObjectId(resume_id)
            update_data = {k: v for k, v in resume.dict().items() if v is not None}
            result = self.model.update(object_id, update_data)
            if result:
                # Convert ObjectIds to strings
                result = self._convert_objectids_to_strings(result)
                return ResumeResponse(**result)
            return None
        except Exception:
            return None
    
    def delete_resume(self, resume_id: str) -> bool:
        """Delete a resume"""
        try:
            object_id = ObjectId(resume_id)
            return self.model.delete(object_id)
        except Exception:
            return False
    
    def search_by_candidate_name(self, name: str, skip: int = 0, limit: int = 100) -> List[ResumeResponse]:
        """Search resumes by candidate name"""
        results = self.model.search_by_candidate_name(name, skip=skip, limit=limit)
        # Convert ObjectIds to strings for each result
        converted_results = []
        for result in results:
            converted_result = self._convert_objectids_to_strings(result)
            converted_results.append(ResumeResponse(**converted_result))
        return converted_results
    
    def get_resumes_by_jd_id(self, jd_id: str, skip: int = 0, limit: int = 100) -> List[ResumeResponse]:
        """Get resumes associated with a specific job description, including evaluation if available"""
        try:
            object_id = ObjectId(jd_id)
            results = self.model.get_by_jd_id(object_id, skip=skip, limit=limit)
            evaluation_service = EvaluationService()
            converted_results = []
            for result in results:
                converted_result = self._convert_objectids_to_strings(result)
                # Fetch evaluation for this resume and jd_id
                evaluation = evaluation_service.get_evaluation_by_jd_and_resume(jd_id, str(converted_result['_id']))
                if evaluation:
                    converted_result['evaluation'] = evaluation.dict()
                converted_results.append(ResumeResponse(**converted_result))
            return converted_results
        except Exception:
            return []
    
    def add_jd_association(self, resume_id: str, jd_id: str) -> bool:
        """Add a job description association to a resume"""
        try:
            resume_object_id = ObjectId(resume_id)
            jd_object_id = ObjectId(jd_id)
            return self.model.add_jd_association(resume_object_id, jd_object_id)
        except Exception:
            return False
    
    def remove_jd_association(self, resume_id: str, jd_id: str) -> bool:
        """Remove a job description association from a resume"""
        try:
            resume_object_id = ObjectId(resume_id)
            jd_object_id = ObjectId(jd_id)
            return self.model.remove_jd_association(resume_object_id, jd_object_id)
        except Exception:
            return False
    
    def get_resume_count(self) -> int:
        """Get total count of resumes"""
        return self.model.count() 