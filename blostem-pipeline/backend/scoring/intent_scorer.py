from datetime import datetime


HIRING_KEYWORDS = ["payments", "banking", "api", "fintech", "partnerships"]

HIGH_FIT_INDUSTRIES = {"neobank", "lending", "wealthtech", "insurtech", "payments"}

SERIES_AB_STAGES = {"series a", "series b"}


def calculate_intent_score(prospect: dict) -> int:
    score = 0

    # --- Funding recency (max 25 pts) ---
    stage = (prospect.get("stage") or "").lower()
    if stage in SERIES_AB_STAGES:
        score += 20

    scraped_at = prospect.get("scraped_at")
    if scraped_at:
        try:
            scraped_dt = datetime.fromisoformat(scraped_at)
            days_since = (datetime.now() - scraped_dt).days
            if days_since < 180:
                score += 5
        except (ValueError, TypeError):
            pass

    # --- Hiring signals (max 25 pts) ---
    signals = prospect.get("signals", [])
    hiring_pts = 0
    for sig in signals:
        if sig.get("signal_type") == "hiring":
            desc = (sig.get("description") or "").lower()
            for kw in HIRING_KEYWORDS:
                if kw in desc:
                    hiring_pts += 8
                    break  # one match per signal
    score += min(hiring_pts, 25)

    # --- Industry fit (max 25 pts) ---
    industry = (prospect.get("industry") or "").lower()
    if industry in HIGH_FIT_INDUSTRIES:
        score += 25
    elif "fintech" in industry:
        score += 15
    else:
        score += 5

    # --- News momentum (max 25 pts) ---
    news_pts = 0
    for sig in signals:
        if sig.get("signal_type") in ("news", "activity"):
            news_pts += 5
    score += min(news_pts, 25)

    return min(score, 100)


def get_score_tier(score: int) -> str:
    if score >= 80:
        return "hot"
    if score >= 60:
        return "warm"
    return "cold"
