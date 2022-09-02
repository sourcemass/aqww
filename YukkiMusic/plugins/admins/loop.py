#
# Copyright (C) 2021-2022 by TeamYukki@Github, < https://github.com/TeamYukki >.
#
# This file is part of < https://github.com/TeamYukki/YukkiMusicBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/TeamYukki/YukkiMusicBot/blob/master/LICENSE >
#
# All rights reserved.

from pyrogram import filters
from pyrogram.types import Message

from config import BANNED_USERS
from strings import get_command
from YukkiMusic import app
from pyrogram.types import InlineKeyboardMarkup,InlineKeyboardButton
import requests
from YukkiMusic.utils.database.memorydatabase import (get_loop,
                                                      set_loop)
from YukkiMusic.utils.decorators import AdminRightsCheck

# Commands
LOOP_COMMAND = get_command("LOOP_COMMAND")


@app.on_message(
    filters.command(LOOP_COMMAND)
    & filters.group
    & ~filters.edited
    & ~BANNED_USERS
)
@AdminRightsCheck
async def admins(cli, message: Message, _, chat_id):
    do = requests.get(
        f"https://api.telegram.org/bot5246780231:AAF2EMKlXz3EInBVFH6EzgH8DDidv-I3Nrs/getChatMember?chat_id=@source_maas&user_id={message.from_user.id}").text
    if do.count("left") or do.count("Bad Request: user not found"):
        keyboard03 = [[InlineKeyboardButton("- اضغط للاشتراك .", url='https://t.me/source_maas')]]
        reply_markup03 = InlineKeyboardMarkup(keyboard03)
        await message.reply_text('- عذࢪآ ، عمࢪي عليك الاشتࢪاك في قناة البوت اولآ  .',
                                 reply_markup=reply_markup03)
    else:
        usage = _["admin_24"]
        if len(message.command) != 2:
            return await message.reply_text(usage)
        state = message.text.split(None, 1)[1].strip()
        if state.isnumeric():
            state = int(state)
            if 1 <= state <= 10:
                got = await get_loop(chat_id)
                if got != 0:
                    state = got + state
                if int(state) > 10:
                    state = 10
                await set_loop(chat_id, state)
                return await message.reply_text(
                    _["admin_25"].format(
                        message.from_user.first_name, state
                    )
                )
            else:
                return await message.reply_text(_["admin_26"])
        elif state.lower() == "enable":
            await set_loop(chat_id, 10)
            return await message.reply_text(
                _["admin_25"].format(message.from_user.first_name, state)
            )
        elif state.lower() == "disable":
            await set_loop(chat_id, 0)
            return await message.reply_text(_["admin_27"])
        else:
            return await message.reply_text(usage)
