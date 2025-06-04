from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_get_customer_summary_invalid_uuid():
    response = client.get("/reports/customer-summary/invalid-uuid")
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid customer_id format"


@patch("app.routes.services.get_customer_summary")
@patch("app.routes.services.is_valid_uuid", return_value=True)
def test_get_customer_summary_not_found(mock_valid_uuid, mock_get_summary):
    mock_get_summary.return_value = None
    response = client.get(
        "/reports/customer-summary/aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Customer not found"


@patch("app.routes.services.get_customer_summary")
@patch("app.routes.services.is_valid_uuid", return_value=True)
def test_get_customer_summary_success(mock_valid_uuid, mock_get_summary):
    mock_get_summary.return_value = {
        "customer_id": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
        "total_amount_pln": "1500.00",
        "unique_products": ["bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb"],
        "last_transaction_date": "2023-01-01T00:00:00",
    }
    response = client.get(
        "/reports/customer-summary/aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"
    )
    assert response.status_code == 200
    assert (
        response.json()["customer_id"]
        == "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"
    )
    assert response.json()["total_amount_pln"] == "1500.00"
