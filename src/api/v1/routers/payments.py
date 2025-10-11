from uuid import UUID

from fastapi import APIRouter, Depends
from starlette import status

from src.api.v1.dependencies.payment import get_create_payment_use_case, get_cancel_payment_use_case, \
    get_capture_payment_use_case, get_payment_use_case, get_payment_list_use_case, get_refund_payment_use_case
from src.api.v1.schemas.payment_schema import PaymentCreateRequest, PaymentCreateResponse, PaymentCancelResponse, \
    PaymentCaptureResponse, PaymentResponse, RefundCreateRequest
from src.app.use_cases.payments.cancel_payment import CancelPaymentUseCase
from src.app.use_cases.payments.capture_payment import CapturePaymentUseCase
from src.app.use_cases.payments.create_payment import CreatePaymentUseCase
from src.app.use_cases.payments.get_payment import GetPaymentUseCase
from src.app.use_cases.payments.get_payment_list import GetPaymentListUseCase
from src.app.use_cases.payments.refund_payment import RefundPaymentUseCase

router = APIRouter(prefix="/payments", tags=["Payments"])


@router.get(
    "/{payment_id}",
    response_model=PaymentResponse,
    status_code=status.HTTP_200_OK,
    summary="Get payment by id"
)
async def get_payment(
    payment_id: UUID,
    use_case: GetPaymentUseCase = Depends(get_payment_use_case)
):
    result = await use_case.execute(
        payment_id=payment_id,
    )
    return PaymentResponse.from_result(result)


@router.get(
    "/",
    response_model=list[PaymentResponse],
    status_code=status.HTTP_200_OK,
    summary="Get payments list"
)
async def get_payments(
    skip: int = 0,
    limit: int = 100,
    use_case: GetPaymentListUseCase = Depends(get_payment_list_use_case)
):
    results = await use_case.execute(
        skip=skip,
        limit=limit,
    )
    return [PaymentResponse.from_result(result) for result in results]


@router.post(
    "/",
    response_model=PaymentCreateResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a payment for an order"
)
async def create_payment(
    request: PaymentCreateRequest,
    use_case: CreatePaymentUseCase = Depends(get_create_payment_use_case)
):
    result = await use_case.execute(
        order_id=request.order_id,
        amount=request.amount,
        description=request.description,
        metadata=request.metadata,
        return_url=request.return_url
    )
    return PaymentCreateResponse.from_result(result)


@router.post(
    "/{payment_id}/cancel",
    response_model=PaymentCancelResponse,
    status_code=status.HTTP_200_OK,
    summary="Cancel payment"
)
async def cancel_payment(
    payment_id: UUID,
    use_case: CancelPaymentUseCase = Depends(get_cancel_payment_use_case)
):
    result = await use_case.execute(
        payment_id=payment_id,
    )
    return PaymentCancelResponse.from_result(result)


@router.post(
    "/{payment_id}/capture",
    response_model=PaymentCaptureResponse,
    status_code=status.HTTP_200_OK,
    summary="Capture payment"
)
async def capture_payment(
    payment_id: UUID,
    use_case: CapturePaymentUseCase = Depends(get_capture_payment_use_case)
):
    result = await use_case.execute(
        payment_id=payment_id,
    )
    return PaymentCaptureResponse.from_result(result)


@router.post(
    "/{payment_id}/refund",
    status_code=status.HTTP_200_OK,
    summary="Refund payment"
    #todo: add response model
)
async def refund_payment(
    payment_id: UUID,
    request_data: RefundCreateRequest,
    use_case: RefundPaymentUseCase = Depends(get_refund_payment_use_case)
):
    result = await use_case.execute(
        payment_id=payment_id,
        reason=request_data.reason
    )
    return result
