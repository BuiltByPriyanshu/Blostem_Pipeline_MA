from fastapi import APIRouter, HTTPException
from backend.db import get_all_partners, get_partner_by_id
from backend.models import PartnerOut, ReengagementOut
from backend.activation.tracker import (
    detect_stall,
    calculate_activation_score,
    get_weekly_trend,
    get_milestones,
)
from backend.langchain_core.reengagement import generate_reengagement_email

router = APIRouter(prefix="/api/activation", tags=["activation"])

STATUS_ORDER = {"critical": 0, "stalled": 1, "new": 2, "active": 3}


def _build_partner_out(partner: dict) -> PartnerOut:
    activity_log = partner.get("activity_log", [])
    stall = detect_stall(partner, activity_log)
    activation_pct = calculate_activation_score(activity_log)
    trend = get_weekly_trend(activity_log)
    milestones = get_milestones(activity_log)

    last_event = partner.get("last_event") or "none"

    return PartnerOut(
        id=partner["id"],
        name=partner["name"],
        contact_name=partner["contact_name"] or "",
        contact_role=partner["contact_role"] or "",
        signed_at=partner["signed_at"],
        activation_pct=activation_pct,
        status=stall.status,
        days_silent=stall.days_silent,
        stall_reason=stall.reason if stall.status in ("stalled", "critical") else None,
        recommendation=stall.recommendation if stall.status in ("stalled", "critical") else None,
        api_call_trend=trend,
        milestones=[{"label": m["label"], "done": m["done"]} for m in milestones],
        last_event=last_event,
    )


@router.get("/pipeline", response_model=list[PartnerOut])
def get_activation_pipeline():
    partners = get_all_partners()
    result = [_build_partner_out(p) for p in partners]
    result.sort(key=lambda x: STATUS_ORDER.get(x.status, 99))
    return result


@router.get("/{partner_id}", response_model=PartnerOut)
def get_partner(partner_id: int):
    partner = get_partner_by_id(partner_id)
    if not partner:
        raise HTTPException(status_code=404, detail="Partner not found")
    return _build_partner_out(partner)


@router.post("/reengage/{partner_id}", response_model=ReengagementOut)
def reengage_partner(partner_id: int):
    partner = get_partner_by_id(partner_id)
    if not partner:
        raise HTTPException(status_code=404, detail="Partner not found")

    activity_log = partner.get("activity_log", [])
    stall = detect_stall(partner, activity_log)

    if stall.status not in ("stalled", "critical"):
        raise HTTPException(
            status_code=400,
            detail=f"Partner status is '{stall.status}'. Re-engagement only for stalled/critical partners.",
        )

    result = generate_reengagement_email(partner, stall)
    return ReengagementOut(**result)
