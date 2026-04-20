# Blostem Pipeline — Project Summary

## What Was Built

A full-stack AI-powered B2B marketing automation engine for Blostem (fintech infrastructure company backed by Rainmatter/Zerodha and MobiKwik).

**Two core problems solved:**
1. **Prospect Identification**: Identify highest-intent enterprise companies before sales makes a call
2. **Partner Re-engagement**: Detect when signed partners go silent and automatically generate outreach

## Project Stats

- **Backend**: 1,200+ lines of Python (FastAPI, LangChain, SQLite)
- **Frontend**: 1,500+ lines of React/JSX (Vite, TailwindCSS, React Router)
- **Database**: 8 tables, 8 prospects, 6 partners, 20 stakeholders, 19 signals, 29 activity logs
- **API Endpoints**: 9 endpoints across 3 routers
- **UI Components**: 12 React components + 3 pages
- **Documentation**: 4 guides (README, SETUP_GUIDE, DEMO_CHECKLIST, ARCHITECTURE)

## File Structure

```
blostem-pipeline/
├── backend/
│   ├── main.py                          # FastAPI app entry point
│   ├── db.py                            # SQLite init, seed, queries
│   ├── models.py                        # Pydantic schemas
│   ├── scoring/intent_scorer.py         # Weighted intent scoring (0–100)
│   ├── activation/tracker.py            # Stall detection engine
│   ├── compliance/checker.py            # Compliance validation
│   ├── langchain_core/
│   │   ├── sequence_generator.py        # 3-email sequence generation
│   │   └── reengagement.py              # Re-engagement email generation
│   └── routers/
│       ├── prospects.py                 # /api/prospects/*
│       ├── sequences.py                 # /api/sequences/*
│       └── activation.py                # /api/activation/*
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   │   ├── Pipeline.jsx             # Prospect ranking page
│   │   │   ├── ActivationTracker.jsx    # Partner health page
│   │   │   └── SequenceViewer.jsx       # Email sequence page
│   │   ├── components/
│   │   │   ├── Sidebar.jsx
│   │   │   ├── ProspectTable.jsx
│   │   │   ├── ProspectDetail.jsx
│   │   │   ├── StakeholderMap.jsx
│   │   │   ├── IntentSignals.jsx
│   │   │   ├── PartnerRow.jsx
│   │   │   ├── MetricCard.jsx
│   │   │   ├── IntentScoreBar.jsx
│   │   │   ├── StatusBadge.jsx
│   │   │   └── SparkLine.jsx
│   │   ├── hooks/
│   │   │   ├── useProspects.js
│   │   │   └── useActivation.js
│   │   ├── utils/formatters.js
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css
│   ├── index.html
│   ├── vite.config.js
│   ├── tailwind.config.js
│   ├── postcss.config.js
│   └── package.json
├── requirements.txt
├── .env.example
├── seed.py
├── README.md
├── SETUP_GUIDE.md
├── DEMO_CHECKLIST.md
└── ARCHITECTURE.md
```

## Key Features

### 1. Intent Scoring (0–100)
Weighted formula identifies highest-intent prospects:
- **Funding recency** (25 pts): Series A/B +20, recent funding +5
- **Hiring signals** (25 pts): +8 per keyword match (payments, banking, API, fintech, partnerships)
- **Industry fit** (25 pts): High-fit industries +25, fintech +15, other +5
- **News momentum** (25 pts): +5 per recent news/activity item

**Result**: PayNearby (91), Fibe (87), Jupiter Money (83), Uni Cards (76), KreditBee (71), Slice (68), Smallcase (54), BharatPe (42)

### 2. Stall Detection
Automatic identification of silent partners with root cause analysis:
- **New**: < 3 days since signing (grace period)
- **Active**: < 7 days silent
- **Stalled**: 7–13 days silent
- **Critical**: 14+ days silent

**Root cause mapping**:
- None → "Never made first API call"
- sandbox_access → "Integration confusion"
- first_api_call → "Stuck on FD product config"
- fd_product_configured → "Awaiting compliance sign-off"
- go_live_approved → "Blocked on frontend integration"

**Demo data**: Slice (21 days, critical), KreditBee (14 days, stalled), Uni Cards (9 days, stalled)

