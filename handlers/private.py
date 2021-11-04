from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from config import BOT_NAME as bn
from helpers.filters import other_filters2


@Client.on_message(other_filters2)
async def start(_, message: Message):
    await message.reply_img("https://te.legra.ph/file/6dcdb51eec92071f66d38.jpg")
    await message.reply_text(
        f"""**ʜᴇʏ, I'm {bn} 🎵❤️
ɪ ᴄᴀɴ ᴘʟᴀʏ ᴍᴜꜱɪᴄ ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ'ꜱ ᴠᴏɪᴄᴇ ᴄᴀʟʟ. ᴅᴇᴠᴇʟᴏᴘᴇᴅ ʙʏ [👑 𝚂𝚘𝚖𝚢𝚊𝚓𝚎𝚎𝚝 𝙼𝚒𝚜𝚑𝚛𝚊 👑](https://t.me/Somyajeet_Mishra).
ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ ᴀɴᴅ ᴘʟᴀʏ ᴍᴜꜱɪᴄ ꜰʀᴇᴇʟʏ ᴛʜᴀɴᴋs 😀!**
        """,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "🛠 Sᴏᴜʀᴄᴇ ᴄᴏᴅᴇ 🛠", url="https://github.com/TeamDlt/TeamDltmusic")
                  ],[
                    InlineKeyboardButton(
                        "• Gʀᴏᴜᴘ •", url="https://t.me/teamDlt"
                    ),
                    InlineKeyboardButton(
                        "• Cʜᴀɴɴᴇʟ •", url="https://t.me/teamDlt_update"
                    )
                ],[ 
                    InlineKeyboardButton(
                        "Mᴀᴋᴇ ʏᴏᴜʀ ᴏᴡɴ ᴛᴏ ᴘʟᴇᴀsᴇ ᴄᴏɴᴛᴀᴄᴛ ᴍʏ ᴅᴇᴠᴇʟᴏᴘᴇʀ", url="https://t.me/Somyajeet_Mishra"
                    )]
            ]
        ),
     disable_web_page_preview=True
    )

@Client.on_message(filters.command("start") & ~filters.private & ~filters.channel)
async def gstart(_, message: Message):
      await message.reply_text("""**ᴀʀᴇ ʏʀʀ ᴊɪɴᴅᴀ ʜᴏᴏ ✅**""",
      reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "⚡Sᴏᴜʀᴄᴇ ᴄᴏᴅᴇ⚡", url="https://github.com/TeamDlt/TeamDltmusic")
                ]
            ]
        )
   )
