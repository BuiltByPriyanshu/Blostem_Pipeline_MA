import os
import requests
from datetime import datetime
from backend.db import get_connection
import uuid

RESEND_API_KEY = os.getenv("RESEND_API_KEY")
RESEND_FROM = os.getenv("RESEND_FROM_EMAIL", "pipeline@blostem.dev")


def send_email(to: str, subject: str, body: str) -> dict:
    """Send email via Resend API (or demo mode if API key not set)."""
    
    # Demo mode - if no API key, simulate successful send
    if not RESEND_API_KEY:
        # Generate a fake Resend ID for demo purposes
        demo_resend_id = f"demo_{uuid.uuid4().hex[:12]}"
        
        # Log to email_sends table
        conn = get_connection()
        conn.execute(
            """INSERT INTO email_sends(to_email, subject, body_snippet, resend_id, success, sent_at)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (to, subject, body[:200], demo_resend_id, 1, datetime.now().isoformat()),
        )
        conn.commit()
        conn.close()
        
        return {
            "sent": True,
            "resend_id": demo_resend_id,
            "to": to,
            "status_code": 200,
            "mode": "demo"
        }

    try:
        response = requests.post(
            "https://api.resend.com/emails",
            headers={
                "Authorization": f"Bearer {RESEND_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "from": RESEND_FROM,
                "to": [to],
                "subject": subject,
                "text": body,
            },
            timeout=10,
        )

        success = response.status_code == 200
        resend_id = response.json().get("id") if success else None

        # Log to email_sends table
        conn = get_connection()
        conn.execute(
            """INSERT INTO email_sends(to_email, subject, body_snippet, resend_id, success, sent_at)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (to, subject, body[:200], resend_id, int(success), datetime.now().isoformat()),
        )
        conn.commit()
        conn.close()

        return {
            "sent": success,
            "resend_id": resend_id,
            "to": to,
            "status_code": response.status_code,
        }
    except Exception as e:
        # Log error
        conn = get_connection()
        conn.execute(
            """INSERT INTO email_sends(to_email, subject, body_snippet, resend_id, success, sent_at)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (to, subject, body[:200], None, 0, datetime.now().isoformat()),
        )
        conn.commit()
        conn.close()
        raise ValueError(f"Failed to send email: {str(e)}")
