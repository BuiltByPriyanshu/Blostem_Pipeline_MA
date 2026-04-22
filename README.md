# Blostem Pipeline — B2B Marketing Automation Engine

[![Tests](https://github.com/yourusername/blostem-pipeline/workflows/Tests/badge.svg)](https://github.com/yourusername/blostem-pipeline/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

AI-powered prospect identification and partner re-engagement for Blostem's fintech infrastructure APIs.

## 🎯 What It Does

Blostem Pipeline solves two critical problems for fintech companies:

1. **Prospect Identification** — Identify highest-intent enterprise companies before sales makes a call
2. **Partner Re-engagement** — Detect when signed partners go silent and automatically generate outreach

### Three Core Features

- **Pipeline**: 8 ranked Indian fintech prospects with intent scores (0–100), stakeholder maps, and AI-generated compliance-checked outreach sequences
- **Activation Tracker**: 6 signed partners monitored for post-signup stalls with automated re-engagement
- **Sequence Viewer**: Per-prospect, per-persona 3-email sequences with compliance validation

## ✨ Key Features

### Intent Scoring (0–100)
Weighted formula identifies highest-intent prospects:
- Funding recency (25 pts)
- Hiring signals (25 pts)
- Industry fit (25 pts)
- News momentum (25 pts)

### Stall Detection
Automatic identification of silent partners with root cause analysis:
- **New**: < 3 days (grace period)
- **Active**: < 7 days silent
- **Stalled**: 7–13 days silent
- **Critical**: 14+ days silent

### LLM-Powered Sequences
AI-generated outreach per persona:
- 4 personas: CTO, CFO, Head of Compliance, Head of Product
- 3 emails: Initial, day 5 follow-up, day 12 nudge
- Personalization with prospect details
- Compliance checking on all emails
- 24-hour caching

### Compliance Checking
Rule-based validation:
- Banned phrases detection
- Unsubscribe link validation
- Word count limit (300 words max)
- Auto-appended disclaimer

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+

### Backend Setup

```bash
# Clone and navigate
git clone https://github.com/yourusername/blostem-pipeline.git
cd blostem-pipeline

# Create environment file
cp .env.example .env

# Install dependencies
pip install -r requirements.txt

# Seed database
python seed.py

# Start backend
cd backend
uvicorn main:app --reload
```

Backend runs at: **http://localhost:8000**

### Frontend Setup (New Terminal)

```bash
cd blostem-pipeline/frontend
npm install
npm run dev
```

Frontend runs at: **http://localhost:5173**

## 📊 Demo Data

### 8 Prospects
- PayNearby (91), Fibe (87), Jupiter Money (83), Uni Cards (76)
- KreditBee (71), Slice (68), Smallcase (54), BharatPe (42)

### 6 Partners
- 2 Active, 3 Critical, 1 New
- With activity logs and onboarding milestones

## 🏗️ Architecture

```
Frontend (React 18)
├── Pipeline page
├── Activation Tracker page
└── Sequence Viewer page
        ↓
Backend (FastAPI)
├── Intent Scorer
├── Stall Detector
├── Compliance Checker
├── Sequence Generator
└── Re-engagement Generator
        ↓
SQLite Database
```

## 📚 API Endpoints

### Prospects
- `GET /api/prospects/pipeline` — All prospects
- `GET /api/prospects/{id}` — Single prospect
- `POST /api/prospects/{id}/score` — Re-run scoring

### Sequences
- `POST /api/sequences/generate` — Generate 3-email sequence
- `GET /api/sequences/{prospect_id}` — All sequences

### Activation
- `GET /api/activation/pipeline` — All partners
- `GET /api/activation/{partner_id}` — Single partner
- `POST /api/activation/reengage/{partner_id}` — Generate re-engagement

## 💻 Tech Stack

### Backend
- FastAPI 0.100+
- SQLModel 0.0.13+
- Pydantic 2.0+
- LangChain 0.0.300+
- SQLite

### Frontend
- React 18.2+
- Vite 5.0+
- TailwindCSS 3.4+
- React Router 6.22+

## 📖 Documentation

- [START_HERE.md](START_HERE.md) — Quick start
- [SETUP_GUIDE.md](SETUP_GUIDE.md) — Detailed setup
- [DEMO_CHECKLIST.md](DEMO_CHECKLIST.md) — Demo prep
- [ARCHITECTURE.md](ARCHITECTURE.md) — System design
- [FEATURES_WORKING.md](FEATURES_WORKING.md) — Feature list

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📝 License

MIT License — see [LICENSE](LICENSE) for details.

## 🎯 Demo Flow (4 Minutes)

1. Pipeline — 8 prospects ranked by intent
2. Stakeholder Map — 3 personas with angles
3. Generate Sequence — 3 compliance-checked emails
4. Activation Tracker — 6 partners, 3 stalled
5. Stall Analysis — Root cause and recommendation
6. Re-engage — Generate re-engagement email
7. Closing — Full pipeline story

## 📞 Support

For issues or questions, open an issue on GitHub.

---

**Status**: ✅ Fully Functional and Ready for Demo
