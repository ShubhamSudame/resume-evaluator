import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, Router } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { ApiService, JobDescription, Resume, Evaluation } from '../../services/api.service';

@Component({
  selector: 'app-job-detail',
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `
    <div class="container mx-auto px-4 py-8">
      <!-- Back Button -->
      <button 
        (click)="goBack()" 
        class="mb-6 flex items-center text-blue-600 hover:text-blue-800 transition-colors"
      >
        <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"></path>
        </svg>
        Back to Job Descriptions
      </button>

      <div *ngIf="loading" class="text-center py-8">
        <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
        <p class="mt-2 text-gray-600">Loading job details...</p>
      </div>

      <div *ngIf="!loading && jobDescription" class="space-y-6">
        <!-- Job Description Header -->
        <div class="bg-white rounded-lg shadow-md p-6">
          <div class="flex justify-between items-start mb-4">
            <div>
              <h1 class="text-3xl font-bold text-gray-900">{{ jobDescription.title }}</h1>
              <p class="text-gray-600 mt-2">Created: {{ formatDate(jobDescription.created_at) }}</p>
            </div>
            <button 
              (click)="showUploadForm = true" 
              class="bg-green-600 hover:bg-green-700 text-white font-medium py-2 px-4 rounded-lg transition-colors"
            >
              Upload Resume
            </button>
          </div>
          <div class="prose max-w-none">
            <h3 class="text-lg font-semibold mb-2">Job Description:</h3>
            <p class="text-gray-700 whitespace-pre-wrap">{{ jobDescription.jd_text }}</p>
          </div>
        </div>

        <!-- Resume Upload Form -->
        <div *ngIf="showUploadForm" class="bg-white rounded-lg shadow-md p-6">
          <h2 class="text-xl font-semibold mb-4">Upload Resume for {{ jobDescription.title }}</h2>
          <form (ngSubmit)="uploadResume()" #uploadForm="ngForm">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
              <div>
                <label for="candidateName" class="block text-sm font-medium text-gray-700 mb-2">Candidate Name</label>
                <input 
                  type="text" 
                  id="candidateName" 
                  name="candidateName" 
                  [(ngModel)]="uploadData.candidateName" 
                  required
                  class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="Enter candidate name"
                >
              </div>
              <div>
                <label for="email" class="block text-sm font-medium text-gray-700 mb-2">Email (Optional)</label>
                <input 
                  type="email" 
                  id="email" 
                  name="email" 
                  [(ngModel)]="uploadData.email" 
                  class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="Enter email address"
                >
              </div>
            </div>
            <div class="mb-4">
              <label for="resumeFile" class="block text-sm font-medium text-gray-700 mb-2">Resume File (PDF)</label>
              <input 
                type="file" 
                id="resumeFile" 
                name="resumeFile" 
                (change)="onFileSelected($event)" 
                accept=".pdf"
                required
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
            </div>
            <div class="flex gap-3">
              <button 
                type="submit" 
                [disabled]="!uploadForm.form.valid || !selectedFile || isUploading"
                class="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white font-medium py-2 px-4 rounded-lg transition-colors"
              >
                {{ isUploading ? 'Uploading...' : 'Upload & Evaluate' }}
              </button>
              <button 
                type="button" 
                (click)="cancelUpload()"
                class="bg-gray-500 hover:bg-gray-600 text-white font-medium py-2 px-4 rounded-lg transition-colors"
              >
                Cancel
              </button>
            </div>
          </form>
        </div>

        <!-- Candidates List -->
        <div class="bg-white rounded-lg shadow-md overflow-hidden">
          <div class="px-6 py-4 border-b border-gray-200">
            <h2 class="text-lg font-semibold text-gray-900">Candidates ({{ candidates.length }})</h2>
          </div>
          
          <div *ngIf="loadingCandidates" class="p-6 text-center">
            <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
            <p class="mt-2 text-gray-600">Loading candidates...</p>
          </div>

          <div *ngIf="!loadingCandidates && candidates.length === 0" class="p-6 text-center">
            <p class="text-gray-600">No candidates have applied yet. Upload the first resume to get started!</p>
          </div>

          <div *ngIf="!loadingCandidates && candidates.length > 0" class="overflow-x-auto">
            <table class="min-w-full divide-y divide-gray-200">
              <thead class="bg-gray-50">
                <tr>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Candidate</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Email</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Match Score</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200">
                <tr *ngFor="let candidate of candidates; let i = index" class="hover:bg-gray-50">
                  <td class="px-6 py-4 whitespace-nowrap">
                    <div class="text-sm font-medium text-gray-900">{{ candidate.candidate_name }}</div>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <div class="text-sm text-gray-500">{{ candidate.email || 'N/A' }}</div>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <ng-container *ngIf="evaluating[i]; else scoreBlock">
                      <div class="flex items-center justify-center">
                        <div class="inline-block animate-spin rounded-full h-6 w-6 border-b-2 border-blue-600"></div>
                      </div>
                    </ng-container>
                    <ng-template #scoreBlock>
                      <div *ngIf="candidate.evaluation" class="flex items-center">
                        <div class="text-sm font-medium text-gray-900">{{ candidate.evaluation.score }}%</div>
                        <div class="ml-2 w-16 bg-gray-200 rounded-full h-2">
                          <div 
                            class="h-2 rounded-full" 
                            [ngClass]="getScoreColor(candidate.evaluation.score)"
                            [style.width.%]="candidate.evaluation.score"
                          ></div>
                        </div>
                      </div>
                      <div *ngIf="!candidate.evaluation" class="text-sm text-gray-500">Not evaluated</div>
                    </ng-template>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <span *ngIf="candidate.evaluation" 
                          class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full"
                          [ngClass]="getStatusClass(candidate.evaluation.verdict)">
                      {{ candidate.evaluation.verdict }}
                    </span>
                    <span *ngIf="!candidate.evaluation" class="text-sm text-gray-500">Pending</span>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm font-medium flex gap-2">
                    <button 
                      (click)="viewCandidateDetails(candidate._id)"
                      class="text-blue-600 hover:text-blue-900"
                    >
                      View Details
                    </button>
                    <button 
                      *ngIf="!candidate.evaluation" 
                      [disabled]="evaluating[i]"
                      (click)="evaluateCandidate(candidate, i)"
                      class="bg-purple-600 hover:bg-purple-700 disabled:bg-gray-400 text-white font-medium py-1 px-3 rounded-lg transition-colors"
                    >
                      {{ evaluating[i] ? 'Evaluating...' : 'Evaluate' }}
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <div *ngIf="!loading && !jobDescription" class="text-center py-8">
        <p class="text-gray-600">Job description not found.</p>
      </div>
    </div>
  `,
  styles: []
})
export class JobDetailComponent implements OnInit {
  jobDescription: JobDescription | null = null;
  candidates: (Resume & { evaluation?: Evaluation })[] = [];
  evaluating: boolean[] = [];
  loading = false;
  loadingCandidates = false;
  showUploadForm = false;
  isUploading = false;
  selectedFile: File | null = null;
  uploadData = {
    candidateName: '',
    email: ''
  };

