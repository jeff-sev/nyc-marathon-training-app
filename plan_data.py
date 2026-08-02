"""Literal NYC Marathon 2026 14-week training plan.

Unlike a generic algorithmic build, this is a specific, hand-authored plan
(sessions, pacing, strength work) targeting one runner's known limiter -
neuromuscular durability exposed by a mile-45 failure at Burning River 50.
training_plan.py lays this data out on a calendar; nothing here should be
"optimized" or regenerated - edit it directly if the plan itself changes.
"""

PLAN_META = {
    "race_name": "TCS New York City Marathon",
    "race_day_note": "Sunday, November 1, 2026",
    "block_start_note": "Week of July 27, 2026 (3 days post-Burning River 50)",
    "running_days_per_week": 6,
    "peak_weekly_miles": "58-60",
    "quality_days": "Tuesday and Thursday, long run Sunday",
    "goal_marathon_pace": "8:00-8:15/mi (~3:30-3:35 finish)",
    "goal_pace_basis": "Set off a 1:37 half, not the 4:24 marathon. Recalibrate after the Week 10 tune-up half.",
    "primary_limiter": (
        "Neuromuscular durability. Built around the mile-45 failure at Burning River - "
        "legs losing force production, not fuel. That means downhill work, late-run "
        "quality, and real strength training, not just aerobic volume."
    ),
}

PACE_GUIDE = [
    {"zone": "Recovery", "pace": "10:15-11:00", "feel": "Conversational, almost lazy"},
    {"zone": "Easy", "pace": "9:30-10:15", "feel": "Comfortable, nose-breathing"},
    {"zone": "Marathon (MP)", "pace": "8:00-8:15", "feel": 'Controlled, "all day"'},
    {"zone": "Threshold (T)", "pace": "7:25-7:40", "feel": "Comfortably hard, ~1hr race effort"},
    {"zone": "10K", "pace": "7:05-7:15", "feel": "Hard, controlled"},
    {"zone": "5K / VO2", "pace": "6:45-6:55", "feel": "Hard, 3-5 min repeat effort"},
    {"zone": "Strides", "pace": "~6:00 effort", "feel": "Relaxed and fast, not a sprint"},
]

STRENGTH_SESSIONS = {
    "A": {
        "name": "Session A - bilateral / posterior",
        "exercises": [
            "Back squat or goblet squat - 3x6",
            "Romanian deadlift - 3x8",
            "Single-leg calf raise - 3x12",
            "Copenhagen plank - 3x20s/side",
        ],
    },
    "B": {
        "name": "Session B - unilateral / stability",
        "exercises": [
            "Bulgarian split squat - 3x8/leg",
            "Hip thrust - 3x8",
            "Slow eccentric step-downs - 3x10/leg",
            "Side plank with leg lift - 3x10/side",
        ],
    },
}

STRENGTH_LOADING_NOTES = (
    "Weeks 1-2 bodyweight only. Weeks 3-9 add load progressively - by Week 9 the "
    "squats and RDLs should feel genuinely heavy. Weeks 10-13 maintain the movements "
    "at reduced load. Week 14, stop after Monday."
)

COURSE_NOTES = [
    {"mile": "1", "note": "Verrazzano climb. Go out slower than feels right - everyone banks time here and pays for it."},
    {"mile": "2", "note": "Steep downhill off the bridge. Do not let the legs run away."},
    {
        "mile": "15-16",
        "note": (
            "Queensboro Bridge climb, then a fast downhill onto First Ave with 16 miles "
            "already in the legs. This is your mile-45 moment. All the downhill training points here."
        ),
    },
    {"mile": "16-19", "note": "First Avenue. Crowd noise pulls people 20 sec/mi too fast. Hold your number."},
    {"mile": "20", "note": "Willis Ave Bridge into the Bronx. Quiet, exposed, often where it unravels."},
    {"mile": "23", "note": "Fifth Avenue climb - a long, grinding rise when you're emptiest."},
    {"mile": "24-26", "note": "Central Park rollers to the finish."},
]

