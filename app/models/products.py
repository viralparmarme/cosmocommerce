from typing import Optional, List
from pydantic import ConfigDict, BaseModel, Field
from app.common.db import PyObjectId


class PaginationInfo(BaseModel):
    limit: int
    next_offset: Optional[int] = None
    prev_offset: Optional[int] = None
    total: int


class ProductModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    name: str = Field(...)
    price: float = Field(...)
    available_quantity: int = Field(...)
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "id": "123",
                "name": "iPhone 16",
                "price": 99.99,
                "available": 100,
            }
        },
    )


class ProductCollection(BaseModel):
    data: List[ProductModel]
    page: PaginationInfo
