"""
config.py
Loads environment variables from .env file using python-dotenv.
"""

import os
from dotenv import load_dotenv

load_dotenv()

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
DEFAULT_USER_ID = os.environ.get("DEFAULT_USER_ID", "student_001")
MONTHLY_BUDGET = float(os.environ.get("MONTHLY_BUDGET", "300"))

if not ANTHROPIC_API_KEY:
    raise EnvironmentError(
        "[Config Error] ANTHROPIC_API_KEY is missing. "
        "Please add it to your .env file."
    )
