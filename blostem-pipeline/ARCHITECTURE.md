# Blostem Pipeline — Architecture & Design

## System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend (React 18)                      │
│  Pipeline | Activation Tracker | Sequence Viewer            │
│  (Vite + TailwindCSS + React Router)                        │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTP/JSON
                         ↓
┌─────────────────────────────────────────────────────────────┐
│                  Backend (FastAPI)                           │
│  ┌──────────────┬──────────────┬──────────────┐             │
│  │  Prospects   │  Sequences   │  Activation  │             │
│  │  Router      │  Router      │  Router      │             │
│  └──────────────┴──────────────┴──────────────┘             │
│                         ↓                                    │
│  ┌──────────────────────────────────────────┐               │
│  │  Core Logic Modules                      │               │
│  │  • Intent Scorer (scoring/)              │               │
│  │  • Stall Detector (activation/tracker)   │               │
│  │  • Compliance Checker (compliance/)      │               │
│  │  • Sequence Generator (langchain_core/)  │               │
│  │  • Reengagement Generator (langchain_core/) │            │
│  └──────────────────────────────────────────┘               │
│                         ↓                                    │
│  ┌──────────────────────────────────────────┐               │
│  │  Data Layer (db.py)                      │               │
│  │  • SQLite connection & queries           │               │
│  │  • Seed functions                        │               │
│  │  • Cache management                      │               │
│  └──────────────────────────────────────────┘               │
└────────────────────────┬────────────────────────────────────┘
                         │
        ┌────────────────┼────────────────┐
        ↓                ↓                ↓
   ┌─────────┐      ┌─────────┐      ┌──────────┐
   │ SQLite  │      │ Groq    │      │ Pydantic │
   │ Database│      │ API     │      │ Models   │
   │ (local) │      │ (LLM)   │      │ (schema) │
   └─────────┘      └─────────┘      └──────────┘
```

## Data Flow

### 1. Prospect Identification Pipeline

```
User opens Pipeline page
    ↓
Frontend: GET /api/prospects/pipeline
    ↓
Backend: db.get_all_prospects()
    ↓
SQLite: SELECT * FROM prospects ORDER BY score DESC
    ↓
For each prospect:
  - Load stakeholders from DB
  - Load intent signals from DB
  - Build ProspectOut model
    ↓
Return JSON array to frontend
    ↓
Frontend: Render table with scores, compliance, seq_ready
```

### 2. Sequence Generation Pipeline

```
User clicks "Generate email" for CTO at PayNearby
    ↓
Frontend: POST /api/sequences/generate
  Body: {prospect_id: 1, persona: "CTO"}
    ↓
Backend: generate_sequence(prospect, persona)
    ↓
Check cache: SELECT * FROM sequences WHERE prospect_id=1 AND persona="CTO"
    ↓
If cached and < 24 hours old:
  Return cached result
Else:
  Call Groq API (LangChain):
    - System prompt: CTO-specific instructions
    - User prompt: Prospect details + signals
    - Generate email_1 (initial)
    - Generate email_2 (day 5 follow-up)
    - Generate email_3 (day 12 nudge)
    ↓
  For each email:
    - Run compliance check
    - Flag banned phrases, missing unsubscribe, word count
    ↓
  Save to DB: INSERT INTO sequences (...)
    ↓
Return SequenceOut model to frontend
    ↓
Frontend: Render 3 email cards with compliance badges
```

### 3. Stall Detection & Re-engagement Pipeline

```
User opens Activation Tracker page
    ↓
Frontend: GET /api/activation/pipeline
    ↓
Backend: get_all_partners()
    ↓
For each partner:
  - Load activity_log from DB
  - Call detect_stall(partner, activity_log)
    ↓
    Stall detection logic:
      - Calculate days_silent from last activity
      - Find last milestone reached
      - Determine status: new | active | stalled | critical
      - Infer stall reason based on last milestone
      - Generate recommendation
    ↓
  - Calculate activation_pct from milestones
  - Get weekly_trend from api_call counts
  - Get milestones list
    ↓
  Build PartnerOut model
    ↓
Sort by status: critical → stalled → new → active
    ↓
Return JSON array to frontend
    ↓
Frontend: Render partner rows with status badges, sparklines
```

### 4. Re-engagement Email Generation

```
User clicks "Re-engage" on Slice (critical partner)
    ↓
Frontend: POST /api/activation/reengage/5
    ↓
Backend: reengage_partner(partner_id=5)
    ↓
Load partner from DB
Load activity_log from DB
Call detect_stall(partner, activity_log)
    ↓
