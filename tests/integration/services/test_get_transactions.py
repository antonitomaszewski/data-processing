from app.services import get_transactions
from tests.test_data import CUSTOMER1_ID, PROD1_ID, TRANSACTION1_ID


def test_get_transactions_all(session_with_data):
    results, total = get_transactions(session_with_data, page=1, size=10)
    assert total == 2
    assert isinstance(results, list)
    assert TRANSACTION1_ID in results


def test_get_transactions_with_customer_filter(session_with_data):
    results, total = get_transactions(
        session_with_data, page=1, size=10, customer_id=CUSTOMER1_ID
    )
    assert total == 1
    assert len(results) == 1


def test_get_transactions_with_product_filter(session_with_data):
    results, total = get_transactions(
        session_with_data, page=1, size=10, product_id=PROD1_ID
    )
    assert total == 1
    assert len(results) == 1


def test_get_transactions_pagination(session_with_data):
    results_page1, total = get_transactions(session_with_data, page=1, size=1)
    results_page2, _ = get_transactions(session_with_data, page=2, size=1)

    assert total == 2
    assert len(results_page1) == 1
    assert len(results_page2) == 1
    assert results_page1 != results_page2
