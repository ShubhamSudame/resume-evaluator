import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { ApiService, JobDescription } from '../../services/api.service';

@Component({
  selector: 'app-job-list',
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `
    <div class="container mx-auto px-4 py-8">
      <div class="flex justify-between items-center mb-6">
        <h1 class="text-3xl font-bold text-gray-900">Job Descriptions</h1>
        <button 
          (click)="showAddForm = true" 
          class="bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded-lg transition-colors"
        >
          Add Job Description
        </button>
      </div>

      <!-- Add Job Description Form -->
      <div *ngIf="showAddForm" class="bg-white rounded-lg shadow-md p-6 mb-6">
        <h2 class="text-xl font-semibold mb-4">Add New Job Description</h2>
        <form (ngSubmit)="addJobDescription()" #jobForm="ngForm">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
            <div>
              <label for="title" class="block text-sm font-medium text-gray-700 mb-2">Job Title</label>
              <input 
                type="text" 
                id="title" 
                name="title" 
                [(ngModel)]="newJob.title" 
                required
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="e.g., Senior Software Engineer"
              >
            </div>
            <div>
              <label for="jd_text" class="block text-sm font-medium text-gray-700 mb-2">Job Description</label>
              <textarea 
                id="jd_text" 
                name="jd_text" 
                [(ngModel)]="newJob.jd_text" 
                required
                rows="4"
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Enter the job description..."
              ></textarea>
            </div>
          </div>
          <div class="flex gap-3">
            <button 
              type="submit" 
              [disabled]="!jobForm.form.valid || isLoading"
              class="bg-green-600 hover:bg-green-700 disabled:bg-gray-400 text-white font-medium py-2 px-4 rounded-lg transition-colors"
            >
              {{ isLoading ? 'Adding...' : 'Add Job Description' }}
            </button>
            <button 
              type="button" 
              (click)="cancelAdd()"
              class="bg-gray-500 hover:bg-gray-600 text-white font-medium py-2 px-4 rounded-lg transition-colors"
            >
              Cancel
            </button>
          </div>
        </form>
      </div>

      <!-- Job Descriptions Table -->
      <div class="bg-white rounded-lg shadow-md overflow-hidden">
        <div class="px-6 py-4 border-b border-gray-200">
          <h2 class="text-lg font-semibold text-gray-900">All Job Descriptions</h2>
        </div>
        
        <div *ngIf="loading" class="p-6 text-center">
          <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
          <p class="mt-2 text-gray-600">Loading job descriptions...</p>
        </div>

        <div *ngIf="!loading && jobDescriptions.length === 0" class="p-6 text-center">
          <p class="text-gray-600">No job descriptions found. Add your first job description to get started!</p>
        </div>

        <div *ngIf="!loading && jobDescriptions.length > 0" class="overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
              <tr>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Job Title</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Description</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Created</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr *ngFor="let job of jobDescriptions" class="hover:bg-gray-50">
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="text-sm font-medium text-gray-900">{{ job.title }}</div>
                </td>
                <td class="px-6 py-4">
                  <div class="text-sm text-gray-900 max-w-xs truncate">{{ job.jd_text }}</div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="text-sm text-gray-500">{{ formatDate(job.created_at) }}</div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                  <button 
                    (click)="viewJobDetails(job._id)"
                    class="text-blue-600 hover:text-blue-900 mr-3"
                  >
                    View Details
                  </button>
                  <button 
                    (click)="deleteJob(job._id)"
                    class="text-red-600 hover:text-red-900"
                  >
                    Delete
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  `,
  styles: []
})
export class JobListComponent implements OnInit {
  jobDescriptions: JobDescription[] = [];
  loading = false;
  showAddForm = false;
  isLoading = false;
  newJob = {
    title: '',
    jd_text: ''
  };

  constructor(
    private apiService: ApiService,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.loadJobDescriptions();
  }

  loadJobDescriptions(): void {
    this.loading = true;
    this.apiService.getJobDescriptions().subscribe({
      next: (jobs) => {
        this.jobDescriptions = jobs;
        this.loading = false;
      },
      error: (error) => {
        console.error('Error loading job descriptions:', error);
        this.loading = false;
      }
    });
  }

  addJobDescription(): void {
    if (!this.newJob.title || !this.newJob.jd_text) return;
    
    this.isLoading = true;
    this.apiService.createJobDescription(this.newJob).subscribe({
      next: (job) => {
        this.jobDescriptions.unshift(job);
        this.cancelAdd();
        this.isLoading = false;
      },
      error: (error) => {
        console.error('Error adding job description:', error);
        this.isLoading = false;
      }
    });
  }

  cancelAdd(): void {
    this.showAddForm = false;
    this.newJob = { title: '', jd_text: '' };
  }

  viewJobDetails(jobId: string): void {
    this.router.navigate(['/job', jobId]);
  }

  deleteJob(jobId: string): void {
    if (confirm('Are you sure you want to delete this job description?')) {
      this.apiService.deleteJobDescription(jobId).subscribe({
        next: () => {
          this.jobDescriptions = this.jobDescriptions.filter(job => job._id !== jobId);
        },
        error: (error) => {
          console.error('Error deleting job description:', error);
        }
      });
    }
  }

  formatDate(dateString: string): string {
    return new Date(dateString).toLocaleDateString();
  }
} 