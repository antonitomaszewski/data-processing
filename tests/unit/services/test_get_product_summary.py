from datetime import datetime
from decimal import Decimal

from app.models import Transaction
from app.schemas import ProductSummaryResponse
from app.services import get_product_summary
from tests.test_data import (
    CUSTOMER1_ID,
    CUSTOMER2_ID,
    PROD1_ID,
    TRANSACTION1_ID,
    TRASNACTION2_ID,
)


def test_product_summary_no_transactions(session):
    result = get_product_summary(session, PROD1_ID)

    assert result is None


def test_get_product_summary_with_transactions(session):
    product_id = PROD1_ID
    customer_id_1 = CUSTOMER1_ID
    customer_id_2 = CUSTOMER2_ID

    transaction1 = Transaction(
        transaction_id=TRANSACTION1_ID,
        timestamp=datetime.now(),
        amount=100.0,
        currency="PLN",
        customer_id=customer_id_1,
        product_id=product_id,
        quantity=2,
    )
    transaction2 = Transaction(
        transaction_id=TRASNACTION2_ID,
        timestamp=datetime.now(),
        amount=200.0,
        currency="PLN",
        customer_id=customer_id_2,
        product_id=product_id,
        quantity=3,
    )

    session.add_all([transaction1, transaction2])
    session.commit()

    summary = get_product_summary(session, product_id)

    assert isinstance(summary, ProductSummaryResponse)
    assert summary.product_id == product_id
    assert summary.total_quantity_sold == 5
    assert summary.total_revenue_pln == Decimal("300.00")
    assert set(summary.unique_customers) == {customer_id_1, customer_id_2}
