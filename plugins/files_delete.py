

import re, logging
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from info import DELETE_CHANNELS, ADMINS
from database.ia_filterdb import col, sec_col, unpack_new_file_id
from utils import get_size

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Debug: Print DELETE_CHANNELS on load
print(f"[files_delete.py] DELETE_CHANNELS loaded: {DELETE_CHANNELS}")

# Check if DELETE_CHANNELS is valid
if not DELETE_CHANNELS or DELETE_CHANNELS == ['']:
    print("[files_delete.py] WARNING: DELETE_CHANNELS is empty! File delete feature disabled.")
    media_filter = filters.document | filters.video | filters.audio
else:
    media_filter = filters.document | filters.video | filters.audio
    print(f"[files_delete.py] File delete handler active for channels: {DELETE_CHANNELS}")

@Client.on_message(filters.chat(DELETE_CHANNELS) & media_filter)
async def deletemultiplemedia(bot, message):
    """Delete files from database when sent to delete channel"""
    try:
        print(f"[files_delete.py] Handler triggered! Chat: {message.chat.id}, Type: {message.chat.type}")

        for file_type in ("document", "video", "audio"):
        media = getattr(message, file_type, None)
        if media is not None:
            break
    else:
        return

    file_id, file_ref = unpack_new_file_id(media.file_id)
    file_name = getattr(media, 'file_name', 'Unknown')
    file_size = get_size(media.file_size)
    total_deleted = 0

    # Try to delete by file_id first
    result = col.delete_one({'file_id': file_id})
    total_deleted += result.deleted_count
    if not result.deleted_count:
        result = sec_col.delete_one({'file_id': file_id})
        total_deleted += result.deleted_count
    
    # If not found by file_id, try by cleaned file_name + size
    if total_deleted == 0:
        cleaned_name = re.sub(r"(_|\-|\.|\+)", " ", str(media.file_name))
        unwanted_chars = ['[', ']', '(', ')', '{', '}']
        for char in unwanted_chars:
            cleaned_name = cleaned_name.replace(char, '')
        cleaned_name = ' '.join(filter(lambda x: not x.startswith('@'), cleaned_name.split()))
    
        result = col.delete_many({'file_name': cleaned_name, 'file_size': media.file_size})
        total_deleted += result.deleted_count
        if not result.deleted_count:
            result = sec_col.delete_many({'file_name': cleaned_name, 'file_size': media.file_size})
            total_deleted += result.deleted_count
        
        # Try with original filename
        if total_deleted == 0:
            result = col.delete_many({'file_name': media.file_name, 'file_size': media.file_size})
            total_deleted += result.deleted_count
            if not result.deleted_count:
                result = sec_col.delete_many({'file_name': media.file_name, 'file_size': media.file_size})
                total_deleted += result.deleted_count

    # Send confirmation reply
    if total_deleted > 0:
        if total_deleted == 1:
            reply_text = f"✅ <b>File Deleted Successfully!</b>\n\n📁 <code>{file_name}</code>\n💾 Size: {file_size}"
        else:
            reply_text = f"✅ <b>{total_deleted} Files Deleted!</b>\n\n📁 <code>{file_name}</code>\n💾 Size: {file_size}\n\n<i>ℹ️ Multiple duplicates were removed</i>"
        print(f'[files_delete.py] Deleted {total_deleted} file(s): {file_name}')
    else:
        reply_text = f"❌ <b>File Not Found in Database</b>\n\n📁 <code>{file_name}</code>\n💾 Size: {file_size}\n\n<i>This file may have already been deleted or was never indexed.</i>"
        print(f'[files_delete.py] File not found in database: {file_name}')
    
    try:
        await message.reply_text(reply_text)
    except Exception as e:
        print(f"[files_delete.py] Error sending reply: {e}")

    except Exception as e:
        print(f"[files_delete.py] ERROR in delete handler: {e}")
        import traceback
        traceback.print_exc()


