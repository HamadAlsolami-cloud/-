
import os
import requests
from datetime import datetime, timezone

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
FINNHUB_KEY = os.getenv("FINNHUB_API_KEY")

BASE_URL = "https://finnhub.io/api/v1"

# قائمة الأسهم المراقبة - قابلة للتعديل
WATCHLIST = [
    "AAPL", "TSLA", "NVDA", "AMD",
    "PLTR", "SOFI", "BBAI", "ONDS"
]

def send_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    response = requests.post(
        url,
        data={
            "chat_id": CHAT_ID,
            "text": text,
            "disable_web_page_preview": True
        },
        timeout=20
    )
    response.raise_for_status()

def get_news():
    url = f"{BASE_URL}/news"

    response = requests.get(
        url,
        params={
            "category": "general",
            "token": FINNHUB_KEY
        },
        timeout=20
    )
    response.raise_for_status()
    return response.json()

def get_quote(symbol):
    response = requests.get(
        f"{BASE_URL}/quote",
        params={
            "symbol": symbol,
            "token": FINNHUB_KEY
        },
        timeout=20
    )
    response.raise_for_status()
    return response.json()

def main():
    if not TOKEN or not CHAT_ID or not FINNHUB_KEY:
        raise ValueError("Missing Telegram or Finnhub settings")

    message = "🇺🇸 فرص السوق الأمريكي\n"
    message += "━━━━━━━━━━━━━━\n"
    message += "📊 حركة الأسهم المراقبة\n\n"

    for symbol in WATCHLIST:
        try:
            quote = get_quote(symbol)

            price = quote.get("c", 0)
            change = quote.get("dp", 0)

            if not price:
                continue

            icon = "🟢" if change > 0 else "🔴" if change < 0 else "⚪"

            message += (
                f"{icon} {symbol}\n"
                f"السعر: ${price:.4f}\n"
                f"التغير: {change:+.2f}%\n\n"
            )

        except Exception as error:
            print(f"Quote error {symbol}: {error}")

    message += "━━━━━━━━━━━━━━\n"
    message += "📰 آخر أخبار السوق الأمريكي\n\n"

    try:
        news = get_news()

        for item in news[:5]:
            title = item.get("headline", "خبر جديد")
            link = item.get("url", "")

            message += f"🔹 {title}\n{link}\n\n"

    except Exception as error:
        print(f"News error: {error}")
        message += "تعذر جلب الأخبار حالياً.\n"

    message += "\nالمصدر: Finnhub"

    send_message(message)

if __name__ == "__main__":
    main()
