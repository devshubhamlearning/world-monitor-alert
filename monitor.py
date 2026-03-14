import requests
import time
import os

SLACK_WEBHOOK = os.getenv("SLACK_WEBHOOK")

URL = "https://www.worldmonitor.app/api/events?timeRange=7d"

seen_events = set()

def send_slack(msg):
    payload = {
        "text": msg
    }
    requests.post(SLACK_WEBHOOK, json=payload)

def check_events():
    global seen_events
    try:
        r = requests.get(URL, timeout=10)
        events = r.json()

        for event in events:
            eid = event.get("id")
            title = event.get("title")
            location = event.get("location")

            if eid not in seen_events:
                seen_events.add(eid)

                message = f"""
🚨 *New Global Event*

*Event:* {title}
*Location:* {location}
Source: World Monitor
"""
                send_slack(message)

    except Exception as e:
        print("Error:", e)

while True:
    check_events()
    time.sleep(300)
