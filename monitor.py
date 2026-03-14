import requests
import time
import os

SLACK_WEBHOOK = os.environ["SLACK_WEBHOOK"]

URL = "https://www.worldmonitor.app/api/events?timeRange=7d"

seen_events = set()

def send_slack(msg):
    requests.post(SLACK_WEBHOOK, json={"text": msg})

def check_events():
    global seen_events

    try:
        r = requests.get(URL, timeout=10)
        events = r.json()

        for event in events:
            eid = event.get("id")

            if eid not in seen_events:
                seen_events.add(eid)

                title = event.get("title")
                location = event.get("location")

                message = f"🚨 New Event\n{title}\nLocation: {location}"
                send_slack(message)

    except Exception as e:
        print(e)

while True:
    check_events()
    time.sleep(300)
