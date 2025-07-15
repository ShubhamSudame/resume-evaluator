import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterOutlet, RouterLink, RouterLinkActive } from '@angular/router';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, RouterOutlet, RouterLink, RouterLinkActive],
  template: `
    <div class="min-h-screen bg-gray-50">
      <!-- Navigation Header -->
      <nav class="bg-white shadow-sm border-b border-gray-200">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div class="flex justify-between h-16">
            <div class="flex items-center">
              <div class="flex-shrink-0 flex items-center">
                <h1 class="text-xl font-bold text-gray-900">Resume Evaluator</h1>
              </div>
              <div class="hidden sm:ml-6 sm:flex sm:space-x-8">
                <a 
                  routerLink="/" 
                  routerLinkActive="border-blue-500 text-gray-900"
                  [routerLinkActiveOptions]="{exact: true}"
                  class="border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium"
                >
                  Job Descriptions
                </a>
                <a 
                  routerLink="/dashboard" 
                  routerLinkActive="border-blue-500 text-gray-900"
                  class="border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium"
                >
                  Dashboard
                </a>
                <a 
                  routerLink="/upload" 
                  routerLinkActive="border-blue-500 text-gray-900"
                  class="border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium"
                >
                  Upload Resume
                </a>
              </div>
            </div>
            <div class="hidden sm:ml-6 sm:flex sm:items-center">
              <div class="text-sm text-gray-500">
                AI-Powered Resume Analysis
              </div>
            </div>
          </div>
        </div>
      </nav>

      <!-- Main Content -->
      <main class="flex-1">
        <router-outlet></router-outlet>
      </main>

      <!-- Footer -->
      <footer class="bg-white border-t border-gray-200 mt-12">
        <div class="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
          <div class="text-center text-sm text-gray-500">
            <p>&copy; 2024 Resume Evaluator. Built with Angular and FastAPI.</p>
          </div>
        </div>
      </footer>
    </div>
  `,
  styles: []
})
export class AppComponent {
  title = 'resume-evaluator';
} 