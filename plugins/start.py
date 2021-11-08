from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from config import BOT_NAME as bn
from helpers.filters import other_filters2
from time import time
from datetime import datetime
from helpers.decorators import authorized_users_only
from config import BOT_USERNAME, ASSISTANT_USERNAME

START_TIME = datetime.utcnow()
START_TIME_ISO = START_TIME.replace(microsecond=0).isoformat()
TIME_DURATION_UNITS = (
    ("week", 60 * 60 * 24 * 7),
    ("day", 60 ** 2 * 24),
    ("hour", 60 ** 2),
    ("min", 60),
    ("sec", 1),
)


async def _human_time_duration(seconds):
    if seconds == 0:
        return "inf"
    parts = []
    for unit, div in TIME_DURATION_UNITS:
        amount, seconds = divmod(int(seconds), div)
        if amount > 0:
            parts.append("{} {}{}".format(amount, unit, "" if amount == 1 else "s"))
    return ", ".join(parts)


@Client.on_message(other_filters2)
async def start(_, message: Message):
        await message.reply_sticker("CAACAgEAAx0CaJTWBAABAaZKYYVpAt94U3bXdW6Oh5rNJI-QrsoAAuYAA1EpDTnakgn2GsThDh4E")
        await message.reply_text(
        f"""**Hey, I'm {bn} ❤️
I Cᴀɴ Pʟᴀʏ Mᴜsɪᴄ Iɴ Yᴏᴜʀ Gʀᴏᴜᴩ Vᴏɪᴄᴇ Cʜᴀᴛ. Dᴇᴠᴇʟᴏᴩᴇᴅ Bʏ [𝚃𝚎𝚊𝚖𝙳𝚕𝚝-𝙳𝚎𝚟𝚜](https://t.me/teamDlt_developers).
Aᴅᴅ Mᴇ Tᴏ Yᴏᴜʀ Gʀᴏᴜᴩ Aɴᴅ Pʟᴀʏ Mᴜsɪᴄ Fʀᴇᴇʟʏ!**
        """,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "• ᴄᴏᴍᴍᴀɴᴅs •", url="https://te.legra.ph/file/e4018cc7caabc1498b15f.jpg")
                  ],[
                    InlineKeyboardButton(
                        "➕ ɢʀᴏᴜᴘ ᴍᴀɪ ᴀᴅᴅ ᴋᴀʀᴏ ➕", url=f"https://t.me/{BOT_USERNAME}?startgroup=true"
                    )
                  ],[
                    InlineKeyboardButton(
                       "• sᴜᴘᴘᴏʀᴛ •", url="https://t.me/teamDlt"
                    ),
                    InlineKeyboardButton(
                        "• ᴜᴘᴅᴀᴛᴇs •", url="https://t.me/teamDlt_update"
                    )
                ],[
                    InlineKeyboardButton(
                        "• sᴏᴜʀᴄᴇ ᴄᴏᴅᴇ •",
                        url="https://github.com/TeamDlt/TeamDltmusic",
                    )
                ]
            ]
        ),
     disable_web_page_preview=True
    )
