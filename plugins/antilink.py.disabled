import re
from pyrogram import Client, filters, enums
from utils import get_settings
from info import ADMINS

@Client.on_message(filters.group & filters.text & filters.incoming)
async def antilink_check(client, message):
    if message.chat.type not in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        return

    text = message.text
    if not text:
        return

    # Check for links
    # Simple regex for http/https links and telegram links
    url_pattern = re.compile(r'(https?://\S+|t\.me/\S+|telegram\.me/\S+)')
    if not url_pattern.search(text):
        return

    # Check settings
    settings = await get_settings(message.chat.id)
    if not settings.get('antilink', False):
        return

    # Check if user is admin
    user_id = message.from_user.id
    if user_id in ADMINS:
        return

    member = await client.get_chat_member(message.chat.id, user_id)
    if member.status in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER]:
        return

    # Delete message
    try:
        await message.delete()
        # Optional: Send a warning message and delete it after a few seconds
        # warning = await message.reply_text(f"Hey {message.from_user.mention}, links are not allowed in this group!")
        # await asyncio.sleep(5)
        # await warning.delete()
    except Exception as e:
        print(f"Error deleting message in antilink: {e}")
