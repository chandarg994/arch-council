# 🏛️ ARCH-COUNCIL

**Multi-Agent AI Solutions Architecture System**
TOGAF-aligned council debate + autonomous ratchet refinement loop

Inspired by Karpathy's [llm-council](https://github.com/karpathy/llm-council) (multi-model debate) and [autoresearch](https://github.com/karpathy/autoresearch) (autonomous improvement ratchet).

---

## What it does

You submit a client requirement. A council of 6 specialized AI architect agents analyze it independently, cross-review each other's proposals, and a Chairman synthesizes a draft. Then an autonomous ratchet loop runs — proposing improvements, scoring them, keeping what works, reverting what doesn't — until you have a production-grade, TOGAF-aligned AI solution architecture.

---

## The Council

| Agent | Domain | Model |
|-------|--------|-------|
| Business Architect | TOGAF Phase B | Claude Sonnet |
| Data Architect | TOGAF Phase C (Data) | GPT-4o |
| Application Architect | TOGAF Phase C (App) | Gemini Flash |
| Technology Architect | TOGAF Phase D | Grok 3 |
| AI/ML Specialist | AI/ML Architecture | GPT-4o |
| Risk & Governance | Architecture Risk | Gemini Flash |
| **Chairman** | **Synthesis & Ratchet** | **Claude Opus** |

---

## Setup

### 1. Prerequisites

- Python 3.10+
- Node.js 18+
- [uv](https://docs.astral.sh/uv/) — `curl -LsSf https://astral.sh/uv/install.sh | sh`
- An [OpenRouter](https://openrouter.ai) API key (covers all models via one key)

### 2. Configure

```bash
cp .env.example .env
# Edit .env and add your OPENROUTER_API_KEY
```

### 3. Run

```bash
chmod +x start.sh
./start.sh
```

Then open http://localhost:5173

---

## First Run

The first time you run, the script will:
1. Install Python dependencies via `uv sync`
2. Populate the knowledge base: `python -m knowledge.ingest`
   - Embeds 12 seed documents (TOGAF ADM phases, AI patterns, MLOps, governance)
   - Stored in `data/chroma/` (local ChromaDB)
3. Install frontend dependencies via `npm install`
4. Start backend (port 8000) + frontend (port 5173)

---

## Usage

1. Click **+ New** in the top nav
2. Fill in the client requirement form (or click **Load Example**)
3. Click **Launch Architecture Council**
4. Watch the pipeline run in real-time:
   - **Stage 1** (5–10 min): 6 agents analyze in parallel
   - **Stage 2** (3–5 min): Cross-review (anonymized)
   - **Stage 3** (2–3 min): Chairman synthesizes initial draft
   - **Stage 4** (20–40 min): Ratchet loop refines the solution
   - **Stage 5** (2–3 min): Final report generation
5. Download the final architecture as Markdown

---

## Project Structure

```
arch-council/
├── backend/
│   ├── config.py       ← Council members, models, ratchet settings
│   ├── models.py       ← Pydantic data models
│   ├── rag.py          ← ChromaDB retrieval
│   ├── council.py      ← Stage 1 (opinions) + Stage 2 (reviews) + synthesis
│   ├── scorer.py       ← 4-dimension architectural scoring (0-100)
│   ├── ratchet.py      ← Autonomous improvement loop
│   └── main.py         ← FastAPI server + pipeline orchestration
├── knowledge/
│   ├── sources.py      ← TOGAF + AI architecture seed documents
│   └── ingest.py       ← Knowledge base ingestion script
├── frontend/
│   └── src/
│       ├── App.jsx
│       └── components/
│           ├── RequirementForm.jsx
│           ├── CouncilView.jsx     ← Tab view of all 6 agent opinions
│           ├── RatchetLog.jsx      ← Live ratchet iteration log + score chart
│           ├── FinalReport.jsx     ← Download final architecture doc
│           └── SessionList.jsx     ← Session history
├── data/
│   ├── chroma/         ← ChromaDB vector store (auto-created)
│   └── sessions/       ← Session JSON files (auto-created)
├── program.md          ← Human-editable research direction (edit this!)
├── .env                ← Your API keys
└── start.sh            ← Start everything
```

---

## Customisation

### Change which models the council uses

Edit `backend/config.py` or set env vars in `.env`:
```
COUNCIL_CHAIRMAN_MODEL=anthropic/claude-opus-4-5
COUNCIL_BUSINESS_MODEL=anthropic/claude-sonnet-4-5
COUNCIL_DATA_MODEL=openai/gpt-4o
```

### Change ratchet iteration count

```
RATCHET_MAX_ITERATIONS=30   # more iterations = better result, more cost
```

### Add your own domain knowledge

```bash
uv run python -m knowledge.ingest --add my_architecture_patterns.md --category "Custom Patterns" --source "Internal Playbook"
```

### Edit research direction

Edit `program.md` — this is your `program.md` equivalent from autoresearch. Change it to steer what the council prioritizes.

---

## Cost Estimate

Per session (20 ratchet iterations):
- Stage 1 (6 parallel calls): ~$0.10–0.30
- Stage 2 (6 review calls): ~$0.10–0.20
- Stage 3 (1 synthesis): ~$0.05–0.15
- Stage 4 (20 iterations × 3 calls each): ~$1.00–3.00
- Stage 5 (1 final report): ~$0.10–0.30
- **Total: ~$1.50–4.00 per session**

Reduce cost: lower `RATCHET_MAX_ITERATIONS` or use cheaper models (e.g. Gemini Flash for all council members).

---

## Tech Stack

- **Backend**: Python 3.10+, FastAPI, httpx (async), Pydantic v2
- **LLM Access**: OpenRouter (GPT-4o, Claude, Gemini, Grok via one API)
- **RAG**: ChromaDB + sentence-transformers (`all-MiniLM-L6-v2`, runs locally)
- **Frontend**: React 18 + Vite, react-markdown
- **Storage**: JSON files (sessions) + ChromaDB (knowledge)
- **Package Management**: uv (Python), npm (JS)

---

## License

MIT
