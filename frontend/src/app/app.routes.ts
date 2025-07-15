import { Routes } from '@angular/router';
import { ResumeUploadComponent } from './resume-upload/resume-upload.component';
import { DashboardComponent } from './dashboard/dashboard.component';
import { JobListComponent } from './components/job-list/job-list.component';
import { JobDetailComponent } from './components/job-detail/job-detail.component';
import { CandidateDetailComponent } from './components/candidate-detail/candidate-detail.component';

export const routes: Routes = [
  { path: '', component: JobListComponent },
  { path: 'dashboard', component: DashboardComponent },
  { path: 'upload', component: ResumeUploadComponent },
  { path: 'job/:id', component: JobDetailComponent },
  { path: 'candidate/:id', component: CandidateDetailComponent },
  { path: '**', redirectTo: '' }
]; 