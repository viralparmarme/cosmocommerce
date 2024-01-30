import os
from typing import Optional, List

import motor.motor_asyncio
from bson import ObjectId
from fastapi import FastAPI, HTTPException
from pydantic import ConfigDict, BaseModel, Field
from pydantic.functional_validators import BeforeValidator
from typing_extensions import Annotated

app = FastAPI(
    title="Cosmocommerce - An Ecommerce app from Cosmocloud",
    summary="Viral Parmar's submission for the Backend Hiring Task at Cosmocloud.",
)
client = motor.motor_asyncio.AsyncIOMotorClient(os.environ["MONGODB_URL"])
db = client.cosmocommerce
product_collection = db.get_collection("products")

PyObjectId = Annotated[str, BeforeValidator(str)]


class ProductModel(BaseModel):
    """
    Container for a single product record.
    """

    # The primary key for the ProductModel, stored as a `str` on the instance.
    # This will be aliased to `_id` when sent to MongoDB,
    # but provided as `id` in the API requests and responses.
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    name: str = Field(...)
    price: float = Field(...)
    available: int = Field(...)
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "name": "iPhone 16",
                "price": 99.99,
                "available": 100,
            }
        },
    )


class ProductCollection(BaseModel):
    products: List[ProductModel]


@app.get(
    "/products",
    response_description="List all products",
    response_model=ProductCollection,
    response_model_by_alias=False,
)
async def list_products():
    """
    List all the product data in the database.

    The response is unpaginated and limited to 1000 results.
    """
    return ProductCollection(products=await product_collection.find().to_list(1000))


@app.get(
    "/products/{product_id}",
    response_description="Get a single product",
    response_model=ProductModel,
    response_model_by_alias=False,
)
async def show_product(product_id: str):
    """
    Get the record for a specific product, looked up by `id`.
    """
    if (
            product := await product_collection.find_one({"_id": ObjectId(product_id)})
    ) is not None:
        return product

    raise HTTPException(status_code=404, detail=f"Product {product_id} not found")
