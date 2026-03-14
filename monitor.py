import requests
import time

BOT_TOKEN = "YOUR_BOT_TOKEN"
CHAT_ID = "YOUR_CHAT_ID"

URL = "https://www.worldmonitor.app/api/events?timeRange=7d"

seen_events = set()

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHAT_ID, "text": msg})

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

                message = f"🚨 New Event\n{title}\nLocation: {location}"
                send_telegram(message)

    except Exception as e:
        print("Error:", e)

while True:
    check_events()
    time.sleep(300)
