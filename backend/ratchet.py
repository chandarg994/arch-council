"""
ARCH-COUNCIL — The Ratchet Loop
Borrowed from Karpathy's autoresearch: propose → apply → score → keep/revert. Repeat.
The architecture draft can ONLY improve. Never regresses.

Analogies:
- autoresearch's train.py     → our architectural draft (the thing being improved)
- autoresearch's val_bpb      → our ArchitecturalScore.total (the metric)
- autoresearch's AI agent     → our rotating council members (proposing improvements)
- autoresearch's git commit   → our iteration log (keeping what worked)
"""
import asyncio
from typing import Callable, Awaitable, List, Optional

from .config import COUNCIL_MEMBERS, CHAIRMAN_MODEL, CHAIRMAN_SYSTEM_PROMPT, RATCHET_MAX_ITERATIONS
from .models import RatchetIteration, ArchitecturalScore
from .council import call_llm
from .scorer import score_draft


# ─── Propose Improvement ─────────────────────────────────────────────────────

async def _propose_improvement(
    agent_index: int,
    current_draft: str,
    requirement_summary: str,
    iteration: int,
    previous_improvements: List[str],
) -> str:
    """
    A council member proposes ONE specific, targeted improvement to the current draft.
    Round-robins through agents each iteration.
    """
    member = COUNCIL_MEMBERS[agent_index % len(COUNCIL_MEMBERS)]

    history_note = ""
    if previous_improvements:
        recent = previous_improvements[-3:]
        history_note = f"\n\nRecent improvements already made (do NOT repeat these):\n" + "\n".join(
            f"- {imp}" for imp in recent
        )

    prompt = f"""## Your Role
You are the **{member.name}** ({member.togaf_domain}) acting as a reviewer in an architecture refinement loop.

## Current Best Architectural Draft (iteration {iteration})
{current_draft[:5000]}{"...[draft truncated for brevity]" if len(current_draft) > 5000 else ""}

## Client Requirement
{requirement_summary}
{history_note}

## Your Task
Propose exactly ONE focused improvement to this architectural draft from your domain perspective.

Rules:
- ONE improvement only — not a full rewrite
- Be specific about which section to improve and exactly what to add/change/strengthen
- The improvement must genuinely strengthen the solution quality
- Think: what is the single most important gap or weakness in THIS draft from my domain?

Format your response as:

**IMPROVEMENT:** [One sentence describing the specific change]

**SECTION AFFECTED:** [Which section of the document]

**REASONING:** [Why this improves the solution quality — what risk does it reduce or what gap does it fill?]

**REVISED CONTENT:**
[The exact new or updated content to insert/replace — be complete and specific]"""

    return await call_llm(member.model, member.system_prompt, prompt, temperature=0.8)


# ─── Apply Improvement ───────────────────────────────────────────────────────

async def _apply_improvement(current_draft: str, improvement_proposal: str) -> str:
    """
    Chairman integrates the proposed improvement into the current draft.
    Maintains document structure and resolves any conflicts with existing content.
    """
    prompt = f"""## Current Architectural Draft
{current_draft}

## Proposed Improvement
{improvement_proposal}

## Your Task
Integrate the proposed improvement into the draft cleanly.
- Maintain the existing document structure and section headings
- Resolve any conflicts between the new content and existing content
- Ensure the result is coherent and reads as a unified document
- Do NOT remove content that isn't being replaced
- If the proposal adds a new section or subsection, add it in the right place

Return the COMPLETE updated architectural draft (all sections)."""

    return await call_llm(CHAIRMAN_MODEL, CHAIRMAN_SYSTEM_PROMPT, prompt, temperature=0.3)


# ─── Ratchet Loop ────────────────────────────────────────────────────────────

