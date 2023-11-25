import random

from aiogram import Bot
from aiogram.types import Message, ReplyKeyboardRemove

import core.keyboards as kb
from core.database.requests import get_hungry_dogs, set_feed_dog
from core.settings import settings
from core.utils.services import get_estimated_time_formatted


async def get_start(message: Message, bot: Bot) -> None:
    hungry_dogs = await get_hungry_dogs()

    if not hungry_dogs:
        await not_have_hungry_dogs_msg(bot=bot)
    else:
        await have_hungry_dogs_msg(bot=bot)
    await direct_hello_msg(message=message, bot=bot)


async def direct_hello_msg(message: Message, bot: Bot):
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


async def have_hungry_dogs_msg(bot: Bot):
    await bot.send_message(
        chat_id=-1001669568306,
        text=(
            "Сейчас есть некормленные собаки. Если ты готов их покормить, "
            "нажми кнопку."
        ),
        reply_markup=await kb.i_will_feeding(),
    )


async def not_have_hungry_dogs_msg(bot: Bot):
    est_time = await get_estimated_time_formatted()
    await bot.send_message(
        chat_id=-1001669568306,
        text=(
            f"Прекрасно! \n"
            "Сейчас все собачки уже накормлены. Следующее кормление "
            f"запланировано через {est_time}.\n"
            "Я обязательно сообщу, когда их нужно будет покормить."
        ),
        reply_markup=ReplyKeyboardRemove(),
    )


async def get_feed(message: Message, bot: Bot) -> None:
    await bot.send_message(
        chat_id=message.from_user.id,
        text="Покорми собаку и нажми кнопку только тогда, когда она поест.",
        reply_markup=await kb.feed_dogs(),
    )
    await message.answer()
    await bot.send_message(
        chat_id=-1001669568306,
        text=f"Отлично! Сейчас {message.from_user.first_name} покормит собак.",
    )


async def next_dog_feed(message: Message, bot: Bot):
    id: int = message.data.split("_")[-1]
    await set_feed_dog(id=id)
    hugry_dogs = await get_hungry_dogs()
    if not hugry_dogs:
        await not_have_hungry_dogs_msg(bot=bot)
        await bot.send_message(
            chat_id=message.from_user.id,
            text="Супер! Все собакевичи сыты и довольны тобой!",
        )
        await message.answer()
    else:
        final_msg = random.choice(settings.final_msgs)
        await bot.send_message(
            chat_id=message.from_user.id,
            text=f"Отлично! {final_msg}",
            reply_markup=await kb.feed_dogs(),
        )
        await message.answer()
