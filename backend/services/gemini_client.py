import os
import json
import logging
from typing import Dict, Any, Optional
from google import genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

class GeminiClient:
    """Google Gemini AI client for resume evaluation"""
    
    def __init__(self):
        """Initialize the Gemini client"""
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY environment variable is required")
        
        # Initialize the Gemini client
        self.client = genai.Client(api_key=self.api_key)
    
    def evaluate_resume_with_jd(self, resume_json: Dict[str, Any], jd_text: str) -> Dict[str, Any]:
        """
        Evaluate a resume against a job description using Gemini AI
        
        Args:
            resume_json: Structured resume dictionary from MongoDB
            jd_text: Job description text
            
        Returns:
            Dictionary containing evaluation results
        """
        try:
            # Prepare the evaluation prompt
            prompt = self._create_evaluation_prompt(resume_json, jd_text)
            
            # Generate content using Gemini
            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            
            # Parse the response
            evaluation_result = self._parse_evaluation_response(response)
            
            logger.info(f"Successfully evaluated resume for candidate: {resume_json.get('candidate_name', 'Unknown')}")
            return evaluation_result
            
        except Exception as e:
            logger.error(f"Error evaluating resume: {str(e)}")
            raise Exception(f"Failed to evaluate resume: {str(e)}")
    
    def _create_evaluation_prompt(self, resume_json: Dict[str, Any], jd_text: str) -> str:
        """
        Create a comprehensive evaluation prompt for Gemini
        
        Args:
            resume_json: Resume data
            jd_text: Job description text
            
        Returns:
            Formatted prompt string
        """
        # Extract key information from resume
        candidate_name = resume_json.get('candidate_name', 'Unknown')
        skills = resume_json.get('skills', [])
        education = resume_json.get('education', [])
        experience = resume_json.get('experience', [])
        # Use markdown_text if available, else raw_text
        resume_text = resume_json.get('markdown_text') or resume_json.get('raw_text', '')
        
        # Format education and experience for better context
        education_text = self._format_education(education)
        experience_text = self._format_experience(experience)
        
        prompt = f"""
You are an expert HR recruiter and resume evaluator. Your task is to evaluate a candidate's resume against a specific job description and provide a comprehensive assessment.

CANDIDATE INFORMATION:
Name: {candidate_name}
Skills: {', '.join(skills) if skills else 'Not specified'}

EDUCATION:
{education_text}

EXPERIENCE:
{experience_text}

RESUME RAW TEXT:
{resume_text[:2000] if resume_text else 'No resume text available'}

JOB DESCRIPTION:
{jd_text}

EVALUATION TASK:
Please evaluate this candidate's resume against the job description and provide a detailed assessment in the following JSON format:

{{
    "score": <0-100>,
    "verdict": "<Shortlist|Needs Review|Reject>",
    "category_breakdown": {{
        "skills": <0-100>,
        "experience": <0-100>,
        "education": <0-100>,
        "jd_alignment": <0-100>
    }},
    "matched_skills": ["skill1", "skill2", ...],
    "missing_skills": ["skill1", "skill2", ...],
    "pros": ["pro1", "pro2", ...],
    "cons": ["con1", "con2", ...],
    "feedback": "<detailed feedback summary>"
}}

EVALUATION CRITERIA:
- Score (0-100): Overall match percentage
- Verdict: 
  * "Shortlist" (80-100): Strong match, recommend for interview
  * "Needs Review" (50-79): Moderate match, consider with reservations
  * "Reject" (0-49): Poor match, not recommended
- Category Breakdown: Individual scores for skills, experience, education, and JD alignment
- Matched Skills: Skills from resume that align with job requirements
- Missing Skills: Important skills from JD that are missing from resume
- Pros: Strengths and positive aspects
- Cons: Weaknesses and areas of concern
- Feedback: Detailed summary of evaluation

IMPORTANT: Return ONLY valid JSON. Do not include any additional text or explanations outside the JSON structure.
"""
        return prompt
    
    def _format_education(self, education: list) -> str:
        """Format education information for the prompt"""
        if not education:
            return "No education information provided"
        
        formatted = []
        for edu in education:
            degree = edu.get('degree', 'Unknown')
            institution = edu.get('institution', 'Unknown')
            year = edu.get('year', 'Unknown')
            gpa = edu.get('gpa', '')
            
            edu_text = f"- {degree} from {institution}"
            if year != 'Unknown':
                edu_text += f" ({year})"
            if gpa:
                edu_text += f" - GPA: {gpa}"
            
            formatted.append(edu_text)
        
        return '\n'.join(formatted)
    
    def _format_experience(self, experience: list) -> str:
        """Format experience information for the prompt"""
        if not experience:
            return "No experience information provided"
        
        formatted = []
        for exp in experience:
            title = exp.get('title', 'Unknown')
            company = exp.get('company', 'Unknown')
            start_date = exp.get('start_date', 'Unknown')
            end_date = exp.get('end_date', 'Present')
            description = exp.get('description', '')
            
            exp_text = f"- {title} at {company} ({start_date} - {end_date})"
            if description:
                exp_text += f"\n  {description}"
            
            formatted.append(exp_text)
        
        return '\n'.join(formatted)
    
    def _parse_evaluation_response(self, response) -> Dict[str, Any]:
        """
        Parse the Gemini response and extract evaluation results
        
        Args:
            response: Gemini API response
            
        Returns:
            Parsed evaluation dictionary
        """
        try:
            # Extract text content from response
            content = response.text
            
            # Try to extract JSON from the response
            # Sometimes Gemini includes markdown formatting
            if '```json' in content:
                # Extract JSON from markdown code block
                start = content.find('```json') + 7
                end = content.find('```', start)
                json_str = content[start:end].strip()
            elif '```' in content:
                # Extract JSON from code block
                start = content.find('```') + 3
                end = content.find('```', start)
                json_str = content[start:end].strip()
            else:
                # Assume the entire response is JSON
                json_str = content.strip()
            
            # Parse JSON
            evaluation = json.loads(json_str)
            
            # Validate required fields
            required_fields = [
                'score', 'verdict', 'category_breakdown', 
                'matched_skills', 'missing_skills', 'pros', 'cons', 'feedback'
            ]
            
            for field in required_fields:
                if field not in evaluation:
                    raise ValueError(f"Missing required field: {field}")
            
            # Validate score range
            if not (0 <= evaluation['score'] <= 100):
                evaluation['score'] = max(0, min(100, evaluation['score']))
            
            # Validate verdict
            valid_verdicts = ['Shortlist', 'Needs Review', 'Reject']
            if evaluation['verdict'] not in valid_verdicts:
                evaluation['verdict'] = 'Needs Review'
            
            # Validate category breakdown
            # Map Gemini output to required schema fields
            cb = evaluation['category_breakdown']
            mapped_cb = {
                'technical_skills': max(0, min(100, cb.get('skills', 0))),
                'experience': max(0, min(100, cb.get('experience', 0))),
                'education': max(0, min(100, cb.get('education', 0))),
                'communication': max(0, min(100, cb.get('communication', 0)))
            }
            evaluation['category_breakdown'] = mapped_cb
            
            return evaluation
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {e}")
            logger.error(f"Raw response: {response.text}")
            raise Exception("Failed to parse evaluation response")
        except Exception as e:
            logger.error(f"Error parsing evaluation response: {e}")
            raise Exception(f"Failed to parse evaluation response: {str(e)}")
    
    def test_connection(self) -> bool:
        """
        Test the Gemini API connection
        
        Returns:
            True if connection is successful, False otherwise
        """
        try:
            # Simple test prompt
            test_prompt = "Hello, please respond with 'OK' if you can read this message."
            
            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=test_prompt
            )
            
            return "OK" in response.text or response.text.strip() == "OK"
            
        except Exception as e:
            logger.error(f"Gemini connection test failed: {e}")
            return False 