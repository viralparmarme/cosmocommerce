import datetime

from fastapi import HTTPException

from app.common.db import order_collection
from app.controllers.products import list_product_by_id, reduce_product_quantity_by_id
from app.models.orders import CreateOrderModel, OrderModel
from fastapi.encoders import jsonable_encoder


async def insert_order(order: CreateOrderModel) -> OrderModel:
    order_dict = jsonable_encoder(order)
    items = order_dict['items']
    await verify_products_exist_in_stock(items)

    order_dict["created_on"] = datetime.datetime.utcnow()
    inserted_order = await order_collection.insert_one(order_dict)
    order_id = inserted_order.inserted_id
    await update_product_quantities(items)

    return OrderModel(id=order_id, **order_dict)


async def verify_products_exist_in_stock(items):
    for item in items:
        product_id = item["product_id"]
        bought_quantity = item['bought_quantity']

        product = await list_product_by_id(product_id)
        if product['available_quantity'] < bought_quantity:
            raise HTTPException(status_code=400, detail=f"Product {product_id} is unavailable "
                                                        f"in quantity {bought_quantity}")


async def update_product_quantities(items):
    for item in items:
        product_id = item["product_id"]
        bought_quantity = item['bought_quantity']
        await reduce_product_quantity_by_id(product_id, bought_quantity)
