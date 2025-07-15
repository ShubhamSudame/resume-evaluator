# Resume Evaluator Backend

A FastAPI-based backend for resume evaluation and job description management with MongoDB integration, PDF parsing capabilities, and AI-powered evaluation using Google Gemini 2.5 Flash.

## Features

- **Job Description Management**: Create, read, update, delete, and search job descriptions
- **Resume Processing**: Upload PDF resumes with automatic text extraction
- **PDF Parsing**: Extract text from PDF files using PyMuPDF and pdfminer.six
- **AI-Powered Evaluation**: Evaluate resumes against job descriptions using Google Gemini 2.5 Flash
- **MongoDB Integration**: Store and retrieve data using MongoDB with PyMongo
- **RESTful API**: Complete CRUD operations with proper error handling
- **CORS Support**: Configured for frontend integration
- **Pydantic Validation**: Type-safe data validation and serialization

## Prerequisites

- Python 3.8+
- MongoDB (local or cloud instance)
- Google Gemini API key
- Virtual environment (recommended)

## Installation

1. **Clone the repository and navigate to the backend directory:**
   ```bash
   cd resume-evaluator/backend
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   ```bash
   cp env.example .env
   # Edit .env with your MongoDB connection details and Gemini API key
   ```

## Configuration

Create a `.env` file with the following variables:

```env
# MongoDB Configuration
MONGODB_URL=mongodb://localhost:27017
MONGODB_DB=resume_evaluator

# Application Configuration
APP_NAME=Resume Evaluator API
APP_VERSION=1.0.0
DEBUG=True

# CORS Configuration
ALLOWED_ORIGINS=http://localhost:4200,http://localhost:3000

# File Upload Configuration
MAX_FILE_SIZE=10485760  # 10MB
UPLOAD_DIR=uploads

# Google Gemini AI Configuration
GEMINI_API_KEY=your-gemini-api-key-here
```

### Getting a Gemini API Key

1. Visit [Google AI Studio](https://aistudio.google.com/)
2. Sign in with your Google account
3. Create a new API key
4. Add the API key to your `.env` file

## Running the Application

### Development Mode
```bash
# Activate virtual environment
source venv/bin/activate

# Run with auto-reload
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Production Mode
```bash
# Run directly
python main.py
```

The API will be available at:
- **API Documentation**: http://localhost:8000/docs
- **ReDoc Documentation**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/api/health

## API Endpoints

### Job Descriptions

#### Create Job Description
```http
POST /api/job-descriptions
Content-Type: application/json

{
  "title": "Software Engineer",
  "jd_text": "We are looking for a skilled software engineer..."
}
```

#### Get All Job Descriptions
```http
GET /api/job-descriptions?skip=0&limit=100
```

#### Get Job Description by ID
```http
GET /api/job-descriptions/{jd_id}
```

#### Update Job Description
```http
PUT /api/job-descriptions/{jd_id}
Content-Type: application/json

{
  "title": "Updated Title",
  "jd_text": "Updated job description..."
}
```

#### Delete Job Description
```http
DELETE /api/job-descriptions/{jd_id}
```

#### Search Job Descriptions
```http
GET /api/job-descriptions/search/?title=engineer&skip=0&limit=100
```

### Resumes

#### Upload PDF Resume
```http
POST /api/resumes/upload
Content-Type: multipart/form-data

file: [PDF file]
jd_id: "507f1f77bcf86cd799439011"
candidate_name: "John Doe" (optional)
email: "john.doe@example.com" (optional)
```

#### Create Resume (Manual)
```http
POST /api/resumes
Content-Type: application/json

{
  "candidate_name": "John Doe",
  "email": "john.doe@example.com",
  "skills": ["Python", "FastAPI", "MongoDB"],
  "education": [...],
  "experience": [...],
  "jd_ids": ["507f1f77bcf86cd799439011"]
}
```

#### Get All Resumes
```http
GET /api/resumes?skip=0&limit=100
```

#### Get Resume by ID
```http
GET /api/resumes/{resume_id}
```

