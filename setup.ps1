# ARCH-COUNCIL — One-Time Setup Script (Windows PowerShell)
# Run this ONCE before starting the project.
# Usage: .\setup.ps1

Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "  ARCH-COUNCIL Setup" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# ── 1. Check Python ──────────────────────────────────────────────────────────
Write-Host "[1/5] Checking Python..." -ForegroundColor Yellow
try {
    $pyVersion = python --version 2>&1
    Write-Host "      Found: $pyVersion" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Python not found." -ForegroundColor Red
    Write-Host "Install Python 3.10+ from https://www.python.org/downloads/" -ForegroundColor Red
    Write-Host "Make sure to check 'Add Python to PATH' during install." -ForegroundColor Red
    exit 1
}

# ── 2. Check Node.js ─────────────────────────────────────────────────────────
Write-Host "[2/5] Checking Node.js..." -ForegroundColor Yellow
try {
    $nodeVersion = node --version 2>&1
    Write-Host "      Found: Node $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Node.js not found." -ForegroundColor Red
    Write-Host "Install Node.js 18+ from https://nodejs.org" -ForegroundColor Red
    exit 1
}

# ── 3. Create Python virtual environment ─────────────────────────────────────
Write-Host "[3/5] Setting up Python virtual environment..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Write-Host "      venv already exists, skipping creation." -ForegroundColor Gray
} else {
    python -m venv venv
    Write-Host "      Created venv/" -ForegroundColor Green
}

# Activate venv
Write-Host "      Activating venv..." -ForegroundColor Gray
& ".\venv\Scripts\Activate.ps1"

# ── 4. Install Python packages ───────────────────────────────────────────────
Write-Host "[4/5] Installing Python packages (this may take 5-10 min first time)..." -ForegroundColor Yellow
Write-Host "      Installing core packages..." -ForegroundColor Gray
pip install --upgrade pip --quiet

# Install torch first (largest package, CPU version to keep it manageable)
Write-Host "      Installing PyTorch (CPU)..." -ForegroundColor Gray
pip install torch --index-url https://download.pytorch.org/whl/cpu --quiet

# Install remaining packages
Write-Host "      Installing remaining packages..." -ForegroundColor Gray
pip install -r requirements.txt --quiet

Write-Host "      Python packages installed." -ForegroundColor Green

# ── 5. Install frontend dependencies ─────────────────────────────────────────
Write-Host "[5/5] Installing frontend (Node) dependencies..." -ForegroundColor Yellow
Set-Location frontend
npm install --silent
Set-Location ..
Write-Host "      Frontend packages installed." -ForegroundColor Green

# ── 6. Check .env ────────────────────────────────────────────────────────────
Write-Host ""
Write-Host "Checking .env..." -ForegroundColor Yellow
if (-not (Test-Path ".env")) {
    Copy-Item ".env.example" ".env"
    Write-Host "WARNING: .env created from template." -ForegroundColor Red
    Write-Host "         Open .env and add your OPENROUTER_API_KEY before running start.ps1" -ForegroundColor Red
} else {
    $envContent = Get-Content ".env" -Raw
    if ($envContent -match "your-key-here") {
        Write-Host "WARNING: .env has placeholder key. Update OPENROUTER_API_KEY in .env" -ForegroundColor Red
    } else {
        Write-Host "         .env found with API key set." -ForegroundColor Green
    }
}

# ── 7. Populate knowledge base ───────────────────────────────────────────────
Write-Host ""
Write-Host "Populating knowledge base (TOGAF + AI architecture docs)..." -ForegroundColor Yellow
python -m knowledge.ingest
Write-Host ""

# ── Done ─────────────────────────────────────────────────────────────────────
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "  Setup Complete!" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next step: run  .\start.ps1  to launch ARCH-COUNCIL" -ForegroundColor White
Write-Host ""
