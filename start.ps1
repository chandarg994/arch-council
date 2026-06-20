# ARCH-COUNCIL — Start Script (Windows PowerShell)
# Starts backend (FastAPI) and frontend (Vite) in separate windows.
# Usage: .\start.ps1

Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "  ARCH-COUNCIL — Starting..." -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# ── Check .env ───────────────────────────────────────────────────────────────
if (-not (Test-Path ".env")) {
    Write-Host "ERROR: .env not found. Run setup.ps1 first." -ForegroundColor Red
    exit 1
}
$envContent = Get-Content ".env" -Raw
if ($envContent -match "your-key-here") {
    Write-Host "ERROR: OPENROUTER_API_KEY still has placeholder value in .env" -ForegroundColor Red
    Write-Host "       Open .env and paste your real OpenRouter key." -ForegroundColor Red
    exit 1
}

# ── Get absolute path for this folder ────────────────────────────────────────
$rootDir = (Get-Location).Path

# ── Start Backend in a new window ────────────────────────────────────────────
Write-Host "Starting Backend  -> http://localhost:8000" -ForegroundColor Green
Start-Process powershell -ArgumentList @(
    "-NoExit",
    "-Command",
    "cd '$rootDir'; Write-Host 'ARCH-COUNCIL Backend' -ForegroundColor Cyan; python -m uvicorn backend.main:app --reload --port 8000"
)

# Brief pause so backend starts before frontend
Start-Sleep -Seconds 2

# ── Start Frontend in a new window ───────────────────────────────────────────
Write-Host "Starting Frontend -> http://localhost:5173" -ForegroundColor Green
Start-Process powershell -ArgumentList @(
    "-NoExit",
    "-Command",
    "cd '$rootDir\frontend'; Write-Host 'ARCH-COUNCIL Frontend' -ForegroundColor Cyan; npm run dev"
)

Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "  Both servers starting in new windows." -ForegroundColor Green
Write-Host "  Open: http://localhost:5173" -ForegroundColor White
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Close the two new PowerShell windows to stop the servers." -ForegroundColor Gray
Write-Host ""
