#(©)Codexbotz

import aiohttp
import asyncio
from pyrogram import filters, Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors import FloodWait
from plugins.data import ODD, EVEN ,BOTEFITMSG, FOMET
from plugins.cbb import DATEDAY
from bot import Bot
from config import ADMINS, CHANNEL_ID, DISABLE_CHANNEL_BUTTON
from datetime import datetime
from helper_func import encode
from pyshorteners import Shortener
import string
import re


@Client.on_message(filters.private & filters.command(["date"]))
async def date(bot, message):
    dat = await message.reply_text("Select Date.........",quote=True,reply_markup=InlineKeyboardMarkup([[ 
        			InlineKeyboardButton("Yesterday",callback_data='ystdy'), 
        			InlineKeyboardButton("Today",callback_data = 'tdy'), 
        			InlineKeyboardButton("Tommorow",callback_data='tmr') ]]))

@Bot.on_message(filters.private & filters.user(ADMINS) & ~filters.text & ~filters.command(['start','users','broadcast','batch','genlink','stats']))
async def channel_post(client: Client, message: Message):
    dateexc = datetime.now().strftime("%d")
    media = message.video or message.document
    filname= media.file_name.split("S0")[0]#[1][2]etc
    botfsno= hk = re.findall("S0.+E\d+", media.file_name)
    if int(dateexc) % 2 != 0:
        if filname in media.file_name:
            # chtid=int(ODD[filname][3])
            pic=ODD[filname][0]
            SL_URL=ODD[filname][1]
            SL_API=ODD[filname][2]
            bot_msg = await message.reply_text("Please Wait...!", quote = True)
            await asyncio.sleep(2)
            e_pic = await client.send_photo(chat_id=message.chat.id, photo=pic, caption=f"....")
            await asyncio.sleep(2)
    elif int(dateexc) % 2 == 0:
        if filname in media.file_name:
            # chtid=int(EVEN[filname][3])
            pic=EVEN[filname][0]
            SL_URL=EVEN[filname][1]
            SL_API=EVEN[filname][2] 
            bot_msg = await message.reply_text("Please Wait...!", quote = True)
            await asyncio.sleep(2)
            e_pic = await client.send_photo(chat_id=message.chat.id, photo=pic, caption=f"....")
            await asyncio.sleep(2)
    else:
        reply_text = await message.reply_text("❌Don't send me messages directly I'm only for serials!")
        
    try:
        post_message = await message.copy(chat_id = client.db_channel.id, disable_notification=True)
    except FloodWait as e:
        await asyncio.sleep(e.x)
        post_message = await message.copy(chat_id = client.db_channel.id, disable_notification=True)
    except Exception as e:
        print(e)
        await reply_text.edit_text("Something went Wrong..!")
        return
    converted_id = post_message.id * abs(client.db_channel.id)
    string = f"get-{converted_id}"
    base64_string = await encode(string)
    Tlink = f"https://telegram.me/{client.username}?start={base64_string}"
    
    Slink = await get_short(SL_URL, SL_API, Tlink)
    await bot_msg.edit(BOTEFITMSG.format(filname, botfsno[0], Tlink, Slink, DATEDAY[0]))
    await e_pic.edit(FOMET.format(DATEDAY[-1], Slink, Slink))

async def get_short(SL_URL, SL_API, Tlink):
    # FireLinks shorten
    try:
        api_url = f"https://{SL_URL}/api"
        params = {'api': SL_API, 'url': Tlink}
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url, params=params, raise_for_status=True) as response:
                data = await response.json()
                url = data["shortenedUrl"]
        return url
    except Exception as error:
        return error
    
@Bot.on_message(filters.channel & filters.incoming & filters.chat(CHANNEL_ID))
async def new_post(client: Client, message: Message):

    if DISABLE_CHANNEL_BUTTON:
        return

    converted_id = message.id * abs(client.db_channel.id)
    string = f"get-{converted_id}"
    base64_string = await encode(string)
    link = f"https://telegram.me/{client.username}?start={base64_string}"
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔁 Share URL", url=f'https://telegram.me/share/url?url={link}')]])
    try:
        await message.edit_reply_markup(reply_markup)
    except Exception as e:
        print(e)
        pass
