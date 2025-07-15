from typing import List, Optional, Dict, Any
from bson import ObjectId
from models.job_description import JobDescriptionModel
from schemas.job_description import JobDescriptionCreate, JobDescriptionUpdate, JobDescriptionResponse

class JobDescriptionService:
    def __init__(self):
        self.model = JobDescriptionModel()
    
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
    
    def create_job_description(self, job_description: JobDescriptionCreate) -> JobDescriptionResponse:
        """Create a new job description"""
        job_description_data = job_description.dict()
        result = self.model.create(job_description_data)
        # Convert ObjectIds to strings
        result = self._convert_objectids_to_strings(result)
        return JobDescriptionResponse(**result)
    
    def get_job_description(self, jd_id: str) -> Optional[JobDescriptionResponse]:
        """Get a job description by ID"""
        try:
            object_id = ObjectId(jd_id)
            result = self.model.get_by_id(object_id)
            if result:
                # Convert ObjectIds to strings
                result = self._convert_objectids_to_strings(result)
                return JobDescriptionResponse(**result)
            return None
        except Exception:
            return None
    
    def get_all_job_descriptions(self, skip: int = 0, limit: int = 100) -> List[JobDescriptionResponse]:
        """Get all job descriptions with pagination"""
        results = self.model.get_all(skip=skip, limit=limit)
        # Convert ObjectIds to strings for each result
        converted_results = []
        for result in results:
            converted_result = self._convert_objectids_to_strings(result)
            converted_results.append(JobDescriptionResponse(**converted_result))
        return converted_results
    
    def update_job_description(self, jd_id: str, job_description: JobDescriptionUpdate) -> Optional[JobDescriptionResponse]:
        """Update a job description"""
        try:
            object_id = ObjectId(jd_id)
            update_data = {k: v for k, v in job_description.dict().items() if v is not None}
            result = self.model.update(object_id, update_data)
            if result:
                # Convert ObjectIds to strings
                result = self._convert_objectids_to_strings(result)
                return JobDescriptionResponse(**result)
            return None
        except Exception:
            return None
    
    def delete_job_description(self, jd_id: str) -> bool:
        """Delete a job description"""
        try:
            object_id = ObjectId(jd_id)
            return self.model.delete(object_id)
        except Exception:
            return False
    
    def search_job_descriptions(self, title: str, skip: int = 0, limit: int = 100) -> List[JobDescriptionResponse]:
        """Search job descriptions by title"""
        results = self.model.search_by_title(title, skip=skip, limit=limit)
        # Convert ObjectIds to strings for each result
        converted_results = []
        for result in results:
            converted_result = self._convert_objectids_to_strings(result)
            converted_results.append(JobDescriptionResponse(**converted_result))
        return converted_results
    
    def get_job_description_count(self) -> int:
        """Get total count of job descriptions"""
        return self.model.count() 