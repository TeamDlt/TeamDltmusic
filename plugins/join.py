# Credit DaisyXMusic, Changes By Blaze, Improve Code By Decode

from pyrogram import Client, filters
from pyrogram.errors import UserAlreadyParticipant
import asyncio
from helpers.decorators import authorized_users_only, errors
from Client.callsmusic import client as USER
from config import SUDO_USERS


@Client.on_message(filters.command(["userbotjoin", "join"]) & ~filters.private & ~filters.bot)
@authorized_users_only
@errors
async def addchannel(client, message):
    chid = message.chat.id
    try:
        invitelink = await client.export_chat_invite_link(chid)
    except:
        await message.reply_text(
            "<b>Add me admin first</b>",
        )
        return

    try:
        user = await USER.get_me()
    except:
        user.first_name = "@DeCode_Assistant"

    try:
        await USER.join_chat(invitelink)
    except UserAlreadyParticipant:
        await message.reply_text(
            f"<b>{user.first_name} Allready join this Group</b>",
        )
    except Exception as e:
        print(e)
        await message.reply_text(
            f"<b>Flood Wait Error\n{user.first_name} can't join your group due to many join requests for userbot! Make sure the user is not banned in the group."
            "\n\nOr manually add the Assistant bot to your Group and try again.</b>",
        )
        return
    await message.reply_text(
        f"<b>{user.first_name} Join Seccsesfully</b>",
    )


@USER.on_message(filters.group & filters.command(["userbotleave"]))
@authorized_users_only
async def rem(USER, message):
    try:
        await USER.leave_chat(message.chat.id)
    except:
        await message.reply_text(
            "<b>Users cannot leave your group! Probably waiting for floodwaits.\n\nOr manually remove me from your Group</b>"
        )

        return


@Client.on_message(filters.command(["userbotleaveall"]))
async def bye(client, message):
    if message.from_user.id not in SUDO_USERS:
        return

    left = 0
    failed = 0
    lol = await message.reply("**Asisten Meninggalkan semua obrolan**")
    async for dialog in USER.iter_dialogs():
        try:
            await USER.leave_chat(dialog.chat.id)
            left += 1
            await lol.edit(
                f"Assistant leaving... Left: {left} chats. Failed: {failed} chats."
            )
        except:
            failed += 1
            await lol.edit(
                f"Assistant leaving... Left: {left} chats. Failed: {failed} chats."
            )
        await asyncio.sleep(0.7)
    await client.send_message(
        message.chat.id, f"Left {left} chats. Failed {failed} chats."
    )

