from fastapi import FastAPI
from app.routes import products, orders
from app.database import get_db

app = FastAPI()

app.include_router(products.router)
app.include_router(orders.router)

@app.on_event("startup")
async def startup_db_client():
    db = get_db()
    try:
        db.command("ping")
        print("successfully connected to MongoDB!")
    except Exception as e:
        print(e)