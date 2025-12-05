import logging
import datetime
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, PreCheckoutQuery, LabeledPrice
from pyrogram.errors import MessageNotModified
from info import ADMINS, PREMIUM_PRICES, FREE_DAILY_LIMIT
from database.users_chats_db import db
from Script import script

logger = logging.getLogger(__name__)


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
    """Handle premium purchase button click"""
    days = int(query.data.split("_")[2])
    stars = PREMIUM_PRICES.get(days)
    
    if not stars:
        return await query.answer("Invalid plan!", show_alert=True)
    
    # Create invoice for Telegram Stars payment
    try:
        await client.send_invoice(
            chat_id=query.from_user.id,
            title=f"Premium - {days} Day{'s' if days > 1 else ''}",
            description=f"Get {days} day{'s' if days > 1 else ''} of Premium access with unlimited downloads. If you already have Premium, this will extend your existing plan.",
            payload=f"premium_{days}_{query.from_user.id}",
            currency="XTR",  # Telegram Stars
            prices=[LabeledPrice(label=f"{days} Day{'s' if days > 1 else ''} Premium", amount=stars)]
        )
        await query.answer()
    except Exception as e:
        logger.error(f"Error creating invoice: {e}")
        await query.answer(f"Error creating payment. Please try again later.", show_alert=True)


@Client.on_pre_checkout_query()
async def pre_checkout_handler(client, query: PreCheckoutQuery):
    """Handle pre-checkout query - approve the payment"""
    try:
        # Parse payload to verify
        payload = query.invoice_payload
        if payload.startswith("premium_"):
            parts = payload.split("_")
            if len(parts) >= 3:
                days = int(parts[1])
                user_id = int(parts[2])
                
                if days in PREMIUM_PRICES and user_id == query.from_user.id:
                    await query.answer(ok=True)
                    return
        
        await query.answer(ok=False, error_message="Invalid payment request")
    except Exception as e:
        logger.error(f"Pre-checkout error: {e}")
        await query.answer(ok=False, error_message="Payment verification failed")


@Client.on_message(filters.successful_payment)
async def successful_payment_handler(client, message):
    """Handle successful payment - activate premium"""
    try:
        payment = message.successful_payment
        payload = payment.invoice_payload
        
        if payload.startswith("premium_"):
            parts = payload.split("_")
            days = int(parts[1])
            user_id = message.from_user.id
            
            # Activate/extend premium
            new_expiry = await db.set_premium(user_id, days)
            
            if new_expiry:
                text = f"""
🎉 <b>Payment Successful!</b>

⭐ <b>Premium Activated!</b>
📅 <b>Duration:</b> {days} day{'s' if days > 1 else ''}
⏰ <b>Valid Until:</b> {new_expiry.strftime('%d %B %Y, %I:%M %p')}
💰 <b>Stars Paid:</b> {payment.total_amount} ⭐

<b>You now have:</b>
✅ Unlimited downloads
✅ No daily limits
✅ Direct access to all files

<i>Thank you for supporting us! ❤️</i>

Use /mystatus to check your premium status anytime.
"""
                await message.reply_text(text)
                
                # Log the payment
                logger.info(f"Premium activated: User {user_id}, {days} days, {payment.total_amount} stars")
            else:
                await message.reply_text("❌ Error activating premium. Please contact support.")
    except Exception as e:
        logger.error(f"Payment processing error: {e}")
        await message.reply_text("❌ Error processing payment. Please contact support with your payment receipt.")


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
