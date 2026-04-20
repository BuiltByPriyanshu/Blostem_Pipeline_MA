from fastapi import APIRouter, HTTPException
from backend.db import get_all_prospects, get_prospect_by_id, update_prospect_score, create_prospect, log_activity
from backend.models import ProspectOut, StakeholderOut, SignalOut, ScoreResponse, CreateProspectRequest, CreateProspectResponse
from backend.scoring.intent_scorer import calculate_intent_score, get_score_tier

router = APIRouter(prefix="/api/prospects", tags=["prospects"])


def _build_prospect_out(row: dict) -> ProspectOut:
    stakeholders = [
        StakeholderOut(
            id=s["id"],
            name=s["name"] or "",
            role=s["role"] or "",
            angle=s["angle"] or "",
            initials=s["initials"] or "",
            email=s.get("email"),
        )
        for s in row.get("stakeholders", [])
    ]
    signals = [
        SignalOut(
            signal_type=s["signal_type"] or "activity",
            description=s["description"] or "",
            detected_at=s["detected_at"] or "",
        )
        for s in row.get("signals", [])
    ]
    return ProspectOut(
        id=row["id"],
        name=row["name"],
        hq_city=row["hq_city"] or "",
        industry=row["industry"] or "",
        stage=row["stage"] or "",
        funding_label=row["funding_label"] or "",
        score=row["score"] or 0,
        compliance=row["compliance"] or "pending",
        seq_ready=bool(row["seq_ready"]),
        stakeholders=stakeholders,
        signals=signals,
        last_news=row.get("last_news"),
    )


@router.get("/pipeline", response_model=list[ProspectOut])
def get_pipeline():
    rows = get_all_prospects()
    return [_build_prospect_out(r) for r in rows]


@router.get("/{prospect_id}", response_model=ProspectOut)
def get_prospect(prospect_id: int):
    row = get_prospect_by_id(prospect_id)
    if not row:
        raise HTTPException(status_code=404, detail="Prospect not found")
    return _build_prospect_out(row)


@router.post("/{prospect_id}/score", response_model=ScoreResponse)
def rescore_prospect(prospect_id: int):
    row = get_prospect_by_id(prospect_id)
    if not row:
        raise HTTPException(status_code=404, detail="Prospect not found")
    new_score = calculate_intent_score(row)
    update_prospect_score(prospect_id, new_score)
    
    # Log activity
    log_activity(
        action_type="prospect_rescored",
        description=f"Prospect rescored: {new_score} ({get_score_tier(new_score)})",
        entity_name=row.get("name", "Unknown")
    )
    
    return ScoreResponse(
        prospect_id=prospect_id,
        score=new_score,
        tier=get_score_tier(new_score),
    )


@router.post("/", response_model=CreateProspectResponse)
def create_new_prospect(req: CreateProspectRequest):
    """Create a new prospect."""
    try:
        prospect_id = create_prospect(
            name=req.name,
            hq_city=req.hq_city,
            industry=req.industry,
            stage=req.stage,
            funding_usd=req.funding_usd,
            funding_label=req.funding_label,
            last_news=req.last_news,
        )
        
        # Log activity
        log_activity(
            action_type="prospect_created",
            description=f"New prospect added: {req.name} ({req.industry}, {req.stage})",
            entity_name=req.name
        )
        
        return CreateProspectResponse(
            id=prospect_id,
            name=req.name,
            message=f"Prospect '{req.name}' created successfully",
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create prospect: {str(e)}")
