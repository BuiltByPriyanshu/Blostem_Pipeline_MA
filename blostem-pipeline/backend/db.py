import sqlite3
import os
from datetime import datetime, timedelta
import json

DB_PATH = os.path.join(os.path.dirname(__file__), "data", "blostem.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.executescript("""
        CREATE TABLE IF NOT EXISTS partners (
            id           INTEGER PRIMARY KEY,
            name         TEXT NOT NULL,
            contact_name TEXT,
            contact_role TEXT,
            signed_at    TEXT NOT NULL,
            last_event   TEXT,
            hq_city      TEXT,
            industry     TEXT
        );

        CREATE TABLE IF NOT EXISTS prospects (
            id             INTEGER PRIMARY KEY AUTOINCREMENT,
            name           TEXT NOT NULL,
            hq_city        TEXT,
            industry       TEXT,
            stage          TEXT,
            funding_usd    INTEGER,
            funding_label  TEXT,
            score          INTEGER DEFAULT 0,
            compliance     TEXT DEFAULT 'pending',
            seq_ready      INTEGER DEFAULT 0,
            scraped_at     TEXT,
            last_news      TEXT
        );

        CREATE TABLE IF NOT EXISTS stakeholders (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            prospect_id  INTEGER NOT NULL,
            name         TEXT,
            role         TEXT,
            angle        TEXT,
            initials     TEXT,
            email        TEXT,
            FOREIGN KEY (prospect_id) REFERENCES prospects(id)
        );

        CREATE TABLE IF NOT EXISTS intent_signals (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            prospect_id  INTEGER NOT NULL,
            signal_type  TEXT,
            description  TEXT,
            detected_at  TEXT,
            FOREIGN KEY (prospect_id) REFERENCES prospects(id)
        );

        CREATE TABLE IF NOT EXISTS sequences (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            prospect_id  INTEGER NOT NULL,
            persona      TEXT,
            email_1      TEXT,
            email_2      TEXT,
            email_3      TEXT,
            compliance   TEXT DEFAULT 'pending',
            generated_at TEXT,
            FOREIGN KEY (prospect_id) REFERENCES prospects(id)
        );

        CREATE TABLE IF NOT EXISTS activity_log (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            partner_id   INTEGER NOT NULL,
            event_type   TEXT NOT NULL,
            timestamp    TEXT NOT NULL,
            metadata     TEXT,
            FOREIGN KEY (partner_id) REFERENCES partners(id)
        );

        CREATE TABLE IF NOT EXISTS reengagements (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            partner_id   INTEGER NOT NULL,
            email_text   TEXT,
            status       TEXT,
            generated_at TEXT,
            FOREIGN KEY (partner_id) REFERENCES partners(id)
        );

        CREATE TABLE IF NOT EXISTS email_sends (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            to_email     TEXT NOT NULL,
            subject      TEXT,
            body_snippet TEXT,
            resend_id    TEXT,
            success      INTEGER DEFAULT 0,
            sent_at      TEXT
        );

        CREATE TABLE IF NOT EXISTS activity_feed (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            action_type  TEXT NOT NULL,
            description  TEXT,
            entity_name  TEXT,
            created_at   TEXT
        );
    """)
    conn.commit()
    conn.close()


PROSPECTS_DATA = [
    {
        "name": "PayNearby",
        "hq_city": "Mumbai",
        "industry": "Payments",
        "stage": "Series B",
        "funding_usd": 14_000_000,
        "funding_label": "$14M Series B",
        "score": 91,
        "compliance": "passed",
        "seq_ready": 0,
        "last_news": "PayNearby expands banking correspondent network to 1.2M retailers across Tier 2 and Tier 3 cities.",
        "stakeholders": [
            {
                "name": "Anand Kumar Bajaj",
                "role": "CEO & MD",
                "angle": "Position Blostem FD APIs as the missing revenue layer for PayNearby's 1.2M retailer network.",
                "initials": "AK",
            },
            {
                "name": "Subhash Chand",
                "role": "CTO",
                "angle": "Highlight Blostem's sub-100ms API latency and sandbox-to-production migration path.",
                "initials": "SC",
            },
            {
                "name": "Rajesh Sharma",
                "role": "Head of Partnerships",
                "angle": "Reference Rainmatter/Zerodha backing to establish credibility in the fintech ecosystem.",
                "initials": "RS",
            },
        ],
        "signals": [
            {
                "signal_type": "hiring",
                "description": "Hiring: Senior Payments API Engineer — 'experience with banking APIs and FD products preferred'",
                "detected_at": "2025-04-10",
            },
            {
                "signal_type": "hiring",
                "description": "Hiring: Fintech Partnerships Manager — 'build integrations with banking infrastructure providers'",
                "detected_at": "2025-04-08",
            },
            {
                "signal_type": "news",
                "description": "PayNearby raises Series B to expand banking services for underserved retailers across India.",
                "detected_at": "2025-03-28",
            },
        ],
    },
    {
        "name": "Fibe (EarlySalary)",
        "hq_city": "Pune",
        "industry": "Lending",
        "stage": "Series B",
        "funding_usd": 110_000_000,
        "funding_label": "$110M Series B",
        "score": 87,
        "compliance": "passed",
        "seq_ready": 0,
        "last_news": "Fibe rebrands from EarlySalary, targets 10M salaried users with embedded financial products.",
        "stakeholders": [
            {
                "name": "Akshay Mehrotra",
                "role": "CEO",
                "angle": "Show how Blostem FD APIs let Fibe offer savings products alongside their lending suite.",
                "initials": "AM",
            },
            {
                "name": "Vivek Jain",
                "role": "CFO",
                "angle": "Present the revenue-share model — FD float income as a new P&L line for Fibe.",
                "initials": "VJ",
            },
            {
                "name": "Priya Nair",
                "role": "Head of Product",
                "angle": "Emphasize Blostem's white-label FD widget that drops into Fibe's existing app in under a sprint.",
                "initials": "PN",
            },
        ],
        "signals": [
            {
                "signal_type": "hiring",
                "description": "Hiring: API Integration Lead — 'banking and fintech API experience required, FD products a plus'",
                "detected_at": "2025-04-12",
            },
            {
                "signal_type": "news",
                "description": "Fibe crosses 5M loan disbursals, announces expansion into savings and investment products.",
                "detected_at": "2025-04-05",
            },
            {
                "signal_type": "activity",
                "description": "Fibe's engineering blog published a post on embedded finance architecture patterns.",
                "detected_at": "2025-04-01",
            },
        ],
    },
    {
        "name": "Jupiter Money",
        "hq_city": "Bangalore",
        "industry": "Neobank",
        "stage": "Series C",
        "funding_usd": 86_000_000,
        "funding_label": "$86M Series C",
        "score": 83,
        "compliance": "passed",
        "seq_ready": 0,
        "last_news": "Jupiter Money partners with Federal Bank to launch co-branded FD products for millennial users.",
        "stakeholders": [
            {
                "name": "Jitendra Gupta",
                "role": "Founder & CEO",
                "angle": "Blostem's multi-bank FD API gives Jupiter the flexibility to offer competitive rates without a single-bank dependency.",
                "initials": "JG",
            },
            {
                "name": "Shobhit Singhal",
                "role": "CTO",
                "angle": "Highlight Blostem's RBI-compliant API stack and the 30+ platforms already live in production.",
                "initials": "SS",
            },
            {
                "name": "Ankit Agarwal",
                "role": "Head of Compliance",
                "angle": "Walk through Blostem's compliance documentation and RBI framework alignment for FD distribution.",
                "initials": "AA",
            },
        ],
        "signals": [
            {
                "signal_type": "news",
                "description": "Jupiter Money raises Series C to deepen banking product suite and expand FD offerings.",
                "detected_at": "2025-04-14",
            },
            {
                "signal_type": "hiring",
                "description": "Hiring: Banking API Developer — 'FD product integration experience strongly preferred'",
                "detected_at": "2025-04-09",
            },
            {
                "signal_type": "activity",
                "description": "Jupiter's product team attended Fintech Festival India and met with banking infrastructure providers.",
                "detected_at": "2025-03-30",
            },
        ],
    },
    {
        "name": "Uni Cards",
        "hq_city": "Bangalore",
        "industry": "Credit",
        "stage": "Series B",
        "funding_usd": 70_000_000,
        "funding_label": "$70M Series B",
        "score": 76,
        "compliance": "review",
        "seq_ready": 0,
        "last_news": "Uni Cards launches pay-in-3 product, explores savings features to increase user stickiness.",
        "stakeholders": [
            {
                "name": "Nitin Gupta",
                "role": "CEO",
                "angle": "Blostem FD APIs let Uni Cards offer savings alongside credit — increasing wallet share per user.",
                "initials": "NG",
            },
            {
                "name": "Prashant Singh",
                "role": "CTO",
                "angle": "Emphasize Blostem's developer-first API design and the 48-hour sandbox-to-integration timeline.",
                "initials": "PS",
            },
        ],
        "signals": [
            {
                "signal_type": "hiring",
                "description": "Hiring: Fintech Partnerships Lead — 'experience with banking API integrations and FD products'",
                "detected_at": "2025-04-11",
            },
            {
                "signal_type": "news",
                "description": "Uni Cards secures Series B to expand credit product suite and launch savings features.",
                "detected_at": "2025-03-25",
            },
        ],
    },
    {
        "name": "KreditBee",
        "hq_city": "Bangalore",
        "industry": "Lending",
        "stage": "Series D",
        "funding_usd": 200_000_000,
        "funding_label": "$200M Series D",
        "score": 71,
        "compliance": "passed",
        "seq_ready": 0,
        "last_news": "KreditBee expands into MSME lending, targets 50M underserved borrowers with embedded finance.",
        "stakeholders": [
            {
                "name": "Madhusudan Ekambaram",
                "role": "CEO",
                "angle": "Position Blostem FD APIs as a way to offer savings to KreditBee's 30M+ borrower base.",
                "initials": "ME",
            },
            {
                "name": "Vivek Veda",
                "role": "CFO",
                "angle": "Present FD float income as a new revenue stream that complements KreditBee's lending margins.",
                "initials": "VV",
            },
            {
                "name": "Arun Kumar",
                "role": "Head of Product",
                "angle": "Show how Blostem's white-label FD widget integrates in one sprint with KreditBee's existing app.",
                "initials": "AK",
            },
        ],
        "signals": [
            {
                "signal_type": "news",
                "description": "KreditBee raises Series D to scale MSME lending and explore embedded savings products.",
                "detected_at": "2025-04-03",
            },
            {
                "signal_type": "hiring",
                "description": "Hiring: API Integration Engineer — 'banking APIs, payments, and fintech infrastructure experience'",
                "detected_at": "2025-03-29",
            },
        ],
    },
    {
        "name": "Slice",
        "hq_city": "Bangalore",
        "industry": "Neobank",
        "stage": "Series B",
        "funding_usd": 220_000_000,
        "funding_label": "$220M Series B",
        "score": 68,
        "compliance": "passed",
        "seq_ready": 0,
        "last_news": "Slice merges with North East Small Finance Bank, pivots to full-stack neobank model.",
        "stakeholders": [
            {
                "name": "Rajan Bajaj",
                "role": "CEO",
                "angle": "Blostem's FD APIs give Slice a fast path to offering savings products post-bank merger.",
                "initials": "RB",
            },
            {
                "name": "Deepak Malhotra",
                "role": "CTO",
                "angle": "Highlight Blostem's proven integration with 30+ platforms and the sandbox-to-live migration path.",
                "initials": "DM",
            },
        ],
        "signals": [
            {
                "signal_type": "news",
                "description": "Slice completes merger with North East Small Finance Bank, now operates as a licensed neobank.",
                "detected_at": "2025-04-07",
            },
            {
                "signal_type": "activity",
                "description": "Slice engineering team published RFP for banking infrastructure API providers.",
                "detected_at": "2025-04-02",
            },
        ],
    },
    {
        "name": "Smallcase",
        "hq_city": "Bangalore",
        "industry": "Wealthtech",
        "stage": "Series C",
        "funding_usd": 40_000_000,
        "funding_label": "$40M Series C",
        "score": 54,
        "compliance": "pending",
        "seq_ready": 0,
        "last_news": "Smallcase expands beyond equity baskets, explores fixed income and FD products for retail investors.",
        "stakeholders": [
            {
                "name": "Vasanth Kamath",
                "role": "CEO",
                "angle": "Blostem FD APIs let Smallcase add fixed income to their portfolio — without building banking infra.",
                "initials": "VK",
            },
            {
                "name": "Anugrah Shrivastava",
                "role": "CTO",
                "angle": "Emphasize Blostem's API-first design and the minimal engineering lift for FD product integration.",
                "initials": "AS",
            },
        ],
        "signals": [
            {
                "signal_type": "news",
                "description": "Smallcase raises Series C to expand into fixed income and debt investment products.",
                "detected_at": "2025-03-20",
            },
            {
                "signal_type": "hiring",
                "description": "Hiring: Fintech Product Manager — 'experience with FD, bonds, or fixed income products preferred'",
                "detected_at": "2025-03-15",
            },
        ],
    },
    {
        "name": "BharatPe",
        "hq_city": "Delhi",
        "industry": "Payments",
        "stage": "Series E",
        "funding_usd": 370_000_000,
        "funding_label": "$370M Series E",
        "score": 42,
        "compliance": "pending",
        "seq_ready": 0,
        "last_news": "BharatPe focuses on merchant lending and BNPL, deprioritizes new banking product integrations.",
        "stakeholders": [
            {
                "name": "Nalin Negi",
                "role": "CEO",
                "angle": "Position Blostem FD APIs as a merchant savings product that increases BharatPe merchant retention.",
                "initials": "NN",
            },
            {
                "name": "Dhruv Bahl",
                "role": "CTO",
                "angle": "Reference Blostem's existing 30+ platform integrations as proof of enterprise-grade reliability.",
                "initials": "DB",
            },
        ],
        "signals": [
            {
                "signal_type": "news",
                "description": "BharatPe launches merchant lending product, targets 10M small businesses across India.",
                "detected_at": "2025-03-10",
            },
            {
                "signal_type": "activity",
                "description": "BharatPe's engineering team attended a banking API summit in Delhi.",
                "detected_at": "2025-02-28",
            },
        ],
    },
]

PARTNERS_DATA = [
    {
        "id": 1,
        "name": "PayNearby",
        "contact_name": "Subhash Chand",
        "contact_role": "CTO",
        "signed_at": (datetime.now() - timedelta(days=45)).strftime("%Y-%m-%d"),
        "hq_city": "Mumbai",
        "industry": "Payments",
        "activity": [
            {"event_type": "sandbox_access", "days_ago": 44},
            {"event_type": "first_api_call", "days_ago": 42},
            {"event_type": "fd_product_configured", "days_ago": 38},
            {"event_type": "go_live_approved", "days_ago": 30},
            {"event_type": "first_live_transaction", "days_ago": 25},
            {"event_type": "api_call", "days_ago": 6},
            {"event_type": "api_call", "days_ago": 5},
            {"event_type": "api_call", "days_ago": 4},
            {"event_type": "api_call", "days_ago": 3},
            {"event_type": "api_call", "days_ago": 2},
            {"event_type": "api_call", "days_ago": 1},
            {"event_type": "api_call", "days_ago": 0},
        ],
    },
    {
        "id": 2,
        "name": "Fibe (EarlySalary)",
        "contact_name": "Vivek Jain",
        "contact_role": "CFO",
        "signed_at": (datetime.now() - timedelta(days=38)).strftime("%Y-%m-%d"),
        "hq_city": "Pune",
        "industry": "Lending",
        "activity": [
            {"event_type": "sandbox_access", "days_ago": 37},
            {"event_type": "first_api_call", "days_ago": 35},
            {"event_type": "fd_product_configured", "days_ago": 30},
            {"event_type": "go_live_approved", "days_ago": 22},
            {"event_type": "first_live_transaction", "days_ago": 18},
            {"event_type": "api_call", "days_ago": 5},
            {"event_type": "api_call", "days_ago": 4},
            {"event_type": "api_call", "days_ago": 3},
            {"event_type": "api_call", "days_ago": 2},
            {"event_type": "api_call", "days_ago": 1},
            {"event_type": "api_call", "days_ago": 0},
        ],
    },
    {
        "id": 3,
        "name": "Uni Cards",
        "contact_name": "Prashant Singh",
        "contact_role": "CTO",
        "signed_at": (datetime.now() - timedelta(days=20)).strftime("%Y-%m-%d"),
        "hq_city": "Bangalore",
        "industry": "Credit",
        "activity": [
            {"event_type": "sandbox_access", "days_ago": 19},
            {"event_type": "first_api_call", "days_ago": 17},
            {"event_type": "fd_product_configured", "days_ago": 14},
        ],
    },
    {
        "id": 4,
        "name": "KreditBee",
        "contact_name": "Arun Kumar",
        "contact_role": "Head of Product",
        "signed_at": (datetime.now() - timedelta(days=25)).strftime("%Y-%m-%d"),
        "hq_city": "Bangalore",
        "industry": "Lending",
        "activity": [
            {"event_type": "sandbox_access", "days_ago": 24},
            {"event_type": "first_api_call", "days_ago": 22},
        ],
    },
    {
        "id": 5,
        "name": "Slice",
        "contact_name": "Deepak Malhotra",
        "contact_role": "CTO",
        "signed_at": (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d"),
        "hq_city": "Bangalore",
        "industry": "Neobank",
        "activity": [
            {"event_type": "sandbox_access", "days_ago": 29},
        ],
    },
    {
        "id": 6,
        "name": "Jupiter Money",
        "contact_name": "Shobhit Singhal",
        "contact_role": "CTO",
        "signed_at": (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d"),
        "hq_city": "Bangalore",
        "industry": "Neobank",
        "activity": [],
    },
]


def seed_prospects():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM prospects")
    if cur.fetchone()[0] > 0:
        conn.close()
        return 0

    now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    count = 0
    for p in PROSPECTS_DATA:
        cur.execute(
            """INSERT INTO prospects
               (name, hq_city, industry, stage, funding_usd, funding_label,
                score, compliance, seq_ready, scraped_at, last_news)
               VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
            (
                p["name"], p["hq_city"], p["industry"], p["stage"],
                p["funding_usd"], p["funding_label"], p["score"],
                p["compliance"], p["seq_ready"], now, p["last_news"],
            ),
        )
        prospect_id = cur.lastrowid

        for s in p["stakeholders"]:
            # Generate email from name
            name_parts = s["name"].lower().split()
            email = f"{name_parts[0]}.{name_parts[-1]}@{p['name'].lower().replace(' ', '')}.com"
            cur.execute(
                "INSERT INTO stakeholders (prospect_id, name, role, angle, initials, email) VALUES (?,?,?,?,?,?)",
                (prospect_id, s["name"], s["role"], s["angle"], s["initials"], email),
            )

        for sig in p["signals"]:
            cur.execute(
                "INSERT INTO intent_signals (prospect_id, signal_type, description, detected_at) VALUES (?,?,?,?)",
                (prospect_id, sig["signal_type"], sig["description"], sig["detected_at"]),
            )
        count += 1

    conn.commit()
    conn.close()
    return count


