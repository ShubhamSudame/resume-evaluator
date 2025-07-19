import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, Router } from '@angular/router';
import { ApiService, Resume, Evaluation, JobDescription } from '../../services/api.service';

@Component({
  selector: 'app-candidate-detail',
  standalone: true,
  imports: [CommonModule],
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
        Back to Job Description
      </button>

      <div *ngIf="loading" class="text-center py-8">
        <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
        <p class="mt-2 text-gray-600">Loading candidate details...</p>
      </div>

      <div *ngIf="!loading && resume" class="space-y-6">
        <!-- Candidate Header -->
        <div class="bg-white rounded-lg shadow-md p-6">
          <div class="flex justify-between items-start">
            <div>
              <h1 class="text-3xl font-bold text-gray-900">{{ resume.candidate_name }}</h1>
              <p class="text-gray-600 mt-2">{{ resume.email || 'No email provided' }}</p>
              <p class="text-gray-500 text-sm">Applied: {{ formatDate(resume.created_at) }}</p>
            </div>
            <div *ngIf="evaluation" class="text-right">
              <div class="text-4xl font-bold" [ngClass]="getScoreTextColor(evaluation.score)">
                {{ evaluation.score }}%
              </div>
              <div class="text-lg font-semibold text-gray-700">{{ evaluation.verdict }}</div>
            </div>
          </div>
        </div>

        <!-- Job Description -->
        <div *ngIf="jobDescription" class="bg-white rounded-lg shadow-md p-6">
          <h2 class="text-xl font-semibold mb-4">Job Description</h2>
          <div class="mb-4">
            <h3 class="text-lg font-medium text-gray-900">{{ jobDescription.title }}</h3>
            <p class="text-gray-600 text-sm">Created: {{ formatDate(jobDescription.created_at) }}</p>
          </div>
          <div class="prose max-w-none">
            <p class="text-gray-700 whitespace-pre-wrap">{{ jobDescription.jd_text }}</p>
          </div>
        </div>

        <!-- Evaluation Details -->
        <div *ngIf="evaluation; else notEvaluatedBlock" class="bg-white rounded-lg shadow-md p-6">
          <h2 class="text-xl font-semibold mb-6">Evaluation Results</h2>
          
          <!-- Overall Score -->
          <div class="mb-8">
            <h3 class="text-lg font-medium text-gray-900 mb-4">Overall Match Score</h3>
            <div class="flex items-center space-x-4">
              <div class="text-3xl font-bold" [ngClass]="getScoreTextColor(evaluation.score)">
                {{ evaluation.score }}%
              </div>
              <div class="flex-1">
                <div class="w-full bg-gray-200 rounded-full h-4">
                  <div 
                    class="h-4 rounded-full transition-all duration-500" 
                    [ngClass]="getScoreColor(evaluation.score)"
                    [style.width.%]="evaluation.score"
                  ></div>
                </div>
              </div>
            </div>
            <div class="mt-2 text-lg font-semibold text-gray-700">{{ evaluation.verdict }}</div>
          </div>

          <!-- Category Breakdown -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
            <div>
              <h3 class="text-lg font-medium text-gray-900 mb-4">Category Breakdown</h3>
              <div class="space-y-4">
                <div>
                  <div class="flex justify-between text-sm mb-1">
                    <span>Skills Match</span>
                    <span class="font-medium">{{ getSkillsMatchPercent() !== null ? getSkillsMatchPercent() + '%' : 'N/A' }}</span>
                  </div>
                  <div class="w-full bg-gray-200 rounded-full h-2">
                    <div class="h-2 rounded-full" [ngClass]="getScoreColor(getSkillsMatchPercent() || 0)" [style.width.%]="getSkillsMatchPercent() || 0"></div>
                  </div>
                </div>
                <div>
                  <div class="flex justify-between text-sm mb-1">
                    <span>Experience</span>
                    <span class="font-medium">{{ evaluation.category_breakdown.experience }}%</span>
                  </div>
                  <div class="w-full bg-gray-200 rounded-full h-2">
                    <div class="h-2 rounded-full" [ngClass]="getScoreColor(evaluation.category_breakdown.experience)" [style.width.%]="evaluation.category_breakdown.experience"></div>
                  </div>
                </div>
                <div>
                  <div class="flex justify-between text-sm mb-1">
                    <span>Education</span>
                    <span class="font-medium">{{ evaluation.category_breakdown.education }}%</span>
                  </div>
                  <div class="w-full bg-gray-200 rounded-full h-2">
                    <div class="h-2 rounded-full" [ngClass]="getScoreColor(evaluation.category_breakdown.education)" [style.width.%]="evaluation.category_breakdown.education"></div>
                  </div>
                </div>
                <div *ngIf="evaluation.category_breakdown.jd_alignment !== undefined">
                  <div class="flex justify-between text-sm mb-1">
                    <span>JD Alignment</span>
                    <span class="font-medium">{{ evaluation.category_breakdown.jd_alignment }}%</span>
                  </div>
                  <div class="w-full bg-gray-200 rounded-full h-2">
                    <div class="h-2 rounded-full" [ngClass]="getScoreColor(evaluation.category_breakdown.jd_alignment)" [style.width.%]="evaluation.category_breakdown.jd_alignment"></div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Skills Analysis -->
            <div>
              <h3 class="text-lg font-medium text-gray-900 mb-4">Skills Analysis</h3>
              <div class="space-y-4">
                <div>
                  <h4 class="text-sm font-medium text-green-700 mb-2">Matched Skills ({{ evaluation.matched_skills.length }})</h4>
                  <div class="flex flex-wrap gap-2">
                    <span 
                      *ngFor="let skill of evaluation.matched_skills" 
                      class="px-2 py-1 bg-green-100 text-green-800 text-xs rounded-full"
                    >
                      {{ skill }}
                    </span>
                  </div>
                </div>
                <div>
                  <h4 class="text-sm font-medium text-red-700 mb-2">Missing Skills ({{ evaluation.missing_skills.length }})</h4>
                  <div class="flex flex-wrap gap-2">
                    <span 
                      *ngFor="let skill of evaluation.missing_skills" 
                      class="px-2 py-1 bg-red-100 text-red-800 text-xs rounded-full"
                    >
                      {{ skill }}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Pros and Cons -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
            <div>
              <h3 class="text-lg font-medium text-green-700 mb-4">Strengths</h3>
              <ul class="space-y-2">
                <li 
                  *ngFor="let pro of evaluation.pros" 
                  class="flex items-start"
                >
                  <svg class="w-5 h-5 text-green-500 mr-2 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
                  </svg>
                  <span class="text-gray-700">{{ pro }}</span>
                </li>
              </ul>
            </div>
            <div>
              <h3 class="text-lg font-medium text-red-700 mb-4">Areas for Improvement</h3>
              <ul class="space-y-2">
                <li 
                  *ngFor="let con of evaluation.cons" 
                  class="flex items-start"
                >
                  <svg class="w-5 h-5 text-red-500 mr-2 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"></path>
                  </svg>
                  <span class="text-gray-700">{{ con }}</span>
                </li>
              </ul>
            </div>
          </div>

          <!-- Detailed Feedback -->
          <div>
            <h3 class="text-lg font-medium text-gray-900 mb-4">Detailed Feedback</h3>
            <div class="bg-gray-50 rounded-lg p-4">
              <p class="text-gray-700 whitespace-pre-wrap">{{ evaluation.feedback }}</p>
            </div>
          </div>
        </div>
        <ng-template #notEvaluatedBlock>
          <div class="bg-white rounded-lg shadow-md p-6 text-center">
            <h2 class="text-xl font-semibold mb-4">Evaluation Results</h2>
            <p class="text-gray-600">This candidate has not been evaluated yet.</p>
          </div>
        </ng-template>

        <!-- Resume Content -->
        <div *ngIf="resume.raw_text" class="bg-white rounded-lg shadow-md p-6">
          <h2 class="text-xl font-semibold mb-4">Resume Content</h2>
          <div class="bg-gray-50 rounded-lg p-4 max-h-96 overflow-y-auto">
            <pre class="text-sm text-gray-700 whitespace-pre-wrap">{{ resume.raw_text }}</pre>
          </div>
        </div>

        <!-- No Evaluation Message -->
        <div *ngIf="!evaluation" class="bg-white rounded-lg shadow-md p-6 text-center">
          <h2 class="text-xl font-semibold mb-4">No Evaluation Available</h2>
          <p class="text-gray-600 mb-4">This candidate's resume hasn't been evaluated yet.</p>
          <button 
            (click)="evaluateResume()" 
            [disabled]="isEvaluating"
            class="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white font-medium py-2 px-4 rounded-lg transition-colors"
          >
            {{ isEvaluating ? 'Evaluating...' : 'Evaluate Resume' }}
          </button>
        </div>
      </div>

      <div *ngIf="!loading && !resume" class="text-center py-8">
        <p class="text-gray-600">Candidate not found.</p>
      </div>
    </div>
  `,
  styles: []
})
export class CandidateDetailComponent implements OnInit {
  resume: Resume | null = null;
  evaluation: Evaluation | null = null;
  jobDescription: JobDescription | null = null;
  loading = false;
  isEvaluating = false;

  constructor(
    private apiService: ApiService,
    private route: ActivatedRoute,
    private router: Router
  ) {}

  ngOnInit(): void {
    const resumeId = this.route.snapshot.paramMap.get('id');
    const nav = this.router.getCurrentNavigation();
    const state = nav && nav.extras && nav.extras.state ? nav.extras.state : {};
    if (resumeId) {
      this.loadCandidateDetails(resumeId);
      if (state && state['evaluation']) {
        this.evaluation = state['evaluation'];
      } else if (state && state['notEvaluated']) {
        this.evaluation = null;
      } else {
        this.loadEvaluation(resumeId);
      }
    }
  }

  loadCandidateDetails(resumeId: string): void {
    this.loading = true;
    this.apiService.getResume(resumeId).subscribe({
      next: (resume) => {
        this.resume = resume;
        // Load job description if available
        if (resume.jd_ids && resume.jd_ids.length > 0) {
          this.loadJobDescription(resume.jd_ids[0]);
        }
        this.loading = false;
      },
      error: (error) => {
        console.error('Error loading candidate details:', error);
        this.loading = false;
      }
    });
  }

  loadJobDescription(jdId: string): void {
    this.apiService.getJobDescription(jdId).subscribe({
      next: (job) => {
        this.jobDescription = job;
      },
      error: (error) => {
        console.error('Error loading job description:', error);
      }
    });
  }

  loadEvaluation(resumeId: string): void {
    this.apiService.getEvaluationsByResume(resumeId).subscribe({
      next: (evaluations) => {
        if (evaluations.length > 0) {
          this.evaluation = evaluations[0]; // Get the first evaluation
        }
      },
      error: (error) => {
        console.error('Error loading evaluation:', error);
      }
    });
  }

  evaluateResume(): void {
    if (!this.resume || !this.resume.jd_ids || this.resume.jd_ids.length === 0) return;
    
    this.isEvaluating = true;
    this.apiService.evaluateResume(this.resume._id, this.resume.jd_ids[0]).subscribe({
      next: (evaluation) => {
        this.evaluation = evaluation;
        this.isEvaluating = false;
      },
      error: (error) => {
        console.error('Error evaluating resume:', error);
        this.isEvaluating = false;
      }
    });
  }

  goBack(): void {
    // Go back to the job detail page if we have a job description
    if (this.jobDescription) {
      this.router.navigate(['/job', this.jobDescription._id]);
    } else {
      this.router.navigate(['/']);
    }
  }

  formatDate(dateString: string): string {
    return new Date(dateString).toLocaleDateString();
  }

  getScoreColor(score: number): string {
    if (score >= 81) return 'bg-green-300'; // light green
    if (score >= 61) return 'bg-green-500'; // green
    if (score >= 41) return 'bg-blue-500'; // blue
    if (score >= 21) return 'bg-yellow-400'; // yellow
    if (score >= 11) return 'bg-orange-400'; // orange
    return 'bg-red-500'; // red
  }
  // Optionally, for the percentage number:
  getScoreTextColor(score: number): string {
    if (score >= 80) return 'text-green-600';
    if (score >= 60) return 'text-yellow-600';
    return 'text-red-600';
  }

  // Add a method to calculate skills match percentage
  getSkillsMatchPercent(): number | null {
    if (!this.evaluation) return null;
    const matched = this.evaluation.matched_skills?.length || 0;
    const missing = this.evaluation.missing_skills?.length || 0;
    const total = matched + missing;
    if (total === 0) return null;
    return Math.round((matched / total) * 100);
  }
} 