from fastapi import APIRouter, HTTPException, Query, status
from app.database import get_db
from app.models.order import Order, OrderItem
from app.schemas.order import OrderResponse, OrderListResponse
from bson import ObjectId
from typing import List

router = APIRouter(prefix="/orders", tags=["orders"])


#there is an issue with the description provided by the team Please check the Readme file for detailed informatio 
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=dict)
async def create_order(order: Order):
    db = get_db()
    order_dict = order.dict()
    
    # Calculate total and validate products
    total = 0.0
    for item in order_dict["items"]:
        product = db.products.find_one({"_id": ObjectId(item["productId"])})
        if not product:
            raise HTTPException(
                status_code=404,
                detail=f"Product {item['productId']} not found"
            )
        
        # Calculating total available quantity across all sizes
        total_available = sum(size["quantity"] for size in product["sizes"])
        
        # Checking if requested quantity is available
        if item["qty"] > total_available:
            raise HTTPException(
                status_code=400,
                detail=f"Not enough quantity available for product {item['productId']}. "
                      f"Requested: {item['qty']}, Available: {total_available}"
            )
        
        total += product["price"] * item["qty"]
    
    order_dict["total"] = total
    result = db.orders.insert_one(order_dict)
    
    return {"id": str(result.inserted_id)}


@router.get("/{user_id}", response_model=OrderListResponse)
async def list_orders(
    user_id: str,
    limit: int = Query(10, gt=0),
    offset: int = Query(0, ge=0)
):
    db = get_db()
    query = {"userId": user_id}
    
    cursor = db.orders.find(query).skip(offset).limit(limit)
    orders = []
    
    for doc in cursor:
        items = []
        for item in doc["items"]:
            product = db.products.find_one({"_id": ObjectId(item["productId"])})
            if product:
                items.append({
                    "productDetails": {
                        "name": product["name"],
                        "id": str(product["_id"])
                    },
                    "qty": item["qty"]
                })
        
        orders.append({
            "id": str(doc["_id"]),
            "items": items,
            "total": doc["total"]
        })
    
    next_offset = offset + limit if len(orders) == limit else None
    prev_offset = offset - limit if offset - limit >= 0 else None
    
    return {
        "data": orders,
        "page": {
            "next": str(next_offset) if next_offset is not None else None,
            "limit": len(orders),
            "previous": str(prev_offset) if prev_offset is not None else None
        }
    }