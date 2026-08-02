from datetime import date, timedelta

from training_plan import RACE_DATE, generate_training_plan


def test_plan_has_one_row_per_day_for_14_weeks():
    plan = generate_training_plan()
    assert len(plan) == 14 * 7


def test_race_day_is_last_sunday_and_full_marathon_distance():
    plan = generate_training_plan()
    race_day = plan[plan["is_race_day"]]
    assert len(race_day) == 1
    assert race_day.iloc[0]["date"] == RACE_DATE
    assert race_day.iloc[0]["planned_miles"] == 26.2
    assert race_day.iloc[0]["date"].strftime("%A") == "Sunday"


def test_default_race_date_matches_2026_nyc_marathon():
    assert RACE_DATE == date(2026, 11, 1)


def test_tune_up_half_marathon_is_week_10():
    plan = generate_training_plan()
    half = plan[plan["workout_type"] == "half_marathon"]
    assert len(half) == 1
    assert half.iloc[0]["week"] == 10
    assert half.iloc[0]["planned_miles"] == 13.1


def test_long_run_peaks_at_21_miles_in_week_11():
    plan = generate_training_plan()
    long_runs = plan[plan["workout_type"] == "long"]
    assert long_runs["planned_miles"].max() == 21
    peak = long_runs[long_runs["planned_miles"] == 21]
    assert peak.iloc[0]["week"] == 11


def test_plan_shifts_with_custom_block_start_date():
    custom_start = date(2027, 1, 4)  # a Monday
    plan = generate_training_plan(block_start_date=custom_start)
    assert plan.iloc[0]["date"] == custom_start
    race_day = plan[plan["is_race_day"]].iloc[0]
    assert race_day["date"] == custom_start + timedelta(weeks=14) - timedelta(days=1)
