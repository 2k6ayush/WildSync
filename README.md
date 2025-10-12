# WildSync
AI-Powered Forest Management System - An intelligent platform that helps forest departments analyze ecosystem data and make data-driven conservation decisions. Upload forest data (tree counts, animal populations, soil quality, location details, past calamities) and get actionable insights through interactive heat maps and AI-generated recommendations for optimal resource allocation and wildlife protection

#Watch our WildSync demo and project pitch here:
https://youtu.be/6qApxHCXO2Y?si=kya8_j0vfhc0Qe5y

#Try WildSync live!
https://wildsync.mgx.world

## Architecture
🗂️ Architecture Diagrams & System Flow
Explore all project architecture diagrams and flowcharts here:
🔗 WildSync Architecture Diagrams

Contains detailed system flows, backend/frontend interactions, database schema, and API/data routing for WildSync.

Essential for understanding project structure and technical implementation.

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

---

## Production-like deployment with Docker

This repo includes a simple containerized stack for running the full application (frontend + backend + PostgreSQL) behind a single origin using nginx.

Prerequisites:
- Docker Desktop installed and running

Steps:
1. Copy environment template and set secrets
   ```powershell
   Copy-Item .env.example .env
   # Edit .env and set at least:
   # - POSTGRES_PASSWORD (required)
   # - FLASK_SECRET_KEY (required)
   # - DB_SEED=1 (optional, seeds admin user)
   # - OPENAI_API_KEY (optional, enables chatbot)
   ```

2. Build and start the stack
   ```powershell
   docker compose build
   docker compose up -d
   ```

3. Access the app
   - Frontend: http://localhost
   - Backend health: http://localhost:8000/api/health

4. First-run behavior
   - Backend starts with gunicorn on port 8000
   - DB_AUTOCREATE=1 creates tables on first run
   - If DB_SEED=1 is set in .env, the database is seeded with:
     - Email: admin@wildsync.local
     - Password: ChangeMe123!

5. Stopping and removing
   ```powershell
   docker compose down
   # Keep DB data:
   # docker compose down --volumes  # removes db data
   ```

Notes:
- nginx serves the static frontend and reverse proxies /api/* to the backend, so the browser sees a single origin (no CORS issues).
- Chatbot options:
  - OpenAI (paid): set OPENAI_API_KEY in .env.
  - Local (free): set OLLAMA_ENABLED=1 (and optionally OLLAMA_MODEL) to use a local model via the Ollama service in docker-compose.
- For HTTPS in production, place this stack behind a TLS terminator (e.g., a cloud load balancer) or extend nginx config with certificates.

### Local LLM via Ollama (free)
- Enabled by docker-compose service `ollama`.
- Configure in .env:
  - OLLAMA_ENABLED=1
  - OLLAMA_MODEL=mistral (default) or llama3.1:8b (more capable but heavier)
- First request may take longer if the model needs to be pulled.
