from pyrogram import filters, Client as Mbot
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from apscheduler.schedulers.background import BackgroundScheduler
from sys import executable
from os import sys, execl, environ

# Replace with your actual channel usernames
CHANNEL_USERNAMES = ['AniverseAnime', 'AniverseTeam']

# Check if the user is subscribed to any of the channels
async def is_subscribed(user_id):
    result = {}
    for channel_username in CHANNEL_USERNAMES:
        try:
            chat_member = await Mbot.get_chat_member(channel_username, user_id)
            result[channel_username] = chat_member.status
        except Exception as e:
            result[channel_username] = f"Error: {e}"
    
    return result

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

# Updated /start command handler
@Mbot.on_message(filters.command("start") & filters.incoming)
async def start(Mbot, message):
    user_id = message.from_user.id
    subscription_status = await is_subscribed(user_id)

    if any(status == 'member' for status in subscription_status.values()):
        # User is subscribed, send the start message or perform other actions
        await Mbot.send_message(user_id, f"👋👋 Assalomu Alaykum 👋👋 {message.from_user.mention()}\n Siz ushbu bot orqali o'zingiz istagan ijtimoiy tarmoqdan video, post, rasm, hikoya va boshqalarni yuklab olishingiz mumkin! \nHozirda ushbu bot orqali siz \n☑️Instagram \n☑️TikTok \n☑️Twitter \n☑️Facebook orqali barcha medialarni yuklab olishingiz mumkin! \nShunchaki botga havolangizni yuboring!",
                                 reply_markup=generate_keyboard())
    else:
        # User is not subscribed, send the force subscribe message or take other actions
        await Mbot.send_message(user_id, "You are not subscribed. Please subscribe first.")

# Function to generate the inline keyboard
def generate_keyboard():
    keyboard_buttons = [
        [InlineKeyboardButton(f"Subscribe to {channel}", url=f'https://t.me/{channel}')] for channel in CHANNEL_USERNAMES
    ]
    # Add the "Check Subscription" button
    keyboard_buttons.append([InlineKeyboardButton("Check Subscription", callback_data="check_subscription")])
    return InlineKeyboardMarkup(keyboard_buttons)

# Rest of the code...

# Callback Query handler for the buttons
@Mbot.on_callback_query()
async def callback_query_handler(Mbot, callback_query):
    user_id = callback_query.from_user.id
    if callback_query.data == "check_subscription":
        # Send a /start command to check the subscription
        await Mbot.send_message(user_id, "/start")
    elif callback_query.data.startswith("subscribe_"):
        # Extract the channel username from the callback data
        channel = callback_query.data.split("_")[1]
        # Open the channel directly using the 'url' parameter
        await Mbot.send_message(user_id, f"Opening {channel} directly...", disable_web_page_preview=True)
             
@Mbot.on_message(filters.command("help") & filters.incoming)
async def help(Mbot, message):
          await message.reply("Hozirda ushbu bot orqali siz \n☑️Instagram \n☑️TikTok \n☑️Twitter \n☑️Facebook orqali barcha medialarni yuklab olishingiz mumkin! \nShunchaki botga havolangizni yuboring! \nMisol uchun:) \n eg: `https://www.instagram.com/reel/CZqWDGODoov/?igshid=MzRlODBiNWFlZA==`\n `post:` `https://www.instagram.com/reel/CuCTtORJbDj/?igshid=MzRlODBiNWFlZA==`")
@Mbot.on_message(filters.command("donate") & filters.command("Donate") & filters.incoming )
async def donate(_, message):
       await message.reply_text(f"Dasturchi 🍪 **$** https://t.me/@LappIand \n**UPI**`https://t.me/@LappIand` \nBot Egasi: https://t.me/@LappIand")
