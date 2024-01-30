from fastapi.params import Body
from starlette import status

from app.controllers.orders import insert_order
from app.models.orders import CreateOrderModel, OrderModel
from fastapi import APIRouter

router = APIRouter()


@router.post(
    "/orders",
    response_description="Create a new order",
    response_model=OrderModel,
    response_model_by_alias=False,
    status_code=status.HTTP_201_CREATED
)
async def post_order(order: CreateOrderModel = Body(...)):
    return await insert_order(order)