### 3. LLM-Powered Sequences
AI-generated outreach sequences per persona:
- **4 personas**: CTO, CFO, Head of Compliance, Head of Product
- **3 emails per persona**: Initial, day 5 follow-up, day 12 nudge
- **Personalization**: References prospect's funding stage, city, signals, and Blostem's backers
- **Compliance**: All emails checked for banned phrases, unsubscribe link, word count
- **Caching**: 24-hour cache to avoid re-hitting Groq API

### 4. Compliance Checking
Rule-based + LLM validation:
- **Banned phrases** (case-insensitive): "guaranteed returns", "risk-free investment", "assured profit", "100% safe", "no risk", "highest interest rate in india", "best fd rates", "guaranteed interest"
- **Required elements**: {{unsubscribe_link}} placeholder
- **Word limit**: 300 words max
- **Auto-disclaimer**: "Fixed Deposits are subject to market risks..."

### 5. Re-engagement Automation
Contextual re-engagement emails based on stall reason:
- **Stalled template**: Peer-to-peer tone, offers unblocking call, 120 words
- **Critical template**: Executive escalation, 80 words
- **Context-aware**: References last milestone, stall reason, and recommendation

## Tech Stack

### Backend
- **Framework**: FastAPI 0.111.0
- **ORM**: SQLModel 0.0.19
- **Validation**: Pydantic 2.7.1
- **LLM**: LangChain 0.2.0 + langchain-groq 0.1.3
- **Database**: SQLite (local file)
- **Server**: Uvicorn 0.29.0

### Frontend
- **Framework**: React 18.2.0
- **Build**: Vite 5.0.8
- **Styling**: TailwindCSS 3.4.1
- **Routing**: React Router 6.22.0
- **Charts**: Recharts 2.10.3

### LLM
- **Provider**: Groq API
- **Model**: Llama 3 70B (llama3-70b-8192)
- **Temperature**: 0.3 (sequences), 0.4 (re-engagement)
- **Caching**: SQLite (24-hour TTL)

## API Endpoints

### Prospects
```
GET  /api/prospects/pipeline          → All prospects sorted by score
GET  /api/prospects/{id}              → Single prospect with details
POST /api/prospects/{id}/score        → Re-run intent scoring
```

### Sequences
```
POST /api/sequences/generate          → Generate 3-email sequence
GET  /api/sequences/{prospect_id}     → All sequences for prospect
```

### Activation
```
GET  /api/activation/pipeline         → All partners with stall status
GET  /api/activation/{partner_id}     → Single partner details
POST /api/activation/reengage/{id}    → Generate re-engagement email
```

## Demo Data

### 8 Prospects (Real Indian Fintech Companies)
1. **PayNearby** — Payments, Series B, $14M, Mumbai, Score 91
2. **Fibe (EarlySalary)** — Lending, Series B, $110M, Pune, Score 87
3. **Jupiter Money** — Neobank, Series C, $86M, Bangalore, Score 83
4. **Uni Cards** — Credit, Series B, $70M, Bangalore, Score 76
5. **KreditBee** — Lending, Series D, $200M, Bangalore, Score 71
6. **Slice** — Neobank, Series B, $220M, Bangalore, Score 68
7. **Smallcase** — Wealthtech, Series C, $40M, Bangalore, Score 54
8. **BharatPe** — Payments, Series E, $370M, Delhi, Score 42

Each prospect has:
- 2–3 stakeholders with outreach angles
- 2–3 intent signals (hiring posts, news, activity)

### 6 Partners (Signed, Post-Onboarding)
1. **PayNearby** — Active (45 days, 5 milestones complete, daily API calls)
2. **Fibe** — Active (38 days, 5 milestones complete, daily API calls)
3. **Uni Cards** — Stalled (20 days, 3 milestones, no activity 9 days)
4. **KreditBee** — Stalled (25 days, 2 milestones, no activity 14 days)
5. **Slice** — Critical (30 days, 1 milestone, no activity 21 days)
6. **Jupiter Money** — New (1 day, grace period)

## Design System