def seed_partners():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM partners")
    if cur.fetchone()[0] > 0:
        conn.close()
        return 0

    count = 0
    for p in PARTNERS_DATA:
        last_event = None
        if p["activity"]:
            last_event = min(p["activity"], key=lambda x: x["days_ago"])["event_type"]

        cur.execute(
            """INSERT INTO partners (id, name, contact_name, contact_role, signed_at, last_event, hq_city, industry)
               VALUES (?,?,?,?,?,?,?,?)""",
            (
                p["id"], p["name"], p["contact_name"], p["contact_role"],
                p["signed_at"], last_event, p["hq_city"], p["industry"],
            ),
        )

        for act in p["activity"]:
            ts = (datetime.now() - timedelta(days=act["days_ago"])).strftime("%Y-%m-%dT%H:%M:%S")
            cur.execute(
                "INSERT INTO activity_log (partner_id, event_type, timestamp) VALUES (?,?,?)",
                (p["id"], act["event_type"], ts),
            )
        count += 1

    conn.commit()
    conn.close()
    return count


def get_all_prospects():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM prospects ORDER BY score DESC")
    rows = [dict(r) for r in cur.fetchall()]
    for row in rows:
        cur.execute("SELECT * FROM stakeholders WHERE prospect_id = ?", (row["id"],))
        row["stakeholders"] = [dict(s) for s in cur.fetchall()]
        cur.execute("SELECT * FROM intent_signals WHERE prospect_id = ?", (row["id"],))
        row["signals"] = [dict(s) for s in cur.fetchall()]
    conn.close()
    return rows