FUELING_NOTES = [
    "Practice 60-90g carbs/hr on every long run and every MP session.",
    "Fix your race-day plan by Week 8 and don't change it.",
    "NYC has fluid stations roughly every mile from mile 3 - carry your own gels.",
]

BLOCK_RULES = [
    "Easy days are actually easy. The single most common way this plan fails is easy days "
    "creeping to 9:00 pace, leaving nothing for Tuesday and Thursday.",
    "If you have to drop a session, drop Tuesday, not Thursday. Specificity beats sharpness.",
    "Downhill soreness is expected. Downhill knee pain is not. Back off the grade if the second signal appears.",
    "Reassess after Week 10. The half result is real data; the current MP is an estimate.",
    "Never make up a missed week. Rejoin the plan where the calendar is.",
]

DOWNHILL_PROTOCOL = (
    "Land under your hips, quick cadence, resist the urge to brake or over-stride. You want "
    "controlled eccentric loading, not free speed. Expect real soreness for 48h after the "
    "first two sessions - that's the adaptation you're buying."
)


def _day(day_name, session, planned_miles, workout_type, strength=None, notes=""):
    return {
        "day_name": day_name,
        "session": session,
        "planned_miles": planned_miles,
        "workout_type": workout_type,
        "strength": strength,
        "notes": notes,
    }


