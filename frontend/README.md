# Resume Evaluator Frontend

A modern Angular application for AI-powered resume evaluation and job description management.

## Features

### 🎯 MVP Features

#### 1. Job Descriptions Management
- **Job List View**: Main landing page showing all job descriptions in a table format
- **Add Job Description**: Form to create new job descriptions with title and description
- **Job Details**: View specific job description with candidate list
- **Delete Job**: Remove job descriptions from the system

#### 2. Resume Upload & Evaluation
- **Upload Interface**: Drag-and-drop or file picker for PDF resume uploads
- **Candidate Information**: Collect candidate name and email during upload
- **Automatic Evaluation**: AI-powered evaluation using Google Gemini 2.5 Flash
- **Real-time Processing**: Immediate feedback and evaluation results

#### 3. Candidate Management
- **Candidate List**: View all candidates for a specific job description
- **Match Scores**: Visual representation of candidate-job match percentages
- **Status Indicators**: Color-coded verdicts (Strong Match, Good Match, etc.)
- **Detailed View**: Comprehensive evaluation breakdown for each candidate

#### 4. Evaluation Analytics
- **Overall Score**: Percentage-based match score with visual progress bars
- **Category Breakdown**: Detailed scores for Skills, Experience, Education, and JD Alignment
- **Skills Analysis**: Matched vs. missing skills with visual tags
- **Pros & Cons**: AI-generated strengths and areas for improvement
- **Detailed Feedback**: Comprehensive written feedback from AI evaluation

### 🎨 UI/UX Features
- **Modern Design**: Clean, responsive interface using Tailwind CSS
- **Navigation**: Intuitive navigation between different views
- **Loading States**: Smooth loading indicators and transitions
- **Error Handling**: User-friendly error messages and fallbacks
- **Mobile Responsive**: Optimized for desktop and mobile devices

## Technology Stack

- **Framework**: Angular 17 (Standalone Components)
- **Styling**: Tailwind CSS
- **HTTP Client**: Angular HttpClient
- **Routing**: Angular Router
- **State Management**: Service-based state management
- **Build Tool**: Angular CLI

## Project Structure

```
src/
├── app/
│   ├── components/
│   │   ├── job-list/           # Main job descriptions table
│   │   ├── job-detail/         # Individual job view with candidates
│   │   └── candidate-detail/   # Detailed candidate evaluation
│   ├── services/
│   │   └── api.service.ts      # Backend API communication
│   ├── environments/           # Environment configuration
│   └── app.component.ts        # Main app component with navigation
├── styles.css                  # Global styles with Tailwind
└── main.ts                     # Application bootstrap
```

## Getting Started

### Prerequisites
- Node.js (v18 or higher)
- npm or yarn
- Backend server running (see backend README)

### Installation

1. **Install Dependencies**
   ```bash
   npm install
   ```

2. **Environment Setup**
   ```bash
   # Copy environment file
   cp src/environments/environment.ts.example src/environments/environment.ts
   
   # Edit environment.ts with your backend URL
   ```

3. **Development Server**
   ```bash
   npm start
   ```
   The application will be available at `http://localhost:4200`

### Environment Configuration

#### Development (`src/environments/environment.ts`)
```typescript
export const environment = {
  production: false,
  apiUrl: 'http://localhost:8000/api'
};
```

#### Production (`src/environments/environment.prod.ts`)
```typescript
export const environment = {
  production: true,
  apiUrl: 'https://your-backend-domain.com/api'
};
```

## Usage Guide

### 1. Managing Job Descriptions

#### View All Jobs
- Navigate to the main page (`/`)
- View all job descriptions in a table format
- See job titles, descriptions, and creation dates

#### Add New Job Description
1. Click "Add Job Description" button
2. Fill in the job title and description
3. Click "Add Job Description" to save
4. The new job will appear in the table

#### View Job Details
1. Click "View Details" on any job description
2. See the full job description
3. View all candidates who have applied
4. Upload new resumes for this position

### 2. Uploading Resumes

#### From Job Detail Page
1. Navigate to a specific job description
2. Click "Upload Resume" button
3. Fill in candidate name and email (optional)
4. Select a PDF resume file
5. Click "Upload & Evaluate"
6. The system will automatically evaluate the resume

#### Resume Processing
- PDF files are parsed and text is extracted
- Candidate information is stored
- AI evaluation is performed automatically
- Results are displayed immediately

### 3. Viewing Candidate Evaluations

#### Candidate List
- View all candidates for a job description
- See match scores and status indicators
- Click "View Details" for comprehensive analysis

#### Detailed Evaluation
- Overall match score with visual progress bar
- Category breakdown (Skills, Experience, Education, JD Alignment)
- Skills analysis (matched vs. missing)
- Pros and cons list
- Detailed AI feedback

## API Integration

The frontend communicates with the backend through the `ApiService` which provides:

### Job Descriptions
- `getJobDescriptions()` - Fetch all job descriptions
- `createJobDescription()` - Create new job description
- `getJobDescription(id)` - Get specific job details
- `deleteJobDescription(id)` - Remove job description

### Resumes
- `uploadResume()` - Upload and process resume
- `getResumesByJobDescription()` - Get candidates for a job
- `getResume(id)` - Get specific resume details

### Evaluations
- `evaluateResume()` - Trigger AI evaluation
- `getEvaluationsByResume()` - Get evaluation results
- `getTopEvaluations()` - Get top candidates

## Development

### Available Scripts

```bash
# Development server
npm start

# Production build
npm run build

# Development build
npm run build:dev

# Production build
npm run build:prod

# Run tests
npm test
```

### Code Style
- Use Angular standalone components
- Follow Angular style guide
- Use TypeScript strict mode
- Implement proper error handling
- Add loading states for better UX

### Adding New Features
1. Create new component in `src/app/components/`
2. Add route in `src/app/app.routes.ts`
3. Update navigation in `src/app/app.component.ts`
4. Add API methods in `src/app/services/api.service.ts`
5. Test thoroughly before deployment

## Deployment

### Production Build
```bash
npm run build:prod
```

### Static File Serving
The built application can be served by any static file server:
- Nginx
- Apache
- CDN services
- Cloud hosting platforms

### Environment Variables
Ensure production environment is properly configured:
- Set correct API URL
- Enable production optimizations
- Configure CORS if needed

## Troubleshooting

### Common Issues

1. **Build Errors**
   - Check TypeScript compilation errors
   - Verify all imports are correct
   - Ensure all dependencies are installed

2. **API Connection Issues**
   - Verify backend server is running
   - Check environment configuration
   - Ensure CORS is properly configured

3. **Styling Issues**
   - Verify Tailwind CSS is properly configured
   - Check PostCSS configuration
   - Ensure styles are imported correctly

### Debug Mode
```bash
# Enable debug logging
npm start -- --verbose
```

## Contributing

1. Follow the existing code structure
2. Add proper TypeScript types
3. Include error handling
4. Test thoroughly
5. Update documentation

## License

This project is part of the Resume Evaluator application. 