import requests
from datetime import datetime
import pytz

# Settings
PING_URL = "https://guidancemate.com/run-cron?key=UHq38qh3q02@!"
TARGET_HOURS = ['08:00', '20:00']
PH_TZ = pytz.timezone("Asia/Manila")

def should_ping():
    now_ph = datetime.now(PH_TZ)
    current_time = now_ph.strftime('%H:%M')
    print(f"⏰ Current time in PH: {current_time}")
    return current_time in TARGET_HOURS

def ping():
    try:
        response = requests.get(PING_URL)
        print(f"📡 Ping sent. Response code: {response.status_code}")
    except Exception as e:
        print(f"❌ Error pinging URL: {e}")

if __name__ == "__main__":
    if should_ping():
        ping()
    else:
        print("⏭ Not the scheduled time. No ping sent.")
