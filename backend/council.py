"""
ARCH-COUNCIL — Council Pipeline
Stage 1: Parallel first opinions from 6 specialized architect agents
Stage 2: Anonymized cross-review
Stage 3: Chairman synthesis into initial draft
"""
import asyncio
import json
import re
from typing import List

import httpx

from .config import (
    COUNCIL_MEMBERS,
    CHAIRMAN_MODEL,
    CHAIRMAN_SYSTEM_PROMPT,
    OPENROUTER_API_KEY,
    OPENROUTER_BASE_URL,
)
from .models import CouncilOpinion, CrossReview, Requirement
from .rag import retrieve_context

try:
    from headroom import compress as _hr_compress
    _HEADROOM_AVAILABLE = True
except ImportError:
    _HEADROOM_AVAILABLE = False

def _compress(text):
    if not _HEADROOM_AVAILABLE or not text or len(text) < 300:
        return text
    try:
        return _hr_compress(text)
    except Exception:
        return text


# ─── LLM Call ───────────────────────────────────────────────────────────────

async def call_llm(model: str, system_prompt: str, user_message: str, temperature: float = 0.7) -> str:
    """Single async LLM call via OpenRouter."""
    if not OPENROUTER_API_KEY:
        raise ValueError(
            "OPENROUTER_API_KEY not set. Copy .env.example to .env and add your key."
        )

    async with httpx.AsyncClient(timeout=180.0) as client:
        response = await client.post(
            f"{OPENROUTER_BASE_URL}/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "HTTP-Referer": "https://arch-council.local",
                "X-Title": "ARCH-COUNCIL",
            },
            json={
                "model": model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message},
                ],
                "temperature": temperature,
            },
        )
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]


# ─── Stage 1: First Opinions ─────────────────────────────────────────────────

async def _get_one_opinion(member, requirement: Requirement, context: str) -> CouncilOpinion:
    """One council member's independent architectural assessment."""
    prompt = f"""## Client Requirement

**Industry:** {requirement.industry}

**Client Context:**
{requirement.client_context}

**Pain Points:**
{requirement.pain_points}

**Constraints:**
{requirement.constraints}

**Existing Systems:**
{requirement.existing_systems}

---

## Relevant Architecture Knowledge
{context}

---

## Your Task
As the **{member.name}** ({member.togaf_domain}), provide your domain-specific architectural assessment.

Structure your response exactly as follows:

### 1. Domain Analysis
[What you observe from your domain perspective — current state, gaps, risks]

### 2. Recommended Architecture Components
[Specific components, patterns, technologies for this domain]

### 3. TOGAF Artifacts to Produce
[Which ADM artifacts should be created, with brief description of content]

### 4. Key Architecture Decisions & Trade-offs
[2-3 critical decisions specific to your domain with reasoning]

### 5. Integration Dependencies
[What you need from other architecture domains to complete your design]

### 6. Architecture Diagram
Include a Mermaid diagram showing your domain's key components and flows.
Use a ```mermaid code block (flowchart TD or LR, or erDiagram for Data Architect).
Keep it to 8-18 nodes with clear labels. No more than 3 subgraph levels.
"""
    opinion_text = await call_llm(member.model, member.system_prompt, prompt)
    return CouncilOpinion(
        agent_id=member.id,
        agent_name=member.name,
        togaf_domain=member.togaf_domain,
        opinion=opinion_text,
        model_used=member.model,
    )


async def run_council_stage1(requirement: Requirement) -> List[CouncilOpinion]:
    """
    Stage 1: All 6 council members analyze the requirement in PARALLEL.
    Each member gets: requirement + RAG-retrieved context relevant to their domain.
    """
    async def get_opinion_with_context(member):
        # Build a domain-aware query for RAG
        domain_query = f"{requirement.pain_points} {requirement.industry} {member.togaf_domain}"
        context = retrieve_context(domain_query, n_results=6)
        return await _get_one_opinion(member, requirement, context)

    opinions = await asyncio.gather(
        *[get_opinion_with_context(m) for m in COUNCIL_MEMBERS],
        return_exceptions=False
    )
    return list(opinions)


# ─── Stage 2: Cross-Review (Anonymized) ─────────────────────────────────────

def _anonymize_opinions(opinions: List[CouncilOpinion]) -> dict:
    """Map opinions to anonymous labels (Response A, B, C...) to prevent bias."""
    return {
        f"Response {chr(65 + i)}": _compress(op.opinion)
        for i, op in enumerate(opinions)
    }


