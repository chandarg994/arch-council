"""
ARCH-COUNCIL Data Models
Pydantic models for all data flowing through the system.
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import datetime
import uuid


class Requirement(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    client_context: str
    pain_points: str
    constraints: str
    industry: str
    existing_systems: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    def as_summary(self) -> str:
        return (
            f"Industry: {self.industry}\n"
            f"Client Context: {self.client_context}\n"
            f"Pain Points: {self.pain_points}\n"
            f"Constraints: {self.constraints}\n"
            f"Existing Systems: {self.existing_systems}"
        )


class CouncilOpinion(BaseModel):
    agent_id: str
    agent_name: str
    togaf_domain: str
    opinion: str
    model_used: str = ""


class CrossReview(BaseModel):
    reviewer_id: str
    reviewer_name: str
    scores: Dict[str, float] = {}   # "Response A" -> score
    feedback: str = ""
    gaps_identified: List[str] = []
    conflicts_identified: List[str] = []


class ArchitecturalScore(BaseModel):
    togaf_compliance: float = 0.0       # 0-25
    technical_feasibility: float = 0.0  # 0-25
    business_alignment: float = 0.0     # 0-25
    risk_governance: float = 0.0        # 0-25
    total: float = 0.0                  # 0-100
    reasoning: str = ""


class RatchetIteration(BaseModel):
    iteration: int
    proposing_agent: str
    proposing_agent_name: str
    proposed_improvement: str
    score_before: float
    score_after: float
    delta: float
    accepted: bool
    reasoning: str


class Session(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    requirement: Optional[Requirement] = None
    status: str = "pending"
    # Stage 1
    council_opinions: List[CouncilOpinion] = []
    # Stage 2
    cross_reviews: List[CrossReview] = []
    # Chairman synthesis
    initial_draft: Optional[str] = None
    initial_score: Optional[ArchitecturalScore] = None
    # Ratchet
    ratchet_iterations: List[RatchetIteration] = []
    best_draft: Optional[str] = None
    best_score: Optional[ArchitecturalScore] = None
    # Final
    final_report: Optional[str] = None
    # Meta
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


# ─── API Request/Response Models ────────────────────────────────────────────

class SubmitRequirementRequest(BaseModel):
    client_context: str = Field(..., min_length=20, description="What the client does and their current situation")
    pain_points: str = Field(..., min_length=10, description="Specific problems to solve")
    constraints: str = Field(..., description="Budget, time, technology, regulatory constraints")
    industry: str = Field(..., description="Client industry vertical")
    existing_systems: str = Field(..., description="Current tech stack and systems in place")


class SessionStatusResponse(BaseModel):
    session_id: str
    status: str
    council_opinions_count: int
    cross_reviews_count: int
    ratchet_iterations: int
    best_score: Optional[float]
    final_report_ready: bool


class SessionSummary(BaseModel):
    id: str
    status: str
    industry: str
    created_at: datetime
    best_score: Optional[float]
