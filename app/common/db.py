import os
import motor.motor_asyncio
from pydantic.functional_validators import BeforeValidator
from typing_extensions import Annotated
from dotenv import load_dotenv

load_dotenv()
client = motor.motor_asyncio.AsyncIOMotorClient(os.environ["MONGODB_URL"])
db = client.cosmocommerce
product_collection = db.get_collection("products")
order_collection = db.get_collection("orders")

PyObjectId = Annotated[str, BeforeValidator(str)]