WEEKS = [
    {
        "week": 1,
        "phase": "Recovery",
        "label": "Jul 27-Aug 2",
        "approx_miles": "~13 mi",
        "week_note": "No strength this week. No strides. If anything feels sharp rather than sore, take the day.",
        "days": [
            _day("Mon", "Walk 20-30 min", 0, "walk"),
            _day("Tue", "Walk 30 min or off", 0, "walk"),
            _day("Wed", "Walk 30 min", 0, "walk"),
            _day("Thu", "Easy 3", 3, "easy"),
            _day("Fri", "Off", 0, "rest"),
            _day("Sat", "Easy 4", 4, "easy"),
            _day("Sun", "Easy 5", 5, "easy"),
        ],
    },
    {
        "week": 2,
        "phase": "Recovery",
        "label": "Aug 3-9",
        "approx_miles": "~25 mi",
        "week_note": "",
        "days": [
            _day("Mon", "Easy 4 + Strength A (bodyweight only)", 4, "easy", "A"),
            _day("Tue", "Easy 5 + 4x20s strides", 5, "easy"),
            _day("Wed", "Easy 4", 4, "easy"),
            _day("Thu", "Easy 6", 6, "easy"),
            _day("Fri", "Off + Strength B (bodyweight only)", 0, "rest", "B"),
            _day("Sat", "Easy 4", 4, "easy"),
            _day("Sun", "Easy 8", 8, "easy"),
        ],
    },
    {
        "week": 3,
        "phase": "Rebuild",
        "label": "Aug 10-16",
        "approx_miles": "~34 mi",
        "week_note": "",
        "days": [
            _day("Mon", "Strength A + optional easy 3", 3, "easy", "A"),
            _day("Tue", "6 total: 6x2min @10K, 2min jog", 6, "quality"),
            _day("Wed", "Easy 6", 6, "easy"),
            _day("Thu", "6 total: 20min continuous @ MP", 6, "quality"),
            _day("Fri", "Easy 4 + Strength B", 4, "easy", "B"),
            _day("Sat", "Easy 5", 5, "easy"),
            _day("Sun", "Long 10 easy", 10, "long"),
        ],
    },
    {
        "week": 4,
        "phase": "Rebuild",
        "label": "Aug 17-23",
        "approx_miles": "~40 mi",
        "week_note": "",
        "days": [
            _day("Mon", "Strength A + easy 3", 3, "easy", "A"),
            _day("Tue", "7 total: 4x5min @T, 90s jog", 7, "quality"),
            _day("Wed", "Easy 6", 6, "easy"),
            _day("Thu", "7 total: 2x15min @MP, 3min float", 7, "quality"),
            _day("Fri", "Easy 4 + Strength B", 4, "easy", "B"),
            _day("Sat", "Easy 6", 6, "easy"),
            _day("Sun", "Long 12 easy", 12, "long"),
        ],
    },
    {
        "week": 5,
        "phase": "Rebuild",
        "label": "Aug 24-30",
        "approx_miles": "~45 mi",
        "week_note": "Downhill work begins. " + DOWNHILL_PROTOCOL,
        "days": [
            _day("Mon", "Strength A + easy 4", 4, "easy", "A"),
            _day("Tue", "7 total: 5x5min @T, 90s jog", 7, "quality"),
            _day("Wed", "Easy 7", 7, "easy"),
            _day(
                "Thu",
                "DOWNHILL 8 total: 8x90s controlled downhill on 3-5% grade @ MP effort, jog back up",
                8,
                "quality",
                notes=DOWNHILL_PROTOCOL,
            ),
            _day("Fri", "Easy 5 + Strength B", 5, "easy", "B"),
            _day("Sat", "Easy 6", 6, "easy"),
            _day("Sun", "Long 14, last 3 @ MP", 14, "long"),
        ],
    },
    {
        "week": 6,
        "phase": "Build",
        "label": "Aug 31-Sep 6",
        "approx_miles": "~50 mi",
        "week_note": "",
        "days": [
            _day("Mon", "Strength A + easy 4", 4, "easy", "A"),
            _day("Tue", "8 total: 20min continuous @T, 3min jog, 4x1min @5K", 8, "quality"),
            _day("Wed", "Easy 7", 7, "easy"),
            _day("Thu", "8 total: 3x12min @MP, 2min jog", 8, "quality"),
            _day("Fri", "Easy 5 + Strength B", 5, "easy", "B"),
            _day("Sat", "Easy 6", 6, "easy"),
            _day("Sun", "Long 15 easy", 15, "long"),
        ],
    },
    {
        "week": 7,
        "phase": "Build",
        "label": "Sep 7-13",
        "approx_miles": "~40 mi",
        "week_note": "Down week.",
        "days": [
            _day("Mon", "Strength A + easy 3", 3, "easy", "A"),
            _day("Tue", "6 total: 6x2min @5K, 2min jog", 6, "quality"),
            _day("Wed", "Easy 6", 6, "easy"),
            _day("Thu", "DOWNHILL 7 total: 10x90s controlled downhill", 7, "quality", notes=DOWNHILL_PROTOCOL),
            _day("Fri", "Easy 4 + Strength B", 4, "easy", "B"),
            _day("Sat", "Easy 5", 5, "easy"),
            _day("Sun", "Long 12 easy", 12, "long"),
        ],
    },
    {
        "week": 8,
        "phase": "Build",
        "label": "Sep 14-20",
        "approx_miles": "~54 mi",
        "week_note": "",
        "days": [
            _day("Mon", "Strength A + easy 5", 5, "easy", "A"),
            _day("Tue", "9 total: 2x15min @T, 3min jog", 9, "quality"),
            _day("Wed", "Easy 7", 7, "easy"),
            _day("Thu", "9 total: 8mi continuous @ MP", 9, "quality"),
            _day("Fri", "Easy 5 + Strength B", 5, "easy", "B"),
            _day("Sat", "Easy 6", 6, "easy"),
            _day("Sun", "Long 17, last 5 @ MP", 17, "long"),
        ],
    },
    {
        "week": 9,
        "phase": "Build",
        "label": "Sep 21-27",
        "approx_miles": "~57 mi",
        "week_note": "",
        "days": [
            _day("Mon", "Strength A + easy 5", 5, "easy", "A"),
            _day("Tue", "9 total: 6x1000m @10K, 2min jog", 9, "quality"),
            _day("Wed", "Easy 7", 7, "easy"),
            _day(
                "Thu",
                "BRIDGE SIM 9 total: 5x4min uphill @T effort, controlled downhill return each time",
                9,
                "quality",
            ),
            _day("Fri", "Easy 5 + Strength B", 5, "easy", "B"),
            _day("Sat", "Easy 7", 7, "easy"),
            _day("Sun", "Long 18 easy", 18, "long"),
        ],
    },
    {
        "week": 10,
        "phase": "Build",
        "label": "Sep 28-Oct 4",
        "approx_miles": "~46 mi",
        "week_note": (
            "Tune-up half. Find a local half around Oct 4. Race it honestly; this is your real "
            "fitness test and the number that sets your NYC pacing."
        ),
        "days": [
            _day("Mon", "Strength A (light) + easy 5", 5, "easy", "A"),
            _day("Tue", "7 total: 15min @T", 7, "quality"),
            _day("Wed", "Easy 6", 6, "easy"),
            _day("Thu", "Easy 6 + 6x20s strides", 6, "easy"),
            _day("Fri", "Off", 0, "rest"),
            _day("Sat", "Easy 3 shakeout + 4 strides", 3, "easy"),
            _day(
                "Sun",
                "HALF MARATHON - race it. Then reset your MP off the result.",
                13.1,
                "half_marathon",
            ),
        ],
    },
    {
        "week": 11,
        "phase": "Build",
        "label": "Oct 5-11",
        "approx_miles": "~60 mi",
        "week_note": "Peak week.",
        "days": [
            _day("Mon", "Strength A + easy 5", 5, "easy", "A"),
            _day("Tue", "9 total: 3x10min @T, 2min jog", 9, "quality"),
            _day("Wed", "Easy 7", 7, "easy"),
            _day("Thu", "10 total: progression run, last 6 @ MP", 10, "quality"),
            _day("Fri", "Easy 5 + Strength B", 5, "easy", "B"),
            _day("Sat", "Easy 7", 7, "easy"),
            _day(
                "Sun",
                "Long 21, last 6 @ MP - the key session of the block",
                21,
                "long",
            ),
        ],
    },
    {
        "week": 12,
        "phase": "Taper",
        "label": "Oct 12-18",
        "approx_miles": "~48 mi",
        "week_note": "",
        "days": [
            _day("Mon", "Strength A (reduced load) + easy 5", 5, "easy", "A"),
            _day("Tue", "8 total: 5x1mi @T, 90s jog", 8, "quality"),
            _day("Wed", "Easy 6", 6, "easy"),
            _day("Thu", "8 total: 6mi @ MP", 8, "quality"),
            _day("Fri", "Easy 4 + Strength B (reduced)", 4, "easy", "B"),
            _day("Sat", "Easy 6", 6, "easy"),
            _day("Sun", "Long 16, last 4 @ MP", 16, "long"),
        ],
    },
    {
        "week": 13,
        "phase": "Taper",
        "label": "Oct 19-25",
        "approx_miles": "~36 mi",
        "week_note": "",
        "days": [
            _day("Mon", "Strength A (light, no soreness) + easy 4", 4, "easy", "A"),
            _day("Tue", "7 total: 3x8min @T", 7, "quality"),
            _day("Wed", "Easy 5", 5, "easy"),
            _day("Thu", "6 total: 4mi @ MP", 6, "quality"),
            _day("Fri", "Off", 0, "rest"),
            _day("Sat", "Easy 5", 5, "easy"),
            _day("Sun", "Long 12 easy", 12, "long"),
        ],
    },
    {
        "week": 14,
        "phase": "Taper",
        "label": "Oct 26-Nov 1",
        "approx_miles": "~22 mi + race",
        "week_note": "",
        "days": [
            _day("Mon", "Easy 5", 5, "easy"),
            _day("Tue", "6 total: 3x3min @MP + 4 strides", 6, "quality"),
            _day("Wed", "Easy 4", 4, "easy"),
            _day("Thu", "Easy 4 + 4x20s strides", 4, "easy"),
            _day("Fri", "Off (travel day)", 0, "rest"),
            _day("Sat", "Easy 3 shakeout", 3, "easy"),
            _day("Sun", "TCS NEW YORK CITY MARATHON", 26.2, "race"),
        ],
    },
]
