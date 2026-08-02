"""Generates an algorithmic marathon training plan leading up to race day.

The plan is a generic, progressively-overloading structure (build weeks with
a periodic cutback week, then a taper) parameterized by race date, plan
length, and long-run mileage targets. It is not a copy of any specific
published coach's plan.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta

import pandas as pd

DAY_LABELS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


@dataclass
class PlanConfig:
    race_date: date
    weeks: int = 18
    start_long_run_miles: float = 8
    peak_long_run_miles: float = 20
    taper_weeks: int = 3
    cutback_every: int = 4


def _long_run_progression(cfg: PlanConfig) -> list[float]:
    """Return one long-run mileage target per week, build weeks then taper."""
    build_weeks = cfg.weeks - cfg.taper_weeks
    progression: list[float] = []
    for i in range(build_weeks):
        frac = i / (build_weeks - 1) if build_weeks > 1 else 1.0
        ideal = cfg.start_long_run_miles + frac * (cfg.peak_long_run_miles - cfg.start_long_run_miles)
        is_cutback = (i + 1) % cfg.cutback_every == 0 and i != build_weeks - 1
        progression.append(round(ideal * 0.7, 1) if is_cutback else round(ideal, 1))

    taper_targets = [cfg.peak_long_run_miles * 0.6, cfg.peak_long_run_miles * 0.4]
    for j in range(cfg.taper_weeks - 1):
        target = taper_targets[j] if j < len(taper_targets) else taper_targets[-1]
        progression.append(round(target, 1))
    progression.append(26.2)  # race week "long run" is the race itself
    return progression


def _race_week_workouts(long_run_miles: float) -> dict[int, tuple[str, float, str]]:
    return {
        0: ("Rest", 0, "Full rest, hydrate and eat normally."),
        1: ("Easy Run", 3, "Easy shakeout, stay relaxed."),
        2: ("Rest", 0, "Rest or light stretching."),
        3: ("Easy Run", 2, "Short shakeout with a few strides."),
        4: ("Rest", 0, "Rest, lay out race gear and bib."),
        5: ("Rest", 0, "Rest, carb-load, hydrate."),
        6: ("Race Day - Marathon!", long_run_miles, "This is it - good luck!"),
    }


def _build_week_workouts(week_number: int, long_run_miles: float, cutback_every: int) -> dict[int, tuple[str, float, str]]:
    is_cutback = week_number % cutback_every == 0
    easy = max(3, round(long_run_miles * 0.35))
    tempo = max(3, round(long_run_miles * 0.3))
    shakeout = max(2, round(long_run_miles * 0.25))
    return {
        0: ("Rest", 0, "Full rest or gentle stretching."),
        1: ("Easy Run", easy, "Conversational pace."),
        2: ("Cross Training", 0, "30-45 min easy bike/swim/elliptical, or rest."),
        3: ("Speed / Tempo Run", tempo, "Tempo pace or intervals - see notes."),
        4: ("Rest", 0, "Full rest."),
        5: ("Easy Run", shakeout, "Easy pace, keep it comfortable."),
        6: (
            "Cutback Long Run" if is_cutback else "Long Run",
            long_run_miles,
            "Recovery week - easy long run." if is_cutback else "Steady, comfortable long run pace.",
        ),
    }


def generate_training_plan(cfg: PlanConfig) -> pd.DataFrame:
    """Build the full week-by-week, day-by-day training plan as a DataFrame."""
    long_runs = _long_run_progression(cfg)
    rows = []

    for week_idx in range(cfg.weeks):
        week_number = week_idx + 1
        sunday = cfg.race_date - timedelta(weeks=(cfg.weeks - 1 - week_idx))
        monday = sunday - timedelta(days=6)
        long_run_miles = long_runs[week_idx]
        is_race_week = week_idx == cfg.weeks - 1

        daily = (
            _race_week_workouts(long_run_miles)
            if is_race_week
            else _build_week_workouts(week_number, long_run_miles, cfg.cutback_every)
        )

        for offset, day_name in enumerate(DAY_LABELS):
            workout_type, miles, notes = daily[offset]
            rows.append(
                {
                    "week": week_number,
                    "date": monday + timedelta(days=offset),
                    "day_name": day_name,
                    "workout_type": workout_type,
                    "planned_miles": miles,
                    "notes": notes,
                    "is_race_day": is_race_week and offset == 6,
                }
            )

    return pd.DataFrame(rows)


if __name__ == "__main__":
    import os

    from config import DATA_DIR, PEAK_LONG_RUN_MILES, PLAN_WEEKS, RACE_DATE, START_LONG_RUN_MILES, TRAINING_PLAN_CSV

    plan = generate_training_plan(
        PlanConfig(
            race_date=RACE_DATE,
            weeks=PLAN_WEEKS,
            start_long_run_miles=START_LONG_RUN_MILES,
            peak_long_run_miles=PEAK_LONG_RUN_MILES,
        )
    )
    os.makedirs(DATA_DIR, exist_ok=True)
    plan.to_csv(TRAINING_PLAN_CSV, index=False)
    print(f"Wrote {len(plan)} planned workouts to {TRAINING_PLAN_CSV}")
