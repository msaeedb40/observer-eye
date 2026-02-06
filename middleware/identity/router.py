from fastapi import APIRouter, HTTPException, Request, Depends
from fastapi.responses import RedirectResponse
import httpx
import os
from typing import List, Dict, Any, Optional
from authlib.integrations.starlette_client import OAuth
from starlette.config import Config

router = APIRouter()

BACKEND_URL = os.environ.get("BACKEND_URL", "http://localhost:8000")
ALLOWED_DOMAINS = os.environ.get("ALLOWED_DOMAINS", "observer-eye.io").split(",")

# OAuth Configuration
config = Config(environ=os.environ)
oauth = OAuth(config)

oauth.register(
    name='google',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'}
)

oauth.register(
    name='github',
    client_id=os.environ.get('GITHUB_KEY'),
    client_secret=os.environ.get('GITHUB_SECRET'),
    access_token_url='https://github.com/login/oauth/access_token',
    authorize_url='https://github.com/login/oauth/authorize',
    api_base_url='https://api.github.com/',
    client_kwargs={'scope': 'user:email'}
)

oauth.register(
    name='gitlab',
    client_id=os.environ.get('GITLAB_KEY'),
    client_secret=os.environ.get('GITLAB_SECRET'),
    authorize_url='https://gitlab.com/oauth/authorize',
    access_token_url='https://gitlab.com/oauth/token',
    api_base_url='https://gitlab.com/api/v4/',
    client_kwargs={'scope': 'read_user'}
)

def validate_domain(email: str):
    """Restrict access to specific organization domains."""
    domain = email.split('@')[-1]
    if domain not in ALLOWED_DOMAINS and "*" not in ALLOWED_DOMAINS:
        raise HTTPException(status_code=403, detail=f"Domain {domain} not authorized for this platform")

@router.get("/oauth/{provider}")
async def login_via_oauth(provider: str, request: Request):
    """Initiate OAuth flow."""
    if provider not in ['google', 'github', 'gitlab']:
        raise HTTPException(status_code=400, detail="Unsupported provider")
    
    redirect_uri = request.url_for('auth_callback', provider=provider)
    return await oauth.create_client(provider).authorize_redirect(request, str(redirect_uri))

@router.get("/oauth/{provider}/callback", name="auth_callback")
async def auth_callback(provider: str, request: Request):
    """Handle OAuth callback and verify identity."""
    client = oauth.create_client(provider)
    token = await client.authorize_access_token(request)
    
    user_info = {}
    if provider == 'google':
        user_info = token.get('userinfo')
    elif provider == 'github':
        resp = await client.get('user', token=token)
        user_info = resp.json()
        # GitHub might hide email, get it separately if needed
        if not user_info.get('email'):
            emails = await client.get('user/emails', token=token)
            primary_email = next((e['email'] for e in emails.json() if e['primary']), None)
            user_info['email'] = primary_email
    elif provider == 'gitlab':
        resp = await client.get('user', token=token)
        user_info = resp.json()

    email = user_info.get('email')
    if not email:
        raise HTTPException(status_code=400, detail="Could not retrieve email from provider")
    
    # Apply Domain Restriction
    validate_domain(email)

    # Exchange for Backend JWT
    async with httpx.AsyncClient() as backend_client:
        resp = await backend_client.post(f"{BACKEND_URL}/api/v1/identity/social-login/", json={
            "provider": provider,
            "token": token.get('access_token'),
            "email": email,
            "full_name": user_info.get('name', user_info.get('login', email))
        })
        
        if resp.status_code != 200:
            raise HTTPException(status_code=resp.status_code, detail="Backend authentication failed")
        
        return resp.json()

@router.get("/metrics")
async def get_identity_metrics():
    """Get identity and authentication performance metrics from backend."""
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{BACKEND_URL}/api/v1/identity-perf/performance/")
            if resp.status_code != 200:
                return {
                    "avg_login_duration": 0.0,
                    "auth_success_rate": 0.0,
                    "active_sessions": 0,
                    "mfa_usage_percent": 0.0
                }
            return resp.json().get('results', resp.json())
    except Exception:
        return {"error": "identity metrics unavailable"}

@router.get("/sessions")
async def get_active_sessions():
    """Get active session details from backend."""
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{BACKEND_URL}/api/v1/identity/sessions/")
            if resp.status_code != 200:
                return {"sessions": []}
            return resp.json().get('results', resp.json())
    except Exception:
        return {"sessions": []}
