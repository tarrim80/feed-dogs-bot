from sqlalchemy import ScalarResult, not_, select

from core.database.db import async_session
from core.models.feed_dogs import FeedDog


async def get_hungry_dogs() -> ScalarResult[FeedDog]:
    async with async_session() as session:
        result = await session.execute(
            statement=select(FeedDog).where(not_(FeedDog.is_feed))
        )
        return result.scalars().all()
