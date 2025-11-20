# notifiers/telegram_notifier.py
import os
import requests

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

def send_telegram(title: str, link: str, short_desc: str):
    if not BOT_TOKEN or not CHAT_ID:
        print("Telegram not configured.")
        return
    text = f"*{title}*\n{short_desc}\n{link}"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "Markdown",
        "disable_web_page_preview": False
    }
    r = requests.post(API_URL, data=payload, timeout=10)
    if r.status_code != 200:
        print("Telegram send failed:", r.status_code, r.text)
    return r.status_code, r.text
