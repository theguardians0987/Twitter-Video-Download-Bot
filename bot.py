from telegram.ext import Application, CommandHandler, MessageHandler, filters
import os
import json
import requests

def bearer_oauth(r):
    r.headers["Authorization"] = f"Bearer {os.environ['BEARER_TOKEN']}"
    r.headers["User-Agent"] = "v2TweetLookupPython"
    return r

api_token = "2129729817:AAHapqfPCAL56r9QJtcN6RjYt0ZJaLWPLpc"

async def start_command(update, context):
    await update.effective_message.reply_chat_action('typing')
    await context.bot.send_message(chat_id = update.message.chat_id,text = f"Hello {update.effective_user.first_name}! \nI'm here to download twitter video!")
    await context.bot.send_message(chat_id = update.message.chat_id, text = "Send me twitter link")

## handling unexpected input from user
async def no_text_handling(update, context):
    await update.effective_message.reply_chat_action('typing')
    await update.effective_message.reply_text("Only Twitter Links are allowed !")


def get_tweet(url):
    id = url.split('?')[0].split("/")[-1]
    expansions = "attachments.media_keys"
    media_fields = "type,url,preview_image_url,variants"
    endpoint = "https://api.twitter.com/2/" + f"tweets?ids={id}&expansions={expansions}&media.fields={media_fields}"
    response = requests.request("GET", endpoint, auth=bearer_oauth)
    if response.status_code != 200:
        return None
    return response.json()


async def video_download(update, context):
    url = update.message.text    
    result = get_tweet(url)
    if result == None:
        await update.effective_message.reply_chat_action('typing')
        await context.bot.send_message(chat_id= update.message.chat_id,text="No video found in this url")

    medias = result["includes"]["media"]
    video_url = None
    for m in medias:
        media_type = m["type"]

        if media_type != "video":
            continue

        variants = m["variants"]
        max_bit_rate = 0
        for v in variants:
            if v["content_type"] == "video/mp4":
                if v["bit_rate"] > max_bit_rate:
                    video_url = v["url"]

    if video_url!= None:
        await update.effective_message.reply_chat_action('upload_video')
        await context.bot.send_video(chat_id = update.message.chat_id,video=video_url)
    else:
        await update.effective_message.reply_chat_action('typing')
        await context.bot.send_message(chat_id= update.message.chat_id,text="No video found in this url")

def main():
    application = Application.builder().token(api_token).build()
    application.add_handler(CommandHandler("start",start_command))
    application.add_handler(MessageHandler(filters.Regex(r'^https://twitter.com/.*'),video_download))
    application.add_handler(MessageHandler(filters.ALL,no_text_handling))
    application.run_polling()


if __name__ == "__main__":
    main()