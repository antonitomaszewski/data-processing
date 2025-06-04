from datetime import datetime, timedelta
from decimal import Decimal

from app.models import Transaction
from app.schemas import CustomerSummaryResponse
from app.services import get_customer_summary
from tests.test_data import (
    CUSTOMER1_ID,
    PROD1_ID,
    PROD2_ID,
    TRANSACTION1_ID,
    TRASNACTION2_ID,
)


def test_customer_summary_not_found(session):
    result = get_customer_summary(session, CUSTOMER1_ID)

    assert result is None


def test_get_customer_summary_with_transactions(session):
    t1 = Transaction(
        transaction_id=TRANSACTION1_ID,
        timestamp=datetime.now() - timedelta(days=2),
        amount=150.0,
        currency="PLN",
        customer_id=CUSTOMER1_ID,
        product_id=PROD1_ID,
        quantity=1,
    )
    t2 = Transaction(
        transaction_id=TRASNACTION2_ID,
        timestamp=datetime.now(),
        amount=250.0,
        currency="PLN",
        customer_id=CUSTOMER1_ID,
        product_id=PROD2_ID,
        quantity=2,
    )

    session.add_all([t1, t2])
    session.commit()

    summary = get_customer_summary(session, CUSTOMER1_ID)

    assert isinstance(summary, CustomerSummaryResponse)
    assert summary.customer_id == CUSTOMER1_ID
    assert summary.total_amount_pln == Decimal("400.00")
    assert set(summary.unique_products) == {PROD1_ID, PROD2_ID}
    assert summary.last_transaction_date == t2.timestamp
