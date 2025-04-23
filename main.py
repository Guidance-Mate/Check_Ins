import requests
import random
from datetime import datetime, timedelta
import pytz
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Constants
PING_URL = "https://guidancemate.com/run-cron?key=y7WqP93aZkLm8VtB"

TARGET_HOURS = ['08:00', '20:00']
PH_TZ = pytz.timezone("Asia/Manila")
PING_DAY_SEED_DATE = datetime(2025, 4, 23).date()  # base date for pattern

def is_time_near(target):
    now = datetime.now(PH_TZ)
    now_minutes = now.hour * 60 + now.minute
    target_hour, target_minute = map(int, target.split(":"))
    target_minutes = target_hour * 60 + target_minute
    return abs(now_minutes - target_minutes) <= 5

def is_ping_day():
    today = datetime.now(PH_TZ).date()
    days_since_seed = (today - PING_DAY_SEED_DATE).days

    # Simulate a repeating pattern: [2, 3, 2, 3, ...]
    pattern = [2, 3]
    total = 0
    index = 0
    while total < days_since_seed:
        total += pattern[index % len(pattern)]
        index += 1

    return total == days_since_seed

def should_ping():
    return is_ping_day() and any(is_time_near(t) for t in TARGET_HOURS)

def ping():
    try:
        response = requests.get(PING_URL)
        print(f"📡 Ping sent. Response code: {response.status_code}")
        return True
    except Exception as e:
        print(f"❌ Error pinging URL: {e}")
        return False

@app.api_route("/health", methods=["GET", "HEAD"])
def health_check():
    if should_ping():
        ping()
        return JSONResponse(content={"message": "Ping sent successfully."}, status_code=200)
    else:
        return JSONResponse(content={"message": "Not a scheduled ping time or day."}, status_code=200)

@app.get("/checkhealth")
def check_health_now():
    success = ping()
    if success:
        return JSONResponse(content={"message": "Immediate ping sent."}, status_code=200)
    else:
        return JSONResponse(content={"message": "Ping failed."}, status_code=500)

@app.get("/")
def root():
    return JSONResponse(content={"status": "ok"}, status_code=200)
