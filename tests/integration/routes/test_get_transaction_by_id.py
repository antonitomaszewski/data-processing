from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_get_transaction_invalid_uuid():
    response = client.get("/transactions/invalid-uuid")
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid transaction_id format"


@patch("app.routes.services.get_transaction_by_id")
@patch("app.routes.services.is_valid_uuid", return_value=True)
def test_get_transaction_not_found(mock_valid_uuid, mock_get_tx):
    mock_get_tx.return_value = None
    response = client.get("/transactions/aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa")
    assert response.status_code == 404
    assert response.json()["detail"] == "Transaction not found"


@patch("app.routes.services.get_transaction_by_id")
@patch("app.routes.services.is_valid_uuid", return_value=True)
def test_get_transaction_success(mock_valid_uuid, mock_get_tx):
    mock_get_tx.return_value = {
        "id": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaad",
        "transaction_id": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
        "timestamp": "2023-01-01T00:00:00",
        "amount": 100,
        "currency": "PLN",
        "customer_id": "bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb",
        "product_id": "cccccccc-cccc-cccc-cccc-cccccccccccc",
        "quantity": 1,
    }
    response = client.get("/transactions/aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa")
    assert response.status_code == 200
    assert (
        response.json()["transaction_id"]
        == "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"
    )
