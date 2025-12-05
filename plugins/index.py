

import logging, re, asyncio, time
from utils import temp
from info import ADMINS, FILTER_BY_EXTENSION
from pyrogram import Client, filters, enums
from pyrogram.errors import FloodWait, MessageNotModified
from pyrogram.errors.exceptions.bad_request_400 import ChannelInvalid, ChatAdminRequired, UsernameInvalid, UsernameNotModified
from info import INDEX_REQ_CHANNEL as LOG_CHANNEL
from database.ia_filterdb import save_file, is_allowed_file, save_checkpoint, get_checkpoint, delete_checkpoint, get_all_checkpoints
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
lock = asyncio.Lock()

# Indexing settings
CHECKPOINT_INTERVAL = 100      # Save checkpoint every N messages
PROGRESS_UPDATE_INTERVAL = 3   # Update progress every N seconds


def format_progress(current, stats, paused=False):
    """Format progress message for indexing."""
    status = "⏸️ **Paused**" if paused else "📥 **Indexing...**"
    filtered_text = f"\n🚫 Filtered: `{stats.get('filtered', 0)}`" if FILTER_BY_EXTENSION else ""
    return (
        f"{status}\n\n"
        f"📊 Messages processed: `{current}`\n"
        f"✅ Saved: `{stats['total']}`\n"
        f"🔄 Duplicates: `{stats['duplicate']}`\n"
        f"🗑️ Deleted: `{stats['deleted']}`\n"
        f"📄 No media: `{stats['no_media']}`\n"
        f"⚠️ Unsupported: `{stats['unsupported']}`"
        f"{filtered_text}\n"
        f"❌ Errors: `{stats['errors']}`"
    )


@Client.on_callback_query(filters.regex(r'^index'))
async def index_files(bot, query):
    if query.data.startswith('index_cancel'):
        temp.CANCEL = True
        return await query.answer("Cancelling Indexing... Progress will be saved.")
    _, raju, chat, lst_msg_id, from_user = query.data.split("#")
    if raju == 'reject':
        await query.message.delete()
        await bot.send_message(
            int(from_user),
            f'Your Submission for indexing {chat} has been declined by our moderators.',
            reply_to_message_id=int(lst_msg_id)
        )
        return

    if lock.locked():
        return await query.answer('Wait until previous process complete.', show_alert=True)
    msg = query.message

    await query.answer('Processing...⏳', show_alert=True)
    if int(from_user) not in ADMINS:
        await bot.send_message(
            int(from_user),
            f'Your Submission for indexing {chat} has been accepted by our moderators and will be added soon.',
            reply_to_message_id=int(lst_msg_id)
        )
    await msg.edit(
        "Starting Indexing",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton('⏸️ Pause', callback_data='index_cancel')]]
        )
    )
    try:
        chat = int(chat)
    except:
        chat = chat
    await index_files_to_db(int(lst_msg_id), chat, msg, bot)


