from pyrogram import filters, Client as Mbot
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from apscheduler.schedulers.background import BackgroundScheduler
from sys import executable
from os import sys, execl, environ

# Replace with your actual channel usernames
CHANNEL_USERNAMES = ['@Channel1Username', '@Channel2Username', '@Channel3Username']

# Check if the user is subscribed to any of the channels
def is_subscribed(user_id):
    for channel_username in CHANNEL_USERNAMES:
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
    if not is_subscribed(user_id):
        # If not subscribed, provide buttons to subscribe to any of the channels
        keyboard_buttons = [
            [InlineKeyboardButton(f"Subscribe to {channel}", url=f'https://t.me/{channel}')] for channel in CHANNEL_USERNAMES
        ]
        keyboard = InlineKeyboardMarkup(keyboard_buttons)
        await message.reply("To use this bot, you need to subscribe to one of our channels. Click one of the buttons below to subscribe.", reply_markup=keyboard)
        return

    # If subscribed, provide a button to check subscription
    check_button = InlineKeyboardButton("Check Subscription", callback_data="check_subscription")
    keyboard = InlineKeyboardMarkup([[check_button]])
    
    await message.reply(f"👋👋 Assalomu Alaykum 👋👋 {message.from_user.mention()}\n Siz ushbu bot orqali o'zingiz istagan ijtimoiy tarmoqdan video, post, rasm, hikoya va boshqalarni yuklab olishingiz mumkin! \nHozirda ushbu bot orqali siz \n☑️Instagram \n☑️TikTok \n☑️Twitter \n☑️Facebook orqali barcha medialarni yuklab olishingiz mumkin! \nShunchaki botga havolangizni yuboring!", reply_markup=keyboard)

# Callback Query handler for the "Check Subscription" button
@Mbot.on_callback_query()
async def callback_query_handler(Mbot, callback_query):
    if callback_query.data == "check_subscription":
        user_id = callback_query.from_user.id
        if is_subscribed(user_id):
            await callback_query.answer("You are subscribed!")
        else:
            await callback_query.answer("You are not subscribed. Please subscribe first.")
             
@Mbot.on_message(filters.command("help") & filters.incoming)
async def help(Mbot, message):
          await message.reply("Hozirda ushbu bot orqali siz \n☑️Instagram \n☑️TikTok \n☑️Twitter \n☑️Facebook orqali barcha medialarni yuklab olishingiz mumkin! \nShunchaki botga havolangizni yuboring! \nMisol uchun:) \n eg: `https://www.instagram.com/reel/CZqWDGODoov/?igshid=MzRlODBiNWFlZA==`\n `post:` `https://www.instagram.com/reel/CuCTtORJbDj/?igshid=MzRlODBiNWFlZA==`")
@Mbot.on_message(filters.command("donate") & filters.command("Donate") & filters.incoming )
async def donate(_, message):
       await message.reply_text(f"Dasturchi 🍪 **$** https://t.me/@LappIand \n**UPI**`https://t.me/@LappIand` \nBot Egasi: https://t.me/@LappIand")
