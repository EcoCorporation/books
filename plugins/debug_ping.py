
from pyrogram import Client, filters

@Client.on_message(filters.group & filters.command("ping"))
async def ping_pong(client, message):
    print(f"DEBUG: /ping received in group {message.chat.id}")
    await message.reply_text("Pong! Group handler is working.")

@Client.on_message(filters.group & filters.text)
async def debug_text_monitor(client, message):
    print(f"DEBUG: Text received in group {message.chat.id}: {message.text}")
