from sqlalchemy import BigInteger, ScalarResult, not_, select

from core.database.db import async_session
from core.models.chat_id import ChatId
from core.models.feed_dogs import FeedDog


async def get_hungry_dogs() -> ScalarResult[FeedDog]:
    async with async_session() as session:
        result = await session.execute(
            statement=select(FeedDog).where(not_(FeedDog.is_feed))
        )
        return result.scalars().all()


async def set_feed_dog(id: FeedDog.id) -> None:
    async with async_session() as session:
        stmt = await session.execute(
            statement=select(FeedDog).where(FeedDog.id == id)
        )
        dog = stmt.scalars().first()
        dog.is_feed = True
        session.add(dog)
        await session.commit()
        await session.refresh(dog)


async def set_chat_id(chat_id: BigInteger):
    async with async_session() as session:
        result = await session.execute(
            statement=select(ChatId).where(ChatId.id == chat_id)
        )
        chat_id_db = result.scalars().first()
        if not chat_id_db:
            session.add(ChatId(id=chat_id))
            await session.commit()


async def get_chat_id() -> BigInteger:
    async with async_session() as session:
        result = await session.execute(statement=select(ChatId))
        chat_id_db = result.scalars().first()
        return chat_id_db.id
