"""
ARCH-COUNCIL — FastAPI Backend
Manages sessions, runs the full pipeline in the background,
exposes REST endpoints for the React frontend.
"""
import json
from datetime import datetime
from pathlib import Path
from typing import List

from fastapi import BackgroundTasks, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .council import chairman_synthesize, run_council_stage1, run_council_stage2
from .models import (
    Requirement,
    Session,
    SessionStatusResponse,
    SessionSummary,
    SubmitRequirementRequest,
)
from .ratchet import generate_final_report, run_ratchet_loop
from .rag import get_knowledge_base_stats
from .scorer import score_draft
from .config import RATCHET_MAX_ITERATIONS

# ─── App Setup ──────────────────────────────────────────────────────────────

app = FastAPI(
    title="ARCH-COUNCIL",
    description="Multi-agent AI Solutions Architecture system — TOGAF-aligned council + ratchet refinement loop",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SESSIONS_DIR = Path(__file__).parent.parent / "data" / "sessions"
SESSIONS_DIR.mkdir(parents=True, exist_ok=True)


# ─── Session Storage ─────────────────────────────────────────────────────────

def _save(session: Session):
    session.updated_at = datetime.utcnow()
    path = SESSIONS_DIR / f"{session.id}.json"
    path.write_text(session.model_dump_json(indent=2), encoding="utf-8")


def _load(session_id: str) -> Session:
    path = SESSIONS_DIR / f"{session_id}.json"
    if not path.exists():
        raise HTTPException(status_code=404, detail=f"Session {session_id} not found")
    content = path.read_text(encoding="utf-8")
    if not content.strip():
        raise HTTPException(status_code=503, detail="Session initializing, retry shortly")
    return Session.model_validate_json(content)


# ─── Pipeline ────────────────────────────────────────────────────────────────

async def _run_pipeline(session_id: str):
    """
    Full ARCH-COUNCIL pipeline — runs as a FastAPI background task.

    Stage 1: Parallel council opinions
    Stage 2: Anonymized cross-review
    Stage 3: Chairman synthesis → initial draft
    Stage 4: Ratchet loop (propose → apply → score → keep/revert)
    Stage 5: Final report generation
    """
    session = _load(session_id)

    try:
        req = session.requirement
        req_summary = req.as_summary()

        # ── Stage 1: Council First Opinions ──────────────────────────────────
        session.status = "stage1_council"
        _save(session)

        opinions = await run_council_stage1(req)
        session.council_opinions = opinions
        _save(session)

        # ── Stage 2: Cross-Review ─────────────────────────────────────────────
        session.status = "stage2_review"
        _save(session)

        reviews = await run_council_stage2(opinions)
        session.cross_reviews = reviews
        _save(session)

        # ── Stage 3: Chairman Synthesis ───────────────────────────────────────
        session.status = "stage3_synthesis"
        _save(session)

        initial_draft = await chairman_synthesize(req, opinions, reviews)
        session.initial_draft = initial_draft
        session.best_draft = initial_draft

        initial_score = await score_draft(initial_draft, req_summary)
        session.initial_score = initial_score
        session.best_score = initial_score
        _save(session)

        # ── Stage 4: Ratchet Loop ─────────────────────────────────────────────
        session.status = "stage4_ratchet"
        _save(session)

        async def on_iteration(iteration):
            """Save every ratchet iteration for live UI updates."""
            session.ratchet_iterations.append(iteration)
            if iteration.accepted:
                session.best_score.total = iteration.score_after
            _save(session)

        best_draft, best_score, all_iterations = await run_ratchet_loop(
            initial_draft=initial_draft,
            requirement_summary=req_summary,
            initial_score=initial_score,
            on_iteration=on_iteration,
            max_iterations=RATCHET_MAX_ITERATIONS,
        )
        session.best_draft = best_draft
        session.best_score = best_score
        _save(session)

        # ── Stage 5: Final Report ─────────────────────────────────────────────
        session.status = "stage5_finalizing"
        _save(session)

        final_report = await generate_final_report(best_draft, all_iterations, req_summary)
        session.final_report = final_report
        session.status = "complete"
        _save(session)

    except Exception as e:
        session.status = f"error: {str(e)[:300]}"
        _save(session)
        raise


# ─── API Routes ──────────────────────────────────────────────────────────────

@app.get("/api/health")
async def health():
    """Health check + knowledge base status."""
    kb_stats = get_knowledge_base_stats()
    return {
        "status": "ok",
        "knowledge_base": kb_stats,
    }


@app.post("/api/sessions", response_model=dict)
async def create_session(body: SubmitRequirementRequest, background_tasks: BackgroundTasks):
    """
    Submit a client requirement and kick off the full ARCH-COUNCIL pipeline.
    The pipeline runs in the background — poll /api/sessions/{id}/status for progress.
    """
    requirement = Requirement(
        client_context=body.client_context,
        pain_points=body.pain_points,
        constraints=body.constraints,
        industry=body.industry,
        existing_systems=body.existing_systems,
    )
    session = Session(requirement=requirement, status="queued")
    _save(session)

    background_tasks.add_task(_run_pipeline, session.id)

    return {"session_id": session.id, "status": "queued"}


@app.get("/api/sessions/{session_id}/status", response_model=SessionStatusResponse)
async def get_status(session_id: str):
    """Lightweight polling endpoint — call every 3-5 seconds for live updates."""
    s = _load(session_id)
    return SessionStatusResponse(
        session_id=s.id,
        status=s.status,
        council_opinions_count=len(s.council_opinions),
        cross_reviews_count=len(s.cross_reviews),
        ratchet_iterations=len(s.ratchet_iterations),
        best_score=s.best_score.total if s.best_score else None,
        final_report_ready=s.final_report is not None,
    )


@app.get("/api/sessions/{session_id}")
async def get_session(session_id: str):
    """Full session data — used to render council opinions, ratchet log, and final report."""
    return _load(session_id)


@app.get("/api/sessions/{session_id}/report")
async def get_report(session_id: str):
    """Return just the final report markdown."""
    s = _load(session_id)
    if not s.final_report:
        raise HTTPException(status_code=404, detail="Final report not yet generated")
    return {"report": s.final_report, "score": s.best_score}


@app.get("/api/sessions", response_model=List[SessionSummary])
async def list_sessions():
    """List all sessions (newest first)."""
    sessions = []
    for path in sorted(SESSIONS_DIR.glob("*.json"), key=lambda p: p.stat().st_mtime, reverse=True):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            sessions.append(
                SessionSummary(
                    id=data["id"],
                    status=data["status"],
                    industry=data.get("requirement", {}).get("industry", "Unknown"),
                    created_at=data["created_at"],
                    best_score=data.get("best_score", {}).get("total") if data.get("best_score") else None,
                )
            )
        except Exception:
            continue
    return sessions


@app.delete("/api/sessions/{session_id}")
async def delete_session(session_id: str):
    """Delete a session."""
    path = SESSIONS_DIR / f"{session_id}.json"
    if path.exists():
        path.unlink()
    return {"deleted": session_id}

