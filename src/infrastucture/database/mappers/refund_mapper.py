from typing import Optional

from src.app.dtos.refunds import RefundCreationData, RefundWithTechnicalData
from src.domain.refund.entities.refund import Refund
from src.domain.refund.value_objects.refund_status import RefundStatus
from src.domain.shared.value_objects.money import Money
from src.infrastucture.database.models import RefundORM


class RefundDataMapper:

    @staticmethod
    def to_domain(orm_refund: RefundORM):
        return Refund(
            id=orm_refund.id,
            payment_id=orm_refund.payment_id,
            amount=Money(
                value=orm_refund.amount,
                currency=orm_refund.currency
            ),
            status=RefundStatus(orm_refund.status),
            reason=orm_refund.reason,
            created_at=orm_refund.created_at,
            refunded_at=orm_refund.refunded_at
        )

    @staticmethod
    def to_orm(
        refund_data: RefundCreationData,
        existing_orm: Optional[RefundORM] = None
    ):
        refund = refund_data.refund

        if existing_orm is None:
            orm_refund = RefundORM()
        else:
            orm_refund = existing_orm

        orm_refund.id = refund.id
        orm_refund.payment_id = refund.payment_id
        orm_refund.amount = refund.amount.value
        orm_refund.currency = refund.amount.currency
        orm_refund.status = refund.status.value
        orm_refund.created_at = refund.created_at
        orm_refund.reason = refund.reason

        # Technical fields
        orm_refund.gateway_refund_id = refund_data.gateway_refund_id

        return orm_refund

    @staticmethod
    def to_domain_with_technical_data(
        refund_orm: RefundORM
    ) -> RefundWithTechnicalData:
        domain_refund = RefundDataMapper.to_domain(refund_orm)

        return RefundWithTechnicalData(
            refund=domain_refund,
            gateway_refund_id=refund_orm.gateway_refund_id,
        )