#### Update Resume
```http
PUT /api/resumes/{resume_id}
Content-Type: application/json

{
  "candidate_name": "Updated Name",
  "skills": ["Updated", "Skills"]
}
```

#### Delete Resume
```http
DELETE /api/resumes/{resume_id}
```

#### Search Resumes
```http
# By name
GET /api/resumes/search/name?name=John&skip=0&limit=100

# By email
GET /api/resumes/search/email/{email}

# By skills
GET /api/resumes/search/skills?skills=Python,FastAPI&skip=0&limit=100

# By job description
GET /api/resumes/by-jd/{jd_id}?skip=0&limit=100
```

#### Associate/Disassociate Job Description
```http
# Add association
POST /api/resumes/{resume_id}/associate-jd/{jd_id}

# Remove association
DELETE /api/resumes/{resume_id}/associate-jd/{jd_id}
```

### AI-Powered Evaluations

#### Evaluate Resume with AI
```http
POST /api/evaluations/evaluate
Content-Type: application/json

{
  "resume_id": "507f1f77bcf86cd799439011",
  "jd_id": "507f1f77bcf86cd799439012"
}
```

**Response:**
```json
{
  "id": "507f1f77bcf86cd799439013",
  "resume_id": "507f1f77bcf86cd799439011",
  "jd_id": "507f1f77bcf86cd799439012",
  "score": 85.5,
  "verdict": "Shortlist",
  "category_breakdown": {
    "skills": 90,
    "experience": 85,
    "education": 80,
    "jd_alignment": 87
  },
  "matched_skills": ["Python", "FastAPI", "MongoDB"],
  "missing_skills": ["Docker", "Kubernetes"],
  "pros": [
    "Strong technical skills",
    "Relevant experience",
    "Good education background"
  ],
  "cons": [
    "Missing some DevOps skills",
    "Limited cloud experience"
  ],
  "feedback": "Strong candidate with excellent technical skills...",
  "created_at": "2024-01-15T10:30:00Z"
}
```

#### Test Gemini Connection
```http
GET /api/evaluations/test-gemini
```

#### Get All Evaluations
```http
GET /api/evaluations?skip=0&limit=100
```

#### Get Evaluation by ID
```http
GET /api/evaluations/{evaluation_id}
```

#### Get Evaluations by Job Description
```http
GET /api/evaluations/by-jd/{jd_id}?skip=0&limit=100
```

#### Get Evaluations by Resume
```http
GET /api/evaluations/by-resume/{resume_id}?skip=0&limit=100
```

#### Get Top Evaluations
```http
GET /api/evaluations/top/{jd_id}?limit=10
```

#### Search Evaluations
```http
# By score range
GET /api/evaluations/search/score-range?min_score=80&max_score=100&skip=0&limit=100

# By verdict
GET /api/evaluations/search/verdict/Shortlist?skip=0&limit=100
```

## AI Evaluation Features

### Gemini 2.5 Flash Integration
The backend uses Google's Gemini 2.5 Flash model for intelligent resume evaluation:

- **Comprehensive Analysis**: Evaluates skills, experience, education, and JD alignment
- **Structured Output**: Returns detailed JSON with scores, verdicts, and feedback
- **Smart Categorization**: Provides category breakdown and skill matching
- **Professional Feedback**: Generates pros, cons, and detailed feedback

### Evaluation Criteria
- **Score (0-100)**: Overall match percentage
- **Verdict**: 
  - "Shortlist" (80-100): Strong match, recommend for interview
  - "Needs Review" (50-79): Moderate match, consider with reservations
  - "Reject" (0-49): Poor match, not recommended
- **Category Breakdown**: Individual scores for skills, experience, education, and JD alignment
- **Skill Analysis**: Matched and missing skills identification
- **Detailed Feedback**: Comprehensive evaluation summary

### Evaluation Process
1. **Data Retrieval**: Fetches resume and job description from database
2. **AI Processing**: Sends structured data to Gemini 2.5 Flash
3. **Response Parsing**: Extracts and validates evaluation results
4. **Database Storage**: Saves evaluation with all details
5. **Result Return**: Returns comprehensive evaluation to client

## PDF Processing Features