  constructor(
    private apiService: ApiService,
    private route: ActivatedRoute,
    private router: Router
  ) {}

  ngOnInit(): void {
    const jobId = this.route.snapshot.paramMap.get('id');
    if (jobId) {
      this.loadJobDescription(jobId);
      this.loadCandidates(jobId);
    }
  }

  loadJobDescription(jobId: string): void {
    this.loading = true;
    this.apiService.getJobDescription(jobId).subscribe({
      next: (job) => {
        this.jobDescription = job;
        this.loading = false;
      },
      error: (error) => {
        console.error('Error loading job description:', error);
        this.loading = false;
      }
    });
  }

  loadCandidates(jobId: string): void {
    this.loadingCandidates = true;
    this.apiService.getResumesByJobDescription(jobId).subscribe({
      next: (resumes) => {
        const candidatesWithEvaluations = resumes.map(resume => {
          const candidate = resume as any;
          this.apiService.getEvaluationsByResume(resume._id).subscribe({
            next: (evaluations) => {
              const jobEvaluation = evaluations.find(evaluation => evaluation.jd_id === jobId);
              if (jobEvaluation) {
                candidate.evaluation = jobEvaluation;
              }
            }
          });
          return candidate;
        });
        this.candidates = candidatesWithEvaluations;
        this.evaluating = this.candidates.map(() => false);
        this.loadingCandidates = false;
      },
      error: (error) => {
        console.error('Error loading candidates:', error);
        this.loadingCandidates = false;
      }
    });
  }

  onFileSelected(event: any): void {
    const file = event.target.files[0];
    if (file && file.type === 'application/pdf') {
      this.selectedFile = file;
    } else {
      alert('Please select a valid PDF file.');
      event.target.value = '';
    }
  }

  uploadResume(): void {
    if (!this.selectedFile || !this.jobDescription) return;
    
    this.isUploading = true;
    this.apiService.uploadResume(
      this.selectedFile, 
      this.jobDescription._id, 
      this.uploadData.candidateName, 
      this.uploadData.email
    ).subscribe({
      next: (resume) => {
        // Add the new candidate instantly, not evaluated yet
        this.candidates.unshift(resume);
        this.evaluating.unshift(false);
        this.cancelUpload();
        this.isUploading = false;
      },
      error: (error) => {
        console.error('Error uploading resume:', error);
        this.isUploading = false;
      }
    });
  }

  evaluateCandidate(candidate: Resume & { evaluation?: Evaluation }, index: number): void {
    if (!this.jobDescription) return;
    this.evaluating[index] = true;
    this.apiService.evaluateResume(candidate._id, this.jobDescription._id).subscribe({
      next: (evaluation) => {
        candidate.evaluation = evaluation;
        this.evaluating[index] = false;
      },
      error: (error) => {
        console.error('Error evaluating candidate:', error);
        this.evaluating[index] = false;
      }
    });
  }

  cancelUpload(): void {
    this.showUploadForm = false;
    this.selectedFile = null;
    this.uploadData = { candidateName: '', email: '' };
  }

  viewCandidateDetails(resumeId: string): void {
    const candidate = this.candidates.find(c => c._id === resumeId);
    if (candidate && candidate.evaluation) {
      // Navigate to candidate detail page with evaluation data (could use state or a service)
      this.router.navigate(['/candidate', resumeId], { state: { evaluation: candidate.evaluation } });
    } else {
      // Navigate to candidate detail page with a flag for 'not evaluated'
      this.router.navigate(['/candidate', resumeId], { state: { notEvaluated: true } });
    }
  }

  goBack(): void {
    this.router.navigate(['/']);
  }

  formatDate(dateString: string): string {
    return new Date(dateString).toLocaleDateString();
  }

  getScoreColor(score: number): string {
    if (score >= 80) return 'bg-green-500';
    if (score >= 60) return 'bg-yellow-500';
    return 'bg-red-500';
  }

  getStatusClass(verdict: string): string {
    switch (verdict.toLowerCase()) {
      case 'strong match':
        return 'bg-green-100 text-green-800';
      case 'good match':
        return 'bg-blue-100 text-blue-800';
      case 'moderate match':
        return 'bg-yellow-100 text-yellow-800';
      case 'weak match':
        return 'bg-red-100 text-red-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  }
} 