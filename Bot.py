import os
import requests
import feedparser
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🦅 Elite Stock Monitor\n"
        "تم تشغيل بوت أخبار الأسهم الأمريكية.\n"
        "اكتب /news للحصول على آخر الأخبار."
    )

async def news(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = "https://feeds.finance.yahoo.com/rss/2.0/headline?s=AAPL,TSLA,NVDA&region=US&lang=en-US"

    feed = feedparser.parse(url)

    if not feed.entries:
        await update.message.reply_text("لا توجد أخبار متاحة حالياً.")
        return

    for item in feed.entries[:5]:
        title = item.title
        link = item.link

        message = f"📰 {title}\n\n🔗 {link}"
        await update.message.reply_text(message)

def main():
    if not TOKEN:
        raise ValueError("TELEGRAM_BOT_TOKEN غير موجود")

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("news", news))

    print("Elite Stock Monitor Started")
    app.run_polling()

if __name__ == "__main__":
    main()
