import logging
import datetime
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors import MessageNotModified
from pyrogram.raw.types import LabeledPrice
from pyrogram.raw.functions.messages import SendMedia
from pyrogram.raw.types import InputMediaInvoice, Invoice, DataJSON
from info import ADMINS, PREMIUM_PRICES, FREE_DAILY_LIMIT
from database.users_chats_db import db
from Script import script

logger = logging.getLogger(__name__)

# Track last invoice message for each user to delete when they select a new plan
last_invoice_messages = {}


def get_readable_time(seconds):
    """Convert seconds to readable time format"""
    if seconds < 60:
        return f"{int(seconds)} seconds"
    elif seconds < 3600:
        return f"{int(seconds / 60)} minutes"
    elif seconds < 86400:
        return f"{int(seconds / 3600)} hours"
    else:
        days = int(seconds / 86400)
        hours = int((seconds % 86400) / 3600)
        if hours > 0:
            return f"{days} days, {hours} hours"
        return f"{days} days"


@Client.on_message(filters.command("premium") & filters.private)
async def premium_command(client, message):
    """Show premium plans and purchase options"""
    user_id = message.from_user.id
    is_premium, expiry = await db.get_premium_status(user_id)
    
    # Build the premium message
    if is_premium and expiry:
        time_left = (expiry - datetime.datetime.now()).total_seconds()
        status_text = f"⭐ <b>Your Premium Status:</b> Active\n⏰ <b>Expires:</b> {expiry.strftime('%d %B %Y, %I:%M %p')}\n⌛ <b>Time Left:</b> {get_readable_time(time_left)}\n\n"
    else:
        status_text = f"📊 <b>Your Status:</b> Free User\n📥 <b>Daily Limit:</b> {FREE_DAILY_LIMIT} downloads/day\n\n"
    
    text = f"""
{status_text}
<b>⭐ Premium Benefits:</b>

✅ <b>Unlimited Downloads</b> - No daily limits
✅ <b>Direct Access</b> - No waiting or ads
✅ <b>Priority Support</b> - Faster responses
✅ <b>Support Development</b> - Help us keep the bot running

<b>ℹ️ Note:</b> Premium gives you <b>ad-free unlimited access</b>. All books are available to everyone - premium just removes limits!

💡 <i>If you already have a plan, buying again will extend it automatically</i>

<b>Choose your plan:</b>
"""
    
    # Create payment buttons
    buttons = [
        [InlineKeyboardButton(f"1 Day - ⭐ {PREMIUM_PRICES[1]}", callback_data="buy_premium_1")],
        [InlineKeyboardButton(f"7 Days - ⭐ {PREMIUM_PRICES[7]}", callback_data="buy_premium_7")],
        [InlineKeyboardButton(f"15 Days - ⭐ {PREMIUM_PRICES[15]}", callback_data="buy_premium_15")],
        [InlineKeyboardButton(f"30 Days - ⭐ {PREMIUM_PRICES[30]}", callback_data="buy_premium_30")],
        [InlineKeyboardButton(f"60 Days - ⭐ {PREMIUM_PRICES[60]}", callback_data="buy_premium_60")],
        [InlineKeyboardButton(f"90 Days - ⭐ {PREMIUM_PRICES[90]}", callback_data="buy_premium_90")],
        [InlineKeyboardButton("❌ Close", callback_data="close_data")]
    ]
    
    await message.reply_text(
        text,
        reply_markup=InlineKeyboardMarkup(buttons),
        disable_web_page_preview=True
    )


