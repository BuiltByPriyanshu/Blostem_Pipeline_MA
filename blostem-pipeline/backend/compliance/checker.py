from backend.models import ComplianceResult

BANNED_PHRASES = [
    "guaranteed returns",
    "risk-free investment",
    "assured profit",
    "100% safe",
    "no risk",
    "highest interest rate in india",
    "best fd rates",
    "guaranteed interest",
]

DISCLAIMER = (
    "Fixed Deposits are subject to market risks. "
    "Please read all scheme-related documents carefully before investing."
)

MAX_WORDS = 300


def run_compliance_check(email_text: str) -> ComplianceResult:
    flags = []
    lower_text = email_text.lower()

    # Check banned phrases
    for phrase in BANNED_PHRASES:
        if phrase in lower_text:
            flags.append({"phrase": phrase, "severity": "high"})

    # Check unsubscribe placeholder
    if "{{unsubscribe_link}}" not in email_text:
        flags.append({"phrase": "Missing {{unsubscribe_link}} placeholder", "severity": "high"})

    # Check word count
    word_count = len(email_text.split())
    if word_count > MAX_WORDS:
        flags.append({
            "phrase": f"Email exceeds 300 words ({word_count} words)",
            "severity": "medium",
        })

    # passed = zero high severity flags
    high_flags = [f for f in flags if f["severity"] == "high"]
    passed = len(high_flags) == 0

    # Always append disclaimer
    email_with_disclaimer = email_text.strip() + "\n\n" + DISCLAIMER

    return ComplianceResult(
        passed=passed,
        flags=flags,
        email_with_disclaimer=email_with_disclaimer,
    )
