import requests
from datetime import datetime
import pytz
from fastapi import FastAPI

# Initialize FastAPI app
app = FastAPI()

# Settings
PING_URL = "https://guidancemate.com/run-cron?key=UHq38qh3q02@!"
TARGET_HOURS = ['08:00', '20:00']
PH_TZ = pytz.timezone("Asia/Manila")

def is_time_near(target):
    now = datetime.now(PH_TZ)
    now_minutes = now.hour * 60 + now.minute
    target_hour, target_minute = map(int, target.split(":"))
    target_minutes = target_hour * 60 + target_minute
    return abs(now_minutes - target_minutes) <= 5  # Acceptable ±5 minutes

def should_ping():
    return any(is_time_near(target) for target in TARGET_HOURS)

def ping():
    try:
        response = requests.get(PING_URL)
        print(f"📡 Ping sent. Response code: {response.status_code}")
    except Exception as e:
        print(f"❌ Error pinging URL: {e}")

@app.get("/ping")
@app.head("/ping")  # Allow both GET and HEAD requests
def ping_endpoint():
    if should_ping():
        ping()
        return {"message": "Ping sent successfully."}
    else:
        return {"message": "Not the scheduled time. No ping sent."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
