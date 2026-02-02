import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, Router } from '@angular/router';

@Component({
    selector: 'app-oauth-callback',
    standalone: true,
    imports: [CommonModule],
    template: `
    <div class="oauth-callback">
      <div class="loading-spinner"></div>
      <p>Authenticating with {{ provider }}...</p>
    </div>
  `,
    styles: [`
    .oauth-callback { min-height: 100vh; display: flex; flex-direction: column; align-items: center; justify-content: center; background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); color: white; }
    .loading-spinner { width: 50px; height: 50px; border: 4px solid rgba(255,255,255,0.3); border-top-color: white; border-radius: 50%; animation: spin 1s linear infinite; margin-bottom: 1rem; }
    @keyframes spin { to { transform: rotate(360deg); } }
  `]
})
export class OAuthCallbackComponent implements OnInit {
    provider = '';

    constructor(private route: ActivatedRoute, private router: Router) { }

    ngOnInit(): void {
        this.provider = this.route.snapshot.params['provider'];
        // Handle OAuth callback
        setTimeout(() => {
            this.router.navigate(['/dashboard']);
        }, 2000);
    }
}
