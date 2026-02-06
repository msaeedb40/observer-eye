import { Routes } from '@angular/router';

import { authGuard } from './guards/auth.guard';

/**
 * Observer-Eye Frontend Routes
 * Presentation Layer - Port 80
 */
export const routes: Routes = [
    // Default redirect
    {
        path: '',
        redirectTo: 'dashboard',
        pathMatch: 'full'
    },

    // Authentication routes
    {
        path: 'auth',
        children: [
            {
                path: 'login',
                loadComponent: () => import('./pages/auth/login/login.component').then(m => m.LoginComponent)
            },
            {
                path: 'register',
                loadComponent: () => import('./pages/auth/register/register.component').then(m => m.RegisterComponent)
            },
            {
                path: 'oauth/:provider',
                loadComponent: () => import('./pages/auth/oauth-callback/oauth-callback.component').then(m => m.OAuthCallbackComponent)
            }
        ]
    },

    // Main application routes (protected)
    {
        path: 'dashboard',
        canActivate: [authGuard],
        loadComponent: () => import('./pages/dashboard/dashboard.component').then(m => m.DashboardComponent)
    },

    // Observability pillars
    {
        path: 'metrics',
        canActivate: [authGuard],
        loadComponent: () => import('./pages/metrics/metrics.component').then(m => m.MetricsComponent)
    },
    {
        path: 'metrics/network',
        canActivate: [authGuard],
        loadComponent: () => import('./pages/network/network.component').then(m => m.NetworkComponent)
    },
    {
        path: 'metrics/system',
        canActivate: [authGuard],
        loadComponent: () => import('./pages/system/system.component').then(m => m.SystemComponent)
    },
    {
        path: 'metrics/security',
        canActivate: [authGuard],
        loadComponent: () => import('./pages/security/security.component').then(m => m.SecurityComponent)
    },
    {
        path: 'events',
        canActivate: [authGuard],
        loadComponent: () => import('./pages/events/events.component').then(m => m.EventsComponent)
    },
    {
        path: 'logs',
        canActivate: [authGuard],
        loadComponent: () => import('./pages/logs/logs.component').then(m => m.LogsComponent)
    },
    {
        path: 'traces',
        canActivate: [authGuard],
        loadComponent: () => import('./pages/traces/traces.component').then(m => m.TracesComponent)
    },
    {
        path: 'topology',
        canActivate: [authGuard],
        loadComponent: () => import('./pages/topology/topology.component').then(m => m.TopologyComponent)
    },

    // Performance Monitoring
    {
        path: 'apm',
        canActivate: [authGuard],
        loadComponent: () => import('./pages/apm/apm.component').then(m => m.ApmComponent)
    },

    // Alerts & Notifications
    {
        path: 'alerts',
        canActivate: [authGuard],
        loadComponent: () => import('./pages/alerts/alerts.component').then(m => m.AlertsComponent)
    },
    {
        path: 'alerts/manage',
        canActivate: [authGuard],
        loadComponent: () => import('./pages/alerts-manage/alerts-manage.component').then(m => m.AlertsManageComponent)
    },
    {
        path: 'integrations',
        canActivate: [authGuard],
        loadComponent: () => import('./pages/integrations/integrations.component').then(m => m.IntegrationsComponent)
    },
    {
        path: 'identity',
        canActivate: [authGuard],
        loadComponent: () => import('./pages/identity/identity.component').then(m => m.IdentityComponent)
    },
    {
        path: 'traffic',
        canActivate: [authGuard],
        loadComponent: () => import('./pages/traffic/traffic.component').then(m => m.TrafficComponent)
    },
    {
        path: 'cloud',
        canActivate: [authGuard],
        loadComponent: () => import('./pages/cloud/cloud.component').then(m => m.CloudComponent)
    },
    {
        path: 'kubernetes',
        canActivate: [authGuard],
        loadComponent: () => import('./pages/kubernetes/kubernetes.component').then(m => m.KubernetesComponent)
    },
    {
        path: 'slo',
        canActivate: [authGuard],
        loadComponent: () => import('./pages/slo/slo.component').then(m => m.SloComponent)
    },
    {
        path: 'incidents',
        canActivate: [authGuard],
        loadComponent: () => import('./pages/incidents/incidents.component').then(m => m.IncidentsComponent)
    },

    // Settings
    {
        path: 'settings',
        canActivate: [authGuard],
        loadComponent: () => import('./pages/settings/settings.component').then(m => m.SettingsComponent),
        children: [
            {
                path: 'general',
                loadComponent: () => import('./pages/settings/general/general.component').then(m => m.SettingsGeneralComponent)
            },
            {
                path: 'alerts',
                loadComponent: () => import('./pages/settings/alerts/alerts.component').then(m => m.SettingsAlertsComponent)
            },
            {
                path: 'integrations',
                loadComponent: () => import('./pages/settings/integrations/integrations.component').then(m => m.SettingsIntegrationsComponent)
            },
            {
                path: 'ai',
                loadComponent: () => import('./pages/settings/ai/ai.component').then(m => m.SettingsAIComponent)
            },
            {
                path: 'security',
                loadComponent: () => import('./pages/settings/security/security.component').then(m => m.SettingsSecurityComponent)
            },
            {
                path: 'billing',
                loadComponent: () => import('./pages/settings/billing/billing.component').then(m => m.SettingsBillingComponent)
            }
        ]
    },
    {
        path: 'insights',
        canActivate: [authGuard],
        loadComponent: () => import('./pages/insights/insights.component').then(m => m.InsightsComponent)
    },
    {
        path: 'reports',
        canActivate: [authGuard],
        loadComponent: () => import('./pages/reports/reports.component').then(m => m.ReportsComponent)
    },
    {
        path: 'explorer',
        canActivate: [authGuard],
        loadComponent: () => import('./pages/explorer/explorer.component').then(m => m.ExplorerComponent)
    },

    // 404
    {
        path: '**',
        loadComponent: () => import('./pages/not-found/not-found.component').then(m => m.NotFoundComponent)
    }
];
