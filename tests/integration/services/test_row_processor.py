from datetime import datetime

from app.models import Transaction
from app.services import RowProcessor
from tests.test_data import (
    CUSTOMER1_ID,
    PROD1_ID,
    TRANSACTION1_ID,
    TRASNACTION3_ID,
)


def test_save_success(session_with_data):
    row = RowProcessor(
        [
            TRASNACTION3_ID,
            datetime.now().isoformat(),
            100.0,
            "PLN",
            CUSTOMER1_ID,
            PROD1_ID,
            2,
        ]
    )

    row.save(session_with_data)

    result = (
        session_with_data.query(Transaction)
        .filter_by(transaction_id=TRASNACTION3_ID)
        .first()
    )

    assert result is not None
    assert row.errors == []


def test_save_integrity_error(monkeypatch, session_with_data):
    row = RowProcessor(
        [
            TRANSACTION1_ID,
            datetime.now().isoformat(),
            100.0,
            "PLN",
            CUSTOMER1_ID,
            PROD1_ID,
            2,
        ]
    )

    row.save(session_with_data)

    assert len(row.errors) == 1
    assert "Integrity error for transaction" in row.errors[0]
