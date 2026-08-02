"""Central configuration loaded from environment variables / a .env file."""
import os
from datetime import datetime

from dotenv import load_dotenv

load_dotenv()

GARMIN_EMAIL = os.getenv("GARMIN_EMAIL")
GARMIN_PASSWORD = os.getenv("GARMIN_PASSWORD")
GARMIN_TOKEN_STORE = os.path.expanduser(os.getenv("GARMIN_TOKEN_STORE", "~/.garminconnect"))

RACE_DATE = datetime.strptime(os.getenv("RACE_DATE", "2026-11-01"), "%Y-%m-%d").date()
PLAN_WEEKS = int(os.getenv("PLAN_WEEKS", "18"))
START_LONG_RUN_MILES = float(os.getenv("START_LONG_RUN_MILES", "8"))
PEAK_LONG_RUN_MILES = float(os.getenv("PEAK_LONG_RUN_MILES", "20"))

DATA_DIR = "data"
TRAINING_PLAN_CSV = os.path.join(DATA_DIR, "training_plan.csv")
ACTIVITIES_CSV = os.path.join(DATA_DIR, "activities.csv")
