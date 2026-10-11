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

def sessions_for(drill):
    swims = [swim for swim in LOG if swim["drill"] == drill]
    return sorted(swims, key=lambda swim: swim["date"])

print(sessions_for("retrieve"))  
