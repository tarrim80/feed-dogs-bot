from aiogram import Bot
from aiogram.types import Message, ReplyKeyboardRemove

import core.keyboards as kb
from core.database.requests import get_hungry_dogs
from core.utils.services import get_estimated_time_formatted


async def get_start(message: Message, bot: Bot) -> None:
    hungry_dogs = await get_hungry_dogs()
    est_time = await get_estimated_time_formatted()
    if not hungry_dogs:
        await bot.send_message(
            chat_id=-1001669568306,
            text=(
                "Сейчас все собачки уже накормлены. Следующее кормление "
                f"запланировано через {est_time}.\n"
                "Я обязательно сообщу, когда их нужно будет покормить."
            ),
            reply_markup=ReplyKeyboardRemove(),
        )
    else:
        await bot.send_message(
            chat_id=-1001669568306,
            text=(
                "Сейчас есть некормленные собаки. Если ты готов их покормить, "
                "нажми кнопку."
            ),
            reply_markup=await kb.i_will_feeding(),
        )
    await bot.send_message(
        chat_id=message.from_user.id,
        text=(
            f"Привет {message.from_user.first_name}. Рад тебя видеть!\n"
            "Теперь ты тоже в списке кормильцев Таужолинских собак. Когда "
            "придёт время кормить их, и ты сможешь это сделать, нажми кнопку "
            "'Я ПОКОРМЛЮ'"
        ),
        reply_markup=ReplyKeyboardRemove(),
    )


async def get_feed(message: Message, bot: Bot) -> None:
    await bot.send_message(
        chat_id=message.from_user.id,
        text="Покорми собаку и нажми кнопку только тогда, когда она поест.",
        reply_markup=await kb.feed_dogs(),
    )
