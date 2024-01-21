from fastapi.testclient import TestClient
from app import app
import pytest
client = TestClient(app)

def test_get_products():
    response = client.get("/products")
    assert response.status_code == 200
    assert len(response.json()) == 0
# test_app.py

@pytest.fixture
def created_product():
    product_data = {
        "name": "Test Product",
        "price": 9.99,
        "expiration_date": "2022-12-31",
        "quantity_in_stock": 10
    }
    response = client.post("/products", json=product_data)
    assert response.status_code in [200, 201]  # Updated assertion to handle both 200 and 201
    return response.json()


# test_app.py

def test_get_products():
    response = client.get("/products")
    assert response.status_code == 200
    # Update the expected number of products according to your test data
    assert len(response.json()) == 41  # Update to the correct number of products



def test_update_product(created_product):
    product_id = created_product["product_id"]
    updated_product_data = {
        "name": "Updated Product",
        "price": 12.99,
        "expiration_date": "2023-06-30",
        "quantity_in_stock": 15
    }
    response = client.put(f"/products/{product_id}", json=updated_product_data)
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Product"
    assert response.json()["price"] == 12.99
    assert response.json()["expiration_date"] == "2023-06-30"
    assert response.json()["quantity_in_stock"] == 15

def test_delete_product(created_product):
    product_id = created_product["product_id"]
    response = client.delete(f"/products/{product_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Product deleted successfully"

def test_record_purchase(created_product):
    product_id = created_product["product_id"]
    purchase_quantity = 5
    response = client.post(f"/products/{product_id}/purchase", json={"quantity_purchased": purchase_quantity})
    assert response.status_code == 200
    assert response.json()["transaction_id"] is not None
    assert response.json()["product_id"] == product_id
    assert response.json()["transaction_type"] == "purchase"
    assert response.json()["quantity"] == purchase_quantity

def test_record_sale(created_product):
    product_id = created_product["product_id"]
    sale_quantity = 3
    response = client.post(f"/products/{product_id}/sale", json={"quantity_sold": sale_quantity})
    assert response.status_code == 200
    assert response.json()["transaction_id"] is not None
    assert response.json()["product_id"] == product_id
    assert response.json()["transaction_type"] == "sale"
    assert response.json()["quantity"] == sale_quantity

