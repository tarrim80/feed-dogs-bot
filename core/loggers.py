import logging
from logging.handlers import RotatingFileHandler

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)

aiogram_logger = logging.getLogger(name="aiogram")
aiogram_logger.setLevel(level=logging.DEBUG)

aiosqlite_logger = logging.getLogger(name="aiosqlite")
aiosqlite_logger.setLevel(level=logging.DEBUG)

sqlalchemy_logger = logging.getLogger(name="sqlalchemy")
sqlalchemy_logger.setLevel(level=logging.DEBUG)

feed_dogs_logger = logging.getLogger(name="feed_dogs")
sqlalchemy_logger.setLevel(level=logging.DEBUG)

log_file = "feed_dogs_bot.log"
handler = RotatingFileHandler(
    filename=log_file, encoding="utf8", maxBytes=1024 * 1024, backupCount=3
)
handler.setLevel(level=logging.DEBUG)

formatter = logging.Formatter(
    fmt="%(asctime)s %(levelname)s %(name)s %(message)s"
)
handler.setFormatter(fmt=formatter)

aiogram_logger.addHandler(hdlr=handler)
aiosqlite_logger.addHandler(hdlr=handler)
sqlalchemy_logger.addHandler(hdlr=handler)
feed_dogs_logger.addHandler(hdlr=handler)
