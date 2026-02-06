import { Component, Input, forwardRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ControlValueAccessor, NG_VALUE_ACCESSOR } from '@angular/forms';

@Component({
    selector: 'app-form-toggle',
    standalone: true,
    imports: [CommonModule],
    providers: [
        {
            provide: NG_VALUE_ACCESSOR,
            useExisting: forwardRef(() => FormToggleComponent),
            multi: true
        }
    ],
    template: `
    <div class="flex items-center justify-between mb-4 group cursor-pointer" (click)="toggle()">
      <div class="flex-1">
        <label *ngIf="label" class="block text-sm font-bold text-slate-200 mb-0.5">{{ label }}</label>
        <p *ngIf="description" class="text-[10px] text-slate-500 leading-tight">{{ description }}</p>
      </div>
      <div class="relative w-12 h-6 rounded-full transition-colors duration-300 ease-in-out border border-white/10"
           [ngClass]="checked ? 'bg-sky-500/20 border-sky-500/40' : 'bg-slate-900/50'">
        <div class="absolute top-1 left-1 w-4 h-4 rounded-full bg-white shadow-lg transition-transform duration-300 ease-in-out flex items-center justify-center overflow-hidden"
             [ngClass]="checked ? 'translate-x-6' : 'translate-x-0'">
             <div class="w-full h-full bg-gradient-to-br from-white to-slate-200" *ngIf="!checked"></div>
             <div class="w-full h-full bg-gradient-to-br from-sky-400 to-indigo-500" *ngIf="checked"></div>
        </div>
      </div>
    </div>
  `
})
export class FormToggleComponent implements ControlValueAccessor {
    @Input() label: string = '';
    @Input() description: string = '';

    checked: boolean = false;
    disabled: boolean = false;

    onChange = (value: any) => { };
    onTouched = () => { };

    writeValue(value: any): void {
        this.checked = value;
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

    toggle(): void {
        if (this.disabled) return;
        this.checked = !this.checked;
        this.onChange(this.checked);
        this.onTouched();
    }
}
