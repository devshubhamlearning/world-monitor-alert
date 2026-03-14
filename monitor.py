import requests
import os
import json

SLACK_WEBHOOK = os.environ["SLACK_WEBHOOK"]

URL = "https://www.worldmonitor.app/api/events?timeRange=7d"

headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json"
}

def send_slack(msg):
    requests.post(SLACK_WEBHOOK, json={"text": msg}, timeout=10)

def check_events():
    print("Fetching events...")

    r = requests.get(URL, headers=headers, timeout=15)

    if r.status_code != 200:
        print("Request failed:", r.status_code, r.text)
        return

    events = r.json()
    print("Events received:", len(events))

check_events()
