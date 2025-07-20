from pydantic import BaseModel
from typing import List, Optional

class ProductSizeCreate(BaseModel):
    size: str
    quantity: int

class ProductCreate(BaseModel):
    name: str
    price: float
    sizes: List[ProductSizeCreate]

class ProductResponse(BaseModel):
    id: str
    name: str
    price: float

class ProductListResponse(BaseModel):
    data: List[ProductResponse]
    page: dict