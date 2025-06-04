from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_get_product_summary_invalid_uuid():
    response = client.get("/reports/product-summary/invalid-uuid")
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid product_id format"


@patch("app.routes.services.get_product_summary")
@patch("app.routes.services.is_valid_uuid", return_value=True)
def test_get_product_summary_not_found(mock_valid_uuid, mock_get_summary):
    mock_get_summary.return_value = None
    response = client.get(
        "/reports/product-summary/bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb"
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Product not found"


@patch("app.routes.services.get_product_summary")
@patch("app.routes.services.is_valid_uuid", return_value=True)
def test_get_product_summary_success(mock_valid_uuid, mock_get_summary):
    mock_get_summary.return_value = {
        "product_id": "bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb",
        "total_quantity_sold": 50,
        "total_revenue_pln": "2500.00",
        "unique_customers": ["aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"],
    }
    response = client.get(
        "/reports/product-summary/bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb"
    )
    assert response.status_code == 200
    assert (
        response.json()["product_id"] == "bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb"
    )
    assert response.json()["total_quantity_sold"] == 50
    assert response.json()["total_revenue_pln"] == "2500.00"
