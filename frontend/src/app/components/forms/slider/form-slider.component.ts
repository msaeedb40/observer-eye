import { Component, Input, forwardRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ControlValueAccessor, NG_VALUE_ACCESSOR, FormsModule } from '@angular/forms';

@Component({
    selector: 'app-form-slider',
    standalone: true,
    imports: [CommonModule, FormsModule],
    providers: [
        {
            provide: NG_VALUE_ACCESSOR,
            useExisting: forwardRef(() => FormSliderComponent),
            multi: true
        }
    ],
    template: `
    <div class="form-group mb-6">
      <div class="flex justify-between items-center mb-4">
        <label *ngIf="label" class="text-[10px] font-black uppercase tracking-widest text-slate-500 ml-1">
          {{ label }}
        </label>
        <span class="text-xs font-mono font-bold text-sky-400 bg-sky-500/10 px-2 py-0.5 rounded border border-sky-500/20">
          {{ value }}{{ unit }}
        </span>
      </div>
      
      <div class="relative group h-6 flex items-center">
        <input
          type="range"
          [min]="min"
          [max]="max"
          [step]="step"
          [disabled]="disabled"
          [(ngModel)]="value"
          (ngModelChange)="onValueChange($event)"
          (blur)="onTouched()"
          class="w-full h-1.5 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-sky-500 focus:outline-none focus:ring-2 focus:ring-sky-500/20 transition-all"
        />
        
        <!-- Track Background with Gradient -->
        <div class="absolute left-0 top-1/2 -translate-y-1/2 h-1.5 rounded-lg bg-gradient-to-r from-sky-600 to-indigo-500 pointer-events-none"
             [style.width.%]="percentage"></div>
      </div>
      
      <div class="flex justify-between mt-2 px-1">
        <span class="text-[8px] font-black text-slate-600 uppercase tracking-tighter">{{ minLabel || min }}</span>
        <span class="text-[8px] font-black text-slate-600 uppercase tracking-tighter">{{ maxLabel || max }}</span>
      </div>
    </div>
  `,
    styles: [`
    input[type='range']::-webkit-slider-thumb {
      -webkit-appearance: none;
      appearance: none;
      width: 18px;
      height: 18px;
      background: white;
      border: 3px solid #0ea5e9;
      border-radius: 50%;
      cursor: pointer;
      box-shadow: 0 0 10px rgba(14, 165, 233, 0.5);
      transition: all 0.2s ease;
      position: relative;
      z-index: 10;
    }
    input[type='range']:hover::-webkit-slider-thumb {
      transform: scale(1.15);
      box-shadow: 0 0 15px rgba(14, 165, 233, 0.8);
    }
    input[type='range']::-moz-range-thumb {
      width: 12px;
      height: 12px;
      background: white;
      border: 3px solid #0ea5e9;
      border-radius: 50%;
      cursor: pointer;
    }
  `]
})
export class FormSliderComponent implements ControlValueAccessor {
    @Input() label: string = '';
    @Input() min: number = 0;
    @Input() max: number = 100;
    @Input() step: number = 1;
    @Input() unit: string = '';
    @Input() minLabel: string = '';
    @Input() maxLabel: string = '';

    value: number = 0;
    disabled = false;

    onChange = (value: any) => { };
    onTouched = () => { };

    get percentage(): number {
        return ((this.value - this.min) / (this.max - this.min)) * 100;
    }

    writeValue(value: any): void {
        this.value = value || 0;
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
