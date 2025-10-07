# WildSync
AI-Powered Forest Management System - An intelligent platform that helps forest departments analyze ecosystem data and make data-driven conservation decisions. Upload forest data (tree counts, animal populations, soil quality, location details, past calamities) and get actionable insights through interactive heat maps and AI-generated recommendations for optimal resource allocation and wildlife protection

## Quick Start (Windows PowerShell)

Prerequisites:
- Python 3 installed (py/python available)
- PowerShell 5+ (this repo is configured for Windows)

Recommended folder: D:\\code_space\\WildSync\\WildSync

### 1) Start the backend

From the repo root:

```powershell
# In D:\\code_space\\WildSync\\WildSync
scripts\\start_backend.ps1 -Port 5000
```

This will:
- Create a virtual env (.venv) if missing
- Install backend requirements
- Start Flask at http://localhost:5000

### 2) Start the frontend

Open a new terminal:

```powershell
# In D:\\code_space\\WildSync\\WildSync
# Option A: Use default API base http://localhost:5000/api
scripts\\start_frontend.ps1 -Port 8080

# Option B: Override API base dynamically
scripts\\start_frontend.ps1 -Port 8080 -ApiBase 'http://localhost:5001/api'
```

This will:
- Generate frontend\\static\\js\\config.js from .env or parameters
- Serve the frontend at http://localhost:8080

### API base via .env
Create a .env in repo root:

```
FRONTEND_API_BASE=http://localhost:5000/api
```

Then simply run:

```powershell
scripts\\start_frontend.ps1
```

The generator also respects API_BASE if FRONTEND_API_BASE is not set.

### Health check
- Backend: http://localhost:5000/api/health
- Frontend: http://localhost:8080/ (index.html)

### Notes
- For cross-origin dev (frontend 8080, backend 5000), CORS with credentials is enabled in the backend. Ensure Flask session cookie settings are compatible for your environment.
- Update frontend/static/js/config.js is not needed manually; the script regenerates it.
