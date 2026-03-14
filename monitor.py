import requests
from bs4 import BeautifulSoup
import os

SLACK_WEBHOOK = os.environ["SLACK_WEBHOOK"]

URL = "https://www.worldmonitor.app/"

headers = {
    "User-Agent": "Mozilla/5.0"
}

KEYWORDS = [
    "attack",
    "missile",
    "explosion",
    "conflict",
    "military",
    "earthquake",
    "outage"
]


def send_slack(msg):
    requests.post(SLACK_WEBHOOK, json={"text": msg}, timeout=10)


def check_site():
    print("Fetching site...")

    r = requests.get(URL, headers=headers, timeout=20)

    if r.status_code != 200:
        print("Request failed:", r.status_code)
        return

    soup = BeautifulSoup(r.text, "html.parser")

    text = soup.get_text().lower()

    for word in KEYWORDS:
        if word in text:
            send_slack(f"⚠️ Keyword detected on WorldMonitor page: {word}")
            print("Alert sent:", word)


check_site()
print("Finished")
