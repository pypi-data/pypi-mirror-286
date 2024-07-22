import datetime
import uuid

from sqlalchemy import Column, DateTime, UUID
from sqlalchemy.orm import Mapped, mapped_column

from webapp_kit.framework.datetimes import utcnow
from webapp_kit.persistence.database import Base


class BaseDBEntity(Base):
    __abstract__ = True

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    created_at: Mapped[datetime.datetime] = Column(DateTime, default=utcnow)
    updated_at: Mapped[datetime.datetime] = Column(DateTime, onupdate=utcnow)

    def __str__(self) -> str:
        return f"<{self.__class__.__name__} id={self.id}>"
