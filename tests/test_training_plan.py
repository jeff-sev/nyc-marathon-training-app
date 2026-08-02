from datetime import date

from training_plan import PlanConfig, generate_training_plan


def test_plan_has_one_row_per_day():
    cfg = PlanConfig(race_date=date(2026, 11, 1), weeks=18)
    plan = generate_training_plan(cfg)
    assert len(plan) == 18 * 7


def test_race_day_is_last_row_and_full_distance():
    cfg = PlanConfig(race_date=date(2026, 11, 1), weeks=18)
    plan = generate_training_plan(cfg)
    race_day = plan[plan["is_race_day"]]
    assert len(race_day) == 1
    assert race_day.iloc[0]["date"] == date(2026, 11, 1)
    assert race_day.iloc[0]["planned_miles"] == 26.2


def test_long_run_builds_toward_peak_without_exceeding_it():
    cfg = PlanConfig(race_date=date(2026, 11, 1), weeks=18, start_long_run_miles=8, peak_long_run_miles=20)
    plan = generate_training_plan(cfg)
    long_runs = plan[plan["workout_type"].isin(["Long Run", "Cutback Long Run"])]
    assert long_runs["planned_miles"].max() <= 20
    assert long_runs["planned_miles"].min() >= 5


def test_shorter_plan_length_is_respected():
    cfg = PlanConfig(race_date=date(2026, 11, 1), weeks=12, taper_weeks=2)
    plan = generate_training_plan(cfg)
    assert plan["week"].max() == 12
    assert len(plan) == 12 * 7
