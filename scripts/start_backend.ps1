# Start WildSync backend (Flask) on port 5000
param(
  [int]$Port = 5000
)

$ErrorActionPreference = 'Stop'

function Get-RepoRoot {
  param([string]$ScriptsPath)
  return (Split-Path -Parent $ScriptsPath)
}

function Invoke-Python {
  param([string[]]$PyArgs)
  $pyCmd = Get-Command python -ErrorAction SilentlyContinue
  if ($pyCmd) {
    & python @PyArgs
    return
  }
  $pyLauncher = Get-Command py -ErrorAction SilentlyContinue
  if ($pyLauncher) {
    & py -3 @PyArgs
    return
  }
  throw "Python not found. Install Python 3 and ensure it is on PATH."
}

$root = Get-RepoRoot -ScriptsPath $PSScriptRoot
Set-Location $root

# Create virtual environment if missing
$venvPath = Join-Path $root ".venv"
$venvPython = Join-Path $venvPath "Scripts\python.exe"
$venvBroken = $false
if (Test-Path $venvPython) {
  $prevErrorAction = $ErrorActionPreference
  $ErrorActionPreference = 'Continue'
  & $venvPython -V 2>$null | Out-Null
  $exitCode = $LASTEXITCODE
  $ErrorActionPreference = $prevErrorAction
  if ($exitCode -ne 0) { $venvBroken = $true }
} else {
  $venvBroken = $true
}

if ((-not (Test-Path $venvPath)) -or $venvBroken) {
  if (Test-Path $venvPath) {
    Write-Host "Removing broken virtual environment (.venv)..." -ForegroundColor Yellow
    Remove-Item -Recurse -Force $venvPath
  }
  Write-Host "Creating virtual environment (.venv)..." -ForegroundColor Yellow
  Invoke-Python -PyArgs @('-m', 'venv', '.venv')
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
