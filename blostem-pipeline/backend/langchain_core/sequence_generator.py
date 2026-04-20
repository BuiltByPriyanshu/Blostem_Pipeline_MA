import os
from datetime import datetime

from backend.db import get_cached_sequence, save_sequence, log_activity
from backend.compliance.checker import run_compliance_check

# Demo email templates - no API required
DEMO_EMAILS = {
    "CTO": {
        "email_1": """Hi {name},

I noticed {company} is expanding your payments infrastructure. We power FD APIs for 30+ platforms across India with sub-100ms latency and RBI-compliant stack.

Our sandbox-to-production path takes 48 hours. No vendor lock-in. Full audit trail for compliance.

Worth a 20-minute call?

Best,
Blostem Team

{{unsubscribe_link}}""",
        "email_2": """Hi {name},

Following up on my email from 5 days ago about Blostem's FD APIs.

30+ platforms are already live on our infrastructure. {company} could be next.

Let's unblock any integration questions.

Best,
Blostem Team

{{unsubscribe_link}}""",
        "email_3": """Hi {name},

Last message: I have a case study of a {industry} company that went live on Blostem in under 2 weeks.

Happy to share if you're interested.

Best,
Blostem Team

{{unsubscribe_link}}"""
    },
    "CFO": {
        "email_1": """Hi {name},

{company} could unlock a new revenue stream with Blostem's FD APIs.

FD float income as a new P&L line. Minimal integration cost. Revenue-share model.

ROI timeline: 6-8 weeks to first transaction.

Worth exploring?

Best,
Blostem Team

{{unsubscribe_link}}""",
        "email_2": """Hi {name},

Following up on my email about FD revenue opportunities for {company}.

Our 30+ partners are seeing 15-20% incremental revenue from FD products.

Let's discuss your specific numbers.

Best,
Blostem Team

{{unsubscribe_link}}""",
        "email_3": """Hi {name},

Last outreach: I have financial models for {industry} companies using Blostem's FD APIs.

Happy to share if you'd like to see the numbers.

Best,
Blostem Team

{{unsubscribe_link}}"""
    },
    "Head of Compliance": {
        "email_1": """Hi {name},

{company} needs RBI-compliant FD distribution. Blostem's APIs are SEBI/RBI-ready with full audit trail.

We handle compliance documentation. You handle customer experience.

Worth a 20-minute call?

Best,
Blostem Team

{{unsubscribe_link}}""",
        "email_2": """Hi {name},

Following up on my email about RBI-compliant FD distribution for {company}.

Our compliance framework is battle-tested across 30+ platforms.

Let's discuss your specific requirements.

Best,
Blostem Team

{{unsubscribe_link}}""",
        "email_3": """Hi {name},

Last message: I have our full compliance documentation and RBI framework alignment guide.

Happy to share with your legal team.

Best,
Blostem Team

{{unsubscribe_link}}"""
    },
    "Head of Product": {
        "email_1": """Hi {name},

{company} could expand your product suite with Blostem's white-label FD widget.

One-sprint integration. Seamless UX. Revenue-generating feature.

Worth exploring?

Best,
Blostem Team

{{unsubscribe_link}}""",
        "email_2": """Hi {name},

Following up on my email about adding FD products to {company}'s platform.

Our widget integrates in under 2 weeks. 30+ platforms already live.

Let's discuss your timeline.

Best,
Blostem Team

{{unsubscribe_link}}""",
        "email_3": """Hi {name},

Last outreach: I have product specs and integration guides for {company}'s use case.

Happy to share if you'd like to move forward.

Best,
Blostem Team

{{unsubscribe_link}}"""
    }
}


def _build_email1_prompt(prospect: dict, persona: str) -> str:
    return f"Generate email 1 for {persona} at {prospect['name']}"


def _build_email2_prompt(prospect: dict, persona: str, email1: str) -> str:
    return f"Generate email 2 (day 5 follow-up) for {persona} at {prospect['name']}"


def _build_email3_prompt(prospect: dict, persona: str) -> str:
    return f"Generate email 3 (day 12 final nudge) for {persona} at {prospect['name']}"


def generate_sequence(prospect: dict, persona: str) -> dict:
    prospect_id = prospect["id"]

    # Check cache first
    cached = get_cached_sequence(prospect_id, persona)
    if cached:
        return {
            "id": cached["id"],
            "prospect_id": cached["prospect_id"],
            "persona": cached["persona"],
            "email_1": cached["email_1"],
            "email_2": cached["email_2"],
            "email_3": cached["email_3"],
            "compliance": cached["compliance"],
            "generated_at": cached["generated_at"],
        }

    # Use demo templates (no API required)
    if persona not in DEMO_EMAILS:
        persona = "CTO"  # Default to CTO
    
    templates = DEMO_EMAILS[persona]
    
    # Format emails with prospect details
    email_1 = templates["email_1"].format(
        name=prospect.get("name", "there"),
        company=prospect.get("name", "your company"),
        industry=prospect.get("industry", "fintech")
    )
    email_2 = templates["email_2"].format(
        name=prospect.get("name", "there"),
        company=prospect.get("name", "your company"),
        industry=prospect.get("industry", "fintech")
    )
    email_3 = templates["email_3"].format(
        name=prospect.get("name", "there"),
        company=prospect.get("name", "your company"),
        industry=prospect.get("industry", "fintech")
    )

    # Run compliance on all three
    c1 = run_compliance_check(email_1)
    c2 = run_compliance_check(email_2)
    c3 = run_compliance_check(email_3)

    all_passed = c1.passed and c2.passed and c3.passed
    compliance_status = "passed" if all_passed else "review"

    seq_id, generated_at = save_sequence(
        prospect_id, persona, email_1, email_2, email_3, compliance_status
    )

    # Log activity
    log_activity(
        action_type="sequence_generated",
        description=f"Sequence generated for {persona} persona",
        entity_name=prospect.get("name", "Unknown")
    )

    return {
        "id": seq_id,
        "prospect_id": prospect_id,
        "persona": persona,
        "email_1": email_1,
        "email_2": email_2,
        "email_3": email_3,
        "compliance": compliance_status,
        "generated_at": generated_at,
    }
