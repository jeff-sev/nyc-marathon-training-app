"""CLI script: log in to Garmin Connect and cache running activities to disk.

Run this from a terminal (not from the Streamlit dashboard) the first time,
so any MFA prompt can be answered interactively:

    python sync_data.py

Re-run any time to refresh data/activities.csv with your latest runs.
"""
import os

from config import ACTIVITIES_CSV, DATA_DIR
from garmin_client import connect, fetch_running_activities
from training_plan import RACE_DATE, BLOCK_START_DATE


def main() -> None:
    os.makedirs(DATA_DIR, exist_ok=True)
    start_date = BLOCK_START_DATE
    end_date = RACE_DATE

    print("Logging in to Garmin Connect...")
    client = connect()

    print(f"Fetching running activities from {start_date} to {end_date}...")
    activities = fetch_running_activities(client, start_date, end_date)
    activities.to_csv(ACTIVITIES_CSV, index=False)
    print(f"Saved {len(activities)} activities to {ACTIVITIES_CSV}")


if __name__ == "__main__":
    main()
