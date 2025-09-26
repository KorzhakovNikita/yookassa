import uuid
from datetime import datetime

from sqlalchemy import func, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, declarative_mixin
from sqlalchemy.dialects.postgresql import UUID


@declarative_mixin
class IDMixin:
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )


@declarative_mixin
class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), default=func.now(), onupdate=func.now()
    )

