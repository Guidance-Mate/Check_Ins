import requests
from datetime import datetime
import pytz
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Initialize FastAPI app
app = FastAPI()

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Settings
PING_URL = "https://guidancemate.com/run-cron?key=UHq38qh3q02@!"
TARGET_HOURS = ['08:00', '20:00']
PH_TZ = pytz.timezone("Asia/Manila")

def is_time_near(target):
    now = datetime.now(PH_TZ)
    now_minutes = now.hour * 60 + now.minute
    target_hour, target_minute = map(int, target.split(":"))
    target_minutes = target_hour * 60 + target_minute
    return abs(now_minutes - target_minutes) <= 5

def should_ping():
    return any(is_time_near(target) for target in TARGET_HOURS)

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
        return JSONResponse(content={"message": "Not the scheduled time. No ping sent."}, status_code=200)

@app.get("/")
def root():
    return JSONResponse(content={"status": "ok"}, status_code=200)