@Client.on_message(filters.private & filters.command('index'))
async def send_for_index(bot, message):
    msg = await bot.ask(message.chat.id, "**📥 Send me your channel's last post link or forward the last message from your index channel.**\n\n💡 Tips:\n• Use /setskip <number> to skip messages\n• Use /resume to continue paused indexing\n• Indexing auto-saves progress every 100 messages")
    if msg.forward_from_chat and msg.forward_from_chat.type == enums.ChatType.CHANNEL:
        last_msg_id = msg.forward_from_message_id
        chat_id = msg.forward_from_chat.username or msg.forward_from_chat.id
    elif msg.text:
        regex = re.compile("(https://)?(t\.me/|telegram\.me/|telegram\.dog/)(c/)?(\d+|[a-zA-Z_0-9]+)/(\d+)$")
        match = regex.match(msg.text)
        if not match:
            return await msg.reply('Invalid link\n\nTry again by /index')
        chat_id = match.group(4)
        last_msg_id = int(match.group(5))
        if chat_id.isnumeric():
            chat_id  = int(("-100" + chat_id))
    else:
        return
    try:
        await bot.get_chat(chat_id)
    except ChannelInvalid:
        return await msg.reply('This may be a private channel / group. Make me an admin over there to index the files.')
    except (UsernameInvalid, UsernameNotModified):
        return await msg.reply('Invalid Link specified.')
    except Exception as e:
        logger.exception(e)
        return await msg.reply(f'Errors - {e}')
    try:
        k = await bot.get_messages(chat_id, last_msg_id)
    except:
        return await message.reply('Make Sure That I am An Admin In The Channel, if channel is private')
    if k.empty:
        return await message.reply('This may be group and I am not an admin of the group.')

    if message.from_user.id in ADMINS:
        # Check for existing checkpoint
        existing = get_checkpoint(chat_id if isinstance(chat_id, int) else chat_id)
        resume_text = ""
        if existing:
            resume_text = f"\n\n⚠️ **Found saved progress at message {existing['current_msg']}**\nUse /resume to continue or start fresh."
        
        buttons = [[
            InlineKeyboardButton('✅ Yes, Start Indexing', callback_data=f'index#accept#{chat_id}#{last_msg_id}#{message.from_user.id}')
        ],[
            InlineKeyboardButton('❌ Close', callback_data='close_data')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        filter_status = "✅ Enabled (ebooks/audiobooks only)" if FILTER_BY_EXTENSION else "❌ Disabled (all files)"
        return await message.reply(
            f'📥 **Index This Channel/Group?**\n\n'
            f'📋 Chat ID: `{chat_id}`\n'
            f'📨 Last Message: `{last_msg_id}`\n'
            f'🔍 Extension Filter: {filter_status}'
            f'{resume_text}',
            reply_markup=reply_markup
        )

    if type(chat_id) is int:
        try:
            link = (await bot.create_chat_invite_link(chat_id)).invite_link
        except ChatAdminRequired:
            return await message.reply('Make sure I am an admin in the chat and have permission to invite users.')
    else:
        link = f"@{message.forward_from_chat.username}"
    buttons = [[
        InlineKeyboardButton('Accept Index', callback_data=f'index#accept#{chat_id}#{last_msg_id}#{message.from_user.id}')
    ],[
        InlineKeyboardButton('Reject Index', callback_data=f'index#reject#{chat_id}#{message.id}#{message.from_user.id}'),
    ]]
    reply_markup = InlineKeyboardMarkup(buttons)
    await bot.send_message(
        LOG_CHANNEL,
        f'#IndexRequest\n\nBy : {message.from_user.mention} (`{message.from_user.id}`)\nChat ID/Username: `{chat_id}`\nLast Message ID: `{last_msg_id}`\nInviteLink: {link}',
        reply_markup=reply_markup
    )
    await message.reply('Thank you for the contribution! Wait for our moderators to verify the files.')


@Client.on_message(filters.command('setskip') & filters.user(ADMINS))
async def set_skip_number(bot, message):
    if ' ' in message.text:
        _, skip = message.text.split(" ", 1)
        try:
            skip = int(skip)
        except:
            return await message.reply("Skip number should be an integer.")
        await message.reply(f"✅ Successfully set SKIP number to **{skip}**\n\nIndexing will start from message #{skip}")
        temp.CURRENT = int(skip)
    else:
        await message.reply(f"**Current skip value:** `{temp.CURRENT}`\n\nUsage: `/setskip <number>`")


@Client.on_message(filters.command('resume') & filters.user(ADMINS))
async def resume_indexing(bot, message):
    """Resume paused/interrupted indexing from checkpoint."""
    checkpoints = get_all_checkpoints()
    
    if not checkpoints:
        return await message.reply("❌ No saved indexing progress found.\n\nUse /index to start indexing a new channel.")
    
    if len(checkpoints) == 1:
        # Auto-resume single checkpoint
        cp = checkpoints[0]
        chat_id = cp['chat_id']
        current_msg = cp['current_msg']
        stats = cp.get('stats', {})
        
        if lock.locked():
            return await message.reply('⏳ Wait until current indexing completes.')
        
        try:
            chat = await bot.get_chat(chat_id)
            chat_name = chat.title or chat_id
        except:
            chat_name = chat_id
        
        buttons = [[
            InlineKeyboardButton('▶️ Resume', callback_data=f'resume_idx#{chat_id}'),
            InlineKeyboardButton('🗑️ Delete', callback_data=f'delete_cp#{chat_id}')
        ]]
        
        return await message.reply(
            f"📥 **Saved Indexing Progress**\n\n"
            f"📋 Channel: `{chat_name}`\n"
            f"📍 Paused at: Message #{current_msg}\n"
            f"✅ Saved: {stats.get('total', 0)} files\n"
            f"🔄 Duplicates: {stats.get('duplicate', 0)}\n\n"
            f"Choose an action:",
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    else:
        # Multiple checkpoints - show list
        text = "📥 **Saved Indexing Progress**\n\n"
        buttons = []
        for i, cp in enumerate(checkpoints[:10], 1):
            chat_id = cp['chat_id']
            current_msg = cp['current_msg']
            stats = cp.get('stats', {})
            text += f"{i}. Chat `{chat_id}` - Message #{current_msg} ({stats.get('total', 0)} saved)\n"
            buttons.append([
                InlineKeyboardButton(f'▶️ Resume #{i}', callback_data=f'resume_idx#{chat_id}'),
                InlineKeyboardButton(f'🗑️', callback_data=f'delete_cp#{chat_id}')
            ])
        
        return await message.reply(text, reply_markup=InlineKeyboardMarkup(buttons))


@Client.on_callback_query(filters.regex(r'^resume_idx#'))
async def resume_callback(bot, query):
    if query.from_user.id not in ADMINS:
        return await query.answer("Only admins can do this!", show_alert=True)
    
    chat_id = query.data.split('#')[1]
    try:
        chat_id = int(chat_id)
    except:
        pass
    
    cp = get_checkpoint(chat_id)
    if not cp:
        return await query.answer("Checkpoint not found!", show_alert=True)
    
    if lock.locked():
        return await query.answer('Wait until current indexing completes.', show_alert=True)
    
    await query.answer("Resuming indexing...")
    
    # Get the last message ID (we need to find it)
    try:
        # Try to get recent messages to find last_msg_id
        async for msg in bot.get_chat_history(chat_id, limit=1):
            last_msg_id = msg.id
            break
    except Exception as e:
        return await query.message.edit(f"❌ Error accessing channel: {e}")
    
    await query.message.edit(
        f"▶️ **Resuming indexing from message #{cp['current_msg']}...**",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('⏸️ Pause', callback_data='index_cancel')]])
    )
    
    await index_files_to_db(last_msg_id, chat_id, query.message, bot, resume=True)