@Client.on_message(filters.command("mystatus") & filters.private)
async def my_status_command(client, message):
    """Check user's premium status and download stats"""
    user_id = message.from_user.id
    is_premium, expiry = await db.get_premium_status(user_id)
    daily_downloads = await db.get_daily_downloads(user_id)
    
    if is_premium and expiry:
        time_left = (expiry - datetime.datetime.now()).total_seconds()
        text = f"""
<b>👤 Your Account Status</b>

⭐ <b>Plan:</b> Premium User
📅 <b>Expires:</b> {expiry.strftime('%d %B %Y, %I:%M %p')}
⌛ <b>Time Left:</b> {get_readable_time(time_left)}
📥 <b>Today's Downloads:</b> Unlimited ∞

<i>Thank you for supporting us! ❤️</i>
"""
    else:
        text = f"""
<b>👤 Your Account Status</b>

📊 <b>Plan:</b> Free User
📥 <b>Today's Downloads:</b> {daily_downloads}/{FREE_DAILY_LIMIT}
📈 <b>Remaining:</b> {max(0, FREE_DAILY_LIMIT - daily_downloads)} downloads

<i>Upgrade to Premium for unlimited downloads!</i>
"""
    
    buttons = [[InlineKeyboardButton("⭐ Upgrade to Premium", callback_data="show_premium")]]
    
    if not is_premium:
        await message.reply_text(text, reply_markup=InlineKeyboardMarkup(buttons))
    else:
        await message.reply_text(text)


@Client.on_callback_query(filters.regex(r"^show_premium$"))
async def show_premium_callback(client, query):
    """Show premium plans from callback"""
    user_id = query.from_user.id
    is_premium, expiry = await db.get_premium_status(user_id)
    
    if is_premium and expiry:
        time_left = (expiry - datetime.datetime.now()).total_seconds()
        status_text = f"⭐ <b>Your Premium Status:</b> Active\n⏰ <b>Expires:</b> {expiry.strftime('%d %B %Y, %I:%M %p')}\n⌛ <b>Time Left:</b> {get_readable_time(time_left)}\n\n"
    else:
        status_text = f"📊 <b>Your Status:</b> Free User\n📥 <b>Daily Limit:</b> {FREE_DAILY_LIMIT} downloads/day\n\n"
    
    text = f"""
{status_text}
<b>⭐ Premium Benefits:</b>

✅ <b>Unlimited Downloads</b> - No daily limits
✅ <b>Direct Access</b> - No waiting or ads
✅ <b>Priority Support</b> - Faster responses
✅ <b>Support Development</b> - Help us keep the bot running

<b>ℹ️ Note:</b> Premium gives you <b>ad-free unlimited access</b>. All books are available to everyone - premium just removes limits!

💡 <i>If you already have a plan, buying again will extend it automatically</i>

<b>Choose your plan:</b>
"""
    
    buttons = [
        [InlineKeyboardButton(f"1 Day - ⭐ {PREMIUM_PRICES[1]}", callback_data="buy_premium_1")],
        [InlineKeyboardButton(f"7 Days - ⭐ {PREMIUM_PRICES[7]}", callback_data="buy_premium_7")],
        [InlineKeyboardButton(f"15 Days - ⭐ {PREMIUM_PRICES[15]}", callback_data="buy_premium_15")],
        [InlineKeyboardButton(f"30 Days - ⭐ {PREMIUM_PRICES[30]}", callback_data="buy_premium_30")],
        [InlineKeyboardButton(f"60 Days - ⭐ {PREMIUM_PRICES[60]}", callback_data="buy_premium_60")],
        [InlineKeyboardButton(f"90 Days - ⭐ {PREMIUM_PRICES[90]}", callback_data="buy_premium_90")],
        [InlineKeyboardButton("« Back", callback_data="back_to_status"), InlineKeyboardButton("❌ Close", callback_data="close_data")]
    ]
    
    try:
        await query.message.edit_text(
            text,
            reply_markup=InlineKeyboardMarkup(buttons),
            disable_web_page_preview=True
        )
    except MessageNotModified:
        pass


