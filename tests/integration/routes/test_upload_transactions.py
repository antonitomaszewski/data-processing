import io
from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_upload_valid_csv_file(monkeypatch):
    content = (
        "transaction_id,timestamp,amount,currency,"
        "customer_id,product_id,quantity\n"
        "550e8400-e29b-41d4-a716-446655440000,"
        "2024-01-01T12:00:00Z,10.0,PLN,"
        "550e8400-e29b-41d4-a716-446655440001,"
        "550e8400-e29b-41d4-a716-446655440002,1"
    )
    file = io.BytesIO(content.encode("utf-8"))
    response = client.post(
        "/transactions/upload",
        files={"file": ("test.csv", file, "text/csv")},
    )
    assert response.status_code == 200
    assert "processed_count" in response.json()


def test_upload_invalid_file_type():
    file = io.BytesIO(b"not a csv")
    response = client.post(
        "/transactions/upload",
        files={"file": ("test.txt", file, "text/plain")},
    )
    assert response.status_code == 400
    assert "Invalid file type" in response.json()["detail"]


def test_upload_invalid_file_extension():
    file = io.BytesIO(b"fake content")
    response = client.post(
        "/transactions/upload",
        files={"file": ("invalid.txt", file, "text/csv")},
    )
    assert response.status_code == 400
    assert "File must have .csv extension" in response.json()["detail"]


def test_upload_transactions_raises_500_on_exception(tmp_path):
    file_path = tmp_path / "test.csv"
    file_path.write_text(
        "transaction_id,timestamp,amount,currency,"
        "customer_id,product_id,quantity\n"
    )

    mock_file = open(file_path, "rb")

    with patch("app.routes.services.CSVProcessor") as MockProcessor:
        instance = MockProcessor.return_value
        instance.process_file.side_effect = Exception("Unexpected error")

        response = client.post(
            "/transactions/upload",
            files={"file": ("test.csv", mock_file, "text/csv")},
        )

    assert response.status_code == 500
    assert (
        "Error processing file: Unexpected error" in response.json()["detail"]
    )
