"""
ARCH-COUNCIL — Architectural Solution Scorer
Replaces autoresearch's val_bpb with a structured 4-dimension rubric.
Score range: 0–100. The ratchet keeps only iterations that improve this score.
"""
import json
import re

from .config import CHAIRMAN_MODEL, SCORING_RUBRIC
from .models import ArchitecturalScore

SCORER_SYSTEM_PROMPT = """You are an objective, strict architectural quality evaluator.
You score architectural solutions against a defined rubric.
Return ONLY valid JSON — no markdown, no explanation outside the JSON."""


async def score_draft(draft: str, requirement_summary: str) -> ArchitecturalScore:
    """
    Score an architectural draft on 4 dimensions (0–25 each, total 0–100).
    Used by the ratchet loop to decide keep vs revert.
    """
    from .council import call_llm

    rubric_desc = "\n".join(
        f"- **{k.replace('_', ' ').title()}** (0-{v['max']}): {v['description']}"
        for k, v in SCORING_RUBRIC.items()
    )

    prompt = f"""## Requirement Summary
{requirement_summary}

## Architectural Draft to Score
{draft[:6000]}{"...[truncated]" if len(draft) > 6000 else ""}

## Scoring Rubric
{rubric_desc}

Score this draft on each dimension. Be strict — a score of 20/25 means genuinely excellent work,
not just adequate. Deduct for: missing sections, vague recommendations, unjustified technology choices,
unaddressed risks, non-TOGAF-compliant structure, or feasibility gaps.

Return ONLY this JSON:
{{
    "togaf_compliance": <integer 0-25>,
    "technical_feasibility": <integer 0-25>,
    "business_alignment": <integer 0-25>,
    "risk_governance": <integer 0-25>,
    "total": <integer 0-100>,
    "reasoning": "<one sentence explaining the key strength and key weakness>"
}}"""

    response = await call_llm(CHAIRMAN_MODEL, SCORER_SYSTEM_PROMPT, prompt, temperature=0.1)

    try:
        json_match = re.search(r'\{.*\}', response, re.DOTALL)
        if json_match:
            data = json.loads(json_match.group())
            # Recalculate total from parts to prevent LLM arithmetic errors
            parts_sum = (
                float(data.get("togaf_compliance", 0))
                + float(data.get("technical_feasibility", 0))
                + float(data.get("business_alignment", 0))
                + float(data.get("risk_governance", 0))
            )
            return ArchitecturalScore(
                togaf_compliance=float(data.get("togaf_compliance", 0)),
                technical_feasibility=float(data.get("technical_feasibility", 0)),
                business_alignment=float(data.get("business_alignment", 0)),
                risk_governance=float(data.get("risk_governance", 0)),
                total=parts_sum,
                reasoning=data.get("reasoning", ""),
            )
    except (json.JSONDecodeError, ValueError, AttributeError):
        pass

    # Fallback: conservative baseline score
    return ArchitecturalScore(
        togaf_compliance=12,
        technical_feasibility=12,
        business_alignment=12,
        risk_governance=12,
        total=48,
        reasoning="Score parse failed — assigned conservative baseline.",
    )
