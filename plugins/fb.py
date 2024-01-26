from pyrogram import filters, Client as Mbot
import bs4, requests,re,asyncio
import wget,os,traceback
from bot import LOG_GROUP,DUMP_GROUP

@Mbot.on_message(filters.regex(r'https?://.*facebook[^\s]+') & filters.incoming,group=-6)
async def link_handler(Mbot, message):
    link = message.matches[0].group(0)
    try:
       m = await message.reply_text("⏳")
       get_api=requests.get(f"https://yasirapi.eu.org/fbdl?link={link}").json()
       if get_api['success'] == "false":
          return await message.reply("⛔️Noto'g'ri TikTok havolasi! Iltimos tekshirib qayta kiriting! :)") 
       if get_api['success'] == "ok":
          if get_api.get('result').get('hd'):
             try:
                 dump_file = await message.reply_video(get_api['result']['hd'],caption="❇️ @InstaProSaverrobot - orqali yuklab olindi!")
             except KeyError:
                 pass 
             except Exception:
                 try:
                     sndmsg = await message.reply(get_api['result']['hd'])
                     await asyncio.sleep(1)
                     dump_file = await message.reply_video(get_api['result']['hd'],caption="❇️ @InstaProSaverrobot - orqali yuklab olindi!")
                     await sndmsg.delete()
                 except Exception:
                     try:
                        down_file = wget.download(get_api['result']['hd'])
                        await message.reply_video(down_file,caption="❇️ @InstaProSaverrobot - orqali yuklab olindi!")
                        await sndmsg.delete()
                        os.remove(down_file)
                     except:
                         return await message.reply("Oops Xatolik!")
          else: 
             if get_api.get('result').get('sd'):
               try:
                   dump_file = await message.reply_video(get_api['result']['sd'],caption="❇️ @InstaProSaverrobot - orqali yuklab olindi!")
               except KeyError:
                   pass
               except Exception:
                   try:
                       sndmsg = await message.reply(get_api['result']['sd'])
                       await asyncio.sleep(1)
                       dump_file = await message.reply_video(get_api['result']['sd'],caption="❇️ @InstaProSaverrobot - orqali yuklab olindi!")
                       await sndmsg.delete()
                   except Exception:
                      try:
                        down_file = wget.download(get_api['result']['sd'])
                        await message.reply_video(down_file,caption="❇️ @InstaProSaverrobot - orqali yuklab olindi!")
                        await sndmsg.delete()
                        os.remove(down_file)
                      except:
                         return await message.reply("Oops Xatolik!")
    except Exception as e:
           if LOG_GROUP:
               await Mbot.send_message(LOG_GROUP,f"Facebook {e} {link}")
               await Mbot.send_message(LOG_GROUP, traceback.format_exc())          
    finally:
          if 'dump_file' in locals():
            if DUMP_GROUP:
               await dump_file.copy(DUMP_GROUP)
          await m.delete()      
