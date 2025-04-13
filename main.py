import requests
from datetime import datetime
import pytz
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

# Initialize FastAPI app
app = FastAPI()

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

@app.api_route("/ping", methods=["GET", "HEAD"])
def ping_endpoint(request: Request):
    if request.method == "HEAD":
        return JSONResponse(content={"message": "HEAD request received"}, status_code=200)

    if should_ping():
        ping()
        return {"message": "Ping sent successfully."}
    else:
        return {"message": "Not the scheduled time. No ping sent."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
