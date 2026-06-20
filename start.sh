#!/bin/bash
# ARCH-COUNCIL — Start Script
# Runs backend (FastAPI) and frontend (Vite) concurrently

set -e

echo ""
echo "🏛️  ARCH-COUNCIL — Starting..."
echo "─────────────────────────────────────"

# Check .env
if [ ! -f ".env" ]; then
    echo "⚠️  .env not found. Copying from .env.example..."
    cp .env.example .env
    echo "📝 Edit .env and add your OPENROUTER_API_KEY, then re-run."
    exit 1
fi

# Check uv
if ! command -v uv &> /dev/null; then
    echo "❌ uv not found. Install with: curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

# Check node
if ! command -v node &> /dev/null; then
    echo "❌ Node.js not found. Install from: https://nodejs.org"
    exit 1
fi

# Install Python deps
echo "📦 Installing Python dependencies..."
uv sync --quiet

# Populate knowledge base (skip if already done)
echo "📚 Checking knowledge base..."
uv run python -m knowledge.ingest --stats 2>/dev/null || {
    echo "📚 Populating knowledge base (first run)..."
    uv run python -m knowledge.ingest
}

# Install frontend deps
echo "📦 Installing frontend dependencies..."
cd frontend && npm install --silent && cd ..

echo ""
echo "✅ Ready! Starting servers..."
echo "   Backend  → http://localhost:8000"
echo "   Frontend → http://localhost:5173"
echo "─────────────────────────────────────"
echo ""

# Start both concurrently
trap 'kill 0' EXIT

uv run python -m uvicorn backend.main:app --reload --port 8000 &
(cd frontend && npm run dev) &

wait
