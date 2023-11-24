from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base

from core.settings import settings

Base = declarative_base()

engine = create_async_engine(url=settings.database_url, echo=True)

async_session = async_sessionmaker(engine)
