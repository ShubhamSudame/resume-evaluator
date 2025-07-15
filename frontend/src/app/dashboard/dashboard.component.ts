import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ApiService, JobDescription, Resume, Evaluation } from '../services/api.service';
import { environment } from '../../environments/environment';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="dashboard">
      <h1>{{ environment.appName }} Dashboard</h1>
      <p>Version: {{ environment.version }}</p>
      <p>Environment: {{ environment.production ? 'Production' : 'Development' }}</p>
      <p>API URL: {{ environment.apiUrl }}</p>
      
      <div class="status-section">
        <h2>System Status</h2>
        <div *ngIf="healthStatus" class="status-item">
          <span class="status-label">Backend Health:</span>
          <span class="status-value" [class.healthy]="healthStatus.status === 'healthy'">
            {{ healthStatus.status }}
          </span>
        </div>
        <div *ngIf="geminiStatus" class="status-item">
          <span class="status-label">Gemini AI:</span>
          <span class="status-value" [class.healthy]="geminiStatus.status === 'connected'">
            {{ geminiStatus.status }}
          </span>
        </div>
      </div>

      <div class="stats-section">
        <h2>Statistics</h2>
        <div class="stats-grid">
          <div class="stat-item">
            <span class="stat-number">{{ jobDescriptionsCount }}</span>
            <span class="stat-label">Job Descriptions</span>
          </div>
          <div class="stat-item">
            <span class="stat-number">{{ resumesCount }}</span>
            <span class="stat-label">Resumes</span>
          </div>
          <div class="stat-item">
            <span class="stat-number">{{ evaluationsCount }}</span>
            <span class="stat-label">Evaluations</span>
          </div>
        </div>
      </div>

      <div class="actions-section">
        <h2>Quick Actions</h2>
        <button (click)="refreshData()" class="btn btn-primary">Refresh Data</button>
        <button (click)="testGemini()" class="btn btn-secondary">Test Gemini AI</button>
      </div>
    </div>
  `,
  styles: [`
    .dashboard {
      padding: 20px;
      max-width: 1200px;
      margin: 0 auto;
    }

    h1 {
      color: #333;
      margin-bottom: 10px;
    }

    .status-section, .stats-section, .actions-section {
      margin: 20px 0;
      padding: 20px;
      border: 1px solid #ddd;
      border-radius: 8px;
      background: #f9f9f9;
    }

    .status-item {
      display: flex;
      justify-content: space-between;
      margin: 10px 0;
      padding: 10px;
      background: white;
      border-radius: 4px;
    }

    .status-value.healthy {
      color: #28a745;
      font-weight: bold;
    }

    .stats-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
      gap: 20px;
      margin-top: 15px;
    }

    .stat-item {
      text-align: center;
      padding: 20px;
      background: white;
      border-radius: 8px;
      box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }

    .stat-number {
      display: block;
      font-size: 2em;
      font-weight: bold;
      color: #007bff;
    }

    .stat-label {
      display: block;
      margin-top: 5px;
      color: #666;
    }

    .btn {
      padding: 10px 20px;
      margin: 5px;
      border: none;
      border-radius: 4px;
      cursor: pointer;
      font-size: 14px;
    }

    .btn-primary {
      background: #007bff;
      color: white;
    }

    .btn-secondary {
      background: #6c757d;
      color: white;
    }

    .btn:hover {
      opacity: 0.8;
    }
  `]
})
export class DashboardComponent implements OnInit {
  environment = environment;
  healthStatus: any = null;
  geminiStatus: any = null;
  jobDescriptionsCount = 0;
  resumesCount = 0;
  evaluationsCount = 0;

  constructor(private apiService: ApiService) {}

  ngOnInit() {
    this.refreshData();
  }

  refreshData() {
    // Get health status
    this.apiService.getHealthCheck().subscribe({
      next: (data) => {
        this.healthStatus = data;
        console.log('Health check:', data);
      },
      error: (error) => {
        console.error('Health check failed:', error);
        this.healthStatus = { status: 'error', message: 'Connection failed' };
      }
    });

    // Get counts (simplified - in a real app you'd have count endpoints)
    this.apiService.getJobDescriptions(0, 1).subscribe({
      next: (data) => {
        // This is a simplified approach - ideally you'd have count endpoints
        console.log('Job descriptions loaded');
      },
      error: (error) => {
        console.error('Failed to load job descriptions:', error);
      }
    });
  }

  testGemini() {
    this.apiService.testGeminiConnection().subscribe({
      next: (data) => {
        this.geminiStatus = data;
        console.log('Gemini test:', data);
      },
      error: (error) => {
        console.error('Gemini test failed:', error);
        this.geminiStatus = { status: 'error', message: 'Test failed' };
      }
    });
  }
} 