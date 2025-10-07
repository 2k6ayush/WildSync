# Start WildSync backend (Flask) on port 5000
param(
  [int]$Port = 5000
)

$ErrorActionPreference = 'Stop'

function Get-RepoRoot {
  param([string]$ScriptsPath)
  return (Split-Path -Parent $ScriptsPath)
}

$root = Get-RepoRoot -ScriptsPath $PSScriptRoot
Set-Location $root

# Create virtual environment if missing
if (-not (Test-Path "$root\.venv")) {
  Write-Host "Creating virtual environment (.venv)..." -ForegroundColor Yellow
  py -m venv .venv
}

# Activate venv
$activate = Join-Path $root ".venv\Scripts\Activate.ps1"
. $activate

# Install dependencies
Write-Host "Installing backend dependencies..." -ForegroundColor Yellow
pip install -r (Join-Path $root 'backend\requirements.txt')

# Ensure Flask environment
$env:FLASK_APP = 'backend.wsgi:app'
if (-not $env:FLASK_ENV) { $env:FLASK_ENV = 'development' }

# Run Flask
Write-Host "Starting backend on http://localhost:$Port ..." -ForegroundColor Green
flask run --port $Port
