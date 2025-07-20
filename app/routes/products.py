from fastapi import APIRouter, HTTPException, Query, status
from app.database import get_db
from app.models.product import Product, ProductSize
from app.schemas.product import ProductCreate, ProductResponse, ProductListResponse
from bson import ObjectId
import re

router = APIRouter(prefix="/products", tags=["products"])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=dict)
async def create_product(product: ProductCreate):
    db = get_db()
    product_dict = product.dict()
    result = db.products.insert_one(product_dict)
    return {"id": str(result.inserted_id)}

@router.get("/", response_model=ProductListResponse)
async def list_products(
    name: str = Query(None),
    size: str = Query(None), 
    limit: int = Query(10, gt=0),
    offset: int = Query(0, ge=0)
):
    db = get_db()
    query = {}
    
    if name:
        query["name"] = {"$regex": re.compile(name, re.IGNORECASE)}
    
    if size:
        query["sizes.size"] = size
    
    cursor = db.products.find(query).skip(offset).limit(limit)
    products = []
    
    for doc in cursor:
        products.append({
            "id": str(doc["_id"]),
            "name": doc["name"],
            "price": doc["price"]
        })
    
    next_offset = offset + limit if len(products) == limit else None
    prev_offset = offset - limit if offset - limit >= 0 else None
    
    return {
        "data": products,
        "page": {
            "next": str(next_offset) if next_offset is not None else None,
            "limit": len(products),
            "previous": str(prev_offset) if prev_offset is not None else None
        }
    }