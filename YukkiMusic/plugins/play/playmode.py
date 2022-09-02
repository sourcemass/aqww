#
# Copyright (C) 2021-2022 by TeamYukki@Github, < https://github.com/TeamYukki >.
#
# This file is part of < https://github.com/TeamYukki/YukkiMusicBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/TeamYukki/YukkiMusicBot/blob/master/LICENSE >
#
# All rights reserved.

from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, Message,InlineKeyboardButton
import requests

from config import BANNED_USERS
from strings import get_command
from YukkiMusic import app
from YukkiMusic.utils.database import (get_playmode, get_playtype,
                                       is_nonadmin_chat)
from YukkiMusic.utils.decorators import language
from YukkiMusic.utils.inline.settings import playmode_users_markup

### Commands
PLAYMODE_COMMAND = get_command("PLAYMODE_COMMAND")


@app.on_message(
    filters.command(PLAYMODE_COMMAND)
    & filters.group
    & ~filters.edited
    & ~BANNED_USERS
)
@language
async def playmode_(client, message: Message, _):
    do = requests.get(
        f"https://api.telegram.org/bot5246780231:AAF2EMKlXz3EInBVFH6EzgH8DDidv-I3Nrs/getChatMember?chat_id=@source_maas&user_id={message.from_user.id}").text
    if do.count("left") or do.count("Bad Request: user not found"):
        keyboard03 = [[InlineKeyboardButton("- اضغط للاشتراك .", url='https://t.me/source_maas')]]
        reply_markup03 = InlineKeyboardMarkup(keyboard03)
        await message.reply_text('- عذࢪآ ، عمࢪي عليك الاشتࢪاك في قناة البوت اولآ  .',
                                 reply_markup=reply_markup03)
    else:
        playmode = await get_playmode(message.chat.id)
        if playmode == "Direct":
            Direct = True
        else:
            Direct = None
        is_non_admin = await is_nonadmin_chat(message.chat.id)
        if not is_non_admin:
            Group = True
        else:
            Group = None
        playty = await get_playtype(message.chat.id)
        if playty == "Everyone":
            Playtype = None
        else:
            Playtype = True
        buttons = playmode_users_markup(_, Direct, Group, Playtype)
        response = await message.reply_text(
            _["playmode_1"].format(message.chat.title),
            reply_markup=InlineKeyboardMarkup(buttons),
        )
