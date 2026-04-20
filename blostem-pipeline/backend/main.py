from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.db import init_db, seed_prospects, seed_partners
from backend.routers import prospects, sequences, activation, email, activity

load_dotenv()

app = FastAPI(title="Blostem Pipeline API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(prospects.router)
app.include_router(sequences.router)
app.include_router(activation.router)
app.include_router(email.router)
app.include_router(activity.router)


@app.on_event("startup")
def startup():
    init_db()
    seed_prospects()
    seed_partners()


@app.get("/health")
def health():
    return {"status": "ok"}
