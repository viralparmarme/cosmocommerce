from fastapi.params import Query

from app.controllers.products import list_products, list_product_by_id
from app.models.products import ProductCollection, ProductModel
from fastapi import APIRouter

router = APIRouter()


@router.get(
    "/products",
    response_description="List all products",
    response_model=ProductCollection,
    response_model_by_alias=False,
)
async def get_products(
    page: int = Query(1, description="Page number of response", gt=0),
    limit: int = Query(1000, description="Max records in response", gt=0, le=1000),
    min_price: float = Query(None, description="Minimum price filter"),
    max_price: float = Query(None, description="Maximum price filter"),
):
    return await list_products(page, limit, min_price, max_price)

@router.get(
    "/products/{product_id}",
    response_description="Get a single product",
    response_model=ProductModel,
    response_model_by_alias=False,
)
async def show_product(product_id: str):
    return await list_product_by_id(product_id)