### Colors
- **Green**: #639922 (active, passed, hot)
- **Amber**: #BA7517 (warning, stalled, warm)
- **Red**: #E24B4A (critical, failed, cold)
- **Blue**: #0C447C (info, stage badges)
- **Purple**: #3C3489 (persona, sequence)

### Typography
- **Font**: Inter (400, 500 weights only)
- **Sizes**: 11px (badge), 13px (secondary), 14px (body), 15px (section), 22px (title)
- **Line height**: 1.6

### Spacing
- **Base**: 4px
- **Card padding**: 16px / 20px
- **Gaps**: 12px between cards, 8px inside cards

### Borders & Radius
- **Cards**: 10px radius, 1px solid #E8E7E2
- **Buttons**: 8px radius
- **Badges**: 20px radius
- **No box shadows** (depth via borders only)

## Quick Start

```bash
# 1. Backend setup
cd blostem-pipeline
cp .env.example .env
# Edit .env with your GROQ_API_KEY
pip install -r requirements.txt
python seed.py
cd backend
uvicorn main:app --reload

# 2. Frontend setup (new terminal)
cd blostem-pipeline/frontend
npm install
npm run dev

# 3. Open http://localhost:5173
```

## Demo Flow (4 Minutes)

1. **Pipeline** (0:30) — Show 8 prospects ranked by intent
2. **Stakeholder Map** (0:45) — Show 3 personas with outreach angles
3. **Generate Sequence** (1:00) — Generate 3 compliance-checked emails
4. **Activation Tracker** (0:30) — Show 6 partners, 3 stalled
5. **Stall Analysis** (0:45) — Show Slice (21 days), root cause, recommendation
6. **Re-engage** (0:30) — Generate re-engagement email
7. **Closing** (0:30) — "Full pipeline from prospect ID to re-engagement"

## Success Criteria

✅ All 3 pages load without errors
✅ 8 prospects visible, sorted by score
✅ Stakeholder map shows 3 personas per prospect
✅ Sequence generation takes < 30 seconds
✅ All emails show "Compliance passed" badge
✅ Activation Tracker shows stalled partners
✅ Re-engagement generates in < 10 seconds
✅ No console errors
✅ API response times < 2s for cached requests
✅ Demo completes in exactly 4 minutes

## What's Included

✅ Complete backend with 9 API endpoints
✅ Complete frontend with 3 pages and 12 components
✅ SQLite database with 8 prospects and 6 partners
✅ Intent scoring algorithm (0–100)
✅ Stall detection engine with root cause analysis
✅ LLM-powered sequence generation (4 personas, 3 emails each)
✅ Compliance checking (banned phrases, unsubscribe link, word count)
✅ Re-engagement email generation
✅ 24-hour caching to avoid re-hitting Groq API
✅ Professional UI with custom design system
✅ Comprehensive documentation (4 guides)

## What's Not Included

❌ Docker (runs locally)
❌ Cloud deployment (localhost only)
❌ Authentication (demo only)
❌ Rate limiting (demo only)
❌ Unit tests (manual testing via DEMO_CHECKLIST.md)
❌ Production database (SQLite only)
❌ Email sending (generation only)
❌ Analytics/logging (basic only)

## Next Steps (Post-Hackathon)

1. **Add authentication** (JWT)
2. **Deploy to cloud** (AWS/GCP with Docker)
3. **Replace SQLite** with PostgreSQL
4. **Add email sending** (SendGrid/Mailgun)
5. **Add analytics** (track opens, clicks, replies)
6. **Add more prospects** (real data from CRM)
7. **Add A/B testing** (test different email variants)
8. **Add feedback loop** (learn from replies)
9. **Add more personas** (expand beyond 4)
10. **Add more LLM models** (GPT-4, Claude, etc.)

## Contact & Support

- **Evaluators**: Blostem engineering and product team
- **Demo Date**: May 9, 2025
- **Demo Location**: In-person (Noida)
- **Demo Duration**: 4 minutes
- **Success Metric**: "Works, looks professional, tells a clear story"

---

**Built for**: Blostem AI Builder Hackathon
**Built by**: Solo hackathon participant
**Tech Stack**: FastAPI + React + LangChain + Groq + SQLite
**Status**: Ready for demo
