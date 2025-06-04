from unittest.mock import Mock

from app.services import get_transactions


class TestGetTransactions:
    def test_get_transactions_no_filters(self):
        mock_db = Mock()
        mock_query = Mock()
        mock_db.query.return_value = mock_query
        mock_query.count.return_value = 5
        mock_query.order_by.return_value = mock_query
        mock_query.offset.return_value = mock_query
        mock_query.limit.return_value = mock_query
        mock_query.all.return_value = [
            Mock(transaction_id="id1"),
            Mock(transaction_id="id2"),
        ]

        result, total = get_transactions(mock_db, page=1, size=2)

        assert total == 5
        assert result == ["id1", "id2"]
        mock_query.offset.assert_called_with(0)
        mock_query.limit.assert_called_with(2)

    def test_get_transactions_with_customer_filter(self):
        mock_db = Mock()
        mock_query = Mock()
        mock_db.query.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.count.return_value = 3
        mock_query.order_by.return_value = mock_query
        mock_query.offset.return_value = mock_query
        mock_query.limit.return_value = mock_query
        mock_query.all.return_value = []

        customer_id = "550e8400-e29b-41d4-a716-446655440000"
        result, total = get_transactions(
            mock_db, page=1, size=10, customer_id=customer_id
        )

        mock_query.filter.assert_called()
        assert total == 3

    def test_get_transactions_with_product_filter(self):
        mock_db = Mock()
        mock_query = Mock()
        mock_db.query.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.count.return_value = 2
        mock_query.order_by.return_value = mock_query
        mock_query.offset.return_value = mock_query
        mock_query.limit.return_value = mock_query
        mock_query.all.return_value = []

        product_id = "550e8400-e29b-41d4-a716-446655440001"
        result, total = get_transactions(
            mock_db, page=1, size=10, product_id=product_id
        )

        mock_query.filter.assert_called()
        assert total == 2

    def test_get_transactions_with_both_filters(self):
        mock_db = Mock()
        mock_query = Mock()
        mock_db.query.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.count.return_value = 1
        mock_query.order_by.return_value = mock_query
        mock_query.offset.return_value = mock_query
        mock_query.limit.return_value = mock_query
        mock_query.all.return_value = []

        customer_id = "550e8400-e29b-41d4-a716-446655440000"
        product_id = "550e8400-e29b-41d4-a716-446655440001"

        result, total = get_transactions(
            mock_db,
            page=1,
            size=10,
            customer_id=customer_id,
            product_id=product_id,
        )

        assert mock_query.filter.call_count == 2
        assert total == 1

    def test_get_transactions_pagination(self):
        mock_db = Mock()
        mock_query = Mock()
        mock_db.query.return_value = mock_query
        mock_query.count.return_value = 100
        mock_query.order_by.return_value = mock_query
        mock_query.offset.return_value = mock_query
        mock_query.limit.return_value = mock_query
        mock_query.all.return_value = []

        result, total = get_transactions(mock_db, page=3, size=10)

        mock_query.offset.assert_called_with(20)
        mock_query.limit.assert_called_with(10)
