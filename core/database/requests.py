from sqlalchemy import ScalarResult, not_, select

from core.database.db import async_session
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
