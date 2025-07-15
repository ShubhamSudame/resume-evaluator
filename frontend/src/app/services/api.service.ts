import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';

export interface JobDescription {
  _id: string;
  title: string;
  jd_text: string;
  created_at: string;
  updated_at: string;
}

export interface Resume {
  _id: string;
  candidate_name: string;
  email: string;
  skills: string[];
  education: any[];
  experience: any[];
  raw_text?: string;
  jd_ids: string[];
  created_at: string;
  updated_at: string;
  evaluation?: any; // Add this line to support evaluation info
}

export interface Evaluation {
  _id: string;
  resume_id: string;
  jd_id: string;
  score: number;
  verdict: string;
  category_breakdown: {
    skills: number;
    experience: number;
    education: number;
    jd_alignment: number;
  };
  matched_skills: string[];
  missing_skills: string[];
  pros: string[];
  cons: string[];
  feedback: string;
  created_at: string;
  updated_at: string;
}

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private apiUrl = environment.apiUrl;

  constructor(private http: HttpClient) { }

  // Job Descriptions
  getJobDescriptions(skip: number = 0, limit: number = 100): Observable<JobDescription[]> {
    const params = new HttpParams()
      .set('skip', skip.toString())
      .set('limit', limit.toString());
    return this.http.get<JobDescription[]>(`${this.apiUrl}/job-descriptions`, { params });
  }

  createJobDescription(jobDescription: { title: string; jd_text: string }): Observable<JobDescription> {
    return this.http.post<JobDescription>(`${this.apiUrl}/job-descriptions`, jobDescription);
  }

  getJobDescription(id: string): Observable<JobDescription> {
    return this.http.get<JobDescription>(`${this.apiUrl}/job-descriptions/${id}`);
  }

  updateJobDescription(id: string, jobDescription: Partial<JobDescription>): Observable<JobDescription> {
    return this.http.put<JobDescription>(`${this.apiUrl}/job-descriptions/${id}`, jobDescription);
  }

  deleteJobDescription(id: string): Observable<any> {
    return this.http.delete(`${this.apiUrl}/job-descriptions/${id}`);
  }

  searchJobDescriptions(title: string, skip: number = 0, limit: number = 100): Observable<JobDescription[]> {
    const params = new HttpParams()
      .set('title', title)
      .set('skip', skip.toString())
      .set('limit', limit.toString());
    return this.http.get<JobDescription[]>(`${this.apiUrl}/job-descriptions/search/`, { params });
  }

  // Resumes
  getResumes(skip: number = 0, limit: number = 100): Observable<Resume[]> {
    const params = new HttpParams()
      .set('skip', skip.toString())
      .set('limit', limit.toString());
    return this.http.get<Resume[]>(`${this.apiUrl}/resumes`, { params });
  }

  uploadResume(file: File, jdId: string, candidateName?: string, email?: string): Observable<Resume> {
    const formData = new FormData();
    // Determine a safe filename
    let safeFilename = file.name;
    if (candidateName) {
      // Use candidate name and original extension if possible
      const ext = file.name.split('.').pop();
      const base = candidateName.replace(/[^a-zA-Z0-9_\-]/g, '_').slice(0, 50);
      safeFilename = `${base}_${Date.now()}.${ext}`;
    }
    // Create a new File object with the safe filename if needed
    let uploadFile = file;
    if (safeFilename !== file.name) {
      uploadFile = new File([file], safeFilename, { type: file.type });
    }
    formData.append('file', uploadFile, safeFilename);
    formData.append('jd_id', jdId);
    if (candidateName) formData.append('candidate_name', candidateName);
    if (email) formData.append('email', email);
    
    return this.http.post<Resume>(`${this.apiUrl}/resumes/upload`, formData);
  }

  createResume(resume: Partial<Resume>): Observable<Resume> {
    return this.http.post<Resume>(`${this.apiUrl}/resumes`, resume);
  }

  getResume(id: string): Observable<Resume> {
    return this.http.get<Resume>(`${this.apiUrl}/resumes/${id}`);
  }

  updateResume(id: string, resume: Partial<Resume>): Observable<Resume> {
    return this.http.put<Resume>(`${this.apiUrl}/resumes/${id}`, resume);
  }

  deleteResume(id: string): Observable<any> {
    return this.http.delete(`${this.apiUrl}/resumes/${id}`);
  }

  searchResumesByName(name: string, skip: number = 0, limit: number = 100): Observable<Resume[]> {
    const params = new HttpParams()
      .set('name', name)
      .set('skip', skip.toString())
      .set('limit', limit.toString());
    return this.http.get<Resume[]>(`${this.apiUrl}/resumes/search/name`, { params });
  }

  getResumesByJobDescription(jdId: string, skip: number = 0, limit: number = 100): Observable<Resume[]> {
    const params = new HttpParams()
      .set('skip', skip.toString())
      .set('limit', limit.toString());
    return this.http.get<Resume[]>(`${this.apiUrl}/resumes/by-jd/${jdId}`, { params });
  }

  // Evaluations
  evaluateResume(resumeId: string, jdId: string): Observable<Evaluation> {
    return this.http.post<Evaluation>(`${this.apiUrl}/evaluations/evaluate`, {
      resume_id: resumeId,
      jd_id: jdId
    });
  }

  getEvaluations(skip: number = 0, limit: number = 100): Observable<Evaluation[]> {
    const params = new HttpParams()
      .set('skip', skip.toString())
      .set('limit', limit.toString());
    return this.http.get<Evaluation[]>(`${this.apiUrl}/evaluations`, { params });
  }

  getEvaluation(id: string): Observable<Evaluation> {
    return this.http.get<Evaluation>(`${this.apiUrl}/evaluations/${id}`);
  }

  getEvaluationsByJobDescription(jdId: string, skip: number = 0, limit: number = 100): Observable<Evaluation[]> {
    const params = new HttpParams()
      .set('skip', skip.toString())
      .set('limit', limit.toString());
    return this.http.get<Evaluation[]>(`${this.apiUrl}/evaluations/by-jd/${jdId}`, { params });
  }

  getEvaluationsByResume(resumeId: string, skip: number = 0, limit: number = 100): Observable<Evaluation[]> {
    const params = new HttpParams()
      .set('skip', skip.toString())
      .set('limit', limit.toString());
    return this.http.get<Evaluation[]>(`${this.apiUrl}/evaluations/by-resume/${resumeId}`, { params });
  }

  getTopEvaluations(jdId: string, limit: number = 10): Observable<Evaluation[]> {
    const params = new HttpParams().set('limit', limit.toString());
    return this.http.get<Evaluation[]>(`${this.apiUrl}/evaluations/top/${jdId}`, { params });
  }

  // Health Check
  getHealthCheck(): Observable<any> {
    return this.http.get(`${this.apiUrl}/health`);
  }

  testGeminiConnection(): Observable<any> {
    return this.http.get(`${this.apiUrl}/evaluations/test-gemini`);
  }
} 