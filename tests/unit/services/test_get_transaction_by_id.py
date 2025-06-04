from unittest.mock import Mock, patch

from app.models import Transaction
from app.schemas import TransactionResponse
from app.services import get_transaction_by_id


class TestGetTransactionById:
    def test_get_transaction_by_id_found(self):
        # Arrange
        mock_db = Mock()
        mock_query = Mock()
        mock_transaction = Mock()
        mock_response = Mock(spec=TransactionResponse)
        mock_db.query.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.first.return_value = mock_transaction

        with patch("app.services.TransactionResponse") as mock_response_class:
            mock_response_class.from_orm.return_value = mock_response

            transaction_id = "550e8400-e29b-41d4-a716-446655440000"

            # Act
            result = get_transaction_by_id(mock_db, transaction_id)

            # Assert
            assert result == mock_response
            mock_db.query.assert_called_once()
            mock_query.filter.assert_called_once()
            mock_query.first.assert_called_once()
            mock_response_class.from_orm.assert_called_once_with(
                mock_transaction
            )

    def test_get_transaction_by_id_not_found(self):
        # Arrange
        mock_db = Mock()
        mock_query = Mock()

        mock_db.query.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.first.return_value = None

        transaction_ids = [
            "550e8400-e29b-41d4-a716-446655440000",
            "550e8400-e29b-41d4-a716-446655440001",
            "123e4567-e89b-12d3-a456-426614174000",
        ]
        for transaction_id in transaction_ids:
            mock_db.reset_mock()
            mock_query.reset_mock()

            # Act
            result = get_transaction_by_id(mock_db, transaction_id)

            # Assert
            assert result is None
            mock_db.query.assert_called_once_with(Transaction)
            mock_db.query.assert_called_once()
            mock_query.filter.assert_called_once()
            mock_query.first.assert_called_once()
