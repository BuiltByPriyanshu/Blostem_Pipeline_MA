from datetime import datetime, timedelta
from backend.models import StallSignal

MILESTONE_ORDER = [
    "sandbox_access",
    "first_api_call",
    "fd_product_configured",
    "go_live_approved",
    "first_live_transaction",
]

MILESTONE_WEIGHTS = {
    "sandbox_access": 10,
    "first_api_call": 20,
    "fd_product_configured": 25,
    "go_live_approved": 20,
    "first_live_transaction": 25,
}

MILESTONE_LABELS = {
    "sandbox_access": "Sandbox access",
    "first_api_call": "First API call",
    "fd_product_configured": "FD product configured",
    "go_live_approved": "Go-live approved",
    "first_live_transaction": "First live transaction",
}

STALL_REASONS = {
    None: "Partner never made first API call. Likely blocked at sandbox setup.",
    "sandbox_access": "Stalled after sandbox access. Possible integration confusion.",
    "first_api_call": "Made initial calls but went quiet. May be stuck on FD product config.",
    "fd_product_configured": "Product configured but no go-live. Likely awaiting compliance sign-off.",
    "go_live_approved": "Go-live approved but no transactions. Blocked on frontend integration.",
    "first_live_transaction": "Live and transacting. Monitor for volume drop-off.",
}

RECOMMENDATIONS = {
    None: "Send sandbox setup guide and offer a 30-minute onboarding call.",
    "sandbox_access": "Share integration quickstart doc and offer a technical walkthrough.",
    "first_api_call": "Send FD product configuration guide and schedule a product demo.",
    "fd_product_configured": "Connect partner with Blostem compliance team for sign-off.",
    "go_live_approved": "Offer frontend integration support and share sample code snippets.",
    "first_live_transaction": "Schedule a quarterly business review to discuss volume growth.",
}


def _infer_stall_reason(last_milestone: str | None, days_silent: int) -> str:
    return STALL_REASONS.get(last_milestone, "Unknown stall point. Manual review recommended.")


def _get_recommendation(last_milestone: str | None) -> str:
    return RECOMMENDATIONS.get(last_milestone, "Reach out to understand current blockers.")


def _get_last_milestone(activity_log: list[dict]) -> str | None:
    """Return the most recent milestone event (not api_call)."""
    milestone_events = [
        a for a in activity_log if a["event_type"] in MILESTONE_ORDER
    ]
    if not milestone_events:
        return None
    # Sort by timestamp descending
    milestone_events.sort(key=lambda x: x["timestamp"], reverse=True)
    return milestone_events[0]["event_type"]


def _get_days_silent(activity_log: list[dict], signed_at: str) -> int:
    """Days since last any activity."""
    if not activity_log:
        try:
            signed_dt = datetime.fromisoformat(signed_at)
            return (datetime.now() - signed_dt).days
        except (ValueError, TypeError):
            return 0

    latest = max(activity_log, key=lambda x: x["timestamp"])
    try:
        latest_dt = datetime.fromisoformat(latest["timestamp"])
        return (datetime.now() - latest_dt).days
    except (ValueError, TypeError):
        return 0


def detect_stall(partner: dict, activity_log: list[dict]) -> StallSignal:
    signed_at = partner.get("signed_at", "")
    try:
        signed_dt = datetime.fromisoformat(signed_at)
        days_since_signing = (datetime.now() - signed_dt).days
    except (ValueError, TypeError):
        days_since_signing = 999

    days_silent = _get_days_silent(activity_log, signed_at)
    last_milestone = _get_last_milestone(activity_log)

    # Grace period: < 3 days since signing
    if days_since_signing < 3:
        return StallSignal(
            status="new",
            days_silent=days_silent,
            reason="Partner recently signed. In grace period.",
            recommendation="Send welcome email with sandbox credentials and quickstart guide.",
        )

    if days_silent >= 14:
        status = "critical"
    elif days_silent >= 7:
        status = "stalled"
    else:
        status = "active"

    reason = _infer_stall_reason(last_milestone, days_silent)
    recommendation = _get_recommendation(last_milestone)

    return StallSignal(
        status=status,
        days_silent=days_silent,
        reason=reason,
        recommendation=recommendation,
    )


def calculate_activation_score(activity_log: list[dict]) -> int:
    completed = {a["event_type"] for a in activity_log}
    total = 0
    for milestone, weight in MILESTONE_WEIGHTS.items():
        if milestone in completed:
            total += weight
    return min(total, 100)


def get_weekly_trend(activity_log: list[dict]) -> list[int]:
    """Returns 7 integers: api_call counts per day, oldest first (index 0 = 7 days ago)."""
    counts = [0] * 7
    now = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

    for entry in activity_log:
        if entry["event_type"] != "api_call":
            continue
        try:
            ts = datetime.fromisoformat(entry["timestamp"])
            ts_day = ts.replace(hour=0, minute=0, second=0, microsecond=0)
            delta = (now - ts_day).days
            if 0 <= delta <= 6:
                counts[6 - delta] += 1
        except (ValueError, TypeError):
            continue

    return counts


def get_milestones(activity_log: list[dict]) -> list[dict]:
    completed = {a["event_type"] for a in activity_log}
    return [
        {"label": MILESTONE_LABELS[m], "done": m in completed}
        for m in MILESTONE_ORDER
    ]
