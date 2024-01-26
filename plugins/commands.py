from pyrogram import filters, Client as Mbot
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from apscheduler.schedulers.background import BackgroundScheduler
from sys import executable
from os import sys, execl, environ

# Replace with your actual channel usernames
CHANNEL_USERNAMES = ['@Aniverseteam', '@Aniverseanime']

# Check if the user is subscribed to any of the channels
def is_subscribed(channel_username, user_id):
    try:
        chat_member = Mbot.get_chat_member(channel_username, user_id)
        if chat_member.status not in ['left', 'kicked']:
            return True
    except Exception as e:
        print(f"Error checking subscription: {e}")
    return False

RESTART_ON = environ.get('RESTART_ON')

def restart():
    execl(executable, executable, "bot.py")

if RESTART_ON:
    scheduler = BackgroundScheduler()
    scheduler.add_job(restart, "interval", hours=6)
    scheduler.start()

@Mbot.on_message(filters.incoming & filters.private, group=-1)
async def monitor(Mbot, message):
    # Replace with your logic to forward messages to the DUMP_GROUP
    # Example: await message.forward(DUMP_GROUP)
    pass

@Mbot.on_message(filters.command("start") & filters.incoming)
async def start(Mbot, message):
    user_id = message.from_user.id
    if not any(is_subscribed(channel, user_id) for channel in CHANNEL_USERNAMES):
        # If not subscribed to any channel, provide buttons to subscribe
        keyboard_buttons = [
            [InlineKeyboardButton(f"Subscribe to {channel}", callback_data=f"subscribe_{channel}")]
            for channel in CHANNEL_USERNAMES
        ]
        # Add the "Check Subscription" button
        keyboard_buttons.append([InlineKeyboardButton("Check Subscription", callback_data="check_subscription")])
        
        keyboard = InlineKeyboardMarkup(keyboard_buttons)
        await message.reply("To use this bot, you need to subscribe to one of our channels. Click one of the buttons below to subscribe.", reply_markup=keyboard)
        return

    # If subscribed, provide a button to check subscription
    check_button = InlineKeyboardButton("Check Subscription", callback_data="check_subscription")
    keyboard = InlineKeyboardMarkup([[check_button]])
    
    await message.reply(f"👋👋 Assalomu Alaykum 👋👋 {message.from_user.mention()}\n Siz ushbu bot orqali o'zingiz istagan ijtimoiy tarmoqdan video, post, rasm, hikoya va boshqalarni yuklab olishingiz mumkin! \nHozirda ushbu bot orqali siz \n☑️Instagram \n☑️TikTok \n☑️Twitter \n☑️Facebook orqali barcha medialarni yuklab olishingiz mumkin! \nShunchaki botga havolangizni yuboring!", reply_markup=keyboard)

# Callback Query handler for the buttons
@Mbot.on_callback_query()
async def callback_query_handler(Mbot, callback_query):
    user_id = callback_query.from_user.id
    if callback_query.data.startswith("subscribe_"):
        channel = callback_query.data.split("_")[1]
        # Implement the logic to subscribe the user to the channel
        # For example, you might want to use the `Mbot.add_chat_member` method
        pass
    elif callback_query.data == "check_subscription":
        if any(is_subscribed(channel, user_id) for channel in CHANNEL_USERNAMES):
            await callback_query.answer("You are subscribed!")
        else:
            await callback_query.answer("You are not subscribed. Please subscribe first.")

             
@Mbot.on_message(filters.command("help") & filters.incoming)
async def help(Mbot, message):
          await message.reply("Hozirda ushbu bot orqali siz \n☑️Instagram \n☑️TikTok \n☑️Twitter \n☑️Facebook orqali barcha medialarni yuklab olishingiz mumkin! \nShunchaki botga havolangizni yuboring! \nMisol uchun:) \n eg: `https://www.instagram.com/reel/CZqWDGODoov/?igshid=MzRlODBiNWFlZA==`\n `post:` `https://www.instagram.com/reel/CuCTtORJbDj/?igshid=MzRlODBiNWFlZA==`")
@Mbot.on_message(filters.command("donate") & filters.command("Donate") & filters.incoming )
async def donate(_, message):
       await message.reply_text(f"Dasturchi 🍪 **$** https://t.me/@LappIand \n**UPI**`https://t.me/@LappIand` \nBot Egasi: https://t.me/@LappIand")
