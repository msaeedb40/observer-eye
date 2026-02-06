import { Component, Input, forwardRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ControlValueAccessor, NG_VALUE_ACCESSOR, FormsModule } from '@angular/forms';

@Component({
    selector: 'app-form-input',
    standalone: true,
    imports: [CommonModule, FormsModule],
    providers: [
        {
            provide: NG_VALUE_ACCESSOR,
            useExisting: forwardRef(() => FormInputComponent),
            multi: true
        }
    ],
    template: `
    <div class="form-group mb-4">
      <label *ngIf="label" class="block text-[10px] font-black uppercase tracking-widest text-slate-500 mb-2 ml-1">
        {{ label }}
      </label>
      <div class="relative group">
        <input
          [type]="type"
          [placeholder]="placeholder"
          [disabled]="disabled"
          [(ngModel)]="value"
          (ngModelChange)="onValueChange($event)"
          (blur)="onTouched()"
          class="w-full bg-slate-900/50 border border-white/10 rounded-xl px-4 py-3 text-sm text-slate-200 placeholder:text-slate-600 focus:outline-none focus:border-sky-500/50 focus:ring-1 focus:ring-sky-500/20 transition-all card-hover-effect"
        />
        <div class="absolute inset-0 rounded-xl bg-gradient-to-r from-sky-500/5 to-indigo-500/5 opacity-0 group-hover:opacity-100 pointer-events-none transition-opacity"></div>
      </div>
    </div>
  `
})
export class FormInputComponent implements ControlValueAccessor {
    @Input() label: string = '';
    @Input() placeholder: string = '';
    @Input() type: string = 'text';

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
