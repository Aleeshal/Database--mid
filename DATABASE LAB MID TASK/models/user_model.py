from pydantic import BaseModel
from typing import List, Optional

class PurchaseItem(BaseModel):
    product_id: str
    quantity: int
    price: float

class User(BaseModel):
    name: str
    email: str
    location: str
    purchase_history: Optional[List[PurchaseItem]] = []