import asyncio
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from core.handlers import apsched
from core.handlers.basic import get_feed, get_start
from core.settings import settings
from core.utils.commands import set_commands


async def start_bot(bot: Bot) -> None:
    await set_commands(bot=bot)
    logging.info("Bot started")


async def stop_bot(bot: Bot) -> None:
    logging.info("Bot stopped")


async def start() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )
    bot = Bot(
        token=settings.bots.bot_token, parse_mode=settings.bots.parse_mode
    )
    dp = Dispatcher()

    scheduller = AsyncIOScheduler(timezone=settings.mode.timezone)

    scheduller.add_job(
        func=apsched.feed_dogs_time,
        trigger="cron",
        hour=1,
        minute=32,
        kwargs={"bot": bot},
    )
    scheduller.start()
    dp.startup.register(callback=start_bot)
    dp.shutdown.register(callback=stop_bot)
    dp.message.register(get_start, Command(commands=["start", "run"]))
    dp.message.register(get_feed, F.text == "Я ПОКОРМЛЮ")
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(start())
    except KeyboardInterrupt:
        ...
