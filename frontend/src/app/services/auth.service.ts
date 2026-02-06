import { Injectable, signal, computed } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { Observable, tap, catchError, of, map } from 'rxjs';
import { environment } from '../../environments/environment';

export interface User {
    id: string;
    email: string;
    full_name: string;
    role: string;
    is_active: boolean;
}

export interface AuthResponse {
    access: string;
    refresh: string;
    user: User;
}

@Injectable({
    providedIn: 'root'
})
export class AuthService {
    private readonly AUTH_URL = `${environment.apiUrl}/v1/identity`;
    private readonly MIDDLEWARE_URL = 'http://localhost:8400/api/v1/identity'; // FastAPI proxy

    // Signals for reactive state
    private _currentUser = signal<User | null>(null);
    private _isAuthenticated = signal<boolean>(false);
    private _isLoading = signal<boolean>(false);

    currentUser = computed(() => this._currentUser());
    isAuthenticated = computed(() => this._isAuthenticated());
    isLoading = computed(() => this._isLoading());

    constructor(
        private http: HttpClient,
        private router: Router
    ) {
        this.checkLocalStorage();
    }

    private checkLocalStorage(): void {
        const token = localStorage.getItem('access_token');
        const userData = localStorage.getItem('user_data');
        if (token && userData) {
            this._currentUser.set(JSON.parse(userData));
            this._isAuthenticated.set(true);
        }
    }

    login(credentials: any): Observable<AuthResponse> {
        this._isLoading.set(true);
        return this.http.post<AuthResponse>(`${this.AUTH_URL}/login/`, credentials).pipe(
            tap(response => this.handleAuthSuccess(response)),
            catchError(err => {
                this._isLoading.set(false);
                throw err;
            })
        );
    }

    register(userData: any): Observable<any> {
        this._isLoading.set(true);
        return this.http.post(`${this.AUTH_URL}/users/`, userData).pipe(
            tap(() => this._isLoading.set(false)),
            catchError(err => {
                this._isLoading.set(false);
                throw err;
            })
        );
    }

    loginWithSocial(provider: string): void {
        window.location.href = `${this.MIDDLEWARE_URL}/oauth/${provider}`;
    }

    handleOAuthCallback(tokenData: AuthResponse): void {
        this.handleAuthSuccess(tokenData);
        this.router.navigate(['/dashboard']);
    }

    private handleAuthSuccess(response: AuthResponse): void {
        localStorage.setItem('access_token', response.access);
        localStorage.setItem('refresh_token', response.refresh);
        localStorage.setItem('user_data', JSON.stringify(response.user));

        this._currentUser.set(response.user);
        this._isAuthenticated.set(true);
        this._isLoading.set(false);
    }

    logout(): void {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('user_data');
        this._currentUser.set(null);
        this._isAuthenticated.set(false);
        this.router.navigate(['/auth/login']);
    }

    refreshToken(): Observable<any> {
        const refresh = localStorage.getItem('refresh_token');
        if (!refresh) return of(null);

        return this.http.post(`${this.AUTH_URL}/token/refresh/`, { refresh }).pipe(
            tap((res: any) => localStorage.setItem('access_token', res.access))
        );
    }
}
