# Cross-Platform Support

## Supported Platforms

Observer-Eye supports deployment on the following platforms:

| Platform | Status | Notes |
|----------|--------|-------|
| **Linux** | ✅ Full Support | Recommended for production |
| **macOS** | ✅ Full Support | Development and production |
| **Windows** | ✅ Full Support | Via Docker Desktop or WSL2 |

## Deployment Options

### Docker (Recommended)
Works identically on all platforms with Docker installed.

```bash
docker-compose up -d
```

### Native Installation

#### Linux (Ubuntu/Debian)
```bash
# Install dependencies
sudo apt update
sudo apt install python3.12 nodejs npm postgresql redis

# Backend
cd backend/infra
pip install -r requirements.txt
python manage.py runserver 0.0.0.0:8000

# Middleware
cd middleware
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8400

# Frontend
cd frontend
npm install
ng serve --host 0.0.0.0 --port 80
```

#### macOS
```bash
# Install via Homebrew
brew install python@3.12 node postgresql redis

# Same commands as Linux
```

#### Windows (via WSL2)
1. Install WSL2 with Ubuntu
2. Follow Linux instructions within WSL2

## Browser Support

| Browser | Minimum Version |
|---------|-----------------|
| Chrome | 100+ |
| Firefox | 100+ |
| Safari | 15+ |
| Edge | 100+ |

## Hardware Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| CPU | 2 cores | 4+ cores |
| RAM | 4 GB | 8+ GB |
| Disk | 10 GB | 50+ GB |
