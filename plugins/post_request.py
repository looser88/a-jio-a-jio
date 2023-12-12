#(©)Codexbotz

import aiohttp
import asyncio
from pyrogram import filters, Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors import FloodWait
from bot import Bot
from config import ADMINS, CHANNEL_ID, DISABLE_CHANNEL_BUTTON
import string
import re

@Bot.on_message(filters.command('start') & filters.private & subscribed)
await message.reply_photo(
            photo="https://graph.org/file/983729d2228bafb4aad71.jp",
            caption="hello buddy ..."),
            quote = True)
        
# /date commend for set date
@Client.on_message(filters.private & filters.user(ADMINS) & filters.command(["date"]))
async def date(bot, message):
    dat = await message.reply_text("Select your Date.........",quote=True,reply_markup=InlineKeyboardMarkup([[ 
        			InlineKeyboardButton("Yesterday",callback_data='ystdy'), 
        			InlineKeyboardButton("Today",callback_data = 'tdy'), 
        			InlineKeyboardButton("Tommorow",callback_data='tmr') ]]))

@Bot.on_message(filters.private & filters.user(ADMINS) & ~filters.text)
async def channel_post(client: Client, message: Message):
