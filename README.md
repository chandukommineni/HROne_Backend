# Ecommerce API with FastAPI and MongoDB

## Inventory Management Note

The current API specification doesn't account for product sizes when placing orders, though products are stored with size-specific quantities. 

**Temporary Workaround**:  
All orders currently deduct from the total quantity across all sizes. For precise size-wise inventory tracking, modify the order request format to include `size`:

```json
{
  "items": [{
    "productId": "123",
    "size": "M",  // it is needed to check the quantity in inventory 
    "qty": 2
  }]
}

A scalable ecommerce backend API with product catalog and order management, built with FastAPI and MongoDB.

## Features

- **Product Management**
  - Create products with multiple size variants
  - List products with search/pagination
- **Order System**
  - Place orders with quantity validation
  - View order history
- **Database**
  - MongoDB Atlas integration
  - Optimized queries with indexing

## API Documentation

Interactive docs available at `/docs` or `/redoc` when deployed:
- Swagger UI: `https://your-api-url/docs`


## Endpoints

| Method | Endpoint            | Description                      |
|--------|---------------------|----------------------------------|
| POST   | `/products`         | Create new product               |
| GET    | `/products`         | List products (filterable)       |
| POST   | `/orders`           | Create new order                 |
| GET    | `/orders/{user_id}` | Get order history for user       |

## Deployment

### 1. Prerequisites

- Python 3.10+
- MongoDB Atlas account
- Render account 

### 2. Local Development

```bash
# Clone repository
git clone https://github.com/yourusername/ecommerce-fastapi.git
cd ecommerce-fastapi

# Set up virtual environment
python -m venv venv
#source venv/bin/activate  # Linux/Mac
venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Set environment variables
echo "MONGODB_URL=mongodb+srv://user:pass@cluster.mongodb.net/" > .env
echo "DB_NAME=ecommerce" >> .env

# Run server
uvicorn app.main:app --reload