@Client.on_message(filters.command("duplicates") & filters.user(ADMINS))
async def find_duplicates(bot, message):
    """Find duplicate files in the database"""
    
    status_msg = await message.reply_text("🔍 <b>Scanning for duplicates...</b>\n\n<i>This may take a while depending on database size.</i>")
    
    try:
        # Find duplicates by file_name and file_size in primary database
        pipeline = [
            {"$group": {
                "_id": {"file_name": "$file_name", "file_size": "$file_size"},
                "count": {"$sum": 1},
                "ids": {"$push": "$_id"}
            }},
            {"$match": {"count": {"$gt": 1}}},
            {"$sort": {"count": -1}},
            {"$limit": 20}
        ]
        
        duplicates = list(col.aggregate(pipeline))
        
        # Also check secondary database
        sec_duplicates = list(sec_col.aggregate(pipeline))
        
        total_duplicates = len(duplicates) + len(sec_duplicates)
        total_wasted = sum(d['count'] - 1 for d in duplicates) + sum(d['count'] - 1 for d in sec_duplicates)
        
        if total_duplicates == 0:
            await status_msg.edit_text("✅ <b>No duplicates found!</b>\n\n<i>Your database is clean.</i>")
            return
        
        report = f"📊 <b>Duplicate Files Report</b>\n\n"
        report += f"🔢 Total duplicate groups: <b>{total_duplicates}</b>\n"
        report += f"🗑️ Redundant copies: <b>{total_wasted}</b>\n\n"
        report += f"<b>Top Duplicates:</b>\n\n"
        
        for i, dup in enumerate(duplicates[:10], 1):
            name = dup['_id']['file_name'][:40] + "..." if len(dup['_id']['file_name']) > 40 else dup['_id']['file_name']
            size = get_size(dup['_id']['file_size']) if dup['_id']['file_size'] else "Unknown"
            report += f"{i}. <code>{name}</code>\n   📋 {dup['count']} copies | 💾 {size}\n\n"
        
        btn = [[InlineKeyboardButton("🗑️ Clean All Duplicates", callback_data="clean_duplicates")]]
        
        await status_msg.edit_text(report, reply_markup=InlineKeyboardMarkup(btn))
        
    except Exception as e:
        logger.error(f"Error finding duplicates: {e}")
        await status_msg.edit_text(f"❌ <b>Error scanning duplicates:</b>\n\n<code>{str(e)}</code>")


@Client.on_callback_query(filters.regex(r"^clean_duplicates"))
async def clean_duplicates(bot, query):
    """Remove duplicate files, keeping only one copy of each"""
    
    if query.from_user.id not in ADMINS:
        return await query.answer("⚠️ Only admins can do this!", show_alert=True)
    
    await query.answer("🧹 Cleaning duplicates...")
    await query.message.edit_text("🧹 <b>Cleaning duplicates...</b>\n\n<i>Please wait...</i>")
    
    try:
        total_removed = 0
        
        # Find and clean duplicates in primary database
        pipeline = [
            {"$group": {
                "_id": {"file_name": "$file_name", "file_size": "$file_size"},
                "count": {"$sum": 1},
                "ids": {"$push": "$_id"}
            }},
            {"$match": {"count": {"$gt": 1}}}
        ]
        
        for db_col in [col, sec_col]:
            duplicates = list(db_col.aggregate(pipeline))
            
            for dup in duplicates:
                # Keep the first one, delete the rest
                ids_to_delete = dup['ids'][1:]  # Skip first ID
                if ids_to_delete:
                    result = db_col.delete_many({"_id": {"$in": ids_to_delete}})
                    total_removed += result.deleted_count
        
        await query.message.edit_text(
            f"✅ <b>Cleanup Complete!</b>\n\n"
            f"🗑️ Removed: <b>{total_removed}</b> duplicate files\n\n"
            f"<i>Your database is now optimized.</i>"
        )
        logger.info(f"Cleaned {total_removed} duplicate files")
        
    except Exception as e:
        logger.error(f"Error cleaning duplicates: {e}")
        await query.message.edit_text(f"❌ <b>Error cleaning duplicates:</b>\n\n<code>{str(e)}</code>")
