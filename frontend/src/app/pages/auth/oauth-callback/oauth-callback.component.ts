import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, Router } from '@angular/router';
import { AuthService } from '../../../services/auth.service';

@Component({
  selector: 'app-oauth-callback',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="observer-container flex items-center justify-center min-h-screen">
      <div class="text-center space-y-4">
        <div class="text-4xl animate-spin">👁️</div>
        <p class="text-slate-400 font-bold uppercase tracking-widest text-xs">Syncing Identity Matrix...</p>
      </div>
    </div>
  `
})
export class OAuthCallbackComponent implements OnInit {
  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private authService: AuthService
  ) { }

  ngOnInit(): void {
    const provider = this.route.snapshot.paramMap.get('provider');

    // In a real flow, the middleware redirects back here with the token data
    // For this implementation, we expect the middleware to redirect to this page 
    // with the JWT info in the query params or fragment, or we fetch it from the middleware session.

    this.route.queryParams.subscribe(params => {
      if (params['access'] && params['refresh']) {
        const authData = {
          access: params['access'],
          refresh: params['refresh'],
          user: JSON.parse(params['user'] || '{}')
        };
        this.authService.handleOAuthCallback(authData);
      } else {
        // Fallback for error or missing params
        console.error('OAuth sync failed');
        this.router.navigate(['/auth/login']);
      }
    });
  }
}
