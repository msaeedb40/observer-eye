import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';

@Component({
    selector: 'app-login',
    standalone: true,
    imports: [CommonModule, FormsModule, ReactiveFormsModule, RouterModule],
    template: `
    <div class="auth-container">
      <div class="auth-card">
        <div class="auth-header">
          <h1>Observer-Eye</h1>
          <h2>Sign In</h2>
        </div>
        
        <form [formGroup]="loginForm" (ngSubmit)="onSubmit()">
          <div class="form-group">
            <label for="email">Email</label>
            <input 
              type="email" 
              id="email" 
              formControlName="email" 
              placeholder="Enter your email"
            />
          </div>
          
          <div class="form-group">
            <label for="password">Password</label>
            <input 
              type="password" 
              id="password" 
              formControlName="password" 
              placeholder="Enter your password (min 16 chars)"
            />
            <div class="password-strength" *ngIf="passwordStrength">
              <span [class]="passwordStrength">{{ passwordStrength }}</span>
            </div>
          </div>
          
          <button type="submit" class="btn-primary" [disabled]="!loginForm.valid">
            Sign In
          </button>
        </form>
        
        <div class="divider">
          <span>or continue with</span>
        </div>
        
        <div class="oauth-buttons">
          <button (click)="loginWithOAuth('github')" class="oauth-btn github">
            GitHub
          </button>
          <button (click)="loginWithOAuth('gitlab')" class="oauth-btn gitlab">
            GitLab
          </button>
          <button (click)="loginWithOAuth('google')" class="oauth-btn google">
            Google
          </button>
          <button (click)="loginWithOAuth('microsoft')" class="oauth-btn microsoft">
            Microsoft
          </button>
        </div>
        
        <p class="auth-footer">
          Don't have an account? <a routerLink="/auth/register">Sign Up</a>
        </p>
      </div>
    </div>
  `,
    styles: [`
    .auth-container {
      min-height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
      background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
      padding: 2rem;
    }
    .auth-card {
      background: white;
      padding: 3rem;
      border-radius: 20px;
      box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
      width: 100%;
      max-width: 420px;
    }
    .auth-header {
      text-align: center;
      margin-bottom: 2rem;
    }
    .auth-header h1 {
      color: #667eea;
      font-size: 2rem;
      margin-bottom: 0.5rem;
    }
    .auth-header h2 {
      color: #333;
      font-size: 1.5rem;
    }
    .form-group {
      margin-bottom: 1.5rem;
    }
    .form-group label {
      display: block;
      margin-bottom: 0.5rem;
      color: #333;
      font-weight: 500;
    }
    .form-group input {
      width: 100%;
      padding: 1rem;
      border: 2px solid #e0e0e0;
      border-radius: 10px;
      font-size: 1rem;
      transition: border-color 0.3s ease;
    }
    .form-group input:focus {
      outline: none;
      border-color: #667eea;
    }
    .password-strength {
      margin-top: 0.5rem;
      font-size: 0.85rem;
      font-weight: 500;
    }
    .password-strength .high { color: #10b981; }
    .password-strength .medium { color: #f59e0b; }
    .password-strength .low { color: #ef4444; }
    .btn-primary {
      width: 100%;
      padding: 1rem;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: white;
      border: none;
      border-radius: 10px;
      font-size: 1.1rem;
      font-weight: 600;
      cursor: pointer;
      transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .btn-primary:hover:not(:disabled) {
      transform: translateY(-2px);
      box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
    }
    .btn-primary:disabled {
      opacity: 0.6;
      cursor: not-allowed;
    }
    .divider {
      text-align: center;
      margin: 2rem 0;
      position: relative;
    }
    .divider span {
      background: white;
      padding: 0 1rem;
      color: #666;
      position: relative;
      z-index: 1;
    }
    .divider::before {
      content: '';
      position: absolute;
      top: 50%;
      left: 0;
      right: 0;
      height: 1px;
      background: #e0e0e0;
    }
    .oauth-buttons {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 1rem;
    }
    .oauth-btn {
      padding: 0.8rem;
      border: 2px solid #e0e0e0;
      border-radius: 10px;
      background: white;
      font-weight: 500;
      cursor: pointer;
      transition: all 0.2s ease;
    }
    .oauth-btn:hover {
      transform: translateY(-2px);
    }
    .oauth-btn.github:hover { border-color: #333; background: #333; color: white; }
    .oauth-btn.gitlab:hover { border-color: #fc6d26; background: #fc6d26; color: white; }
    .oauth-btn.google:hover { border-color: #ea4335; background: #ea4335; color: white; }
    .oauth-btn.microsoft:hover { border-color: #00a4ef; background: #00a4ef; color: white; }
    .auth-footer {
      text-align: center;
      margin-top: 2rem;
      color: #666;
    }
    .auth-footer a {
      color: #667eea;
      font-weight: 600;
      text-decoration: none;
    }
  `]
})
export class LoginComponent {
    loginForm: FormGroup;
    passwordStrength: string = '';

    constructor(private fb: FormBuilder) {
        this.loginForm = this.fb.group({
            email: ['', [Validators.required, Validators.email]],
            password: ['', [Validators.required, Validators.minLength(16)]]
        });

        this.loginForm.get('password')?.valueChanges.subscribe(value => {
            this.checkPasswordStrength(value);
        });
    }

    checkPasswordStrength(password: string): void {
        if (!password) {
            this.passwordStrength = '';
            return;
        }

        const hasLower = /[a-z]/.test(password);
        const hasUpper = /[A-Z]/.test(password);
        const hasNumber = /[0-9]/.test(password);
        const hasSpecial = /[!@#$%^&*(),.?":{}|<>]/.test(password);
        const isLongEnough = password.length >= 16;

        const strength = [hasLower, hasUpper, hasNumber, hasSpecial, isLongEnough].filter(Boolean).length;

        if (strength >= 5) this.passwordStrength = 'high';
        else if (strength >= 3) this.passwordStrength = 'medium';
        else this.passwordStrength = 'low';
    }

    onSubmit(): void {
        if (this.loginForm.valid) {
            console.log('Login submitted:', this.loginForm.value);
        }
    }

    loginWithOAuth(provider: string): void {
        window.location.href = `/api/v1/auth/oauth/${provider}`;
    }
}
