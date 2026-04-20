from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime
from backend.email_sender import send_email
from backend.db import get_connection, log_activity

router = APIRouter(prefix="/api/email", tags=["email"])


class SendRequest(BaseModel):
    sequence_id: int
    email_index: int  # 1, 2, or 3
    recipient_email: str
    prospect_name: str


class SendResponse(BaseModel):
    sent: bool
    resend_id: str | None
    message: str


class EmailHistoryItem(BaseModel):
    id: int
    to_email: str
    subject: str
    body_snippet: str
    prospect_name: str | None
    resend_id: str | None
    success: int
    sent_at: str


class EmailHistoryResponse(BaseModel):
    total: int
    limit: int
    offset: int
    items: list[EmailHistoryItem]


@router.post("/send", response_model=SendResponse)
def send_sequence_email(req: SendRequest):
    """Send a sequence email to a prospect."""
    # Validate email_index
    if req.email_index not in [1, 2, 3]:
        raise HTTPException(status_code=400, detail="email_index must be 1, 2, or 3")

    # Fetch the sequence from db
    conn = get_connection()
    row = conn.execute("SELECT * FROM sequences WHERE id = ?", (req.sequence_id,)).fetchone()
    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail="Sequence not found")

    # Get the email body
    email_map = {1: "email_1", 2: "email_2", 3: "email_3"}
    field = email_map[req.email_index]
    body = dict(row)[field]

    # Extract subject line — assume first line of email is "Subject: ..."
    lines = body.strip().split("\n")
    if lines[0].startswith("Subject:"):
        subject = lines[0].replace("Subject:", "").strip()
        email_body = "\n".join(lines[1:]).strip()
    else:
        subject = f"Partnership opportunity — Blostem x {req.prospect_name}"
        email_body = body

    # Send email
    try:
        result = send_email(to=req.recipient_email, subject=subject, body=email_body)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    # Write to activity feed
    conn = get_connection()
    conn.execute(
        """INSERT INTO activity_feed (action_type, description, entity_name, created_at)
           VALUES (?, ?, ?, ?)""",
        (
            "email_sent",
            f"Email {req.email_index} sent to {req.recipient_email}",
            req.prospect_name,
            datetime.now().isoformat(),
        ),
    )
    conn.commit()
    conn.close()

    # Also log via the log_activity function
    log_activity(
        action_type="email_sent",
        description=f"Email {req.email_index} sent to {req.recipient_email}",
        entity_name=req.prospect_name
    )

    return SendResponse(
        sent=result["sent"],
        resend_id=result.get("resend_id"),
        message="Email sent successfully" if result["sent"] else "Send failed — check Resend API key",
    )


@router.get("/sends")
def get_email_sends():
    """Get recent email sends."""
    conn = get_connection()
    rows = conn.execute("SELECT * FROM email_sends ORDER BY sent_at DESC LIMIT 50").fetchall()
    conn.close()
    return [dict(r) for r in rows]


@router.get("/history", response_model=EmailHistoryResponse)
def get_email_history(
    status: str | None = None,
    prospect_name: str | None = None,
    search: str | None = None,
    limit: int = 50,
    offset: int = 0,
    sort_by: str = "sent_at",
    sort_order: str = "desc",
):
    """Get email send history with filtering and pagination."""
    conn = get_connection()
    
    # Validate sort parameters
    valid_sort_fields = ["sent_at", "to_email", "subject", "success"]
    if sort_by not in valid_sort_fields:
        sort_by = "sent_at"
    
    valid_sort_orders = ["asc", "desc"]
    if sort_order.lower() not in valid_sort_orders:
        sort_order = "desc"
    
    # Build query
    query = "SELECT * FROM email_sends WHERE 1=1"
    params = []
    
    if status == "success":
        query += " AND success = 1"
    elif status == "failed":
        query += " AND success = 0"
    
    if prospect_name:
        # Note: We don't have prospect_name in email_sends table
        # This would require a JOIN with sequences and prospects
        # For now, we'll skip this filter
        pass
    
    if search:
        query += " AND (to_email LIKE ? OR subject LIKE ?)"
        search_term = f"%{search}%"
        params.extend([search_term, search_term])
    
    # Get total count
    count_query = query.replace("SELECT *", "SELECT COUNT(*)")
    total = conn.execute(count_query, params).fetchone()[0]
    
    # Get paginated results
    query += f" ORDER BY {sort_by} {sort_order.upper()} LIMIT ? OFFSET ?"
    params.extend([limit, offset])
    
    rows = conn.execute(query, params).fetchall()
    conn.close()
    
    items = [
        EmailHistoryItem(
            id=r["id"],
            to_email=r["to_email"],
            subject=r["subject"] or "",
            body_snippet=r["body_snippet"] or "",
            prospect_name=None,  # Would need JOIN to get this
            resend_id=r["resend_id"],
            success=r["success"],
            sent_at=r["sent_at"],
        )
        for r in rows
    ]
    
    return EmailHistoryResponse(
        total=total,
        limit=limit,
        offset=offset,
        items=items,
    )


@router.post("/retry/{email_id}", response_model=SendResponse)
def retry_email_send(email_id: int):
    """Retry sending a failed email."""
    conn = get_connection()
    row = conn.execute("SELECT * FROM email_sends WHERE id = ?", (email_id,)).fetchone()
    conn.close()
    
    if not row:
        raise HTTPException(status_code=404, detail="Email record not found")
    
    row_dict = dict(row)
    
    # Resend the email
    try:
        result = send_email(
            to=row_dict["to_email"],
            subject=row_dict["subject"] or "Partnership opportunity",
            body=row_dict["body_snippet"] or "",
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    return SendResponse(
        sent=result["sent"],
        resend_id=result.get("resend_id"),
        message="Email resent successfully" if result["sent"] else "Resend failed — check Resend API key",
    )
