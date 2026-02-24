import datetime
import enum
from typing import Optional

from sqlalchemy import String, func, Text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Enum as SQLAlchemyEnum
from core.db import Base


class Status(enum.Enum):
    NEW = 'new'
    PROCESSING ='processing'
    DONE = 'done'
    FAILED = 'failed'

class Task(Base):
    __tablename__ = 'tasks'
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[Status] = mapped_column(SQLAlchemyEnum(Status), default=Status.NEW, index=True)
    result: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now(), onupdate=func.now())