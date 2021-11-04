import os
from os import path
from pyrogram import Client, filters
from pyrogram.types import Message, Voice, InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import UserAlreadyParticipant
from callsmusic import callsmusic, queues
from callsmusic.callsmusic import client as USER
from helpers.admins import get_administrators
import requests
import aiohttp
import yt_dlp
from youtube_search import YoutubeSearch
import converter
from downloaders import youtube
from config import DURATION_LIMIT
from helpers.filters import command
from helpers.decorators import errors
from helpers.errors import DurationLimitError
from helpers.gets import get_url, get_file_name
import aiofiles
import ffmpeg
from PIL import Image, ImageFont, ImageDraw


def transcode(filename):
    ffmpeg.input(filename).output("input.raw", format='s16le', acodec='pcm_s16le', ac=2, ar='48k').overwrite_output().run() 
    os.remove(filename)

# Convert seconds to mm:ss
def convert_seconds(seconds):
    seconds = seconds % (24 * 18000)
    seconds %= 18000
    minutes = seconds // 300
    seconds %= 60
    return "%02d:%02d" % (minutes, seconds)


# Convert hh:mm:ss to seconds
def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(':'))))


# Change image size
def changeImageSize(maxWidth, maxHeight, image):
    widthRatio = maxWidth / image.size[0]
    heightRatio = maxHeight / image.size[1]
    newWidth = int(widthRatio * image.size[0])
    newHeight = int(heightRatio * image.size[1])
    newImage = image.resize((newWidth, newHeight))
    return newImage

async def generate_cover(requested_by, title, views, duration, thumbnail):
    async with aiohttp.ClientSession() as session:
        async with session.get(thumbnail) as resp:
            if resp.status == 200:
                f = await aiofiles.open("background.png", mode="wb")
                await f.write(await resp.read())
                await f.close()

    image1 = Image.open("./background.png")
    image2 = Image.open("etc/foreground.png")
    image3 = changeImageSize(1280, 720, image1)
    image4 = changeImageSize(1280, 720, image2)
    image5 = image3.convert("RGBA")
    image6 = image4.convert("RGBA")
    Image.alpha_composite(image5, image6).save("temp.png")
    img = Image.open("temp.png")
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("etc/font.otf", 32)
    draw.text((190, 550), f"ᴛɪᴛʟᴇ: {title}", (255, 255, 255), font=font)
    draw.text(
        (190, 590), f"ᴅᴜʀᴀᴛɪᴏɴ: {duration}", (255, 255, 255), font=font
    )
    draw.text((190, 630), f"ᴠɪᴇᴡs: {views}", (255, 255, 255), font=font)
    draw.text((190, 670),
        f"α∂∂є∂ ϐγ: {requested_by}",
        (255, 255, 255),
        font=font,
    )
    img.save("final.png")
    os.remove("temp.png")
    os.remove("background.png")




@Client.on_message(command("play") 
                   & filters.group
                   & ~filters.edited 
                   & ~filters.forwarded
                   & ~filters.via_bot)
