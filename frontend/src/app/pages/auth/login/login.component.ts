import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { AuthService } from '../../../services/auth.service';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, FormsModule, ReactiveFormsModule, RouterModule],
  template: `
    <div class="observer-container flex items-center justify-center min-h-screen page-transition">
      <div class="glass-panel p-10 w-full max-w-md relative overflow-hidden">
        <div class="absolute -top-24 -right-24 w-64 h-64 bg-sky-500/10 rounded-full blur-3xl"></div>
        
        <div class="text-center mb-8 relative z-10">
          <div class="text-4xl mb-2">👁️</div>
          <h1 class="text-2xl font-bold text-white mb-1">Observer-Eye</h1>
          <p class="text-slate-500 text-sm">Sign in to your observability dashboard</p>
        </div>
        
        <form [formGroup]="loginForm" (ngSubmit)="onSubmit()" class="space-y-6 relative z-10">
          @if (error) {
            <div class="bg-red-500/10 border border-red-500/20 text-red-400 text-[10px] font-bold uppercase tracking-widest p-3 rounded-xl text-center">
              {{ error }}
            </div>
          }
          
          <div class="space-y-2">
            <label class="text-xs font-bold text-slate-500 uppercase tracking-widest">Email Address</label>
            <input 
              type="email" 
              formControlName="email" 
              placeholder="admin@observereye.io"
              class="w-full bg-slate-900/50 border border-white/10 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-sky-500/50 transition-colors"
            />
          </div>
          
          <div class="space-y-2">
            <div class="flex justify-between">
              <label class="text-xs font-bold text-slate-500 uppercase tracking-widest">Password</label>
              <a href="#" class="text-[10px] text-sky-400 font-bold hover:underline">Forgot?</a>
            </div>
            <input 
              type="password" 
              formControlName="password" 
              placeholder="••••••••••••••••"
              class="w-full bg-slate-900/50 border border-white/10 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-sky-500/50 transition-colors"
            />
          </div>
          
          <button type="submit" class="btn-premium w-full py-3 flex items-center justify-center gap-2" [disabled]="!loginForm.valid || authService.isLoading()">
            @if (authService.isLoading()) {
              <span class="w-4 h-4 border-2 border-white/20 border-t-white rounded-full animate-spin"></span>
            }
            <span>Initialize Session</span>
          </button>
        </form>
        
        <div class="mt-8 relative z-10">
          <div class="flex items-center gap-4 mb-6">
            <div class="h-px flex-1 bg-white/5"></div>
            <span class="text-[10px] text-slate-600 font-bold uppercase tracking-widest">OAuth Matrix</span>
            <div class="h-px flex-1 bg-white/5"></div>
          </div>
          
          <div class="grid grid-cols-2 gap-3">
            <button (click)="loginWithOAuth('github')" class="flex items-center justify-center gap-2 py-2 rounded-xl bg-white/5 border border-white/5 hover:bg-white/10 transition-colors text-xs text-white">
              <span>GitHub</span>
            </button>
            <button (click)="loginWithOAuth('google')" class="flex items-center justify-center gap-2 py-2 rounded-xl bg-white/5 border border-white/5 hover:bg-white/10 transition-colors text-xs text-white">
              <span>Google</span>
            </button>
          </div>
        </div>
        
        <p class="mt-8 text-center text-xs text-slate-500 relative z-10">
          New to the platform? <a routerLink="/auth/register" class="text-sky-400 font-bold hover:underline">Request Access</a>
        </p>
      </div>
    </div>
  `,
  styles: [`
    :host { display: block; min-height: 100vh; background: #020617; }
  `]
})
export class LoginComponent {
  loginForm: FormGroup;
  error: string | null = null;

  constructor(
    private fb: FormBuilder,
    public authService: AuthService
  ) {
    this.loginForm = this.fb.group({
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required, Validators.minLength(16)]]
    });
  }

  onSubmit(): void {
    if (this.loginForm.valid) {
      this.error = null;
      this.authService.login(this.loginForm.value).subscribe({
        next: () => {
          // AuthService handles navigation on success
        },
        error: (err) => {
          this.error = 'Access Denied: Invalid Authorization Matrix';
          console.error('Login failed:', err);
        }
      });
    }
  }

  loginWithOAuth(provider: string): void {
    this.authService.loginWithSocial(provider);
  }
}
