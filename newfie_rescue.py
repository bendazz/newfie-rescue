from datetime import date

import anthropic
from dotenv import load_dotenv

load_dotenv()  # the key comes from .env
client = anthropic.Anthropic()
MODEL = "claude-haiku-5-5"
DOG = "Nana"

# One training swim per row.
LOG = [
    {"date": "2027-05-08", "drill": "retrieve", "meters": 20, "seconds": 40},
    {"date": "2027-05-22", "drill": "retrieve", "meters": 30, "seconds": 50},
    {"date": "2027-06-05", "drill": "line_carry", "meters": 30, "seconds": 60},
    {"date": "2027-06-12", "drill": "retrieve", "meters": 40, "seconds": 50},
    {"date": "2027-06-26", "drill": "line_carry", "meters": 40, "seconds": 64},
    {"date": "2027-07-03", "drill": "boat_tow", "meters": 25, "seconds": 100},
    {"date": "2027-07-10", "drill": "retrieve", "meters": 50, "seconds": 50},
    {"date": "2027-07-17", "drill": "victim_rescue", "meters": 30, "seconds": 75},
    {"date": "2027-07-24", "drill": "line_carry", "meters": 60, "seconds": 80},
    {"date": "2027-07-31", "drill": "boat_tow", "meters": 40, "seconds": 125},
    {"date": "2027-08-07", "drill": "victim_rescue", "meters": 50, "seconds": 100},
    {"date": "2027-08-21", "drill": "boat_tow", "meters": 50, "seconds": 125},
    {"date": "2027-08-28", "drill": "victim_rescue", "meters": 60, "seconds": 100},
    {"date": "2027-09-11", "drill": "victim_rescue", "meters": 70, "seconds": 100},
]
DRILLS = ["retrieve", "line_carry", "boat_tow", "victim_rescue"]

#---------helper functions--------------

def parse_date(text):
    try:
        return date.fromisoformat(text)
    except ValueError:
        raise ValueError(f"'{text}' is not a real date in YYYY-MM-DD form.") from None

def sessions_for(drill):
    if drill not in DRILLS:
        raise ValueError(f"'{drill}' isn't a drill in the log. Drills: {', '.join(DRILLS)}.")
    swims = [swim for swim in LOG if swim["drill"] == drill]
    return sorted(swims, key=lambda swim: swim["date"])

def pace(swim):
    return swim["meters"] / swim["seconds"]

#----------------tools-----------------------

def find_sessions(drill="any", start_date="2000-01-01", end_date="2100-12-31"):
    start, end = parse_date(start_date), parse_date(end_date)
    if start > end:
        raise ValueError("start_date is after end_date.")
    swims = LOG if drill == "any" else sessions_for(drill)
    return [
        {**swim, "pace_m_per_s": round(pace(swim), 2)}
        for swim in swims
        if start <= parse_date(swim["date"]) <= end
    ]

# Each bad call is wrapped in try/except so the script keeps going
# and we can see every error message in one run.

# Bad drill: caught by sessions_for
try:
    print(find_sessions(drill="swimming"))
except ValueError as err:
    print("Error:", err)
print("\n\n")

# Date in the wrong format: caught by parse_date
try:
    print(find_sessions(start_date="July 1, 2027"))
except ValueError as err:
    print("Error:", err)
print("\n\n")

# Date that doesn't exist: caught by parse_date
try:
    print(find_sessions(end_date="2027-06-31"))
except ValueError as err:
    print("Error:", err)
print("\n\n")

# Dates in the wrong order: caught by find_sessions
try:
    print(find_sessions(start_date="2027-08-31", end_date="2027-08-01"))
except ValueError as err:
    print("Error:", err)

