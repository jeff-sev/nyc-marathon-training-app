"""Central configuration loaded from environment variables / a .env file."""
import os
from datetime import datetime

from dotenv import load_dotenv

load_dotenv()

GARMIN_EMAIL = os.getenv("GARMIN_EMAIL")
GARMIN_PASSWORD = os.getenv("GARMIN_PASSWORD")
GARMIN_TOKEN_STORE = os.path.expanduser(os.getenv("GARMIN_TOKEN_STORE", "~/.garminconnect"))

# The Monday Week 1 of the training plan starts. Defaults to this block's
# actual start date; RACE_DATE and PLAN_WEEKS (in training_plan.py) are
# derived from this plus the fixed plan data in plan_data.py.
BLOCK_START_DATE = datetime.strptime(os.getenv("BLOCK_START_DATE", "2026-07-27"), "%Y-%m-%d").date()

DATA_DIR = "data"
TRAINING_PLAN_CSV = os.path.join(DATA_DIR, "training_plan.csv")
ACTIVITIES_CSV = os.path.join(DATA_DIR, "activities.csv")