If status not in (stalled, critical):
  Return 400 error
Else:
  Call generate_reengagement_email(partner, stall)
    ↓
    Select template based on status:
      - "stalled": peer-to-peer tone, 120 words
      - "critical": executive escalation, 80 words
    ↓
    Call Groq API with template + partner details
    ↓
    Save to DB: INSERT INTO reengagements (...)
    ↓
Return ReengagementOut model to frontend
    ↓
Frontend: Show email in detail panel
```

## Module Breakdown

### Backend Modules

#### `db.py` — Database Layer
- **init_db()**: Create all tables
- **seed_prospects()**: Insert 8 demo prospects with stakeholders and signals
- **seed_partners()**: Insert 6 demo partners with activity logs
- **get_all_prospects()**: Fetch all prospects with nested data
- **get_prospect_by_id()**: Fetch single prospect
- **get_all_partners()**: Fetch all partners with activity logs
- **get_partner_by_id()**: Fetch single partner
- **get_cached_sequence()**: Check if sequence exists and is < 24 hours old
- **save_sequence()**: Insert generated sequence
- **save_reengagement()**: Insert generated re-engagement email

#### `models.py` — Pydantic Schemas
- **ProspectOut**: Prospect with stakeholders and signals
- **PartnerOut**: Partner with activation metrics and trends
- **SequenceOut**: 3-email sequence with compliance status
- **StallSignal**: Stall detection result
- **ComplianceResult**: Compliance check result with flags

#### `scoring/intent_scorer.py` — Intent Scoring
- **calculate_intent_score(prospect)**: Weighted formula (0–100)
  - Funding recency: 25 pts
  - Hiring signals: 25 pts
  - Industry fit: 25 pts
  - News momentum: 25 pts
- **get_score_tier(score)**: hot | warm | cold

#### `activation/tracker.py` — Stall Detection
- **detect_stall(partner, activity_log)**: Determine status and reason
- **calculate_activation_score(activity_log)**: Milestone completion %
- **get_weekly_trend(activity_log)**: 7-day API call counts
- **get_milestones(activity_log)**: Milestone completion status

#### `compliance/checker.py` — Compliance Validation
- **run_compliance_check(email_text)**: Check for banned phrases, unsubscribe link, word count
- Returns: passed (bool), flags (list), email_with_disclaimer (str)

#### `langchain_core/sequence_generator.py` — Email Generation
- **generate_sequence(prospect, persona)**: Generate 3-email sequence
  - Check cache first (24-hour TTL)
  - Call Groq API for each email
  - Run compliance check on all three
  - Save to DB
  - Return SequenceOut

#### `langchain_core/reengagement.py` — Re-engagement Generation
- **generate_reengagement_email(partner, stall)**: Generate re-engagement email
  - Select template based on stall status
  - Call Groq API
  - Save to DB
  - Return ReengagementOut

#### `routers/prospects.py` — Prospects API
- `GET /api/prospects/pipeline` → list[ProspectOut]
- `GET /api/prospects/{id}` → ProspectOut
- `POST /api/prospects/{id}/score` → ScoreResponse

#### `routers/sequences.py` — Sequences API
- `POST /api/sequences/generate` → SequenceOut
- `GET /api/sequences/{prospect_id}` → list[SequenceOut]

#### `routers/activation.py` — Activation API
- `GET /api/activation/pipeline` → list[PartnerOut]
- `GET /api/activation/{partner_id}` → PartnerOut
- `POST /api/activation/reengage/{partner_id}` → ReengagementOut

#### `main.py` — FastAPI App
- CORS middleware for localhost:5173
- Router registration
- Startup event: init_db(), seed_prospects(), seed_partners()

### Frontend Components

#### Pages
- **Pipeline.jsx**: Prospect table with filters, metrics, expandable rows
- **ActivationTracker.jsx**: Partner table with status filters, metrics, expandable rows
- **SequenceViewer.jsx**: Prospect selector, persona tabs, email cards

#### Components
- **Sidebar.jsx**: Navigation with active state
- **ProspectTable.jsx**: Renders prospect rows with inline expansion
- **ProspectDetail.jsx**: Tabs for stakeholder map and intent signals
- **StakeholderMap.jsx**: 3-column grid of persona cards
- **IntentSignals.jsx**: Signal list with type badges
- **PartnerRow.jsx**: Partner row with sparkline and re-engage button
- **MetricCard.jsx**: Summary metric display
- **IntentScoreBar.jsx**: Progress bar with score badge
- **StatusBadge.jsx**: Status/compliance badge with colors
- **SparkLine.jsx**: 7-bar chart for API call trend

#### Hooks
- **useProspects.js**: Fetch prospects, manage loading/error
- **useActivation.js**: Fetch partners, manage reengage function

#### Utils
- **formatters.js**: formatDaysAgo, formatFunding, getScoreColor, getStatusColor, getComplianceColor

## Database Schema

```sql
prospects (8 rows)
├── id (PK)
├── name
├── hq_city
├── industry
├── stage
├── funding_usd
├── funding_label
├── score (0–100)
├── compliance (passed | review | pending)
├── seq_ready (0 | 1)
├── scraped_at
└── last_news