### Text Extraction
The backend uses two PDF parsing libraries for robust text extraction:

1. **PyMuPDF (fitz)**: Primary parser for faster and more reliable extraction
2. **pdfminer.six**: Fallback parser for complex PDFs

### Information Extraction
The system automatically extracts:
- **Raw text content** from PDF files
- **Candidate name** (basic pattern matching)
- **Email addresses** (regex pattern matching)

### File Validation
- File type validation (PDF only)
- PDF integrity validation
- File size limits (configurable)

## Data Models

### Job Description
```python
{
  "_id": ObjectId,
  "title": str,
  "jd_text": str,
  "created_at": datetime,
  "updated_at": datetime
}
```

### Resume
```python
{
  "_id": ObjectId,
  "candidate_name": str,
  "email": str,
  "skills": List[str],
  "education": List[Education],
  "experience": List[Experience],
  "raw_text": str,  # Extracted from PDF
  "jd_ids": List[ObjectId],
  "created_at": datetime,
  "updated_at": datetime
}
```

### Evaluation
```python
{
  "_id": ObjectId,
  "resume_id": ObjectId,
  "jd_id": ObjectId,
  "score": float,  # 0-100
  "verdict": str,  # "Shortlist", "Needs Review", "Reject"
  "category_breakdown": {
    "skills": float,
    "experience": float,
    "education": float,
    "jd_alignment": float
  },
  "matched_skills": List[str],
  "missing_skills": List[str],
  "pros": List[str],
  "cons": List[str],
  "feedback": str,
  "created_at": datetime,
  "updated_at": datetime
}
```

## Error Handling

The API provides comprehensive error handling:

- **400 Bad Request**: Invalid input data or file format
- **404 Not Found**: Resource not found
- **422 Unprocessable Entity**: Validation errors
- **500 Internal Server Error**: Server-side errors

## Testing

### Backend Tests
Run the test script to verify backend functionality:

```bash
python test_backend.py
```

### Gemini AI Tests
Run the Gemini integration tests:

```bash
python test_gemini.py
```

## Development

### Project Structure
```
backend/
├── main.py                 # FastAPI application entry point
├── requirements.txt        # Python dependencies
├── env.example            # Environment variables template
├── test_backend.py        # Backend test script
├── test_gemini.py         # Gemini AI test script
├── schemas/               # Pydantic models
│   ├── base.py           # Base schemas and utilities
│   ├── job_description.py
│   ├── resume.py
│   └── evaluation.py
├── models/                # MongoDB models
│   ├── job_description.py
│   ├── resume.py
│   └── evaluation.py
├── services/              # Business logic
│   ├── job_description_service.py
│   ├── resume_service.py
│   ├── evaluation_service.py
│   └── gemini_client.py   # AI evaluation client
├── routes/                # API endpoints
│   ├── job_descriptions.py
│   ├── resumes.py
│   └── evaluations.py
└── utils/                 # Utility functions
    └── pdf_parser.py      # PDF text extraction
```

### Adding New Features

1. **Create/Update schemas** in the `schemas/` directory
2. **Add business logic** in the `services/` directory
3. **Define API endpoints** in the `routes/` directory
4. **Update models** if needed in the `models/` directory
5. **Add tests** to verify functionality

## Troubleshooting

### Common Issues

1. **MongoDB Connection Error**
   - Verify MongoDB is running
   - Check connection string in `.env`
   - Ensure network connectivity

2. **PDF Parsing Errors**
   - Verify PDF file is not corrupted
   - Check file size limits
   - Ensure PDF is not password-protected

3. **Gemini API Errors**
   - Verify GEMINI_API_KEY is set correctly
   - Check API key validity in Google AI Studio
   - Ensure internet connectivity
   - Check API usage limits

4. **Import Errors**
   - Activate virtual environment
   - Install missing dependencies
   - Check Python path

### Logs

Enable debug logging by setting `DEBUG=True` in your `.env` file.

## Contributing

1. Follow the existing code structure
2. Add proper error handling
3. Include docstrings for functions
4. Test your changes
5. Update documentation

## License

This project is licensed under the MIT License. 