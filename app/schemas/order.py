from pydantic import BaseModel
from typing import List

class ProductDetails(BaseModel):
    name: str
    id: str

class OrderItemResponse(BaseModel):
    productDetails: ProductDetails
    qty: int

class OrderResponse(BaseModel):
    id: str
    items: List[OrderItemResponse]
    total: float

class OrderListResponse(BaseModel):
    data: List[OrderResponse]
    page: dict