@Client.on_callback_query(filters.regex(r"^buy_premium_(\d+)$"))
async def buy_premium_callback(client, query):
    """Handle premium purchase button click - show confirmation"""
    days = int(query.data.split("_")[2])
    stars = PREMIUM_PRICES.get(days)
    
    if not stars:
        return await query.answer("Invalid plan!", show_alert=True)
    
    # Show confirmation message in the same message
    text = f"""
<b>⭐ Confirm Your Purchase</b>

📦 <b>Plan:</b> {days} Day{'s' if days > 1 else ''} Premium
💰 <b>Price:</b> ⭐ {stars} Stars

<b>Benefits:</b>
✅ Unlimited Downloads
✅ No daily limits
✅ Direct access to all books

💡 <i>If you already have Premium, this will extend your existing plan.</i>

<b>Click "Confirm & Pay" to proceed with payment.</b>
"""
    
    buttons = [
        [InlineKeyboardButton(f"✅ Confirm & Pay ⭐ {stars}", callback_data=f"confirm_premium_{days}")],
        [InlineKeyboardButton("« Back to Plans", callback_data="show_premium")],
        [InlineKeyboardButton("❌ Cancel", callback_data="close_data")]
    ]
    
    try:
        await query.message.edit_text(
            text,
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    except MessageNotModified:
        pass


@Client.on_callback_query(filters.regex(r"^confirm_premium_(\d+)$"))
async def confirm_premium_callback(client, query):
    """Handle confirmed premium purchase - send invoice"""
    days = int(query.data.split("_")[2])
    stars = PREMIUM_PRICES.get(days)
    user_id = query.from_user.id
    
    if not stars:
        return await query.answer("Invalid plan!", show_alert=True)
    
    # Delete previous invoice message if exists
    if user_id in last_invoice_messages:
        try:
            await client.delete_messages(user_id, last_invoice_messages[user_id])
        except:
            pass
    
    # Delete the confirmation message
    try:
        await query.message.delete()
    except:
        pass
    
    # Create invoice for Telegram Stars payment
    try:
        # Use raw API to send invoice
        peer = await client.resolve_peer(user_id)
        
        invoice = Invoice(
            currency="XTR",  # Telegram Stars
            prices=[LabeledPrice(label=f"{days} Day{'s' if days > 1 else ''} Premium", amount=stars)],
            test=False,
            name_requested=False,
            phone_requested=False,
            email_requested=False,
            shipping_address_requested=False,
            flexible=False
        )
        
        media = InputMediaInvoice(
            title=f"Premium - {days} Day{'s' if days > 1 else ''}",
            description=f"Get {days} day{'s' if days > 1 else ''} of Premium access with unlimited downloads.",
            invoice=invoice,
            payload=f"premium_{days}_{user_id}".encode(),
            provider="",  # Empty for Telegram Stars
            provider_data=DataJSON(data="{}")
        )
        
        result = await client.invoke(
            SendMedia(
                peer=peer,
                media=media,
                message="",
                random_id=client.rnd_id()
            )
        )
        
        # Track this invoice message
        if result.updates:
            for update in result.updates:
                if hasattr(update, 'message') and hasattr(update.message, 'id'):
                    last_invoice_messages[user_id] = update.message.id
                    break
        
        await query.answer()
    except Exception as e:
        logger.error(f"Error creating invoice: {e}")
        await query.answer(f"Error creating payment. Please try again later.", show_alert=True)


@Client.on_raw_update()
async def raw_update_handler(client, update, users, chats):
    """Handle raw updates including pre_checkout_query"""
    from pyrogram.raw.types import UpdateBotPrecheckoutQuery
    
    if isinstance(update, UpdateBotPrecheckoutQuery):
        try:
            payload = update.payload.decode()
            if payload.startswith("premium_"):
                parts = payload.split("_")
                if len(parts) >= 3:
                    days = int(parts[1])
                    expected_user_id = int(parts[2])
                    
                    if days in PREMIUM_PRICES and expected_user_id == update.user_id:
                        # Approve the payment
                        from pyrogram.raw.functions.messages import SetBotPrecheckoutResults
                        await client.invoke(
                            SetBotPrecheckoutResults(
                                query_id=update.query_id,
                                success=True
                            )
                        )
                        return
            
            # Reject if validation failed
            from pyrogram.raw.functions.messages import SetBotPrecheckoutResults
            await client.invoke(
                SetBotPrecheckoutResults(
                    query_id=update.query_id,
                    success=False,
                    error="Invalid payment request"
                )
            )
        except Exception as e:
            logger.error(f"Pre-checkout error: {e}")
    
    # Handle successful payment
    from pyrogram.raw.types import UpdateNewMessage, MessageService, MessageActionPaymentSentMe
    
    if isinstance(update, UpdateNewMessage):
        if hasattr(update, 'message') and isinstance(update.message, MessageService):
            if isinstance(update.message.action, MessageActionPaymentSentMe):
                try:
                    action = update.message.action
                    payload = action.payload.decode()
                    
                    if payload.startswith("premium_"):
                        parts = payload.split("_")
                        days = int(parts[1])
                        user_id = update.message.peer_id.user_id if hasattr(update.message.peer_id, 'user_id') else int(parts[2])
                        
                        # Activate/extend premium
                        new_expiry = await db.set_premium(user_id, days)
                        
                        if new_expiry:
                            text = f"""
🎉 <b>Payment Successful!</b>

⭐ <b>Premium Activated!</b>
📅 <b>Duration:</b> {days} day{'s' if days > 1 else ''}
⏰ <b>Valid Until:</b> {new_expiry.strftime('%d %B %Y, %I:%M %p')}
💰 <b>Stars Paid:</b> {action.total_amount} ⭐

<b>You now have:</b>
✅ Unlimited downloads
✅ No daily limits
✅ Direct access to all files

<i>Thank you for supporting us! ❤️</i>

Use /mystatus to check your premium status anytime.
"""
                            await client.send_message(user_id, text)
                            logger.info(f"Premium activated: User {user_id}, {days} days, {action.total_amount} stars")
                        else:
                            await client.send_message(user_id, "❌ Error activating premium. Please contact support.")
                except Exception as e:
                    logger.error(f"Payment processing error: {e}")


# Admin commands for premium management
@Client.on_message(filters.command("addpremium") & filters.user(ADMINS))
async def add_premium_command(client, message):
    """Admin command to add premium to a user"""
    if len(message.command) < 3:
        return await message.reply_text("Usage: /addpremium <user_id> <days>")
    
    try:
        user_id = int(message.command[1])
        days = int(message.command[2])
        
        new_expiry = await db.set_premium(user_id, days)
        if new_expiry:
            await message.reply_text(f"✅ Premium added!\n\n👤 User: {user_id}\n📅 Days: {days}\n⏰ Expires: {new_expiry.strftime('%d %B %Y, %I:%M %p')}")
            
            # Notify user
            try:
                await client.send_message(
                    user_id,
                    f"🎉 <b>You've been gifted Premium!</b>\n\n📅 <b>Duration:</b> {days} days\n⏰ <b>Valid Until:</b> {new_expiry.strftime('%d %B %Y, %I:%M %p')}\n\n<i>Enjoy unlimited downloads!</i>"
                )
            except:
                pass
        else:
            await message.reply_text("❌ Error adding premium. User may not exist in database.")
    except ValueError:
        await message.reply_text("Invalid user_id or days. Both must be numbers.")


@Client.on_message(filters.command("removepremium") & filters.user(ADMINS))
async def remove_premium_command(client, message):
    """Admin command to remove premium from a user"""
    if len(message.command) < 2:
        return await message.reply_text("Usage: /removepremium <user_id>")
    
    try:
        user_id = int(message.command[1])
        
        from database.users_chats_db import db
        await db.col.update_one(
            {'id': int(user_id)},
            {'$set': {'is_premium': False, 'premium_expiry': None}}
        )
        
        await message.reply_text(f"✅ Premium removed from user {user_id}")
    except ValueError:
        await message.reply_text("Invalid user_id. Must be a number.")


@Client.on_message(filters.command("premiumusers") & filters.user(ADMINS))
async def premium_users_command(client, message):
    """Admin command to list premium users"""
    total_premium = await db.get_premium_stats()
    
    if total_premium == 0:
        return await message.reply_text("No premium users found.")
    
    premium_users = db.col.find({'is_premium': True})
    
    text = f"<b>⭐ Premium Users ({total_premium})</b>\n\n"
    count = 0
    async for user in premium_users:
        if count >= 20:  # Limit to 20 users
            text += f"\n<i>...and {total_premium - 20} more</i>"
            break
        
        user_id = user.get('id')
        name = user.get('name', 'Unknown')
        expiry = user.get('premium_expiry')
        expiry_str = expiry.strftime('%d %b %Y') if expiry else 'N/A'
        
        text += f"• <code>{user_id}</code> - {name} (expires: {expiry_str})\n"
        count += 1
    
    await message.reply_text(text)


@Client.on_message(filters.command("stars") & filters.user(ADMINS))
async def stars_balance_command(client, message):
    """Admin command to check bot's Star balance and recent transactions"""
    try:
        # Get star transactions
        transactions = await client.get_star_transactions(limit=10)
        
        text = "<b>⭐ Bot Stars Dashboard</b>\n\n"
        
        # Total balance
        if hasattr(transactions, 'star_count'):
            text += f"💰 <b>Current Balance:</b> ⭐ {transactions.star_count}\n\n"
        
        text += "<b>📊 Recent Transactions:</b>\n"
        
        if transactions.transactions:
            for txn in transactions.transactions:
                # Transaction direction
                if txn.source:
                    direction = "📥 IN"
                    user_info = ""
                    if hasattr(txn.source, 'user') and txn.source.user:
                        user_info = f" from {txn.source.user.first_name} ({txn.source.user.id})"
                else:
                    direction = "📤 OUT"
                    user_info = ""
                
                # Format date
                txn_date = txn.date.strftime('%d %b %Y, %I:%M %p') if txn.date else 'N/A'
                
                text += f"\n{direction} ⭐ {txn.amount}{user_info}\n"
                text += f"   📅 {txn_date}\n"
        else:
            text += "\n<i>No transactions found.</i>"
        
        await message.reply_text(text)
        
    except Exception as e:
        logger.error(f"Error getting star transactions: {e}")
        await message.reply_text(f"❌ Error fetching star data: {e}")


@Client.on_message(filters.command("starhistory") & filters.user(ADMINS))
async def stars_history_command(client, message):
    """Admin command to get detailed star transaction history"""
    try:
        limit = 25
        if len(message.command) > 1:
            try:
                limit = min(int(message.command[1]), 100)
            except:
                pass
        
        transactions = await client.get_star_transactions(limit=limit)
        
        text = f"<b>⭐ Star Transaction History (Last {limit})</b>\n\n"
        
        if hasattr(transactions, 'star_count'):
            text += f"💰 <b>Current Balance:</b> ⭐ {transactions.star_count}\n\n"
        
        total_in = 0
        total_out = 0
        
        if transactions.transactions:
            for txn in transactions.transactions:
                if txn.source:
                    total_in += txn.amount
                else:
                    total_out += txn.amount
            
            text += f"📥 <b>Total Received:</b> ⭐ {total_in}\n"
            text += f"📤 <b>Total Withdrawn:</b> ⭐ {total_out}\n"
            text += f"📊 <b>Transactions:</b> {len(transactions.transactions)}\n"
        else:
            text += "<i>No transactions found.</i>"
        
        await message.reply_text(text)
        
    except Exception as e:
        logger.error(f"Error getting star history: {e}")
        await message.reply_text(f"❌ Error fetching star history: {e}")
