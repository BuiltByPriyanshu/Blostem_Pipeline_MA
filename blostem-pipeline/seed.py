#!/usr/bin/env python3
import sys
sys.path.insert(0, '.')

from backend.db import init_db, seed_prospects, seed_partners

if __name__ == "__main__":
    init_db()
    p_count = seed_prospects()
    pa_count = seed_partners()
    print(f"Database seeded. {p_count} prospects, {pa_count} partners inserted.")
