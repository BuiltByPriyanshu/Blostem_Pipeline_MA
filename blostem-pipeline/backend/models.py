from pydantic import BaseModel
from typing import Optional


class StakeholderOut(BaseModel):
    id: int
    name: str
    role: str
    angle: str
    initials: str
    email: Optional[str] = None


class SignalOut(BaseModel):
    signal_type: str  # 'hiring' | 'news' | 'activity'
    description: str
    detected_at: str


class ProspectOut(BaseModel):
    id: int
    name: str
    hq_city: str
    industry: str
    stage: str
    funding_label: str
    score: int
    compliance: str  # 'passed' | 'review' | 'pending'
    seq_ready: bool
    stakeholders: list[StakeholderOut]
    signals: list[SignalOut]
    last_news: Optional[str] = None


class StallSignal(BaseModel):
    status: str        # 'active' | 'stalled' | 'critical' | 'new'
    days_silent: int
    reason: str
    recommendation: str


class MilestoneOut(BaseModel):
    label: str
    done: bool


class PartnerOut(BaseModel):
    id: int
    name: str
    contact_name: str
    contact_role: str
    signed_at: str
    activation_pct: int
    status: str
    days_silent: int
    stall_reason: Optional[str] = None
    recommendation: Optional[str] = None
    api_call_trend: list[int]   # 7 values, oldest first
    milestones: list[dict]      # {label: str, done: bool}
    last_event: str


class SequenceOut(BaseModel):
    id: int
    prospect_id: int
    persona: str
    email_1: str
    email_2: str
    email_3: str
    compliance: str
    generated_at: str


class ComplianceFlag(BaseModel):
    phrase: str
    severity: str


class ComplianceResult(BaseModel):
    passed: bool
    flags: list[dict]
    email_with_disclaimer: str


class GenerateSequenceRequest(BaseModel):
    prospect_id: int
    persona: str


class ScoreResponse(BaseModel):
    prospect_id: int
    score: int
    tier: str


class ReengagementOut(BaseModel):
    email: str
    status: str
    generated_at: str


class CreateProspectRequest(BaseModel):
    name: str
    hq_city: str
    industry: str
    stage: str
    funding_usd: int
    funding_label: str
    last_news: Optional[str] = None


class CreateProspectResponse(BaseModel):
    id: int
    name: str
    message: str
