import asyncio

from aiogram import Bot, Dispatcher, F
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.filters import Command
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from core.handlers import apsched
from core.handlers.basic import get_feed, get_help, get_start, next_dog_feed
from core.loggers import feed_dogs_logger
from core.settings import settings
from core.utils.commands import set_commands


async def start_bot(bot: Bot) -> None:
    await set_commands(bot=bot)
    feed_dogs_logger.info(msg="Bot started")


async def stop_bot(bot: Bot) -> None:
    feed_dogs_logger.info(msg="Bot stopped")


async def start() -> None:
    session = AiohttpSession(proxy=settings.bots.proxy_url)
    bot = Bot(
        token=settings.bots.bot_token,
        parse_mode=settings.bots.parse_mode,
        session=session,
    )
    dp = Dispatcher()

    scheduller = AsyncIOScheduler(timezone=settings.mode.timezone)

    scheduller.add_job(
        func=apsched.feed_dogs_time,
        trigger="cron",
        hour=settings.mode.first_time,
        kwargs={"bot": bot},
    )
    scheduller.add_job(
        func=apsched.feed_dogs_time,
        trigger="cron",
        hour=settings.mode.second_time,
        kwargs={"bot": bot},
    )
    scheduller.start()
    dp.startup.register(callback=start_bot)
    dp.shutdown.register(callback=stop_bot)
    dp.message.register(get_start, Command(commands=["start", "run"]))
    dp.message.register(get_help, Command(commands=["help", "rules"]))
    dp.callback_query.register(get_feed, F.data == "i_feed")
    dp.callback_query.register(next_dog_feed, F.data.contains("dog_feed"))
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main=start())
    except KeyboardInterrupt:
        feed_dogs_logger.info(msg="Прервано пользователем")
