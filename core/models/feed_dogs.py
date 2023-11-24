from sqlalchemy import Boolean, Column, Integer, String

from core.database.db import Base


class FeedDog(Base):
    __tablename__ = "dogs"
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String(50), unique=True, nullable=False)
    is_feed = Column(Boolean, default=True, nullable=False)
