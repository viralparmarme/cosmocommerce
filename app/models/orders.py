import datetime
from typing import Optional, List
from pydantic import ConfigDict, BaseModel, Field
from app.common.db import PyObjectId


class OrderItemModel(BaseModel):
    product_id: Optional[PyObjectId] = Field(...)
    bought_quantity: int = Field(..., gt=0)


class UserAddressModel(BaseModel):
    city: str = Field(...)
    country: str = Field(...)
    zip_code: int = Field(...)


class CreateOrderModel(BaseModel):
    items: List[OrderItemModel]
    total_amount: int = Field(...)
    user_address: UserAddressModel
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "items": [
                    {
                        "product_id": "123",
                        "bought_quantity": 1
                    },
                    {
                        "product_id": "456",
                        "bought_quantity": 2
                    }
                ],
                "total_amount": 200,
                "user_address": {
                    "city": "ABC",
                    "country": "IN",
                    "zip_code": 123456
                }
            }
        },
    )


class OrderModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    created_on: datetime.datetime = Field(...)
    items: List[OrderItemModel]
    total_amount: int = Field(...)
    user_address: UserAddressModel
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "id": "123",
                "created_on": "ABC",
                "items": [
                    {
                        "product_id": "123",
                        "bought_quantity": 1
                    },
                    {
                        "product_id": "456",
                        "bought_quantity": 2
                    }
                ],
                "total_amount": 200,
                "user_address": {
                    "city": "ABC",
                    "country": "IN",
                    "zip_code": 123456
                }
            }
        },
    )
