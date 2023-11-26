import random

from aiogram import Bot
from aiogram.types import Message, ReplyKeyboardRemove

import core.keyboards as kb
from core.database.requests import (
    get_chat_id,
    get_hungry_dogs,
    set_chat_id,
    set_feed_dog,
)
from core.settings import settings
from core.utils.services import get_estimated_time_formatted


async def get_start(message: Message, bot: Bot) -> None:
    hungry_dogs = await get_hungry_dogs()
    await set_chat_id(chat_id=message.chat.id)
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


async def have_hungry_dogs_msg(bot: Bot) -> None:
    await bot.send_message(
        chat_id=await get_chat_id(),
        text=(
            "Сейчас есть некормленные собаки. Если ты готов их покормить, "
            "нажми кнопку."
        ),
        reply_markup=await kb.i_will_feeding(),
    )


async def not_have_hungry_dogs_msg(bot: Bot) -> None:
    est_time = await get_estimated_time_formatted()
    await bot.send_message(
        chat_id=await get_chat_id(),
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
        chat_id=await get_chat_id(),
        text=f"Отлично! Сейчас {message.from_user.first_name} покормит собак.",
    )


async def next_dog_feed(message: Message, bot: Bot) -> None:
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


async def get_help(message: Message, bot: Bot) -> None:
    await bot.send_message(
        chat_id=message.from_user.id,
        text=(
            "Предоставление домашней собаке свободного доступа к корму может "
            "быть не самым лучшим вариантом, особенно если ваша собака имеет "
            "склонность к перееданию или склонна к ожирению. Контролируемое "
            "питание обеспечивает более здоровое и сбалансированное питание "
            "для вашего питомца.\n\n"
            "Рекомендуется следовать рекомендациям ветеринара относительно "
            "количества корма, необходимого для вашей собаки, и разделять его "
            "на несколько приемов пищи в течение дня. Это обеспечивает более "
            "здоровый режим питания и предотвращает возможные проблемы, "
            "связанные с избыточным питанием."
        ),
    )
    await bot.send_message(
        chat_id=message.from_user.id,
        text="Если ваша собака не сразу подходит к еде, это может быть "
        "вызвано различными причинами: \n\n"
        "<b>Переедание:</b>\n"
        "Если вы ранее предоставляли собаке свободный доступ к еде, возможно, "
        "она просто не голодна в данный момент. Регулируйте порции и время "
        "кормления. \n\n"
        "<b>Избалованность:</b>\n"
        "Если собака часто получает угощения или дополнительные лакомства "
        "между приемами пищи, она может потерять интерес к обычному корму. "
        "Старайтесь ограничивать количество лакомств.",
    )
    await bot.send_message(
        chat_id=message.from_user.id,
        text="<b>Регулируйте порции и время кормления.</b>\n"
        "Если вы предоставляли свободный доступ к еде, может быть полезно "
        "перейти на регулярное расписание приемов пищи с определенными "
        "порциями.\n\n"
        "<b>Раздельное кормление.</b>\n"
        "Если у вас несколько собак, попробуйте кормить их в разных местах, "
        "чтобы предотвратить конфликты за еду. Это может уменьшить "
        "напряженность и сделать процесс кормления более спокойным.\n\n"
        "<b>Мониторинг взаимодействия.</b>\n"
        "Внимательно следите за тем, как ваши собаки взаимодействуют при "
        "кормлении. Если одна из них доминирует над другими, это может "
        "создавать стресс и влиять на аппетит менее доминирующих собак.\n\n"
        "<b>Регулировка времени кормления.</b>\n"
        "Разделяйте приемы пищи на несколько временных интервалов или "
        "предоставляйте корм в отдельных мисках в разных местах, чтобы собаки "
        "не соприкасались в процессе кормления.\n\n"
        "<b>Следите за поведением.</b>\n"
        "Обратите внимание на поведение собак во время приема пищи. Если вы "
        "замечаете агрессивное или напряженное поведение, может потребоваться "
        "дополнительная работа по управлению взаимодействием между собаками.",
    )
