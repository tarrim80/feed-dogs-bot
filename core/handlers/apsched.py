from aiogram import Bot

import core.keyboards as kb
from core.database.requests import get_chat_id, set_hungry_dogs


async def feed_dogs_time(bot: Bot) -> None:
    await set_hungry_dogs()
    await bot.send_message(
        chat_id=await get_chat_id(),
        text="Пора покормить собачек!",
        reply_markup=await kb.i_will_feeding(),
    )
