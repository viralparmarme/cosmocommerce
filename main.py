from fastapi import FastAPI
from app.routes import products ,orders

app = FastAPI(
    title="Cosmocommerce - An Ecommerce app from Cosmocloud",
    summary="Viral Parmar's submission for the Backend Hiring Task at Cosmocloud",
)
app.include_router(products.router)
app.include_router(orders.router)