# NYC Marathon Training Dashboard

A dashboard for tracking a specific 14-week NYC Marathon 2026 training block:
it lays out a hand-authored training plan (see `plan_data.py`), pulls actual
runs from Garmin Connect via
[python-garminconnect](https://github.com/cyberjunky/python-garminconnect),
and shows planned vs. actual progress in a Streamlit dashboard.

> Unofficial project, not affiliated with Garmin or NYRR. Use at your own
> risk - `python-garminconnect` talks to Garmin's undocumented mobile API,
> which can change or rate-limit without notice.

## The plan

`plan_data.py` encodes a specific 14-week build (race day Sunday, November 1,
2026; block starts the week of July 27, 2026, three days post-Burning River
50). It targets one runner's known limiter - neuromuscular durability
exposed by a mile-45 failure in that ultra - with 6 running days/week
peaking at 58-60 miles, quality on Tuesday and Thursday, downhill-specific
work, a Week 10 tune-up half to recalibrate marathon pace, and a Week 11
peak long run (21 miles, last 6 @ marathon pace) before a 3-week taper. It
also carries the pace guide, twice-weekly strength program, NYC course
notes, fueling guidance, and the block's rules - all shown in the
dashboard's sidebar.

This is literal, edit-it-directly data, not an algorithm - if the plan
changes, change `plan_data.py`. `training_plan.py` only maps that data onto
real calendar dates, anchored on `BLOCK_START_DATE`.

## Features

- The full 14-week plan (98 days) laid out on the calendar, with phase
  (Recovery/Rebuild/Build/Taper), the literal session text, strength
  sessions, and per-week notes (e.g. downhill protocol, tune-up half).
- Syncs running activities from Garmin Connect and caches them locally.
- Streamlit dashboard: current week/phase, days to race, planned vs. actual
  daily/weekly mileage, long-run progression, and reference panels for pace
  zones, strength work, course notes, fueling, and block rules.

## Setup

1. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Copy `.env.example` to `.env` and fill in your Garmin Connect credentials:

   ```bash
   cp .env.example .env
   ```

   | Variable | Description |
   | --- | --- |
   | `GARMIN_EMAIL` / `GARMIN_PASSWORD` | Your Garmin Connect login. |
   | `GARMIN_TOKEN_STORE` | Where the login session is cached (default `~/.garminconnect`). |
   | `BLOCK_START_DATE` | The Monday Week 1 starts (default `2026-07-27`). Race day and every week's dates shift automatically if you change this. |

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
   the first time the dashboard runs.

## Project layout

```
plan_data.py          The literal 14-week plan: sessions, strength program,
                       pace guide, course notes, fueling, block rules
config.py              Environment/config loading
training_plan.py        Maps plan_data.py onto real calendar dates
garmin_client.py         Garmin Connect login + activity fetching
sync_data.py             CLI script to refresh cached activity data
dashboard.py              Streamlit dashboard
tests/                    Unit tests for the plan/calendar mapping
data/                     Cached CSVs (gitignored)
```

## Running tests

```bash
pytest
```

## Acknowledgments

Built on top of [cyberjunky/python-garminconnect](https://github.com/cyberjunky/python-garminconnect)
(MIT licensed) for Garmin Connect access.
