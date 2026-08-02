# NYC Marathon Training Dashboard

A small dashboard for tracking NYC Marathon training: it generates a
week-by-week training plan, pulls your actual runs from Garmin Connect via
[python-garminconnect](https://github.com/cyberjunky/python-garminconnect),
and shows planned vs. actual mileage in a Streamlit dashboard.

> Unofficial project, not affiliated with Garmin or NYRR. Use at your own
> risk - `python-garminconnect` talks to Garmin's undocumented mobile API,
> which can change or rate-limit without notice.

## Features

- Algorithmically generated training plan (configurable length, start date
  driven off your race day, and long-run build-up), with a periodic cutback
  week and a taper into race day.
- Syncs your running activities from Garmin Connect and caches them locally.
- Streamlit dashboard comparing planned vs. actual daily/weekly mileage,
  long-run progression, and the current week's workouts.

## Setup

1. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Copy `.env.example` to `.env` and fill in your Garmin Connect credentials
   and race details:

   ```bash
   cp .env.example .env
   ```

   | Variable | Description |
   | --- | --- |
   | `GARMIN_EMAIL` / `GARMIN_PASSWORD` | Your Garmin Connect login. |
   | `GARMIN_TOKEN_STORE` | Where the login session is cached (default `~/.garminconnect`). |
   | `RACE_DATE` | Race day, `YYYY-MM-DD` (defaults to the 2026 NYC Marathon, 2026-11-01). |
   | `PLAN_WEEKS` | Length of the training plan in weeks (default 18). |
   | `START_LONG_RUN_MILES` / `PEAK_LONG_RUN_MILES` | Long-run mileage at the start of the plan and at its peak. |

3. Sync your Garmin activities (run this from a terminal, not the dashboard,
   the first time - it may prompt for an MFA code):

   ```bash
   python sync_data.py
   ```

   This logs in, caches the session token, and writes `data/activities.csv`.
   Re-run it any time to pull your latest runs.

4. Launch the dashboard:

   ```bash
   streamlit run dashboard.py
   ```

   The training plan (`data/training_plan.csv`) is generated automatically
   the first time the dashboard runs, using the settings in `.env`.

## Project layout

```
config.py           Environment/config loading
training_plan.py     Generates the week-by-week training plan
garmin_client.py      Garmin Connect login + activity fetching
sync_data.py          CLI script to refresh cached activity data
dashboard.py           Streamlit dashboard
tests/                 Unit tests for the plan generator
data/                  Cached CSVs (gitignored)
```

## Running tests

```bash
pytest
```

## Acknowledgments

Built on top of [cyberjunky/python-garminconnect](https://github.com/cyberjunky/python-garminconnect)
(MIT licensed) for Garmin Connect access.
