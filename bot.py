from telegram.ext import Application, CommandHandler, MessageHandler, filters
from functions import start, video_download, no_text
from decouple import config
import logging

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

def main():
    TOKEN = config("BOT_TOKEN")
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start",start))
    application.add_handler(MessageHandler(filters.Regex(r'^https://twitter.com/.*'),video_download))
    application.add_handler(MessageHandler(filters.ALL,no_text))
    application.run_polling()


if __name__ == "__main__":
    main()