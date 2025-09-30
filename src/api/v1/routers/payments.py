from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from src.api.v1.dependencies.payment import get_create_payment_use_case
from src.api.v1.schemas.payment_schema import PaymentCreateRequest, PaymentCreateResponse
from src.app.use_cases.payments.create_payment import CreatePaymentUseCase

router = APIRouter(prefix="/payments", tags=["payments"])


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
    try:
        result = await use_case.execute(
            order_id=request.order_id,
            amount=request.amount,
            description=request.description,
            metadata=request.metadata,
            return_url=request.return_url
        )
        return PaymentCreateResponse.from_result(result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
