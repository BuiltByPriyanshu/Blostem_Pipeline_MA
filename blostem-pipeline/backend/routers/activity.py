from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime, timedelta
from backend.db import get_connection

router = APIRouter(prefix="/api/activity", tags=["activity"])


class ActivityItem(BaseModel):
    id: int
    action_type: str
    description: str
    entity_name: str
    created_at: str


class ActivityFeedResponse(BaseModel):
    total: int
    limit: int
    offset: int
    items: list[ActivityItem]


class ActivityStats(BaseModel):
    total_actions: int
    actions_today: int
    emails_sent: int
    sequences_generated: int
    last_action: str | None


@router.get("/feed", response_model=ActivityFeedResponse)
def get_activity_feed(
    action_type: str | None = None,
    entity_name: str | None = None,
    search: str | None = None,
    limit: int = 50,
    offset: int = 0,
):
    """Get activity feed with optional filtering."""
    conn = get_connection()
    
    # Build query
    query = "SELECT * FROM activity_feed WHERE 1=1"
    params = []
    
    if action_type:
        query += " AND action_type = ?"
        params.append(action_type)
    
    if entity_name:
        query += " AND entity_name = ?"
        params.append(entity_name)
    
    if search:
        query += " AND (description LIKE ? OR entity_name LIKE ?)"
        search_term = f"%{search}%"
        params.extend([search_term, search_term])
    
    # Get total count
    count_query = query.replace("SELECT *", "SELECT COUNT(*)")
    total = conn.execute(count_query, params).fetchone()[0]
    
    # Get paginated results
    query += " ORDER BY created_at DESC LIMIT ? OFFSET ?"
    params.extend([limit, offset])
    
    rows = conn.execute(query, params).fetchall()
    conn.close()
    
    items = [
        ActivityItem(
            id=r["id"],
            action_type=r["action_type"],
            description=r["description"] or "",
            entity_name=r["entity_name"] or "",
            created_at=r["created_at"],
        )
        for r in rows
    ]
    
    return ActivityFeedResponse(
        total=total,
        limit=limit,
        offset=offset,
        items=items,
    )


@router.get("/stats", response_model=ActivityStats)
def get_activity_stats():
    """Get activity statistics."""
    conn = get_connection()
    
    # Total actions
    total = conn.execute("SELECT COUNT(*) FROM activity_feed").fetchone()[0]
    
    # Actions today
    today = datetime.now().strftime("%Y-%m-%d")
    actions_today = conn.execute(
        "SELECT COUNT(*) FROM activity_feed WHERE created_at LIKE ?",
        (f"{today}%",),
    ).fetchone()[0]
    
    # Emails sent
    emails_sent = conn.execute(
        "SELECT COUNT(*) FROM activity_feed WHERE action_type = ?",
        ("email_sent",),
    ).fetchone()[0]
    
    # Sequences generated
    sequences_generated = conn.execute(
        "SELECT COUNT(*) FROM activity_feed WHERE action_type = ?",
        ("sequence_generated",),
    ).fetchone()[0]
    
    # Last action
    last_action = conn.execute(
        "SELECT created_at FROM activity_feed ORDER BY created_at DESC LIMIT 1"
    ).fetchone()
    last_action_time = last_action[0] if last_action else None
    
    conn.close()
    
    return ActivityStats(
        total_actions=total,
        actions_today=actions_today,
        emails_sent=emails_sent,
        sequences_generated=sequences_generated,
        last_action=last_action_time,
    )
