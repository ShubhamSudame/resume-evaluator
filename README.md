# Resume Evaluator - AI-Powered Resume Analysis

A comprehensive full-stack application for AI-powered resume evaluation and job description management. Built with FastAPI backend and Angular frontend, featuring Google Gemini 2.5 Flash for intelligent resume analysis.

## 🚀 MVP Features

### For HR Representatives
- **Job Description Management**: Create, view, and manage job descriptions
- **Resume Upload**: Upload candidate resumes with automatic PDF parsing
- **AI Evaluation**: Instant AI-powered evaluation using Google Gemini 2.5 Flash
- **Candidate Dashboard**: View all candidates with match scores and rankings
- **Detailed Analytics**: Comprehensive evaluation breakdowns and insights

### Key Capabilities
- **Smart Matching**: AI analyzes skills, experience, education, and job alignment
- **Visual Analytics**: Progress bars, charts, and color-coded status indicators
- **Real-time Processing**: Immediate evaluation results with detailed feedback
- **Modern UI**: Clean, responsive interface built with Angular and Tailwind CSS

## 🏗️ Architecture

```
resume-evaluator/
├── backend/                 # FastAPI Python backend
│   ├── models/             # MongoDB data models
│   ├── routes/             # API endpoints
│   ├── services/           # Business logic
│   ├── schemas/            # Pydantic schemas
│   └── utils/              # Utility functions
├── frontend/               # Angular 17 frontend
│   ├── src/app/
│   │   ├── components/     # UI components
│   │   ├── services/       # API services
│   │   └── environments/   # Environment config
│   └── dist/               # Built application
└── README.md              # This file
```

## 🛠️ Technology Stack

### Backend
- **Framework**: FastAPI (Python)
- **Database**: MongoDB with PyMongo
- **AI**: Google Gemini 2.5 Flash
- **PDF Processing**: PyMuPDF, pdfminer.six
- **Validation**: Pydantic v2

### Frontend
- **Framework**: Angular 17 (Standalone Components)
- **Styling**: Tailwind CSS
- **HTTP Client**: Angular HttpClient
- **Routing**: Angular Router

## ⚡ Quick Start

### Prerequisites
- Python 3.8+
- Node.js 18+
- MongoDB (local or cloud)
- Google Gemini API key

### 1. Clone and Setup
```bash
git clone <repository-url>
cd resume-evaluator
```

### 2. Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp env.example .env
# Edit .env with your MongoDB and Gemini API credentials

# Start backend server
python main.py
```

### 3. Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

### 4. Access Application
- Frontend: http://localhost:4200
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## 📖 Usage Guide

### 1. Create Job Description
1. Navigate to the main page
2. Click "Add Job Description"
3. Enter job title and description
4. Save to create the job posting

### 2. Upload Resumes
1. Click "View Details" on a job description
2. Click "Upload Resume"
3. Enter candidate information
4. Select PDF resume file
5. Upload and get instant AI evaluation

### 3. Review Candidates
1. View candidate list with match scores
2. Click "View Details" for comprehensive analysis
3. Review skills analysis, pros/cons, and detailed feedback

## 🔧 Configuration

### Environment Variables (Backend)
```bash
# MongoDB
MONGODB_URL=mongodb://localhost:27017/resume_evaluator

# Google Gemini
GEMINI_API_KEY=your_gemini_api_key

# Application
MODE=development  # or production
```

### Environment Variables (Frontend)
```typescript
// src/environments/environment.ts
export const environment = {
  production: false,
  apiUrl: 'http://localhost:8000/api'
};
```

## 🚀 Deployment

### Backend Deployment
```bash
cd backend
pip install -r requirements.txt
python main.py
```

### Frontend Deployment
```bash
cd frontend
npm run build:prod
# Copy dist/resume-evaluator/ to your web server
```

### Production Considerations
- Set up MongoDB with authentication
- Configure CORS for production domains
- Use environment variables for secrets
- Set up proper logging and monitoring
- Configure SSL/TLS certificates

## 📊 API Endpoints

### Job Descriptions
- `GET /api/job-descriptions` - List all jobs
- `POST /api/job-descriptions` - Create new job
- `GET /api/job-descriptions/{id}` - Get specific job
- `DELETE /api/job-descriptions/{id}` - Delete job

### Resumes
- `POST /api/resumes/upload` - Upload resume
- `GET /api/resumes/by-jd/{jd_id}` - Get candidates for job
- `GET /api/resumes/{id}` - Get specific resume

### Evaluations
- `POST /api/evaluations/evaluate` - Evaluate resume
- `GET /api/evaluations/by-resume/{resume_id}` - Get evaluation results

## 🔍 Features in Detail

### AI Evaluation Process
1. **PDF Parsing**: Extract text and metadata from resume
2. **Content Analysis**: Analyze skills, experience, education
3. **Job Matching**: Compare resume against job requirements
4. **Scoring**: Generate comprehensive match scores
5. **Feedback**: Provide detailed insights and recommendations

### Evaluation Metrics
- **Overall Score**: Percentage match (0-100%)
- **Category Breakdown**: Skills, Experience, Education, JD Alignment
- **Skills Analysis**: Matched vs. missing skills
- **Pros & Cons**: Strengths and areas for improvement
- **Detailed Feedback**: Comprehensive written analysis

### UI Components
- **Job List**: Table view with add/delete functionality
- **Job Detail**: Full job description with candidate list
- **Candidate Detail**: Comprehensive evaluation breakdown
- **Upload Form**: Drag-and-drop resume upload
- **Navigation**: Intuitive routing between views

## 🐛 Troubleshooting

### Common Issues

1. **Backend Won't Start**
   - Check MongoDB connection
   - Verify environment variables
   - Check port availability (8000)

2. **Frontend Build Errors**
   - Clear node_modules: `rm -rf node_modules && npm install`
   - Check TypeScript errors
   - Verify Angular CLI version

3. **API Connection Issues**
   - Check CORS configuration
   - Verify API URL in environment
   - Check network connectivity

4. **AI Evaluation Fails**
   - Verify Gemini API key
   - Check API quota limits
   - Review error logs

### Debug Mode
```bash
# Backend debug
python main.py --debug

# Frontend debug
npm start -- --verbose
```

## 📈 Future Enhancements

### Planned Features
- **Advanced Analytics**: Dashboard with charts and metrics
- **Bulk Upload**: Multiple resume upload
- **Email Notifications**: Automated candidate updates
- **Interview Scheduling**: Integrated calendar
- **Custom Scoring**: Configurable evaluation criteria
- **Export Reports**: PDF/Excel evaluation reports

### Technical Improvements
- **Caching**: Redis for performance optimization
- **Queue System**: Background job processing
- **File Storage**: Cloud storage for resumes
- **Authentication**: User management system
- **API Rate Limiting**: Request throttling

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

### Development Guidelines
- Follow PEP 8 for Python code
- Use Angular style guide for frontend
- Add proper error handling
- Include documentation
- Test thoroughly

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For support and questions:
- Check the troubleshooting section
- Review API documentation at `/docs`
- Open an issue on GitHub
- Contact the development team

---

**Built with ❤️ using FastAPI, Angular, and Google Gemini AI** 