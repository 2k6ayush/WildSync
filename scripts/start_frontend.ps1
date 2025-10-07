# Start WildSync frontend static server and generate config
param(
  [int]$Port = 8080,
  [string]$ApiBase
)

$ErrorActionPreference = 'Stop'

function Get-RepoRoot {
  param([string]$ScriptsPath)
  return (Split-Path -Parent $ScriptsPath)
}

$root = Get-RepoRoot -ScriptsPath $PSScriptRoot

# Generate frontend config (reads .env or uses -ApiBase)
Write-Host "Generating frontend config..." -ForegroundColor Yellow
& (Join-Path $root 'scripts\generate_frontend_config.ps1') -ApiBase:$ApiBase

# Start static server
$frontendDir = Join-Path $root 'frontend'
Set-Location $frontendDir
Write-Host "Serving frontend on http://localhost:$Port from $frontendDir" -ForegroundColor Green
python -m http.server $Port
