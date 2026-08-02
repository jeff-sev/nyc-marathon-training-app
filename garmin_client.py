"""Thin wrapper around python-garminconnect (cyberjunky) for pulling running activities.

See https://github.com/cyberjunky/python-garminconnect for the underlying library.
"""
from __future__ import annotations

from datetime import date

import pandas as pd
from garminconnect import Garmin

from config import GARMIN_EMAIL, GARMIN_PASSWORD, GARMIN_TOKEN_STORE

METERS_PER_MILE = 1609.344


def connect() -> Garmin:
    """Log in to Garmin Connect, reusing a cached token when available.

    On first run this may prompt for an MFA code on the terminal. The
    resulting session token is cached at GARMIN_TOKEN_STORE, so subsequent
    logins (including from the Streamlit dashboard) succeed silently.
    """
    client = Garmin(GARMIN_EMAIL, GARMIN_PASSWORD, prompt_mfa=lambda: input("Garmin MFA code: ").strip())
    client.login(GARMIN_TOKEN_STORE)
    return client


def _to_miles(meters: float | None) -> float:
    return round((meters or 0) / METERS_PER_MILE, 2)


def _pace_min_per_mile(avg_speed_mps: float | None) -> float | None:
    if not avg_speed_mps:
        return None
    miles_per_second = avg_speed_mps / METERS_PER_MILE
    if miles_per_second <= 0:
        return None
    return round((1 / miles_per_second) / 60, 2)


def fetch_running_activities(client: Garmin, start_date: date, end_date: date) -> pd.DataFrame:
    """Fetch running activities in [start_date, end_date] as a tidy DataFrame."""
    raw = client.get_activities_by_date(start_date.isoformat(), end_date.isoformat(), "running")

    rows = []
    for activity in raw:
        rows.append(
            {
                "activity_id": activity.get("activityId"),
                "date": (activity.get("startTimeLocal") or "")[:10],
                "activity_name": activity.get("activityName"),
                "distance_miles": _to_miles(activity.get("distance")),
                "duration_min": round((activity.get("duration") or 0) / 60, 1),
                "avg_pace_min_per_mile": _pace_min_per_mile(activity.get("averageSpeed")),
                "avg_hr": activity.get("averageHR"),
                "elevation_gain_ft": round((activity.get("elevationGain") or 0) * 3.28084, 1),
            }
        )

    return pd.DataFrame(rows)
