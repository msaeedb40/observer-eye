import { Component, Input, forwardRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ControlValueAccessor, NG_VALUE_ACCESSOR, FormsModule } from '@angular/forms';

export interface SelectOption {
  label: string;
  value: any;
}

@Component({
  selector: 'app-form-select',
  standalone: true,
  imports: [CommonModule, FormsModule],
  providers: [
    {
      provide: NG_VALUE_ACCESSOR,
      useExisting: forwardRef(() => FormSelectComponent),
      multi: true
    }
  ],
  template: `
    <div class="form-group mb-4">
      <label *ngIf="label" class="block text-[10px] font-black uppercase tracking-widest text-slate-500 mb-2 ml-1">
        {{ label }}
      </label>
      <div class="relative group">
        <select
          [disabled]="disabled"
          [(ngModel)]="value"
          (change)="onValueChange(value)"
          (blur)="onTouched()"
          class="w-full bg-slate-900/50 border border-white/10 rounded-xl px-4 py-3 text-sm text-slate-200 focus:outline-none focus:border-sky-500/50 transition-all cursor-pointer appearance-none card-hover-effect"
        >
          <option value="" disabled selected>{{ placeholder || 'Select an option' }}</option>
          <option *ngFor="let opt of options" [value]="opt.value" class="bg-slate-900 text-slate-200">
            {{ opt.label }}
          </option>
        </select>
        <div class="absolute right-4 top-1/2 -translate-y-1/2 pointer-events-none text-slate-500">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="19 9l-7 7-7-7" />
          </svg>
        </div>
      </div>
    </div>
  `
})
export class FormSelectComponent implements ControlValueAccessor {
  @Input() label: string = '';
  @Input() placeholder: string = '';
  @Input() options: SelectOption[] = [];

  value: any = '';
  disabled = false;

  onChange = (value: any) => { };
  onTouched = () => { };

  writeValue(value: any): void {
    this.value = value;
  }

  registerOnChange(fn: any): void {
    this.onChange = fn;
  }

  registerOnTouched(fn: any): void {
    this.onTouched = fn;
  }

  setDisabledState(isDisabled: boolean): void {
    this.disabled = isDisabled;
  }

  onValueChange(value: any): void {
    this.value = value;
    this.onChange(value);
  }
}
