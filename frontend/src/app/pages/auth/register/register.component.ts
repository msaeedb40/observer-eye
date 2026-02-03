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
    <div class="observer-container flex items-center justify-center min-h-screen page-transition">
      <div class="glass-panel p-10 w-full max-w-lg relative overflow-hidden">
        <div class="absolute -bottom-24 -left-24 w-64 h-64 bg-indigo-500/10 rounded-full blur-3xl"></div>
        
        <div class="text-center mb-8 relative z-10">
          <div class="text-4xl mb-2">🔭</div>
          <h1 class="text-2xl font-bold text-white mb-1">Create Account</h1>
          <p class="text-slate-500 text-sm">Join the Observer-Eye observability network</p>
        </div>
        
        <form [formGroup]="registerForm" (ngSubmit)="onSubmit()" class="space-y-4 relative z-10">
          <div class="space-y-1">
            <label class="text-[10px] font-bold text-slate-500 uppercase tracking-widest">Display Name</label>
            <input type="text" formControlName="name" placeholder="John Doe" 
                   class="w-full bg-slate-900/50 border border-white/10 rounded-xl px-4 py-2.5 text-white focus:outline-none focus:border-sky-500/50 transition-colors text-sm" />
          </div>
          
          <div class="space-y-1">
            <label class="text-[10px] font-bold text-slate-500 uppercase tracking-widest">Email Address</label>
            <input type="email" formControlName="email" placeholder="john@company.com" 
                   class="w-full bg-slate-900/50 border border-white/10 rounded-xl px-4 py-2.5 text-white focus:outline-none focus:border-sky-500/50 transition-colors text-sm" />
          </div>
          
          <div class="space-y-1">
            <label class="text-[10px] font-bold text-slate-500 uppercase tracking-widest">Secure Password</label>
            <input type="password" formControlName="password" placeholder="••••••••••••••••"
                   class="w-full bg-slate-900/50 border border-white/10 rounded-xl px-4 py-2.5 text-white focus:outline-none focus:border-sky-500/50 transition-colors text-sm" />
            <div class="flex gap-2 pt-1">
              <span class="px-2 py-0.5 rounded-[4px] text-[8px] font-bold uppercase transition-colors"
                    [ngClass]="hasLowercase ? 'bg-emerald-500/20 text-emerald-400' : 'bg-white/5 text-slate-600'">abc</span>
              <span class="px-2 py-0.5 rounded-[4px] text-[8px] font-bold uppercase transition-colors"
                    [ngClass]="hasUppercase ? 'bg-emerald-500/20 text-emerald-400' : 'bg-white/5 text-slate-600'">ABC</span>
              <span class="px-2 py-0.5 rounded-[4px] text-[8px] font-bold uppercase transition-colors"
                    [ngClass]="hasNumber ? 'bg-emerald-500/20 text-emerald-400' : 'bg-white/5 text-slate-600'">123</span>
              <span class="px-2 py-0.5 rounded-[4px] text-[8px] font-bold uppercase transition-colors"
                    [ngClass]="hasSpecial ? 'bg-emerald-500/20 text-emerald-400' : 'bg-white/5 text-slate-600'">!#$</span>
              <span class="px-2 py-0.5 rounded-[4px] text-[8px] font-bold uppercase transition-colors"
                    [ngClass]="hasMinLength ? 'bg-emerald-500/20 text-emerald-400' : 'bg-white/5 text-slate-600'">16+</span>
            </div>
          </div>
          
          <div class="space-y-1">
            <label class="text-[10px] font-bold text-slate-500 uppercase tracking-widest">Confirm Password</label>
            <input type="password" formControlName="confirmPassword" placeholder="••••••••••••••••"
                   class="w-full bg-slate-900/50 border border-white/10 rounded-xl px-4 py-2.5 text-white focus:outline-none focus:border-sky-500/50 transition-colors text-sm" />
          </div>
          
          <div class="pt-4">
            <button type="submit" class="btn-premium w-full py-3" [disabled]="!registerForm.valid">
              Provision Account
            </button>
          </div>
        </form>
        
        <p class="mt-8 text-center text-xs text-slate-500 relative z-10">
          Already have an account? <a routerLink="/auth/login" class="text-sky-400 font-bold hover:underline">Sign In</a>
        </p>
      </div>
    </div>
  `,
  styles: [`
    :host { display: block; min-height: 100vh; background: #020617; }
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
      password: ['', [Validators.required, Validators.minLength(8), this.passwordValidator.bind(this)]],
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
    this.hasMinLength = (password || '').length >= 16;
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