stakeholders (20 rows)
├── id (PK)
├── prospect_id (FK)
├── name
├── role
├── angle
└── initials

intent_signals (19 rows)
├── id (PK)
├── prospect_id (FK)
├── signal_type (hiring | news | activity)
├── description
└── detected_at

sequences (cached)
├── id (PK)
├── prospect_id (FK)
├── persona (CTO | CFO | Head of Compliance | Head of Product)
├── email_1
├── email_2
├── email_3
├── compliance (passed | review)
└── generated_at

partners (6 rows)
├── id (PK)
├── name
├── contact_name
├── contact_role
├── signed_at
├── last_event
├── hq_city
└── industry

activity_log (29 rows)
├── id (PK)
├── partner_id (FK)
├── event_type (sandbox_access | first_api_call | fd_product_configured | go_live_approved | first_live_transaction | api_call)
├── timestamp
└── metadata

reengagements (cached)
├── id (PK)
├── partner_id (FK)
├── email_text
├── status (stalled | critical)
└── generated_at
```

## Caching Strategy

### Sequence Caching
- **Key**: prospect_id + persona
- **TTL**: 24 hours
- **Check**: Before calling Groq API
- **Benefit**: Instant response for repeated requests, reduced API costs

### Reengagement Caching
- **Key**: partner_id
- **TTL**: Unlimited (one per partner)
- **Check**: On re-engage endpoint
- **Benefit**: Track re-engagement history

## Error Handling

### Frontend
- Try/catch on all fetch calls
- Show "Loading..." text during requests
- Show error messages in red
- Disable buttons during generation

### Backend
- HTTPException for 404 (not found), 400 (bad request)
- Pydantic validation on request bodies
- Try/catch on Groq API calls
- Graceful fallback if API key missing

## Performance Considerations

### API Response Times
- GET /api/prospects/pipeline: < 100ms (SQLite)
- GET /api/activation/pipeline: < 100ms (SQLite)
- POST /api/sequences/generate: 10–30s (Groq API) or < 100ms (cached)
- POST /api/activation/reengage/{id}: 5–10s (Groq API)

### Frontend Rendering
- ProspectTable: O(n) where n = 8 prospects
- PartnerRow: O(n) where n = 6 partners
- Expandable rows: Lazy render on click
- No pagination needed (small dataset)

### Database
- SQLite (single file, no server)
- Indexes on prospect_id, partner_id (implicit via FK)
- No complex joins (data is denormalized)
- Seed time: < 1 second

## Deployment Notes

### Local Development
- No Docker needed
- Python 3.11+ required
- Node.js 18+ required
- Runs on localhost:8000 (backend) and localhost:5173 (frontend)

### Production Deployment
- Would require Docker + cloud hosting (AWS, GCP, Heroku)
- Replace SQLite with PostgreSQL
- Add authentication (JWT)
- Add rate limiting
- Add monitoring/logging
- Use environment variables for secrets
- Deploy frontend to CDN (Vercel, Netlify)
- Deploy backend to serverless (Lambda, Cloud Functions)

## Security Considerations

### Current (Demo)
- No authentication
- No rate limiting
- CORS allows only localhost:5173
- Groq API key in .env (not committed)

### Production
- Add JWT authentication
- Add rate limiting per user
- Validate all inputs (Pydantic does this)
- Use HTTPS only
- Rotate API keys regularly
- Add audit logging
- Sanitize email content before display
- Use parameterized queries (SQLite does this)

## Testing Strategy

### Unit Tests (Not Included)
- Intent scorer: test weighted formula
- Stall detector: test status determination
- Compliance checker: test banned phrases
- Formatters: test date/currency formatting

### Integration Tests (Not Included)
- Sequence generation: test Groq API integration
- Database: test seed and query functions
- API endpoints: test request/response

### Manual Testing (Included in DEMO_CHECKLIST.md)
- All 3 pages load
- Data displays correctly
- Sequences generate and cache
- Re-engagement works
- No console errors
