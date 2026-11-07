import os
import requests
import feedparser

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": text
    }, timeout=20)

def main():
    if not TOKEN or not CHAT_ID:
        raise ValueError("Telegram settings are missing")

    url = "https://feeds.finance.yahoo.com/rss/2.0/headline?s=AAPL,TSLA,NVDA&region=US&lang=en-US"
    feed = feedparser.parse(url)

    if not feed.entries:
        send_message("🦅 Elite Stock Monitor\nلا توجد أخبار جديدة حالياً.")
        return

    message = "🦅 Elite Stock Monitor\n🇺🇸 أخبار الأسهم الأمريكية\n\n"

    for item in feed.entries[:5]:
        message += f"📰 {item.title}\n{item.link}\n\n"

    send_message(message)

if __name__ == "__main__":
    main()
