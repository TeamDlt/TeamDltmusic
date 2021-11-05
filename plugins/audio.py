from os import path

from pyrogram import Client
from pyrogram.types import Message, Voice
from pytgcalls.types.input_stream import InputAudioStream
from Client import callsmusic, queues

import converter
from youtube import youtube

from config import BOT_NAME as bn, DURATION_LIMIT, UPDATES_CHANNEL, AUD_IMG, QUE_IMG, GROUP_SUPPORT
from helpers.filters import command, other_filters
from helpers.decorators import errors
from helpers.errors import DurationLimitError
from helpers.gets import get_url, get_file_name
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


@Client.on_message(command("audio") & other_filters)
@errors
async def stream(_, message: Message):

    lel = await message.reply("🎙 **𝐏𝐥𝐞𝐚𝐬𝐞 𝐖𝐚𝐢𝐭**  𝐒𝐞𝐚𝐫𝐜𝐡𝐢𝐧𝐠....")
    sender_id = message.from_user.id
    sender_name = message.from_user.first_name

    keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="✨ ɢʀᴏᴜᴘ",
                        url=f"https://t.me/teamDlt"),
                    InlineKeyboardButton(
                        text="📢 ᴄʜᴀɴɴᴇʟ",
                        url=f"https://t.me/{UPDATES_CHANNEL}")
                ]
            ]
        )

    audio = (message.reply_to_message.audio or message.reply_to_message.voice) if message.reply_to_message else None
    url = get_url(message)

    if audio:
        if round(audio.duration / 60) > DURATION_LIMIT:
            raise DurationLimitError(
                f"❌ 𝐒𝐨𝐫𝐫𝐲 𝐦𝐮𝐬𝐢𝐜 𝐰𝐢𝐭𝐡 𝐝𝐮𝐫𝐚𝐭𝐢𝐨𝐧 𝐦𝐨𝐫𝐞 𝐭𝐡𝐚𝐧 {DURATION_LIMIT} 𝐦𝐢𝐧𝐮𝐭𝐞(𝐬) 𝐚𝐫𝐞𝐧'𝐭 𝐚𝐥𝐥𝐨𝐰𝐞𝐝 𝐭𝐨 𝐩𝐥𝐚𝐲!"
            )

        file_name = get_file_name(audio)
        file_path = await converter.convert(
            (await message.reply_to_message.download(file_name))
            if not path.isfile(path.join("downloads", file_name)) else file_name
        )
    elif url:
        file_path = await converter.convert(youtube.download(url))
    else:
        return await lel.edit_text("! 𝐲𝐨𝐮 𝐝𝐢𝐝 𝐧𝐨𝐭 𝐠𝐢𝐯𝐞 𝐦𝐞 𝐚𝐮𝐝𝐢𝐨 𝐟𝐢𝐥𝐞 𝐨𝐫 𝐲𝐭 𝐥𝐢𝐧𝐤 𝐭𝐨 𝐬𝐭𝐫𝐞𝐚𝐦!")
    ACTV_CALLS = []
    for x in callsmusic.pytgcalls.active_calls:
        ACTV_CALLS.append(int(x.chat_id))    
    if int(message.chat.id) in ACTV_CALLS:
        position = await queues.put(message.chat.id, file=file_path)
        await message.reply_photo(
        photo=f"{QUE_IMG}",
        reply_markup=keyboard,
        caption=f"#⃣  𝐲𝐨𝐮𝐫 𝐫𝐞𝐪𝐮𝐞𝐬𝐭𝐞𝐝 𝐬𝐨𝐧𝐠 𝐰𝐚𝐬 𝐚𝐝𝐝𝐞𝐝 𝐭𝐨 *𝐪𝐮𝐞𝐮𝐞* 𝐚𝐭 𝐩𝐨𝐬𝐢𝐭𝐢𝐨𝐧 {position}!\n\n⚡ __𝐏𝐨𝐰𝐞𝐫𝐞𝐝 𝐛𝐲 𝐓𝐞𝐚𝐦𝐃𝐥𝐭 𝐀.𝐈__")
        return await lel.delete()
    else:
        await callsmusic.pytgcalls.join_group_call(message.chat.id, InputAudioStream(file_path))
        costumer = message.from_user.mention
        await message.reply_photo(
        photo=f"{AUD_IMG}",
        reply_markup=keyboard,
        caption=f"🎧 **𝐍𝐨𝐰 𝐩𝐥𝐚𝐲𝐢𝐧𝐠** 𝐚 𝐬𝐨𝐧𝐠 𝐫𝐞𝐪𝐮𝐞𝐬𝐭𝐞𝐝 𝐛𝐲 {costumer}!\n\n⚡ __𝐏𝐨𝐰𝐞𝐫𝐞𝐝 𝐛𝐲 𝐓𝐞𝐚𝐦𝐃𝐥𝐭 𝐀.𝐈__"
        )
        return await lel.delete()
