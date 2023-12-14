import aiohttp
import asyncio
from pyrogram import filters, Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors import FloodWait
from bot import Bot
from config import ADMINS, CHANNEL_ID, DISABLE_CHANNEL_BUTTON
from pathlib import Path
import subprocess
import requests
import jwt
import string
import re

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

m3u8DL_RE = 'N_m3u8DL-RE'

def replace_invalid_chars(title: str) -> str:
    invalid_chars = {'<': '\u02c2', '>': '\u02c3',
    ':': '\u02d0', '"': '\u02ba', '/': '\u2044',
    '\\': '\u29f9', '|': '\u01c0', '?': '\u0294',
    '*': '\u2217'}
    
    return ''.join(invalid_chars.get(c, c) for c in title)
    

def get_accesstoken():
            IdURL = "https://cs-jv.voot.com/clickstream/v1/get-id"
            GuestURL = "https://auth-jiocinema.voot.com/tokenservice/apis/v4/guest"
            id = requests.get(url=IdURL).json()['id']
        
            token = requests.post(url=GuestURL, json={
                    'adId': id,
                    "appName": "RJIL_JioCinema",
                    "appVersion": "23.10.13.0-841c2bc7",
                    "deviceId": id,
                    "deviceType": "phone",
                    "freshLaunch": True,
                    "os": "ios"
                }, headers={
                    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
                }).json()
    
            return token["authToken"],token["deviceId"]
    
    
@Bot.on_message(filters.command('start') & filters.private )
async def start_command(client: Client, message: Message):
    await message.reply_text("hello buddy ......",quote=True)
        

@Client.on_message(filters.private & filters.user(ADMINS) & filters.command(["date"]))
async def date(bot, message):
    if not update.from_user:
        return await update.reply_text("I don't know about you sar :(")
    # await add_user_to_database(bot, update)
    await bot.send_chat_action(
       chat_id=update.chat.id,
       action="typing"
    )
    #logger.info(update.from_user)
    text_from_user = update.text
    chk = await bot.send_message(
            chat_id=update.chat.id,
            text=f'<b>Processing... ⏳</b>',
            disable_web_page_preview=True,
            reply_to_message_id=update.message_id
          )
    if "jiocinema" in text_from_user:
        url = text_from_user
        print(url)
        logger.info(url)
        global dlink
        dlink = url
        hk = await mpd_call(dlink)
        pmpd,pkey,ptitle = hk
        await chk.dlete()
        await main_j_bot(bot, update,pmpd,pkey,ptitle)
        return url   
        
    else:
        await bot.edit_message_text(
        text=f'<b>I can download only JioCinema links..?\nSend jiocinema links to download...!!</b>',
        chat_id=update.chat.id,
        message_id=update.message_id
        )
        
        
import base64, requests, sys, xmltodict, json
from WKSKEYS.pywidevin.L3.cdm import deviceconfig
from base64 import b64encode
from WKSKEYS.pywidevin.L3.getPSSH import get_pssh
from WKSKEYS.pywidevin.L3.decrypt.wvdecryptcustom import WvDecrypt
import time
import re

async def WV_Function(pssh, lic_url, cert_b64=None):
                wvdecrypt = WvDecrypt(init_data_b64=pssh, cert_data_b64=cert_b64, device=deviceconfig.device_android_generic)                   
                widevine_license = requests.post(url=lic_url, data=wvdecrypt.get_challenge(), headers=headers, verify=False)
                license_b64 = b64encode(widevine_license.content)
                wvdecrypt.update_license(license_b64)
                Correct, keyswvdecrypt = wvdecrypt.start_process()
                if Correct:
                    return Correct, keyswvdecrypt
            Correct, keys = WV_Function(pssh, lic_url)

