import os
from backend.db import save_reengagement
from backend.models import StallSignal

# Demo re-engagement templates
STALLED_EMAIL_TEMPLATE = """Hi {name},

I noticed {company} has been quiet since {last_event}.

We're here to help unblock any integration questions. {recommendation}

Let's schedule a 20-minute call?

Best,
Blostem Team

{{unsubscribe_link}}"""

CRITICAL_EMAIL_TEMPLATE = """Hi {name},

{company} has been silent for {days_silent} days. We want to help.

{recommendation}

Can we schedule a call this week?

Best,
Blostem Team

{{unsubscribe_link}}"""


def generate_reengagement_email(partner: dict, stall: StallSignal) -> dict:
    if stall.status == "critical":
        template = CRITICAL_EMAIL_TEMPLATE
    else:
        template = STALLED_EMAIL_TEMPLATE

    try:
        email_text = template.format(
            name=partner.get("contact_name", "there"),
            company=partner.get("name", "your company"),
            last_event=partner.get("last_event", "sandbox access"),
            days_silent=stall.days_silent,
            recommendation=stall.recommendation
        )
    except (KeyError, AttributeError, TypeError) as e:
        # Fallback if formatting fails
        email_text = f"Hi {partner.get('contact_name', 'there')},\n\nWe noticed {partner.get('name', 'your company')} has been quiet. Let's reconnect.\n\nBest,\nBlostem Team"

    generated_at = save_reengagement(partner["id"], email_text, stall.status)

    return {
        "email": email_text,
        "status": stall.status,
        "generated_at": generated_at,
    }