async def run_ratchet_loop(
    initial_draft: str,
    requirement_summary: str,
    initial_score: ArchitecturalScore,
    on_iteration: Optional[Callable[[RatchetIteration], Awaitable[None]]] = None,
    max_iterations: int = RATCHET_MAX_ITERATIONS,
) -> tuple[str, ArchitecturalScore, List[RatchetIteration]]:
    """
    The ratchet: propose → apply → score → keep/revert.

    Args:
        initial_draft: The chairman's initial synthesis
        requirement_summary: Client requirement text
        initial_score: Score of the initial draft
        on_iteration: Async callback called after each iteration (for live UI updates)
        max_iterations: How many improvement attempts to run

    Returns:
        (best_draft, best_score, all_iterations)
    """
    current_draft = initial_draft
    current_score = initial_score
    iterations: List[RatchetIteration] = []
    improvement_history: List[str] = []

    for i in range(max_iterations):
        agent_index = i % len(COUNCIL_MEMBERS)
        agent = COUNCIL_MEMBERS[agent_index]

        try:
            # 1. Propose improvement
            proposal = await _propose_improvement(
                agent_index, current_draft, requirement_summary, i + 1, improvement_history
            )

            # 2. Apply it
            new_draft = await _apply_improvement(current_draft, proposal)

            # 3. Score
            new_score = await score_draft(new_draft, requirement_summary)

            # 4. Keep or revert
            delta = new_score.total - current_score.total
            accepted = delta > 0

            # Extract one-line improvement summary for history
            imp_summary = proposal.split("\n")[0].replace("**IMPROVEMENT:**", "").strip()[:120]

            iteration = RatchetIteration(
                iteration=i + 1,
                proposing_agent=agent.id,
                proposing_agent_name=agent.name,
                proposed_improvement=imp_summary,
                score_before=current_score.total,
                score_after=new_score.total,
                delta=delta,
                accepted=accepted,
                reasoning=new_score.reasoning,
            )
            iterations.append(iteration)

            if accepted:
                current_draft = new_draft
                current_score = new_score
                improvement_history.append(imp_summary)

            # Notify callback (for real-time UI updates)
            if on_iteration:
                await on_iteration(iteration)

            # Brief pause to avoid rate limiting
            await asyncio.sleep(0.5)

        except Exception as e:
            # Log failure iteration and continue — never crash the loop
            fail_iter = RatchetIteration(
                iteration=i + 1,
                proposing_agent=agent.id,
                proposing_agent_name=agent.name,
                proposed_improvement=f"[ERROR: {str(e)[:100]}]",
                score_before=current_score.total,
                score_after=current_score.total,
                delta=0.0,
                accepted=False,
                reasoning=f"Iteration failed: {str(e)[:200]}",
            )
            iterations.append(fail_iter)
            if on_iteration:
                await on_iteration(fail_iter)
            await asyncio.sleep(2)

    return current_draft, current_score, iterations


# ─── Final Report ────────────────────────────────────────────────────────────

async def generate_final_report(
    best_draft: str,
    iterations: List[RatchetIteration],
    requirement_summary: str,
) -> str:
    """
    Generate the polished final deliverable from the best draft.
    This is the client-ready document.
    """
    accepted_count = sum(1 for it in iterations if it.accepted)
    total_count = len(iterations)
    final_score = iterations[-1].score_after if iterations else 0

    accepted_improvements = [
        it.proposed_improvement for it in iterations if it.accepted
    ]
    improvements_text = "\n".join(
        f"{i+1}. {imp}" for i, imp in enumerate(accepted_improvements)
    ) or "Initial synthesis only."

    prompt = f"""## Optimized Architectural Draft
{best_draft}

## Council Process Summary
- Council members: 6 specialized TOGAF/AI architects
- Ratchet iterations run: {total_count}
- Improvements accepted: {accepted_count}
- Final quality score: {final_score:.1f}/100

## Key Improvements Made Through Ratchet
{improvements_text}

## Client Requirement
{requirement_summary}

---

## Your Task
Produce the FINAL, polished, client-ready AI Solution Architecture document.
This is the deliverable. It must be complete, professional, and actionable.

Structure:

# AI Solution Architecture
### Prepared by ARCH-COUNCIL Multi-Agent Architecture Review System
### Date: [today]
### Quality Score: {final_score:.1f}/100 (after {total_count} refinement iterations)

---

## 1. Executive Summary
[4-6 sentences: problem, proposed AI solution, business value, key risks, recommended approach]

## 2. Business Architecture (TOGAF Phase B)
### 2.1 Business Capability Assessment
[Capability map with maturity and AI enhancement potential ratings]
### 2.2 Value Stream Analysis
[Current vs target state]
### 2.3 Target Operating Model
[How the organization operates post-AI implementation]

## 3. Data Architecture (TOGAF Phase C — Data)
### 3.1 Current Data Landscape
### 3.2 Target Data Architecture
### 3.3 AI/ML Data Pipeline Design
### 3.4 Data Governance & Quality Framework

## 4. Application Architecture (TOGAF Phase C — Application)
### 4.1 Solution Component Overview
### 4.2 AI/LLM Integration Pattern
[Name the pattern, explain why it was selected over alternatives]
### 4.3 API & Integration Design
### 4.4 User Experience Architecture

## 5. Technology Architecture (TOGAF Phase D)
### 5.1 Cloud Infrastructure Design
### 5.2 MLOps Platform & Tooling
### 5.3 Security Architecture
### 5.4 Infrastructure Cost Estimate

## 6. AI/ML Architecture
### 6.1 AI Pattern Selection & Justification
### 6.2 Model Selection & Rationale
### 6.3 Prompt Strategy / Fine-tuning Plan
### 6.4 Evaluation Framework
### 6.5 AI Governance & Compliance

## 7. Risk Register
| # | Risk | Domain | Severity | Likelihood | Mitigation | Owner |
|---|------|--------|----------|------------|------------|-------|

## 8. Implementation Roadmap
### Phase 1 (0–3 months): Foundation
### Phase 2 (3–6 months): Core AI Solution
### Phase 3 (6–12 months): Scale & Optimise
### Success Metrics per Phase

## 9. Architecture Decision Records
[3-5 key ADRs for the most critical decisions made]

## 10. Assumptions, Constraints & Open Questions
"""

    return await call_llm(CHAIRMAN_MODEL, CHAIRMAN_SYSTEM_PROMPT, prompt, temperature=0.4)
