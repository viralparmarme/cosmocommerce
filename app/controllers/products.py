from bson import ObjectId
from bson.errors import InvalidId
from fastapi import HTTPException
from app.common.db import product_collection
from app.models.products import ProductCollection, PaginationInfo


async def list_products(page, limit, min_price=None, max_price=None):
    query = {}
    if min_price or max_price:
        query["price"] = {}
    if min_price is not None:
        query["price"]["$gte"] = min_price
    if max_price is not None:
        query["price"]["$lte"] = max_price

    pipeline = [
        {"$match": query},
        {"$facet": {
            "products": [
                {"$skip": (page - 1) * limit},
                {"$limit": limit},
            ],
            "total_count": [
                {"$count": "value"}
            ]
        }}
    ]

    cursor = product_collection.aggregate(pipeline)
    result = await cursor.to_list(length=1)

    products = result[0]["products"] if "products" in result[0] else []
    total_count = result[0]["total_count"][0]["value"] if "total_count" in result[0] and result[0]["total_count"] else 0

    next_offset = (page - 1) * limit + limit + 1 if total_count > page * limit else None
    prev_offset = (page - 2) * limit + 1 if page > 1 else None

    page = PaginationInfo(
        page=page,
        limit=limit,
        next_offset=next_offset,
        prev_offset=prev_offset,
        total=total_count
    )

    return ProductCollection(data=products, page=page)


async def list_product_by_id(product_id: str):
    try:
        ObjectId(product_id)
    except InvalidId as e:
        raise HTTPException(status_code=404, detail=f"Product {product_id} not found")

    product = await product_collection.find_one({"_id": ObjectId(product_id)})
    if product is not None:
        return product

    raise HTTPException(status_code=404, detail=f"Product {product_id} not found")


async def reduce_product_quantity_by_id(product_id, reduce_by):
    try:
        ObjectId(product_id)
    except InvalidId as e:
        raise HTTPException(status_code=404, detail=f"Product {product_id} not found")

    if not isinstance(reduce_by, int) or reduce_by <= 0:
        raise HTTPException(status_code=400, detail="Invalid quantity reduction value")

    product = await product_collection.find_one({"_id": ObjectId(product_id)})

    if not product:
        raise HTTPException(status_code=404, detail=f"Product {product_id} not found")

    available_quantity = product.get("available_quantity", 0)
    if reduce_by > available_quantity:
        raise HTTPException(status_code=400, detail="Insufficient quantity available")

    updated_quantity = available_quantity - reduce_by
    await product_collection.update_one({"_id": ObjectId(product_id)},
                                        {"$set": {"available_quantity": updated_quantity}})
