import os
from dataclasses import dataclass

from aiogram.enums.parse_mode import ParseMode
from dotenv import load_dotenv

load_dotenv()


@dataclass
class TimeMode:
    first_time: int
    second_time: int
    timezone: str


@dataclass
class Bots:
    bot_token: str
    admin_id: int
    parse_mode: str
    proxy_url: str


@dataclass
class Settings:
    bots: Bots
    mode: TimeMode
    database_url: str
    final_msgs: list[str]

    class Config:
        env_file = ".env"


def get_settings() -> Settings:
    return Settings(
        bots=Bots(
            bot_token=os.getenv(key="TELEGRAM_TOKEN"),
            admin_id=os.getenv(key="ADMIN_TELEGRAM_ID"),
            parse_mode=ParseMode.HTML,
            proxy_url=os.getenv(key="PROXY_URL"),
        ),
        mode=TimeMode(
            first_time=os.getenv(key="FIRST_TIME"),
            second_time=os.getenv(key="SECOND_TIME"),
            timezone=os.getenv(key="TIMEZONE"),
        ),
        database_url=os.getenv(key="DATABASE_URL"),
        final_msgs=[
            "Не отставливайся!",
            "Продолжай!",
            "Покорми следующую собаню!",
        ],
    )


settings = get_settings()