@Client.on_callback_query(filters.regex(r'^delete_cp#'))
async def delete_checkpoint_callback(bot, query):
    if query.from_user.id not in ADMINS:
        return await query.answer("Only admins can do this!", show_alert=True)
    
    chat_id = query.data.split('#')[1]
    try:
        chat_id = int(chat_id)
    except:
        pass
    
    delete_checkpoint(chat_id)
    await query.answer("Checkpoint deleted!")
    await query.message.edit("🗑️ Checkpoint deleted successfully.")


async def index_files_to_db(lst_msg_id, chat, msg, bot, resume=False):
    """
    Index files from a channel to database.
    
    Features:
    - Resume from checkpoint
    - Extension filtering (ebooks/audiobooks)
    - FloodWait handling with auto-retry
    - Progress saving every 100 messages
    - Time-based progress updates
    """
    
    # Initialize or restore stats
    if resume:
        cp = get_checkpoint(chat)
        if cp:
            stats = cp.get('stats', {
                'total': 0, 'duplicate': 0, 'errors': 0,
                'deleted': 0, 'no_media': 0, 'unsupported': 0, 'filtered': 0
            })
            start_from = cp['current_msg']
        else:
            stats = {'total': 0, 'duplicate': 0, 'errors': 0, 'deleted': 0, 'no_media': 0, 'unsupported': 0, 'filtered': 0}
            start_from = temp.CURRENT
    else:
        stats = {'total': 0, 'duplicate': 0, 'errors': 0, 'deleted': 0, 'no_media': 0, 'unsupported': 0, 'filtered': 0}
        start_from = temp.CURRENT
    
    current = start_from
    last_update = time.time()
    
    async with lock:
        temp.CANCEL = False
        try:
            async for message in bot.iter_messages(chat, lst_msg_id, start_from):
                # Check for cancel/pause
                if temp.CANCEL:
                    save_checkpoint(chat, current, stats)
                    await msg.edit(
                        f"⏸️ **Indexing Paused!**\n\n"
                        f"Progress saved at message #{current}\n"
                        f"Use /resume to continue.\n\n"
                        + format_progress(current, stats, paused=True)
                    )
                    return
                
                current += 1
                
                # Time-based progress update (every 3 seconds)
                if time.time() - last_update > PROGRESS_UPDATE_INTERVAL:
                    try:
                        await msg.edit_text(
                            format_progress(current, stats),
                            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('⏸️ Pause', callback_data='index_cancel')]])
                        )
                    except MessageNotModified:
                        pass
                    last_update = time.time()
                
                # Save checkpoint periodically
                if current % CHECKPOINT_INTERVAL == 0:
                    save_checkpoint(chat, current, stats)
                
                # Handle deleted/empty messages
                if message.empty:
                    stats['deleted'] += 1
                    continue
                
                # Handle non-media messages
                if not message.media:
                    stats['no_media'] += 1
                    continue
                
                # Handle unsupported media types
                if message.media not in [enums.MessageMediaType.VIDEO, enums.MessageMediaType.AUDIO, enums.MessageMediaType.DOCUMENT]:
                    stats['unsupported'] += 1
                    continue
                
                media = getattr(message, message.media.value, None)
                if not media:
                    stats['unsupported'] += 1
                    continue
                
                # Filter by extension (ebooks/audiobooks only)
                if FILTER_BY_EXTENSION and not is_allowed_file(getattr(media, 'file_name', '')):
                    stats['filtered'] += 1
                    continue
                
                # Save the file
                media.caption = message.caption
                try:
                    success, code = await save_file(media)
                    if success:
                        stats['total'] += 1
                    elif code == 0:
                        stats['duplicate'] += 1
                    elif code == 2:
                        stats['errors'] += 1
                except Exception as e:
                    stats['errors'] += 1
                    logger.error(f"Error saving file: {e}")
                    
        except FloodWait as e:
            # Save progress before waiting
            save_checkpoint(chat, current, stats)
            wait_time = e.value + 5
            await msg.edit(
                f"⏳ **Rate Limited!**\n\n"
                f"Waiting {wait_time} seconds...\n"
                f"Progress saved at message #{current}\n\n"
                + format_progress(current, stats)
            )
            await asyncio.sleep(wait_time)
            # Resume after wait
            await msg.edit("▶️ Resuming indexing...")
            return await index_files_to_db(lst_msg_id, chat, msg, bot, resume=True)
            
        except Exception as e:
            save_checkpoint(chat, current, stats)
            logger.exception(e)
            await msg.edit(
                f"❌ **Error:** `{e}`\n\n"
                f"Progress saved at message #{current}\n"
                f"Use /resume to continue.\n\n"
                + format_progress(current, stats)
            )
            return
        
        # Successful completion
        delete_checkpoint(chat)
        filtered_text = f"\n🚫 Filtered out: `{stats['filtered']}`" if FILTER_BY_EXTENSION else ""
        await msg.edit(
            f"✅ **Indexing Complete!**\n\n"
            f"📊 Total messages: `{current}`\n"
            f"✅ Files saved: `{stats['total']}`\n"
            f"🔄 Duplicates skipped: `{stats['duplicate']}`\n"
            f"🗑️ Deleted messages: `{stats['deleted']}`\n"
            f"📄 Non-media: `{stats['no_media']}`\n"
            f"⚠️ Unsupported: `{stats['unsupported']}`"
            f"{filtered_text}\n"
            f"❌ Errors: `{stats['errors']}`"
        )

#EbookGuy
