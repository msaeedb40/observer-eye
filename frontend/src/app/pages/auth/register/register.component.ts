import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';
import { FormBuilder, FormGroup, Validators, AbstractControl, ValidationErrors } from '@angular/forms';

@Component({
    selector: 'app-register',
    standalone: true,
    imports: [CommonModule, FormsModule, ReactiveFormsModule, RouterModule],
    template: `
    <div class="auth-container">
      <div class="auth-card">
        <div class="auth-header">
          <h1>Observer-Eye</h1>
          <h2>Create Account</h2>
        </div>
        
        <form [formGroup]="registerForm" (ngSubmit)="onSubmit()">
          <div class="form-group">
            <label for="name">Full Name</label>
            <input type="text" id="name" formControlName="name" placeholder="Enter your name" />
          </div>
          
          <div class="form-group">
            <label for="email">Email</label>
            <input type="email" id="email" formControlName="email" placeholder="Enter your email" />
          </div>
          
          <div class="form-group">
            <label for="password">Password</label>
            <input type="password" id="password" formControlName="password" placeholder="Min 16 chars, mixed case, numbers, special" />
            <div class="password-requirements">
              <span [class.valid]="hasLowercase">lowercase</span>
              <span [class.valid]="hasUppercase">UPPERCASE</span>
              <span [class.valid]="hasNumber">123</span>
              <span [class.valid]="hasSpecial">!&#64;#</span>
              <span [class.valid]="hasMinLength">16+ chars</span>
            </div>
          </div>
          
          <div class="form-group">
            <label for="confirmPassword">Confirm Password</label>
            <input type="password" id="confirmPassword" formControlName="confirmPassword" placeholder="Confirm your password" />
          </div>
          
          <button type="submit" class="btn-primary" [disabled]="!registerForm.valid">
            Create Account
          </button>
        </form>
        
        <p class="auth-footer">
          Already have an account? <a routerLink="/auth/login">Sign In</a>
        </p>
      </div>
    </div>
  `,
    styles: [`
    .auth-container { min-height: 100vh; display: flex; align-items: center; justify-content: center; background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); padding: 2rem; }
    .auth-card { background: white; padding: 3rem; border-radius: 20px; box-shadow: 0 20px 60px rgba(0,0,0,0.3); width: 100%; max-width: 420px; }
    .auth-header { text-align: center; margin-bottom: 2rem; }
    .auth-header h1 { color: #667eea; font-size: 2rem; margin-bottom: 0.5rem; }
    .auth-header h2 { color: #333; font-size: 1.5rem; }
    .form-group { margin-bottom: 1.5rem; }
    .form-group label { display: block; margin-bottom: 0.5rem; color: #333; font-weight: 500; }
    .form-group input { width: 100%; padding: 1rem; border: 2px solid #e0e0e0; border-radius: 10px; font-size: 1rem; }
    .password-requirements { display: flex; flex-wrap: wrap; gap: 0.5rem; margin-top: 0.5rem; }
    .password-requirements span { font-size: 0.75rem; padding: 0.25rem 0.5rem; background: #fee2e2; color: #991b1b; border-radius: 4px; }
    .password-requirements span.valid { background: #d1fae5; color: #065f46; }
    .btn-primary { width: 100%; padding: 1rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none; border-radius: 10px; font-size: 1.1rem; font-weight: 600; cursor: pointer; }
    .btn-primary:disabled { opacity: 0.6; cursor: not-allowed; }
    .auth-footer { text-align: center; margin-top: 2rem; color: #666; }
    .auth-footer a { color: #667eea; font-weight: 600; text-decoration: none; }
  `]
})
export class RegisterComponent {
    registerForm: FormGroup;

    hasLowercase = false;
    hasUppercase = false;
    hasNumber = false;
    hasSpecial = false;
    hasMinLength = false;

    constructor(private fb: FormBuilder) {
        this.registerForm = this.fb.group({
            name: ['', [Validators.required]],
            email: ['', [Validators.required, Validators.email]],
            password: ['', [Validators.required, Validators.minLength(16), this.passwordValidator.bind(this)]],
            confirmPassword: ['', [Validators.required]]
        }, { validators: this.matchPasswords });

        this.registerForm.get('password')?.valueChanges.subscribe(value => {
            this.checkPassword(value);
        });
    }

    checkPassword(password: string): void {
        this.hasLowercase = /[a-z]/.test(password);
        this.hasUppercase = /[A-Z]/.test(password);
        this.hasNumber = /[0-9]/.test(password);
        this.hasSpecial = /[!@#$%^&*(),.?":{}|<>]/.test(password);
        this.hasMinLength = password.length >= 16;
    }

    passwordValidator(control: AbstractControl): ValidationErrors | null {
        const value = control.value;
        if (!value) return null;

        const hasAll = /[a-z]/.test(value) && /[A-Z]/.test(value) && /[0-9]/.test(value) && /[!@#$%^&*(),.?":{}|<>]/.test(value);
        return hasAll ? null : { passwordStrength: true };
    }

    matchPasswords(group: AbstractControl): ValidationErrors | null {
        const password = group.get('password')?.value;
        const confirm = group.get('confirmPassword')?.value;
        return password === confirm ? null : { passwordMismatch: true };
    }

    onSubmit(): void {
        if (this.registerForm.valid) {
            console.log('Register submitted:', this.registerForm.value);
        }
    }
}
