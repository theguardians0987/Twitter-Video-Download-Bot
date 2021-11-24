from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from functions import extract_download_links

api_token = "2129729817:AAHapqfPCAL56r9QJtcN6RjYt0ZJaLWPLpc"

def start_command(update, context):
    context.bot.send_message(chat_id = update.message.chat_id,text = f"Hello {update.effective_user.first_name}! \nI'm here to download twitter video!")
    context.bot.send_message(chat_id = update.message.chat_id, text = "Send me only twitter video link")

## handling unexpected input from user
def no_text_handling(update, context):
    update.effective_message.reply_text("Only texts allowed !")
    start_command(update, context)

def video_download(update, context):
    url = update.message.text
    # if not url.startswith('https://www.twitter.com/'):
    #     context.bot.send_message(chat_id = update.message.chat_id, text = "It may not be twitter link !\nCheck once again and send me")
    #     return
        
    l = extract_download_links(url)

    if l is None:
        context.bot.send_message(chat_id = update.message.chat_id, text = "Video not found! Sorry!")
    else:
        context.bot.send_video(chat_id = update.message.chat_id, video= l)


def main():
    updater = Updater(api_token, use_context = True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start",start_command))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command,video_download))
    dispatcher.add_handler(MessageHandler(Filters.all,no_text_handling))
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()