"""
config.py — Central configuration for Multi-Agent Assistant
"""

import os
from dotenv import load_dotenv

load_dotenv()

# ── LLM Settings ──────────────────────────────────────────────────────────────
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
MODEL_NAME     = os.getenv("MODEL_NAME", "gpt-4o-mini")   # cheap & fast default
TEMPERATURE    = float(os.getenv("TEMPERATURE", "0"))

# ── Agent Settings ────────────────────────────────────────────────────────────
MAX_ITERATIONS = int(os.getenv("MAX_ITERATIONS", "10"))   # guard against infinite loops
VERBOSE        = os.getenv("VERBOSE", "true").lower() == "true"

# ── Validation ────────────────────────────────────────────────────────────────
if not OPENAI_API_KEY:
    raise EnvironmentError(
        "OPENAI_API_KEY is not set. Copy .env.example → .env and add your key."
    )
