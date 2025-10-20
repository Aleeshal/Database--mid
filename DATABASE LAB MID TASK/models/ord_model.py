from pydantic import BaseModel
from typing import List
from datetime import datetime

class ProductItem(BaseModel):
    product_id: str
    quantity: int
    price: float

class Order(BaseModel):
    user_id: str
    products: List[ProductItem]
    total_cost: float
    timestamp: datetime