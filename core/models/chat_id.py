from sqlalchemy import BigInteger, Column

from core.database.db import Base


class ChatId(Base):
    __tablename__ = "chat_ids"
    id = Column(
        BigInteger, primary_key=True, autoincrement=True, nullable=False
    )
