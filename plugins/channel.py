

from pyrogram import Client, filters
from info import CHANNELS
from database.ia_filterdb import save_file

media_filter = filters.document | filters.video

@Client.on_message(filters.chat(CHANNELS) & media_filter)
async def media(bot, message):
    media = getattr(message, message.media.value, None)
    media.caption = message.caption
    _, _, users_to_notify = await save_file(media)
    for user_id, query in users_to_notify:
        try:
            await bot.send_message(
                chat_id=int(user_id),
                text=f"Your requested file **{query}** is now available!\n\nFile Name: {media.file_name}"
            )
        except Exception as e:
            print(f"Failed to notify user {user_id}: {e}")
