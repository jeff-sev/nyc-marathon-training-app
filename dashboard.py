"""Streamlit dashboard comparing the NYC marathon training plan to actual Garmin activities.

Run with:

    streamlit run dashboard.py
"""
import os
from datetime import date

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from config import ACTIVITIES_CSV, DATA_DIR, TRAINING_PLAN_CSV
from plan_data import BLOCK_RULES, COURSE_NOTES, FUELING_NOTES, PACE_GUIDE, PLAN_META, STRENGTH_LOADING_NOTES, STRENGTH_SESSIONS
from training_plan import PLAN_WEEKS, RACE_DATE, generate_training_plan

st.set_page_config(page_title="NYC Marathon Training Dashboard", page_icon="🏙️", layout="wide")


@st.cache_data
def load_plan() -> pd.DataFrame:
    if not os.path.exists(TRAINING_PLAN_CSV):
        plan = generate_training_plan()
        os.makedirs(DATA_DIR, exist_ok=True)
        plan.to_csv(TRAINING_PLAN_CSV, index=False)
    return pd.read_csv(TRAINING_PLAN_CSV, parse_dates=["date"])


def load_activities() -> pd.DataFrame:
    if not os.path.exists(ACTIVITIES_CSV):
        return pd.DataFrame(columns=["date", "distance_miles"])
    return pd.read_csv(ACTIVITIES_CSV, parse_dates=["date"])


st.title("🏙️ NYC Marathon Training Dashboard")

days_to_race = (RACE_DATE - date.today()).days
st.caption(f"{PLAN_META['race_name']} — {RACE_DATE:%A, %B %d, %Y} — {days_to_race} days to go")
st.caption(f"Goal marathon pace: {PLAN_META['goal_marathon_pace']}. {PLAN_META['goal_pace_basis']}")

with st.sidebar:
    st.header("Data")
    st.write("Sync your latest activities from Garmin Connect:")
    st.code("python sync_data.py", language="bash")
    st.caption("Run it from a terminal the first time so an MFA prompt (if any) can be answered.")
    if st.button("🔄 Reload cached data"):
        st.cache_data.clear()
        st.rerun()

    st.header("Reference")
    with st.expander("Pace guide"):
        st.dataframe(pd.DataFrame(PACE_GUIDE), use_container_width=True, hide_index=True)
    with st.expander("Strength program"):
        for session in STRENGTH_SESSIONS.values():
            st.markdown(f"**{session['name']}**")
            for exercise in session["exercises"]:
                st.markdown(f"- {exercise}")
        st.caption(STRENGTH_LOADING_NOTES)
    with st.expander("Course notes"):
        for note in COURSE_NOTES:
            st.markdown(f"**Mile {note['mile']}:** {note['note']}")
    with st.expander("Fueling"):
        for note in FUELING_NOTES:
            st.markdown(f"- {note}")
    with st.expander("Rules for the block"):
        for i, rule in enumerate(BLOCK_RULES, start=1):
            st.markdown(f"{i}. {rule}")

plan = load_plan()
activities = load_activities()

if activities.empty:
    st.info("No Garmin activity data yet. Run `python sync_data.py` from a terminal, then reload.")

daily_actual = (
    activities.groupby("date", as_index=False)["distance_miles"]
    .sum()
    .rename(columns={"distance_miles": "actual_miles"})
    if not activities.empty
    else pd.DataFrame(columns=["date", "actual_miles"])
)

merged = plan.merge(daily_actual, on="date", how="left")
merged["actual_miles"] = merged["actual_miles"].fillna(0)
merged["date"] = merged["date"].dt.date

today = date.today()
to_date = merged[merged["date"] <= today]
total_planned = to_date["planned_miles"].sum()
total_actual = to_date["actual_miles"].sum()
current_week = int(to_date["week"].max()) if not to_date.empty else 1
current_phase = to_date["phase"].iloc[-1] if not to_date.empty else merged["phase"].iloc[0]

col1, col2, col3, col4 = st.columns(4)
col1.metric("Current week", f"{current_week} / {PLAN_WEEKS} ({current_phase})")
col2.metric("Days to race", days_to_race)
col3.metric("Planned miles to date", f"{total_planned:.1f}")
col4.metric("Actual miles to date", f"{total_actual:.1f}", delta=f"{total_actual - total_planned:+.1f}")

st.subheader("Weekly mileage: planned vs. actual")
weekly = merged.groupby("week", as_index=False)[["planned_miles", "actual_miles"]].sum()
fig = go.Figure()
fig.add_bar(x=weekly["week"], y=weekly["planned_miles"], name="Planned")
fig.add_bar(x=weekly["week"], y=weekly["actual_miles"], name="Actual")
fig.update_layout(barmode="group", xaxis_title="Training week", yaxis_title="Miles")
st.plotly_chart(fig, use_container_width=True)

st.subheader("Long run progression (Sundays)")
long_runs = merged[merged["is_long_run"]]
fig2 = go.Figure()
fig2.add_scatter(x=long_runs["week"], y=long_runs["planned_miles"], name="Planned long run", mode="lines+markers")
fig2.add_scatter(x=long_runs["week"], y=long_runs["actual_miles"], name="Actual long run", mode="lines+markers")
fig2.update_layout(xaxis_title="Training week", yaxis_title="Miles")
st.plotly_chart(fig2, use_container_width=True)

st.subheader(f"Week {current_week} plan")
this_week = merged[merged["week"] == current_week][
    ["date", "day_name", "session", "strength_session", "planned_miles", "actual_miles", "notes"]
]
st.dataframe(this_week, use_container_width=True, hide_index=True)

week_note = merged.loc[merged["week"] == current_week, "week_note"].iloc[0]
if isinstance(week_note, str) and week_note:
    st.info(week_note)

with st.expander("Full training plan"):
    st.dataframe(
        merged[
            ["week", "phase", "date", "day_name", "session", "strength_session", "planned_miles", "actual_miles", "notes"]
        ],
        use_container_width=True,
        hide_index=True,
    )
