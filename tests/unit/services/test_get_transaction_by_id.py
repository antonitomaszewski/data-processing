from datetime import datetime

from app.models import Transaction
from app.schemas import TransactionResponse
from app.services import get_transaction_by_id
from tests.test_data import CUSTOMER1_ID, PROD1_ID, TRANSACTION1_ID


def test_get_transaction_by_id_found(session):
    transaction = Transaction(
        transaction_id=TRANSACTION1_ID,
        timestamp=datetime.now(),
        amount=120.0,
        currency="PLN",
        customer_id=CUSTOMER1_ID,
        product_id=PROD1_ID,
        quantity=1,
    )
    session.add(transaction)
    session.commit()

    result = get_transaction_by_id(session, TRANSACTION1_ID)

    assert isinstance(result, TransactionResponse)
    assert result.transaction_id == TRANSACTION1_ID


def test_get_transaction_by_id_not_found(session):
    result = get_transaction_by_id(session, TRANSACTION1_ID)
    assert result is None
