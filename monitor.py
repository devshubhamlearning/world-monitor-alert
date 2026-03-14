import requests
import os
import json

SLACK_WEBHOOK = os.environ["SLACK_WEBHOOK"]

URL = "https://www.worldmonitor.app/api/events?timeRange=7d"
FILE = "seen_events.json"

def load_seen():
    try:
        with open(FILE, "r") as f:
            return set(json.load(f))
    except:
        return set()

def save_seen(seen):
    with open(FILE, "w") as f:
        json.dump(list(seen), f)

def send_slack(msg):
    requests.post(SLACK_WEBHOOK, json={"text": msg}, timeout=10)

def check_events():
    print("Fetching events...")

    try:
        r = requests.get(URL, timeout=15)
        r.raise_for_status()
    except Exception as e:
        print("API request failed:", e)
        return

    events = r.json()
    print(f"Total events received: {len(events)}")

    seen = load_seen()
    new_count = 0

    for event in events[:50]:   # limit processing
        eid = event.get("id")

        if eid not in seen:
            seen.add(eid)

            title = event.get("title")
            location = event.get("location")

            message = f"🚨 New Event\n{title}\nLocation: {location}"
            send_slack(message)
            new_count += 1

    save_seen(seen)
    print(f"New alerts sent: {new_count}")

check_events()
print("Finished.")
