from aiogram import Bot

import core.keyboards as kb


async def feed_dogs_time(bot: Bot) -> None:
    await bot.send_message(
        -1001669568306,
        "Пора покормить собачек!",
        reply_markup=await kb.i_will_feeding(),
    )
