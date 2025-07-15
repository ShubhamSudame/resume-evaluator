from typing import List, Optional, Dict, Any
from bson import ObjectId
from models.evaluation import EvaluationModel
from schemas.evaluation import EvaluationCreate, EvaluationUpdate, EvaluationResponse
import logging
from models.resume import ResumeModel
from services.job_description_service import JobDescriptionService
from services.gemini_client import GeminiClient

logger = logging.getLogger(__name__)

class EvaluationService:
    def __init__(self):
        self.model = EvaluationModel()
        self.resume_model = ResumeModel()
        self.jd_service = JobDescriptionService()
        self.gemini_client = GeminiClient()
    
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
    
    def create_evaluation(self, evaluation: EvaluationCreate) -> EvaluationResponse:
        """Create a new evaluation"""
        evaluation_data = evaluation.dict()
        result = self.model.create(evaluation_data)
        # Convert ObjectIds to strings
        result = self._convert_objectids_to_strings(result)
        return EvaluationResponse(**result)
    
    def get_evaluation(self, evaluation_id: str) -> Optional[EvaluationResponse]:
        """Get an evaluation by ID"""
        try:
            object_id = ObjectId(evaluation_id)
            result = self.model.get_by_id(object_id)
            if result:
                # Convert ObjectIds to strings
                result = self._convert_objectids_to_strings(result)
                return EvaluationResponse(**result)
            return None
        except Exception:
            return None
    
    def get_all_evaluations(self, skip: int = 0, limit: int = 100) -> List[EvaluationResponse]:
        """Get all evaluations with pagination"""
        results = self.model.get_all(skip=skip, limit=limit)
        # Convert ObjectIds to strings for each result
        converted_results = []
        for result in results:
            converted_result = self._convert_objectids_to_strings(result)
            converted_results.append(EvaluationResponse(**converted_result))
        return converted_results
    
    def update_evaluation(self, evaluation_id: str, evaluation: EvaluationUpdate) -> Optional[EvaluationResponse]:
        """Update an evaluation"""
        try:
            object_id = ObjectId(evaluation_id)
            update_data = {k: v for k, v in evaluation.dict().items() if v is not None}
            result = self.model.update(object_id, update_data)
            if result:
                # Convert ObjectIds to strings
                result = self._convert_objectids_to_strings(result)
                return EvaluationResponse(**result)
            return None
        except Exception:
            return None
    
    def delete_evaluation(self, evaluation_id: str) -> bool:
        """Delete an evaluation"""
        try:
            object_id = ObjectId(evaluation_id)
            return self.model.delete(object_id)
        except Exception:
            return False
    
    def get_evaluations_by_jd_id(self, jd_id: str, skip: int = 0, limit: int = 100) -> List[EvaluationResponse]:
        """Get evaluations for a specific job description"""
        try:
            object_id = ObjectId(jd_id)
            results = self.model.get_by_jd_id(object_id, skip=skip, limit=limit)
            # Convert ObjectIds to strings for each result
            converted_results = []
            for result in results:
                converted_result = self._convert_objectids_to_strings(result)
                converted_results.append(EvaluationResponse(**converted_result))
            return converted_results
        except Exception:
            return []
    
    def get_evaluations_by_resume_id(self, resume_id: str, skip: int = 0, limit: int = 100) -> List[EvaluationResponse]:
        """Get evaluations for a specific resume"""
        try:
            object_id = ObjectId(resume_id)
            results = self.model.get_by_resume_id(object_id, skip=skip, limit=limit)
            # Convert ObjectIds to strings for each result
            converted_results = []
            for result in results:
                converted_result = self._convert_objectids_to_strings(result)
                converted_results.append(EvaluationResponse(**converted_result))
            return converted_results
        except Exception:
            return []
    
    def get_evaluation_by_jd_and_resume(self, jd_id: str, resume_id: str) -> Optional[EvaluationResponse]:
        """Get evaluation for a specific job description and resume combination"""
        try:
            jd_object_id = ObjectId(jd_id)
            resume_object_id = ObjectId(resume_id)
            result = self.model.get_by_jd_and_resume(jd_object_id, resume_object_id)
            if result:
                # Convert ObjectIds to strings
                result = self._convert_objectids_to_strings(result)
                return EvaluationResponse(**result)
            return None
        except Exception:
            return None
    
    def get_top_evaluations(self, jd_id: str, limit: int = 10) -> List[EvaluationResponse]:
        """Get top evaluations for a job description by score"""
        try:
            object_id = ObjectId(jd_id)
            results = self.model.get_top_evaluations(object_id, limit=limit)
            # Convert ObjectIds to strings for each result
            converted_results = []
            for result in results:
                converted_result = self._convert_objectids_to_strings(result)
                converted_results.append(EvaluationResponse(**converted_result))
            return converted_results
        except Exception:
            return []
    
    def get_evaluation_count(self) -> int:
        """Get total count of evaluations"""
        return self.model.count()
    
    def get_evaluation_count_by_jd_id(self, jd_id: str) -> int:
        """Get count of evaluations for a specific job description"""
        try:
            object_id = ObjectId(jd_id)
            return self.model.count_by_jd_id(object_id)
        except Exception:
            return 0
    
    def get_evaluation_count_by_resume_id(self, resume_id: str) -> int:
        """Get count of evaluations for a specific resume"""
        try:
            object_id = ObjectId(resume_id)
            return self.model.count_by_resume_id(object_id)
        except Exception:
            return 0 

    def evaluate_resume_with_ai(self, resume_id: str, jd_id: str) -> EvaluationResponse:
        """
        Evaluate a resume against a job description using Gemini AI.
        Uses markdown_text if available, otherwise falls back to raw_text.
        """
        # Fetch resume and job description
        resume = self.resume_model.get_by_id(ObjectId(resume_id))
        if not resume:
            raise Exception("Resume not found")
        jd = self.jd_service.get_job_description(jd_id)
        if not jd:
            raise Exception("Job description not found")

        # Use markdown_text if available, else raw_text
        resume_for_ai = dict(resume)
        resume_for_ai['raw_text'] = resume.get('markdown_text') or resume.get('raw_text') or ''
        jd_text = getattr(jd, 'jd_text', None) or jd.jd_text if hasattr(jd, 'jd_text') else jd.get('jd_text', '')

        # Call Gemini
        evaluation_result = self.gemini_client.evaluate_resume_with_jd(resume_for_ai, jd_text)

        # Prepare evaluation data for storage
        evaluation_data = EvaluationCreate(
            resume_id=str(resume_id),
            jd_id=str(jd_id),
            score=evaluation_result.get('score', 0),
            verdict=evaluation_result.get('verdict', ''),
            category_breakdown=evaluation_result.get('category_breakdown', {}),
            matched_skills=evaluation_result.get('matched_skills', []),
            missing_skills=evaluation_result.get('missing_skills', []),
            pros=evaluation_result.get('pros', []),
            cons=evaluation_result.get('cons', []),
            feedback=evaluation_result.get('feedback', ''),
        )
        return self.create_evaluation(evaluation_data) 