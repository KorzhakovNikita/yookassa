import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import String, Boolean, ForeignKey, Numeric, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID, JSONB

from src.domain.order.value_objects.order_status import OrderStatus
from src.domain.payment.value_objects.payment_status import PaymentStatus
from src.infrastucture.database.base import Base
from src.infrastucture.database.mixins import IDMixin, TimestampMixin


# todo: add relationships

class UserORM(Base, IDMixin, TimestampMixin):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False
    )
    username: Mapped[Optional[str]] = mapped_column(
        String(100),
        unique=True,
        nullable=True
    )
    full_name: Mapped[Optional[str]] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)


class OrderORM(Base, IDMixin, TimestampMixin):
    __tablename__ = "orders"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False
    )
    service_type: Mapped[str] = mapped_column(String(50), nullable=False)
    amount: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), default="RUB")
    status: Mapped[OrderStatus] = mapped_column(
        String(20),
        default=OrderStatus.PENDING.value
    )


class PaymentORM(Base, IDMixin, TimestampMixin):
    __tablename__ = "payments"

    order_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("orders.id"),
        nullable=False
    )
    amount: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), default="RUB")
    status: Mapped[PaymentStatus] = mapped_column(
        String(30),
        nullable=False,
        default=PaymentStatus.PENDING.value
    )

    confirmation_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    payment_method: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    refundable: Mapped[bool] = mapped_column(Boolean, default=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    payment_metadata: Mapped[dict] = mapped_column(JSONB, default=dict)
    idempotency_key: Mapped[Optional[UUID]] = mapped_column(
        UUID(as_uuid=True),
        unique=True,
        nullable=True
    )

    captured_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    cancelled_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    expires_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
