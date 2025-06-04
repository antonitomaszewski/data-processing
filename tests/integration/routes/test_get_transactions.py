from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_get_transactions_default_pagination():
    response = client.get("/transactions")
    assert response.status_code == 200
    assert "data" in response.json()
    assert "total" in response.json()


def test_get_transactions_invalid_pagination():
    response = client.get("/transactions?page=0&size=200")
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid pagination"


def test_get_transactions_invalid_customer_id():
    response = client.get("/transactions?customer_id=invalid-uuid")
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid customer_id format"


def test_get_transactions_invalid_product_id():
    response = client.get("/transactions?product_id=not-a-uuid")
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid product_id format"