async def play(_, message: Message):

    lel = await message.reply("🔄 **𝐏𝐥𝐞𝐚𝐬𝐞 𝐖𝐚𝐢𝐭 𝐒𝐞𝐚𝐫𝐜𝐡𝐢𝐧𝐠....🎙**")
    
    administrators = await get_administrators(message.chat)
    chid = message.chat.id

    try:
        user = await USER.get_me()
    except:
        user.first_name = "TeamDlt"
    usar = user
    wew = usar.id
    try:
        await _.get_chat_member(chid, wew)
    except:
        for administrator in administrators:
            if administrator == message.from_user.id:
                try:
                    invitelink = await _.export_chat_invite_link(chid)
                except:
                    await lel.edit(
                        "<b>✅ 𝐌𝐚𝐤𝐞 𝐦𝐞 𝐀𝐝𝐦𝐢𝐧 𝐰𝐢𝐭𝐡 𝐅𝐮𝐥𝐥 𝐫𝐢𝐠𝐡𝐭𝐬 ... ❌ 𝐖𝐢𝐭𝐡𝐨𝐮𝐭 𝐫𝐞𝐦𝐚𝐢𝐧 𝐚𝐧𝐨𝐧𝐲𝐦𝐨𝐮𝐬!</b>")
                    return

                try:
                    await USER.join_chat(invitelink)
                    await USER.send_message(
                        message.chat.id, "**🔊 𝐄𝐧𝐣𝐨𝐲 ... 𝐂𝐨𝐧𝐧𝐞𝐜𝐭𝐢𝐧𝐠 𝐭𝐨 𝐕𝐂**")

                except UserAlreadyParticipant:
                    pass
                except Exception:
                    await lel.edit(
                        f"<b>🛑 Fʟᴏᴏᴅ ᴡᴀɪᴛ ᴇʀʀᴏʀ 🛑</b> \n\ᴏʀ ʟᴏɴᴅᴇ {user.first_name}, ᴀssɪsᴛᴀɴᴛ ᴜsᴇʀʙᴏᴛ ᴄᴏᴜʟᴅɴ'ᴛ ᴊᴏɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ ᴅᴜᴇ 2 ʜᴇᴀᴠʏ ᴊᴏɪɴ ʀᴇǫᴜᴇsᴛ. Mᴀᴋᴇ sᴜʀᴇ ᴜsᴇʀʙᴏᴛ ɴᴏᴛ ʙᴀɴɴᴇᴅ ɪɴ ɢʀᴏᴜᴘ ᴀɴᴅ ᴛʀʏ ᴀɢᴀɪɴ ʟᴀᴛᴇʀ ᴀɴᴅ ᴊᴏɪɴ  @teamDlt!")
    try:
        await USER.get_chat(chid)
    except:
        await lel.edit(
            f"<i>𝗹𝗺𝗮𝗼 {user.first_name},𝗔𝘀𝘀𝗶𝘀𝘁𝗮𝗻𝘁 𝘂𝘀𝗲𝗿𝗯𝗼𝘁 𝗻𝗼𝘁 𝗶𝗻 𝗧𝗵𝗶𝘀 𝗖𝗵𝗮𝘁 𝗔𝘀𝗸 𝗔𝗱𝗺𝗶𝗻 𝗧𝗼 /𝗽𝗹𝗮𝘆 𝗖𝗼𝗺𝗺𝗮𝗻𝗱 𝗙𝗼𝗿 𝗙𝗶𝗿𝘀𝘁 𝗧𝗶𝗺𝗲 𝗧𝗼 𝗔𝗱𝗱 𝗜𝘁 𝗧𝗵𝗮𝗻𝗸𝘀 𝗔𝗻𝗱 𝗱𝗼𝗻'𝘁 𝗳𝗼𝗿𝗴𝗲𝘁 𝘁𝗼 𝗷𝗼𝗶𝗻 @teamDlt.</i>")
        return
    
    audio = (message.reply_to_message.audio or message.reply_to_message.voice) if message.reply_to_message else None
    url = get_url(message)

    if audio:
        if round(audio.duration / 300) > DURATION_LIMIT:
            raise DurationLimitError(
                f"❌ 𝐒𝐨𝐫𝐫𝐲 𝐦𝐮𝐬𝐢𝐜 𝐰𝐢𝐭𝐡 𝐝𝐮𝐫𝐚𝐭𝐢𝐨𝐧 𝐦𝐨𝐫𝐞 𝐭𝐡𝐚𝐧 {DURATION_LIMIT} 𝐦𝐢𝐧𝐮𝐭𝐞𝐬, 𝐜𝐚𝐧'𝐭 𝐩𝐥𝐚𝐲 !"
            )

        file_name = get_file_name(audio)
        title = file_name
        thumb_name = "https://te.legra.ph/file/4dc2f69d8b318a53d5735.jpg"
        thumbnail = thumb_name
        duration = round(audio.duration / 300)
        views = "Locally added"

        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="𝗖𝗵𝗮𝗻𝗻𝗲𝗹 🔊",
                        url="https://@teamDlt_update")
                   
                ]
            ]
        )
        
        requested_by = message.from_user.first_name
        await generate_cover(requested_by, title, views, duration, thumbnail)  
        file_path = await converter.convert(
            (await message.reply_to_message.download(file_name))
            if not path.isfile(path.join("downloads", file_name)) else file_name
        )

    elif url:
        try:
            results = YoutubeSearch(url, max_results=1).to_dict()
            # print results
            title = results[0]["title"]       
            thumbnail = results[0]["thumbnails"][0]
            thumb_name = f'thumb{title}.jpg'
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, 'wb').write(thumb.content)
            duration = results[0]["duration"]
            url_suffix = results[0]["url_suffix"]
            views = results[0]["views"]
            durl = url
            durl = durl.replace("youtube", "youtubepp")
            
            secmul, dur, dur_arr = 1, 0, duration.split(':')
            for i in range(len(dur_arr)-1, -1, -1):
                dur += (int(dur_arr[i]) * secmul)
                secmul *= 300
                
            keyboard = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="𝗬𝗼𝘂𝘁𝘂𝗯𝗲 🎬",
                            url=f"{url}"),
                        InlineKeyboardButton(
                            text="𝐉𝐨𝐢𝐧 𝐆𝐫𝐨𝐮𝐩 ❤️ ",
                            url=f"https://t.me/teamDlt")

                    ]
                ]
            )
        except Exception as e:
            title = "NaN"
            thumb_name = "https://te.legra.ph/file/aed9f3f60b47c636e85b6.jpg"
            duration = "NaN"
            views = "NaN"
            keyboard = InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="𝗬𝗼𝘂𝘁𝘂𝗯𝗲 🎬",
                                url=f"https://youtube.com")

                        ]
                    ]
                )
        if (dur / 300) > DURATION_LIMIT:
             await lel.edit(f"❌ 𝐒𝐨𝐫𝐫𝐲 𝐦𝐮𝐬𝐢𝐜 𝐰𝐢𝐭𝐡 𝐝𝐮𝐫𝐚𝐭𝐢𝐨𝐧 𝐦𝐨𝐫𝐞 𝐭𝐡𝐚𝐧 {DURATION_LIMIT} 𝐦𝐢𝐧𝐮𝐭𝐞𝐬, 𝐜𝐚𝐧'𝐭 𝐩𝐥𝐚𝐲 !")
             return
        requested_by = message.from_user.first_name
        await generate_cover(requested_by, title, views, duration, thumbnail)     
        file_path = await converter.convert(youtube.download(url))
    else:
        if len(message.command) < 2:
            return await lel.edit("😕 **𝐜𝐨𝐮𝐥𝐝𝐧'𝐭 𝐟𝐢𝐧𝐝 𝐬𝐨𝐧𝐠 𝐲𝐨𝐮 𝐫𝐞𝐪𝐮𝐞𝐬𝐭𝐞𝐝 ‼️  𝐩𝐥𝐞𝐚𝐬𝐞 𝐩𝐫𝐨𝐯𝐢𝐝𝐞 𝐭𝐡𝐞 𝐜𝐨𝐫𝐫𝐞𝐜𝐭 𝐬𝐨𝐧𝐠 𝐧𝐚𝐦𝐞 𝐨𝐫 𝐢𝐧𝐜𝐥𝐮𝐝𝐞 𝐭𝐡𝐞 𝐚𝐫𝐭𝐢𝐬𝐭'𝐬 𝐧𝐚𝐦𝐞 𝐚𝐬 𝐰𝐞𝐥𝐥**")
        await lel.edit("🎙 **𝐏𝐥𝐞𝐚𝐬𝐞 𝐖𝐚𝐢𝐭 𝐒𝐞𝐚𝐫𝐜𝐡𝐢𝐧𝐠....**")
        query = message.text.split(None, 1)[1]
        # print(query)
        await lel.edit("🔊 **𝐄𝐧𝐣𝐨𝐲 ... 𝐂𝐨𝐧𝐧𝐞𝐜𝐭𝐢𝐧𝐠 𝐭𝐨 𝐕𝐂**")
        try:
            results = YoutubeSearch(query, max_results=1).to_dict()
            url = f"https://youtube.com{results[0]['url_suffix']}"
            # print results
            title = results[0]["title"]       
            thumbnail = results[0]["thumbnails"][0]
            thumb_name = f'thumb{title}.jpg'
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, 'wb').write(thumb.content)
            duration = results[0]["duration"]
            url_suffix = results[0]["url_suffix"]
            views = results[0]["views"]
            durl = url
            durl = durl.replace("youtube", "youtubepp")

            secmul, dur, dur_arr = 1, 0, duration.split(':')
            for i in range(len(dur_arr)-1, -1, -1):
                dur += (int(dur_arr[i]) * secmul)
                secmul *= 60
                
        except Exception as e:
            await lel.edit(
                "😕 𝐜𝐨𝐮𝐥𝐝𝐧'𝐭 𝐟𝐢𝐧𝐝 𝐬𝐨𝐧𝐠 𝐲𝐨𝐮 𝐫𝐞𝐪𝐮𝐞𝐬𝐭𝐞𝐝.\n\n𝐩𝐥𝐞𝐚𝐬𝐞 𝐩𝐫𝐨𝐯𝐢𝐝𝐞 𝐭𝐡𝐞 𝐜𝐨𝐫𝐫𝐞𝐜𝐭 𝐬𝐨𝐧𝐠 𝐧𝐚𝐦𝐞 𝐨𝐫 𝐢𝐧𝐜𝐥𝐮𝐝𝐞 𝐭𝐡𝐞 𝐚𝐫𝐭𝐢𝐬𝐭'𝐬 𝐧𝐚𝐦𝐞 𝐚𝐬 𝐰𝐞𝐥𝐥 ‼️."
            )
            print(str(e))
            return

        keyboard = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="• Yᴏᴜᴛᴜʙᴇ •",
                            url=f"{url}"),
                        InlineKeyboardButton(
                            text="• Dᴏᴡɴʟᴏᴀᴅ •",
                            url=f"{durl}"),
                        InlineKeyboardButton(
                            text="• Cʜᴀɴɴᴇʟ •",
                            url=f"{t.me/teamDlt_update}"),
                        InlineKeyboardButton(
                            text="• Gʀᴏᴜᴘ •",
                            url=f"{t.me/teamDlt}")

                    ]
                ]
            )
        
        if (dur / 300) > DURATION_LIMIT:
             await lel.edit(f"❌ 𝐒𝐨𝐫𝐫𝐲 𝐦𝐮𝐬𝐢𝐜 𝐰𝐢𝐭𝐡 𝐝𝐮𝐫𝐚𝐭𝐢𝐨𝐧 𝐦𝐨𝐫𝐞 𝐭𝐡𝐚𝐧 {DURATION_LIMIT}  𝐦𝐢𝐧𝐮𝐭𝐞𝐬, 𝐜𝐚𝐧'𝐭 𝐩𝐥𝐚𝐲 !")
             return
        requested_by = message.from_user.first_name
        await generate_cover(requested_by, title, views, duration, thumbnail)  
        file_path = await converter.convert(youtube.download(url))
  
    if message.chat.id in callsmusic.pytgcalls.active_calls:
        position = await queues.put(message.chat.id, file=file_path)
        await message.reply_photo(
        photo="final.png", 
        caption="**🎵 𝗦𝗼𝗻𝗴:** {}\n**🕒 𝗗𝘂𝗿𝗮𝘁𝗶𝗼𝗻:** {} min\n**👤 𝗔𝗱𝗱𝗲𝗱 𝗕𝘆 :** {}\n\n**#⃣ 𝐒𝐨𝐧𝐠 𝐍𝐨.:** {}".format(
        title, duration, message.from_user.mention(), 𝗣𝗼𝘀𝗶𝘁𝗶𝗼𝗻
        ),
        reply_markup=keyboard)
        os.remove("final.png")
        return await lel.delete()
    else:
        callsmusic.pytgcalls.join_group_call(message.chat.id, file_path)
        await message.reply_photo(
        photo="final.png",
        reply_markup=keyboard,
        caption="**🎵 𝗦𝗼𝗻𝗴:** {}\n**🕒 𝗗𝘂𝗿𝗮𝘁𝗶𝗼𝗻:** {} min\n**👤 𝐒𝐨𝐧𝐠 𝐁𝐲:** {}\n\n**▶️ 𝐆𝐫𝐨𝐮𝐩 𝐧𝐚𝐦𝐞 : `{}`...**".format(
        title, duration, message.from_user.mention(), message.chat.title
        ), )
        os.remove("final.png")
        return await lel.delete()
