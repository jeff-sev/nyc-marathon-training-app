"""Lays the literal plan in plan_data.py out on a calendar.

The workouts themselves are fixed, hand-authored data (see plan_data.py).
This module only maps that data onto real dates, anchored on
config.BLOCK_START_DATE (the Monday the plan's Week 1 starts).
"""
from __future__ import annotations

from datetime import date, timedelta

import pandas as pd

from config import BLOCK_START_DATE
from plan_data import WEEKS

DAY_OFFSETS = {"Mon": 0, "Tue": 1, "Wed": 2, "Thu": 3, "Fri": 4, "Sat": 5, "Sun": 6}

PLAN_WEEKS = len(WEEKS)
RACE_DATE = BLOCK_START_DATE + timedelta(days=PLAN_WEEKS * 7 - 1)


def generate_training_plan(block_start_date: date = BLOCK_START_DATE) -> pd.DataFrame:
    """Build the full week-by-week, day-by-day training plan as a DataFrame."""
    rows = []
    is_last_week_number = WEEKS[-1]["week"]

    for week in WEEKS:
        week_start = block_start_date + timedelta(weeks=week["week"] - 1)
        is_last_week = week["week"] == is_last_week_number

        for day in week["days"]:
            day_date = week_start + timedelta(days=DAY_OFFSETS[day["day_name"]])
            rows.append(
                {
                    "week": week["week"],
                    "date": day_date,
                    "day_name": day["day_name"],
                    "phase": week["phase"],
                    "week_note": week["week_note"],
                    "workout_type": day["workout_type"],
                    "planned_miles": day["planned_miles"],
                    "session": day["session"],
                    "strength_session": day["strength"],
                    "notes": day["notes"],
                    "is_long_run": day["day_name"] == "Sun",
                    "is_race_day": is_last_week and day["day_name"] == "Sun",
                }
            )

    return pd.DataFrame(rows)


if __name__ == "__main__":
    import os

    from config import DATA_DIR, TRAINING_PLAN_CSV

    plan = generate_training_plan()
    os.makedirs(DATA_DIR, exist_ok=True)
    plan.to_csv(TRAINING_PLAN_CSV, index=False)
    print(f"Wrote {len(plan)} planned workouts to {TRAINING_PLAN_CSV} (race day {RACE_DATE})")