async def _one_cross_review(member, others: dict) -> CrossReview:
    """One member reviews all other members' proposals (anonymized)."""
    responses_block = "\n\n".join(
        f"### {label}\n{text}" for label, text in others.items()
    )

    prompt = f"""You are reviewing architectural proposals from your peers (identities hidden to prevent bias).

## Anonymized Proposals
{responses_block}

---

## Your Task
Review each proposal from your domain expertise ({member.togaf_domain}). Evaluate:
- Completeness and quality of the architectural thinking
- Gaps that could affect enterprise architecture success
- Conflicts or contradictions between proposals that need resolution

Respond ONLY with valid JSON in this exact format:
{{
    "scores": {{"Response A": 7.5, "Response B": 8.0, "Response C": 6.0}},
    "feedback": "Your overall assessment of the proposals as a set",
    "gaps": [
        "Gap or missing element #1",
        "Gap or missing element #2"
    ],
    "conflicts": [
        "Conflict between proposals that needs resolution #1"
    ]
}}

Scores are 0-10. Return ONLY the JSON, no other text."""

    review_text = await call_llm(member.model, member.system_prompt, prompt, temperature=0.3)

    # Parse JSON — be resilient to LLM adding markdown fences
    try:
        json_match = re.search(r'\{.*\}', review_text, re.DOTALL)
        if json_match:
            data = json.loads(json_match.group())
        else:
            data = {}
    except (json.JSONDecodeError, AttributeError):
        data = {}

    return CrossReview(
        reviewer_id=member.id,
        reviewer_name=member.name,
        scores=data.get("scores", {}),
        feedback=data.get("feedback", review_text[:500]),
        gaps_identified=data.get("gaps", []),
        conflicts_identified=data.get("conflicts", []),
    )


async def run_council_stage2(opinions: List[CouncilOpinion]) -> List[CrossReview]:
    """
    Stage 2: Each member reviews all OTHER members' proposals (anonymized).
    Identifies gaps and conflicts across the architectural domains.
    """
    anonymized = _anonymize_opinions(opinions)

    async def review_for_member(i, member):
        # Give each member all responses EXCEPT their own (also anonymized, so they don't know which is theirs)
        others = {k: v for j, (k, v) in enumerate(anonymized.items()) if j != i}
        return await _one_cross_review(member, others)

    reviews = await asyncio.gather(
        *[review_for_member(i, m) for i, m in enumerate(COUNCIL_MEMBERS)],
        return_exceptions=False
    )
    return list(reviews)


# ─── Stage 3: Chairman Synthesis ─────────────────────────────────────────────

async def chairman_synthesize(
    requirement: Requirement,
    opinions: List[CouncilOpinion],
    reviews: List[CrossReview],
) -> str:
    """
    Chairman receives all opinions and cross-review findings,
    synthesizes them into a single coherent initial architectural draft.
    """
    opinions_block = "\n\n".join(
        f"### {op.agent_name} ({op.togaf_domain})\n{_compress(op.opinion)}"
        for op in opinions
    )

    all_gaps = []
    all_conflicts = []
    for r in reviews:
        all_gaps.extend(r.gaps_identified)
        all_conflicts.extend(r.conflicts_identified)

    # Deduplicate
    unique_gaps = list(dict.fromkeys(all_gaps))[:12]
    unique_conflicts = list(dict.fromkeys(all_conflicts))[:8]

    gaps_text = "\n".join(f"- {g}" for g in unique_gaps) or "None identified."
    conflicts_text = "\n".join(f"- {c}" for c in unique_conflicts) or "None identified."

    prompt = f"""## Client Requirement

**Industry:** {requirement.industry}
**Context:** {requirement.client_context}
**Pain Points:** {requirement.pain_points}
**Constraints:** {requirement.constraints}
**Existing Systems:** {requirement.existing_systems}

---

## Domain Expert Opinions

{opinions_block}

---

## Cross-Review Findings

**Identified Gaps:**
{gaps_text}

**Identified Conflicts:**
{conflicts_text}

---

## Your Task — Initial Architectural Draft

As Chairman, synthesize all domain perspectives into a unified initial architectural draft.
Resolve conflicts. Fill gaps where you have enough context. Flag remaining open questions.

Use this exact structure:

# AI Solution Architecture — Draft v0
## Prepared by ARCH-COUNCIL

## Executive Summary
[3-5 sentences: what problem, what solution, what value]

## Business Architecture (TOGAF Phase B)
### Business Capability Assessment
### Target Operating Model
### Value Stream Design

## Data Architecture (TOGAF Phase C — Data)
### Data Landscape & Gaps
### AI/ML Data Pipeline
### Data Governance Requirements

## Application Architecture (TOGAF Phase C — Application)
### Solution Components
### AI/LLM Integration Pattern (specify which pattern and why)
### Integration Architecture

## Technology Architecture (TOGAF Phase D)
### Cloud Infrastructure Design
### MLOps Platform Selection
### Security & Compliance Architecture

## AI/ML Architecture
### Recommended AI Pattern & Justification
### Model Selection
### Evaluation Framework

## Risk Register
| Risk | Severity | Likelihood | Mitigation |
|------|----------|------------|------------|

## Implementation Roadmap
### Phase 1 (0-3 months): Foundation
### Phase 2 (3-6 months): Core Delivery
### Phase 3 (6-12 months): Scale & Optimize

## Open Questions & Assumptions
"""

    return await call_llm(CHAIRMAN_MODEL, CHAIRMAN_SYSTEM_PROMPT, prompt)


