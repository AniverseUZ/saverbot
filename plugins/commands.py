from pyrogram import filters, Client as Mbot
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from apscheduler.schedulers.background import BackgroundScheduler
from sys import executable
from os import sys, execl, environ

# Replace with your actual channel invite link
CHANNEL_INVITE_LINK = "https://t.me/AniverseAnime"

# Function to check subscription logic (replace this with your actual logic)
async def check_subscription_logic(user_id):
    # Replace this with your subscription check logic (e.g., check in a database)
    # For now, assuming everyone is subscribed
    return True

# Restart scheduler (if you are using it)
RESTART_ON = environ.get('RESTART_ON')
def restart():
     execl(executable, executable, "bot.py")

if RESTART_ON:
   scheduler = BackgroundScheduler()
   scheduler.add_job(restart, "interval", hours=6)
   scheduler.start()

@Mbot.on_message(filters.incoming & filters.private, group=-1)
async def monitor(Mbot, message):
    if DUMP_GROUP:
        await message.forward(DUMP_GROUP)

@Mbot.on_message(filters.command("start") & filters.incoming)
async def start(Mbot, message):
    # Check if the user is subscribed (you may need to replace this with your logic)
    is_subscribed = await check_subscription_logic(message.from_user.id)

    if not is_subscribed:
        # User is not subscribed, send force sub message with "Try Again" button
        buttons = [
            [
                InlineKeyboardButton(
                    "Join Channel",
                    url=CHANNEL_INVITE_LINK
                )
            ],
            [
                InlineKeyboardButton(
                    "Try Again",
                    url=f"https://t.me/{Mbot.username}?start=start"
                )
            ]
        ]
        await message.reply(
            text="You are not subscribed! Please join our channel to access the content.",
            reply_markup=InlineKeyboardMarkup(buttons)
        )
        return

    # User is subscribed, continue with your existing code
    await message.reply(f"👋👋 Assalomu Alaykum 👋👋 {message.from_user.mention()}\n Siz ushbu bot orqali o'zingiz istagan ijtimoiy tarmoqdan video, post, rasm, hikoya va boshqalarni yuklab olishingiz mumkin! \nHozirda ushbu bot orqali siz \n☑️Instagram \n☑️TikTok \n☑️Twitter \n☑️Facebook orqali barcha medialarni yuklab olishingiz mumkin! \nShunchaki botga havolangizni yuboring!")

@Mbot.on_message(filters.command("help") & filters.incoming)
async def help(Mbot, message):
    await message.reply("Hozirda ushbu bot orqali siz \n☑️Instagram \n☑️TikTok \n☑️Twitter \n☑️Facebook orqali barcha medialarni yuklab olishingiz mumkin! \nShunchaki botga havolangizni yuboring! \nMisol uchun:) \n eg: `https://www.instagram.com/reel/CZqWDGODoov/?igshid=MzRlODBiNWFlZA==`\n `post:` `https://www.instagram.com/reel/CuCTtORJbDj/?igshid=MzRlODBiNWFlZA==`")

@Mbot.on_message(filters.command("donate") & filters.command("Donate") & filters.incoming)
async def donate(_, message):
    await message.reply_text(f"Dasturchi 🍪 **$** https://t.me/@LappIand \n**UPI**`https://t.me/@LappIand` \nBot Egasi: https://t.me/@LappIand")
