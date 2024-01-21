# app.py
from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime, date, timedelta
from uuid import uuid4
from pydantic import BaseModel
from models import Product, Transaction
from database import create_app
from typing import List
from sqlalchemy import create_engine
import uvicorn
from fastapi.responses import PlainTextResponse
from fastapi import HTTPException, Path, Body
from typing import Union, Dict, List




# Define the Pydantic model for the response
class ProductResponse(BaseModel):
    product_id: str
    name: str
    price: float
    expiration_date: date
    quantity_in_stock: int

class ProductRequest(BaseModel):
    name: str
    price: float
    expiration_date: date
    quantity_in_stock: int

app, engine = create_app()

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8080",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# Create a session dependency
def get_db():
    db = Session(bind=engine)
    try:
        yield db
    finally:
        db.close()

# API routes
@app.get('/products', response_model=List[ProductResponse])
async def get_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()

    # Convert Product instances to ProductResponse instances
    response_products = [
        ProductResponse(
            product_id=product.product_id,
            name=product.name,
            price=product.price,
            expiration_date=product.expiration_date,
            quantity_in_stock=product.quantity_in_stock
        )
        for product in products
    ]

    return response_products

@app.post('/products', response_model=ProductResponse)
async def add_product(product: ProductRequest, db: Session = Depends(get_db)):
    # Convert Pydantic model to SQLAlchemy model
    new_product = Product(
        product_id=str(uuid4()),
        name=product.name,
        price=product.price,
        expiration_date=product.expiration_date,
        quantity_in_stock=product.quantity_in_stock,
    )

    db.add(new_product)
    db.commit()

    # Return a custom response content
    response_content = {
        "message": "Product added successfully",
        "product_id": new_product.product_id
    }

    return JSONResponse(content=response_content)


# API route to update a product by ID
from fastapi.responses import JSONResponse
from fastapi import HTTPException

# ... (other imports and setup code)

@app.put('/products/{product_id}', response_model=None)
async def update_product(product_id: str, product: ProductRequest, db: Session = Depends(get_db)):
    # Try to get the product by ID
    existing_product = db.query(Product).filter(Product.product_id == product_id).first()

    # Check if the product exists
    if existing_product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    # Update the product details
    existing_product.name = product.name
    existing_product.price = product.price
    existing_product.expiration_date = product.expiration_date
    existing_product.quantity_in_stock = product.quantity_in_stock

    db.commit()

    # Return a custom response content
    response_content = {"message": "Product updated successfully"}

    return JSONResponse(content=response_content)

# API route to delete a product by ID
@app.delete('/products/{product_id}', response_model=dict)
async def delete_product(product_id: str, db: Session = Depends(get_db)):
    # Try to get the product by ID
    existing_product = db.query(Product).filter(Product.product_id == product_id).first()

    # Check if the product exists
    if existing_product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    # Delete the product
    db.delete(existing_product)
    db.commit()

    # Return a success message
    return {"message": "Product deleted successfully"}

def check_expiration_dates(db: Session):
    today = datetime.utcnow().date()
    approaching_products = [product for product in db.query(Product).all() if product.is_approaching_expiration()]

    for product in approaching_products:
        print(f"Product '{product.name}' is approaching its expiration date on {product.expiration_date}")

# API route to trigger expiration date check
def check_expiration_dates(db: Session) -> List[str]:
    today = datetime.utcnow().date()
    approaching_products = [product for product in db.query(Product).all() if product.is_approaching_expiration(days_threshold=7)]

    log_messages = []

    for product in approaching_products:
        log_message = f"Product '{product.name}' is approaching its expiration date on {product.expiration_date}"
        log_messages.append(log_message)
        print(log_message)  # Print to console

    return log_messages

@app.post('/check_expiration_dates', response_model=dict)
async def trigger_expiration_check(db: Session = Depends(get_db)):
    log_messages = check_expiration_dates(db)

    # Return log messages as JSON
    return {"log_messages": log_messages}

@app.post('/products/{product_id}/purchase', response_model=dict)
async def record_purchase(
    product_id: str,
    quantity_purchased: int = Body(..., embed=True),
    db: Session = Depends(get_db)
):
    print(f"Received data: product_id={product_id}, quantity_purchased={quantity_purchased}")
    
    product = db.query(Product).filter(Product.product_id == product_id).first()

    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    # Record the purchase transaction
    purchase_transaction = Transaction(
        transaction_id=str(uuid4()),  # Generate a new UUID
        product_id=product_id,
        transaction_type='purchase',
        quantity=quantity_purchased
    )

    db.add(purchase_transaction)
    
    # Update the product quantity_in_stock after the purchase
    product.quantity_in_stock += quantity_purchased
    
    db.commit()

    return {"message": "Purchase recorded successfully"}




@app.post('/products/{product_id}/sale', response_model=dict)
async def record_sale(
    product_id: str,
    quantity_sold: int = Body(..., embed=True),
    db: Session = Depends(get_db)
):
    print(f"Received data: product_id={product_id}, quantity_sold={quantity_sold}")
    
    product = db.query(Product).filter(Product.product_id == product_id).first()

    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    if quantity_sold > product.quantity_in_stock:
        raise HTTPException(status_code=400, detail="Not enough quantity in stock for sale")

    # Record the sale transaction
    sale_transaction = Transaction(
        transaction_id=str(uuid4()),  # Generate a new UUID
        product_id=product_id,
        transaction_type='sale',
        quantity=quantity_sold
    )

    db.add(sale_transaction)

    # Update the product quantity
    product.quantity_in_stock -= quantity_sold
    product.quantity_sold += quantity_sold

    db.commit()

    return {"message": "Sale recorded successfully"}


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)


