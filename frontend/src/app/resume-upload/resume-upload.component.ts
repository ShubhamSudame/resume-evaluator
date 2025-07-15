import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient, HttpEventType, HttpResponse } from '@angular/common/http';

@Component({
  selector: 'app-resume-upload',
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `
    <div class="upload-container">
      <div class="upload-card">
        <h2>Upload Your Resume</h2>
        <p class="description">
          Upload your resume in PDF, DOC, or DOCX format to get AI-powered analysis and insights.
        </p>
        
        <div class="upload-area" 
             [class.dragover]="isDragOver"
             (dragover)="onDragOver($event)"
             (dragleave)="onDragLeave($event)"
             (drop)="onDrop($event)">
          
          <div class="upload-icon">
            <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
              <polyline points="7,10 12,15 17,10"></polyline>
              <line x1="12" y1="15" x2="12" y2="3"></line>
            </svg>
          </div>
          
          <p class="upload-text">
            Drag and drop your resume here, or 
            <label for="file-input" class="file-label">browse files</label>
          </p>
          
          <input 
            type="file" 
            id="file-input" 
            class="file-input"
            accept=".pdf,.doc,.docx"
            (change)="onFileSelected($event)"
            [disabled]="isUploading">
        </div>
        
        <div *ngIf="selectedFile" class="file-info">
          <p><strong>Selected file:</strong> {{ selectedFile.name }}</p>
          <p><strong>Size:</strong> {{ formatFileSize(selectedFile.size) }}</p>
        </div>
        
        <div *ngIf="uploadProgress > 0 && uploadProgress < 100" class="progress-container">
          <div class="progress-bar">
            <div class="progress-fill" [style.width.%]="uploadProgress"></div>
          </div>
          <p class="progress-text">{{ uploadProgress }}% uploaded</p>
        </div>
        
        <button 
          class="upload-button" 
          (click)="uploadFile()"
          [disabled]="!selectedFile || isUploading">
          {{ isUploading ? 'Uploading...' : 'Analyze Resume' }}
        </button>
        
        <div *ngIf="analysisResult" class="analysis-result">
          <h3>Analysis Results</h3>
          <div class="result-content">
            <pre>{{ analysisResult | json }}</pre>
          </div>
        </div>
        
        <div *ngIf="errorMessage" class="error-message">
          {{ errorMessage }}
        </div>
      </div>
    </div>
  `,
  styles: [`
    .upload-container {
      display: flex;
      justify-content: center;
      align-items: center;
      min-height: 60vh;
    }
    
    .upload-card {
      background: white;
      border-radius: 12px;
      box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
      padding: 2rem;
      max-width: 600px;
      width: 100%;
    }
    
    .upload-card h2 {
      text-align: center;
      color: #333;
      margin-bottom: 0.5rem;
    }
    
    .description {
      text-align: center;
      color: #666;
      margin-bottom: 2rem;
    }
    
    .upload-area {
      border: 2px dashed #ddd;
      border-radius: 8px;
      padding: 2rem;
      text-align: center;
      transition: all 0.3s ease;
      cursor: pointer;
      margin-bottom: 1rem;
    }
    
    .upload-area:hover {
      border-color: #667eea;
      background-color: #f8f9ff;
    }
    
    .upload-area.dragover {
      border-color: #667eea;
      background-color: #f0f2ff;
    }
    
    .upload-icon {
      color: #667eea;
      margin-bottom: 1rem;
    }
    
    .upload-text {
      color: #666;
      margin: 0;
    }
    
    .file-label {
      color: #667eea;
      cursor: pointer;
      text-decoration: underline;
    }
    
    .file-input {
      display: none;
    }
    
    .file-info {
      background: #f8f9fa;
      padding: 1rem;
      border-radius: 6px;
      margin-bottom: 1rem;
    }
    
    .file-info p {
      margin: 0.25rem 0;
      color: #495057;
    }
    
    .progress-container {
      margin-bottom: 1rem;
    }
    
    .progress-bar {
      width: 100%;
      height: 8px;
      background-color: #e9ecef;
      border-radius: 4px;
      overflow: hidden;
    }
    
    .progress-fill {
      height: 100%;
      background: linear-gradient(90deg, #667eea, #764ba2);
      transition: width 0.3s ease;
    }
    
    .progress-text {
      text-align: center;
      margin: 0.5rem 0 0 0;
      color: #666;
      font-size: 0.9rem;
    }
    
    .upload-button {
      width: 100%;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: white;
      border: none;
      padding: 1rem;
      border-radius: 6px;
      font-size: 1.1rem;
      cursor: pointer;
      transition: all 0.3s ease;
    }
    
    .upload-button:hover:not(:disabled) {
      transform: translateY(-2px);
      box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }
    
    .upload-button:disabled {
      opacity: 0.6;
      cursor: not-allowed;
    }
    
    .analysis-result {
      margin-top: 2rem;
      padding: 1rem;
      background: #f8f9fa;
      border-radius: 6px;
      border-left: 4px solid #667eea;
    }
    
    .analysis-result h3 {
      margin: 0 0 1rem 0;
      color: #333;
    }
    
    .result-content {
      background: white;
      padding: 1rem;
      border-radius: 4px;
      overflow-x: auto;
    }
    
    .result-content pre {
      margin: 0;
      font-size: 0.9rem;
      color: #495057;
    }
    
    .error-message {
      background: #f8d7da;
      color: #721c24;
      padding: 1rem;
      border-radius: 6px;
      margin-top: 1rem;
      border: 1px solid #f5c6cb;
    }
  `]
})
export class ResumeUploadComponent {
  selectedFile: File | null = null;
  isDragOver = false;
  isUploading = false;
  uploadProgress = 0;
  analysisResult: any = null;
  errorMessage = '';

  constructor(private http: HttpClient) {}

  onDragOver(event: DragEvent) {
    event.preventDefault();
    this.isDragOver = true;
  }

  onDragLeave(event: DragEvent) {
    event.preventDefault();
    this.isDragOver = false;
  }

  onDrop(event: DragEvent) {
    event.preventDefault();
    this.isDragOver = false;
    
    const files = event.dataTransfer?.files;
    if (files && files.length > 0) {
      this.selectedFile = files[0];
    }
  }

  onFileSelected(event: any) {
    const file = event.target.files[0];
    if (file) {
      this.selectedFile = file;
    }
  }

  formatFileSize(bytes: number): string {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  }

  uploadFile() {
    if (!this.selectedFile) return;

    this.isUploading = true;
    this.uploadProgress = 0;
    this.errorMessage = '';
    this.analysisResult = null;

    const formData = new FormData();
    formData.append('file', this.selectedFile);

    // For now, we'll use a mock API call since the backend isn't fully set up
    // In a real implementation, you would call your FastAPI backend
    this.http.post('http://localhost:8000/api/resume/analyze', formData, {
      reportProgress: true,
      observe: 'events'
    }).subscribe({
      next: (event: any) => {
        if (event.type === HttpEventType.UploadProgress) {
          this.uploadProgress = Math.round(100 * event.loaded / event.total);
        } else if (event instanceof HttpResponse) {
          this.analysisResult = event.body;
          this.isUploading = false;
        }
      },
      error: (error) => {
        this.errorMessage = 'Upload failed. Please try again.';
        this.isUploading = false;
        console.error('Upload error:', error);
      }
    });
  }
} 