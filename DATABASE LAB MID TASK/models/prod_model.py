from pydantic import BaseModel
from typing import Optional

class Product(BaseModel):
    name: str
    description: str
    category: str
    brand: str
    price: float
    rating: Optional[float] = 0.0
    stock: int
    popularity: Optional[int] = 0