from utility import get_tweet, get_HDVideo

async def start(update, context):
    chat_id = update.message.chat_id
    welcome_msg = f"Hello {update.effective_user.first_name}! \nI'm here to download twitter video!"
    task_msg = "Send me a link which contains twitter video"
    await update.effective_message.reply_chat_action('typing')
    await context.bot.send_message(chat_id = chat_id, text = welcome_msg)
    await context.bot.send_message(chat_id = chat_id, text = task_msg)


# handling unexpected input from user
async def no_text(update, context):
    error_msg = "Only Twitter Video Links are allowed !"
    await update.effective_message.reply_chat_action('typing')
    await update.effective_message.reply_text(error_msg)


async def video_download(update, context):
    url = update.message.text
    result = get_tweet(url)
    error_msg = "No video found in this url"

    if not result or not result.get("includes", None):
        await update.effective_message.reply_chat_action('typing')
        await update.effective_message.reply_text(text= error_msg)
        return

    video_url = get_HDVideo(result["includes"]["media"])

    if not video_url:
        await update.effective_message.reply_chat_action('typing')
        await update.effective_message.reply_text(text= error_msg)
        return

    await update.effective_message.reply_chat_action('upload_video')
    try:
        # upload directly video
        await context.bot.send_video(chat_id = update.message.chat_id, video= video_url)
    except:
        # send video link if bot api reaches its upload limit
        await context.bot.send_message(chat_id= update.message.chat_id, text= video_url)

    
