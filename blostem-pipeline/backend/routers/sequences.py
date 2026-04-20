from fastapi import APIRouter, HTTPException
from backend.db import get_prospect_by_id, get_sequences_for_prospect
from backend.models import SequenceOut, GenerateSequenceRequest
from backend.langchain_core.sequence_generator import generate_sequence

router = APIRouter(prefix="/api/sequences", tags=["sequences"])

VALID_PERSONAS = ["CTO", "CFO", "Head of Compliance", "Head of Product"]


@router.post("/generate", response_model=SequenceOut)
def generate_sequence_endpoint(body: GenerateSequenceRequest):
    prospect = get_prospect_by_id(body.prospect_id)
    if not prospect:
        raise HTTPException(status_code=404, detail="Prospect not found")

    if body.persona not in VALID_PERSONAS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid persona. Must be one of: {VALID_PERSONAS}",
        )

    result = generate_sequence(prospect, body.persona)
    return SequenceOut(**result)


@router.get("/{prospect_id}", response_model=list[SequenceOut])
def get_sequences(prospect_id: int):
    prospect = get_prospect_by_id(prospect_id)
    if not prospect:
        raise HTTPException(status_code=404, detail="Prospect not found")
    rows = get_sequences_for_prospect(prospect_id)
    return [SequenceOut(**r) for r in rows]