global pkey
pkey = keys[2]
            
            
import asyncio
import json
import math
import os
import shutil
import time
from datetime import datetime
from plugins.config import Config
from plugins.translation import Translation
# from plugins.custom_thumbnail import *
logging.getLogger("pyrogram").setLevel(logging.WARNING)
from pyrogram.types import InputMediaPhoto
from plugins.stuff import progress_for_pyrogram, humanbytes, random_char
# from plugins.database.database import db
from PIL import Image
#from jlink import mpd_call
ptitle= 
pmpd=
pkey= 

async def main_j_bot(bot, update,pmpd,pkey,ptitle):
    youtube_dl_url = pmpd
    random1 = random_char(5)
    custom_vfile_name = "video" + ".mp4"
    custom_dvfile_name = "videos" + ".mp4"
    custom_afile_name = "audio" + ".m4a"
    custom_dafile_name = "audios" + ".m4a"
    youtube_dl_username = None
    youtube_dl_password = None
    if "|" in youtube_dl_url:
        url_parts = youtube_dl_url.split("|")
        if len(url_parts) == 2:
            youtube_dl_url = url_parts[0]
            custom_file_name = url_parts[1]
        elif len(url_parts) == 4:
            youtube_dl_url = url_parts[0]
            custom_file_name = url_parts[1]
            youtube_dl_username = url_parts[2]
            youtube_dl_password = url_parts[3]
        else:
            for entity in update.message.reply_to_message.entities:
                if entity.type == "text_link":
                    youtube_dl_url = entity.url
                elif entity.type == "url":
                    o = entity.offset
                    l = entity.length
                    youtube_dl_url = youtube_dl_url[o:o + l]
        if youtube_dl_url is not None:
            youtube_dl_url = youtube_dl_url.strip()
        if custom_file_name is not None:
            custom_file_name = custom_file_name.strip()
        # https://stackoverflow.com/a/761825/4723940
        if youtube_dl_username is not None:
            youtube_dl_username = youtube_dl_username.strip()
        if youtube_dl_password is not None:
            youtube_dl_password = youtube_dl_password.strip()
        logger.info(youtube_dl_url)
        logger.info(custom_file_name)
    else:
        for entity in update.message.reply_to_message.entities:
            if entity.type == "text_link":
                youtube_dl_url = entity.url
            elif entity.type == "url":
                o = entity.offset
                l = entity.length
                youtube_dl_url = youtube_dl_url[o:o + l]
    await bot.edit_message_text(
        text=Translation.DOWNLOAD_START,
        chat_id=update.message.chat.id,
        message_id=update.message.message_id
    )
    description = Translation.CUSTOM_CAPTION_UL_FILE
    if description is None:
          description = ptitle
          #description = response_json["fulltitle"][0:1021]
        # escape Markdown and special characters
    tmp_directory_for_each_user = Config.DOWNLOAD_LOCATION + "/" + str(update.from_user.id) + f'{random1}'
    if not os.path.isdir(tmp_directory_for_each_user):
        os.makedirs(tmp_directory_for_each_user)
    download_V_directory = tmp_directory_for_each_user + "/" + custom_vfile_name
    download_DV_directory = tmp_directory_for_each_user + "/" + custom_dvfile_name
    download_A_directory = tmp_directory_for_each_user + "/" + custom_afile_name
    download_DA_directory = tmp_directory_for_each_user + "/" + custom_dafile_name
    download_FV_directory = tmp_directory_for_each_user + "/" + ptitle + ".mkv"
    command_to_exec = []
    if youtube_dl_url is not None:
        await bot.send_message(
            chat_id=update.chat.id,
            text=Translation.DOWNLOAD_START,
            disable_web_page_preview=True,
            reply_to_message_id=update.message_id
          )
        #downloading video
        command_to_exec = [
            "yt-dlp",
            "-f", "video=600000",
            "--max-filesize", str(Config.TG_MAX_FILE_SIZE),
            youtube_dl_url,
            "--allow-unplayable",
            "-o", download_V_directory
        ]
        if Config.HTTP_PROXY != "":
            command_to_exec.append("--proxy")
            command_to_exec.append(Config.HTTP_PROXY)
        if youtube_dl_username is not None:
            command_to_exec.append("--username")
            command_to_exec.append(youtube_dl_username)
        if youtube_dl_password is not None:
            command_to_exec.append("--password")
            command_to_exec.append(youtube_dl_password)
        command_to_exec.append("--no-warnings")
        # command_to_exec.append("--quiet")
        logger.info(command_to_exec)
        start = datetime.now()
        process = await asyncio.create_subprocess_exec(
            *command_to_exec,
            # stdout must a pipe to be accessible as process.stdout
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        # Wait for the subprocess to finish
        stdout, stderr = await process.communicate()
        e_response = stderr.decode().strip()
        t_response = stdout.decode().strip()
        logger.info(e_response)
        logger.info(t_response)
        ad_string_to_replace = "please report this issue on https://yt-dl.org/bug . Make sure you are using the latest version; see  https://yt-dl.org/update  on how to update. Be sure to call youtube-dl with the --verbose flag and include its complete output."
        if e_response and ad_string_to_replace in e_response:
            error_message = e_response.replace(ad_string_to_replace, "")
            await bot.edit_message_text(
                chat_id=update.message.chat.id,
                message_id=update.message.message_id,
                text=error_message
            )
            return False

        # downloading audio
        command_to_exec = [
            "yt-dlp",
            "-f", "bestaudio",
            youtube_dl_url,
            "--allow-unplayable",
            "-o", download_A_directory
        ]

        await bot.edit_message_text(
                chat_id=update.message.chat.id,
                message_id=update.message.message_id,
                text=f"Downloading audio..!!"
            )

        command_to_exec.append("--no-warnings")
        # command_to_exec.append("--quiet")
        logger.info(command_to_exec)
        # start = datetime.now()
        process = await asyncio.create_subprocess_exec(
            *command_to_exec,
            # stdout must a pipe to be accessible as process.stdout
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        # Wait for the subprocess to finish
        stdout, stderr = await process.communicate()
        e_response = stderr.decode().strip()
        t_response = stdout.decode().strip()

        # Decrypting video
        command_to_exec = [
            'mp4decrypt',
            '--key',pkey,
            download_V_directory,download_DV_directory
        ]
        await bot.edit_message_text(
                chat_id=update.message.chat.id,
                message_id=update.message.message_id,
                text=f"Decrypting video..!!"
            )
        logger.info(command_to_exec)
        process = await asyncio.create_subprocess_exec(
            *command_to_exec,
            # stdout must a pipe to be accessible as process.stdout
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        # Wait for the subprocess to finish
        stdout, stderr = await process.communicate()
        e_response = stderr.decode().strip()
        t_response = stdout.decode().strip()

        # Decrypting audio
        command_to_exec = [
            'mp4decrypt',
            '--key',pkey,
            download_A_directory,download_DA_directory
        ]
        await bot.edit_message_text(
                chat_id=update.message.chat.id,
                message_id=update.message.message_id,
                text=f"Decrypting audio..!!"
            )
        logger.info(command_to_exec)
        process = await asyncio.create_subprocess_exec(
            *command_to_exec,
            # stdout must a pipe to be accessible as process.stdout
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        # Wait for the subprocess to finish
        stdout, stderr = await process.communicate()
        e_response = stderr.decode().strip()
        t_response = stdout.decode().strip()

        # Merging video and audio
        command_to_exec = [
            'ffmpeg',
            '-i', download_DV_directory,'-i', download_DA_directory,'-vcodec' ,'copy' ,'-acodec' ,'copy',download_FV_directory
        ]
        await bot.edit_message_text(
                chat_id=update.message.chat.id,
                message_id=update.message.message_id,
                text=f"Merging video and audio..!!"
            )
        logger.info(command_to_exec)
        process = await asyncio.create_subprocess_exec(
            *command_to_exec,
            # stdout must a pipe to be accessible as process.stdout
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        # Wait for the subprocess to finish
        stdout, stderr = await process.communicate()
        e_response = stderr.decode().strip()
        t_response = stdout.decode().strip()
      
        end_one = datetime.now()
        time_taken_for_download = (end_one -start).seconds
        file_size = Config.TG_MAX_FILE_SIZE + 1
        try:
            file_size = os.stat(download_FV_directory).st_size
        except FileNotFoundError as exc:
            download_FV_directory = os.path.splitext(download_FV_directory)[0] + "." + "mkv"
            # https://stackoverflow.com/a/678242/4723940
            file_size = os.stat(download_FV_directory).st_size
        if file_size > Config.TG_MAX_FILE_SIZE:
            await bot.edit_message_text(
                chat_id=update.message.chat.id,
                text=Translation.RCHD_TG_API_LIMIT.format(time_taken_for_download, humanbytes(file_size)),
                message_id=update.message.message_id
            )
        else:
            is_w_f = False
            '''images = await generate_screen_shots(
                download_directory,
                tmp_directory_for_each_user,
                is_w_f,
                Config.DEF_WATER_MARK_FILE,
                300,
                9
            )
            logger.info(images)'''
            await bot.edit_message_text(
                text=f"Download completed.",
                chat_id=update.message.chat.id,
                message_id=update.message.message_id
            )

            # ref: message from @Sources_codes
            start_time = time.time()
            if os.path.exists(download_FV_directory):
                try:
                    thumbnail = await Gthumb(bot, update)
                    await bot.send_document(
                        chat_id=update.message.chat.id,
                        document=download_FV_directory,
                        thumb=thumbnail,
                        caption=description,
                        reply_to_message_id=update.message.reply_to_message.message_id,
                        progress=progress_for_pyrogram,
                        progress_args=(
                            "Uploading Document..!",
                            update.message,
                            start_time
                        )
                    )
                except:
                     width, height, duration = await Mdata01(download_directory)
                     thumb_image_path = await Gthumb(bot, update, duration, download_directory)
                     await bot.send_video(
                        chat_id=update.message.chat.id,
                        video=download_FV_directory,
                        caption=description,
                        duration=duration,
                        width=width,
                        height=height,
                        supports_streaming=True,
                        thumb=thumb_image_path,
                        reply_to_message_id=update.message.reply_to_message.message_id,
                        progress=progress_for_pyrogram,
                        progress_args=(
                            "Uploading Video",
                            update.message,
                            start_time
                        )
                    )
            
            else:
                logger.info("Did this happen? :\\")
                await bot.send_message(
                text=f"Downloaded file not found..!",
                chat_id=update.message.chat.id,
                message_id=update.message.message_id,
                disable_web_page_preview=True
                )
              
            end_two = datetime.now()
            time_taken_for_upload = (end_two - end_one).seconds
            try:
                shutil.rmtree(tmp_directory_for_each_user)
                os.remove(thumbnail)
            except:
                pass
            await bot.edit_message_text(
                text=Translation.AFTER_SUCCESSFUL_UPLOAD_MSG_WITH_TS.format(time_taken_for_download, time_taken_for_upload),
                chat_id=update.message.chat.id,
                message_id=update.message.message_id,
                disable_web_page_preview=True
            )
    # Delete the contenet(video and audio stuff)
    # os.remove(tmp_directory_for_each_user)
    else:
        # command_to_exec = ["youtube-dl", "-f", youtube_dl_format, "--hls-prefer-ffmpeg", "--recode-video", "mp4", "-k", youtube_dl_url, "-o", download_directory]
        await bot.edit_message_text(
                chat_id=update.message.chat.id,
                message_id=update.message.message_id,
                text=f"There is problem with your link please send valid link..!!"
            )

    if t_response:
        logger.info(t_response)
        try:
            os.remove(save_ytdl_json_path)
        except FileNotFoundError as exc:
            pass