def get_prospect_by_id(prospect_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM prospects WHERE id = ?", (prospect_id,))
    row = cur.fetchone()
    if not row:
        conn.close()
        return None
    row = dict(row)
    cur.execute("SELECT * FROM stakeholders WHERE prospect_id = ?", (prospect_id,))
    row["stakeholders"] = [dict(s) for s in cur.fetchall()]
    cur.execute("SELECT * FROM intent_signals WHERE prospect_id = ?", (prospect_id,))
    row["signals"] = [dict(s) for s in cur.fetchall()]
    conn.close()
    return row


def update_prospect_score(prospect_id: int, score: int):
    conn = get_connection()
    conn.execute("UPDATE prospects SET score = ? WHERE id = ?", (score, prospect_id))
    conn.commit()
    conn.close()


def get_all_partners():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM partners")
    rows = [dict(r) for r in cur.fetchall()]
    for row in rows:
        cur.execute(
            "SELECT * FROM activity_log WHERE partner_id = ? ORDER BY timestamp ASC",
            (row["id"],),
        )
        row["activity_log"] = [dict(a) for a in cur.fetchall()]
    conn.close()
    return rows


def get_partner_by_id(partner_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM partners WHERE id = ?", (partner_id,))
    row = cur.fetchone()
    if not row:
        conn.close()
        return None
    row = dict(row)
    cur.execute(
        "SELECT * FROM activity_log WHERE partner_id = ? ORDER BY timestamp ASC",
        (partner_id,),
    )
    row["activity_log"] = [dict(a) for a in cur.fetchall()]
    conn.close()
    return row


def get_cached_sequence(prospect_id: int, persona: str):
    conn = get_connection()
    cur = conn.cursor()
    cutoff = (datetime.now() - timedelta(hours=24)).strftime("%Y-%m-%dT%H:%M:%S")
    cur.execute(
        """SELECT * FROM sequences
           WHERE prospect_id = ? AND persona = ? AND generated_at > ?
           ORDER BY generated_at DESC LIMIT 1""",
        (prospect_id, persona, cutoff),
    )
    row = cur.fetchone()
    conn.close()
    return dict(row) if row else None


def save_sequence(prospect_id: int, persona: str, email_1: str, email_2: str, email_3: str, compliance: str):
    conn = get_connection()
    now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    cur = conn.cursor()
    cur.execute(
        """INSERT INTO sequences (prospect_id, persona, email_1, email_2, email_3, compliance, generated_at)
           VALUES (?,?,?,?,?,?,?)""",
        (prospect_id, persona, email_1, email_2, email_3, compliance, now),
    )
    seq_id = cur.lastrowid
    conn.execute("UPDATE prospects SET seq_ready = 1 WHERE id = ?", (prospect_id,))
    conn.commit()
    conn.close()
    return seq_id, now


def get_sequences_for_prospect(prospect_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM sequences WHERE prospect_id = ? ORDER BY generated_at DESC",
        (prospect_id,),
    )
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return rows


def save_reengagement(partner_id: int, email_text: str, status: str):
    conn = get_connection()
    now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    conn.execute(
        "INSERT INTO reengagements (partner_id, email_text, status, generated_at) VALUES (?,?,?,?)",
        (partner_id, email_text, status, now),
    )
    conn.commit()
    conn.close()
    return now


def create_prospect(name: str, hq_city: str, industry: str, stage: str, funding_usd: int, funding_label: str, last_news: str = None):
    """Create a new prospect."""
    conn = get_connection()
    now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    
    cur = conn.cursor()
    cur.execute(
        """INSERT INTO prospects
           (name, hq_city, industry, stage, funding_usd, funding_label,
            score, compliance, seq_ready, scraped_at, last_news)
           VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
        (name, hq_city, industry, stage, funding_usd, funding_label, 50, "pending", 0, now, last_news),
    )
    prospect_id = cur.lastrowid
    conn.commit()
    conn.close()
    
    return prospect_id


def log_activity(action_type: str, description: str, entity_name: str = None):
    """Log an activity to the activity_feed table."""
    conn = get_connection()
    now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    
    conn.execute(
        """INSERT INTO activity_feed (action_type, description, entity_name, created_at)
           VALUES (?, ?, ?, ?)""",
        (action_type, description, entity_name, now),
    )
    conn.commit()
    conn.close()
