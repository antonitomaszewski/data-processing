from app.services import RowProcessor


class TestValidateCustomerId:
    def test_valid_customer_id(self):
        columns = [
            "550e8400-e29b-41d4-a716-446655440000",
            "2024-01-15T17:00:00Z",
            "100.50",
            "PLN",
            "550e8400-e29b-41d4-a716-446655440001",
            "550e8400-e29b-41d4-a716-446655440002",
            "2",
        ]
        processor = RowProcessor(columns)
        assert processor.validate_customer_id() is True

    def test_invalid_customer_id(self):
        columns = [
            "550e8400-e29b-41d4-a716-446655440000",
            "2024-01-15T17:00:00Z",
            "100.50",
            "PLN",
            "invalid-uuid",
            "550e8400-e29b-41d4-a716-446655440002",
            "2",
        ]
        processor = RowProcessor(columns)
        assert processor.validate_customer_id() is False
        assert any("customer_id" in error for error in processor.errors)


class TestValidateProductId:
    def test_valid_product_id(self):
        columns = [
            "550e8400-e29b-41d4-a716-446655440000",
            "2024-01-15T17:00:00Z",
            "100.50",
            "PLN",
            "550e8400-e29b-41d4-a716-446655440001",
            "550e8400-e29b-41d4-a716-446655440002",
            "2",
        ]
        processor = RowProcessor(columns)
        assert processor.validate_product_id() is True

    def test_invalid_product_id(self):
        columns = [
            "550e8400-e29b-41d4-a716-446655440000",
            "2024-01-15T17:00:00Z",
            "100.50",
            "PLN",
            "550e8400-e29b-41d4-a716-446655440001",
            "invalid-uuid",
            "2",
        ]
        processor = RowProcessor(columns)
        assert processor.validate_product_id() is False
        assert any("product_id" in error for error in processor.errors)


class TestValidateTransactionId:
    def test_valid_transaction_id(self):
        columns = [
            "550e8400-e29b-41d4-a716-446655440000",
            "2024-01-15T17:00:00Z",
            "100.50",
            "PLN",
            "550e8400-e29b-41d4-a716-446655440001",
            "550e8400-e29b-41d4-a716-446655440002",
            "2",
        ]
        processor = RowProcessor(columns)
        assert processor.validate_transaction_id() is True

    def test_invalid_transaction_id(self):
        columns = [
            "invalid-uuid",
            "2024-01-15T17:00:00Z",
            "100.50",
            "PLN",
            "550e8400-e29b-41d4-a716-446655440001",
            "550e8400-e29b-41d4-a716-446655440002",
            "2",
        ]
        processor = RowProcessor(columns)
        assert processor.validate_transaction_id() is False
        assert any("transaction_id" in error for error in processor.errors)


class TestValidateTimestamp:
    def test_valid_iso_timestamp(self):
        columns = [
            "550e8400-e29b-41d4-a716-446655440000",
            "2024-01-15T17:00:00Z",
            "100",
            "PLN",
            "550e8400-e29b-41d4-a716-446655440001",
            "550e8400-e29b-41d4-a716-446655440002",
            "2",
        ]
        processor = RowProcessor(columns)
        assert processor.validate_timestamp() is True

    def test_valid_iso_timestamp_no_z(self):
        columns = [
            "550e8400-e29b-41d4-a716-446655440000",
            "2024-01-15T17:00:00",
            "100",
            "PLN",
            "550e8400-e29b-41d4-a716-446655440001",
            "550e8400-e29b-41d4-a716-446655440002",
            "2",
        ]
        processor = RowProcessor(columns)
        assert processor.validate_timestamp() is True

    def test_valid_simplified_iso_timestamp_format(self):
        columns = [
            "550e8400-e29b-41d4-a716-446655440000",
            "2024-01-15 17:00:00",
            "100",
            "PLN",
            "550e8400-e29b-41d4-a716-446655440001",
            "550e8400-e29b-41d4-a716-446655440002",
            "2",
        ]
        processor = RowProcessor(columns)
        assert processor.validate_timestamp() is True

    def test_invalid_timestamp_random_string(self):
        columns = [
            "550e8400-e29b-41d4-a716-446655440000",
            "not-a-date",
            "100",
            "PLN",
            "550e8400-e29b-41d4-a716-446655440001",
            "550e8400-e29b-41d4-a716-446655440002",
            "2",
        ]
        processor = RowProcessor(columns)
        assert processor.validate_timestamp() is False
        assert any("timestamp" in error for error in processor.errors)


class TestValidateQuantity:
    def test_valid_positive_quantity(self):
        columns = [
            "550e8400-e29b-41d4-a716-446655440000",
            "2024-01-15T17:00:00Z",
            "100",
            "PLN",
            "550e8400-e29b-41d4-a716-446655440001",
            "550e8400-e29b-41d4-a716-446655440002",
            "5",
        ]
        processor = RowProcessor(columns)
        assert processor.validate_quantity() is True

    def test_invalid_zero_quantity(self):
        columns = [
            "550e8400-e29b-41d4-a716-446655440000",
            "2024-01-15T17:00:00Z",
            "100",
            "PLN",
            "550e8400-e29b-41d4-a716-446655440001",
            "550e8400-e29b-41d4-a716-446655440002",
            "0",
        ]
        processor = RowProcessor(columns)
        assert processor.validate_quantity() is False
        assert any("quantity" in error for error in processor.errors)

    def test_invalid_negative_quantity(self):
        columns = [
            "550e8400-e29b-41d4-a716-446655440000",
            "2024-01-15T17:00:00Z",
            "100",
            "PLN",
            "550e8400-e29b-41d4-a716-446655440001",
            "550e8400-e29b-41d4-a716-446655440002",
            "-1",
        ]
        processor = RowProcessor(columns)
        assert processor.validate_quantity() is False
        assert any("quantity" in error for error in processor.errors)

    def test_invalid_non_numeric_quantity(self):
        columns = [
            "550e8400-e29b-41d4-a716-446655440000",
            "2024-01-15T17:00:00Z",
            "100",
            "PLN",
            "550e8400-e29b-41d4-a716-446655440001",
            "550e8400-e29b-41d4-a716-446655440002",
            "abc",
        ]
        processor = RowProcessor(columns)
        assert processor.validate_quantity() is False
        assert any("quantity" in error for error in processor.errors)

    def test_invalid_float_quantity(self):
        columns = [
            "550e8400-e29b-41d4-a716-446655440000",
            "2024-01-15T17:00:00Z",
            "100",
            "PLN",
            "550e8400-e29b-41d4-a716-446655440001",
            "550e8400-e29b-41d4-a716-446655440002",
            "2.5",
        ]
        processor = RowProcessor(columns)
        assert processor.validate_quantity() is False
        assert any("quantity" in error for error in processor.errors)


class TestColumnCount:
    def test_too_few_columns(self):
        columns = [
            "550e8400-e29b-41d4-a716-446655440000",
            "2024-01-15T17:00:00Z",
            "100.50",
            "PLN",
            "550e8400-e29b-41d4-a716-446655440001",
        ]
        processor = RowProcessor(columns)
        assert processor.is_valid() is False
        assert any("number of columns" in error for error in processor.errors)

    def test_too_many_columns(self):
        columns = [
            "550e8400-e29b-41d4-a716-446655440000",
            "2024-01-15T17:00:00Z",
            "100.50",
            "PLN",
            "550e8400-e29b-41d4-a716-446655440001",
            "550e8400-e29b-41d4-a716-446655440002",
            "2",
            "extra_column",
        ]
        processor = RowProcessor(columns)
        assert processor.is_valid() is False
        assert any("number of columns" in error for error in processor.errors)

    def test_empty_columns(self):
        columns = []
        processor = RowProcessor(columns)
        assert processor.is_valid() is False
        assert any("number of columns" in error for error in processor.errors)

    def test_single_column(self):
        columns = ["550e8400-e29b-41d4-a716-446655440000"]
        processor = RowProcessor(columns)
        assert processor.is_valid() is False
        assert any("number of columns" in error for error in processor.errors)


class TestValidateAmount:
    def test_valid_positive_amount(self):
        columns = [
            "550e8400-e29b-41d4-a716-446655440000",
            "2024-01-15T17:00:00Z",
            "100.50",
            "PLN",
            "550e8400-e29b-41d4-a716-446655440001",
            "550e8400-e29b-41d4-a716-446655440002",
            "2",
        ]
        processor = RowProcessor(columns)
        assert processor.validate_amount() is True

    def test_valid_integer_amount(self):
        columns = [
            "550e8400-e29b-41d4-a716-446655440000",
            "2024-01-15T17:00:00Z",
            "100",
            "PLN",
            "550e8400-e29b-41d4-a716-446655440001",
            "550e8400-e29b-41d4-a716-446655440002",
            "2",
        ]
        processor = RowProcessor(columns)
        assert processor.validate_amount() is True

    def test_valid_decimal_with_many_places(self):
        columns = [
            "550e8400-e29b-41d4-a716-446655440000",
            "2024-01-15T17:00:00Z",
            "123.456789",
            "PLN",
            "550e8400-e29b-41d4-a716-446655440001",
            "550e8400-e29b-41d4-a716-446655440002",
            "2",
        ]
        processor = RowProcessor(columns)
        assert processor.validate_amount() is True

    def test_invalid_negative_amount(self):
        columns = [
            "550e8400-e29b-41d4-a716-446655440000",
            "2024-01-15T17:00:00Z",
            "-100.50",
            "PLN",
            "550e8400-e29b-41d4-a716-446655440001",
            "550e8400-e29b-41d4-a716-446655440002",
            "2",
        ]
        processor = RowProcessor(columns)
        assert processor.validate_amount() is False
        assert any("amount" in error for error in processor.errors)

    def test_invalid_zero_amount(self):
        columns = [
            "550e8400-e29b-41d4-a716-446655440000",
            "2024-01-15T17:00:00Z",
            "0",
            "PLN",
            "550e8400-e29b-41d4-a716-446655440001",
            "550e8400-e29b-41d4-a716-446655440002",
            "2",
        ]
        processor = RowProcessor(columns)
        assert processor.validate_amount() is False
        assert any("amount" in error for error in processor.errors)

    def test_invalid_zero_decimal_amount(self):
        columns = [
            "550e8400-e29b-41d4-a716-446655440000",
            "2024-01-15T17:00:00Z",
            "0.00",
            "PLN",
            "550e8400-e29b-41d4-a716-446655440001",
            "550e8400-e29b-41d4-a716-446655440002",
            "2",
        ]
        processor = RowProcessor(columns)
        assert processor.validate_amount() is False
        assert any("amount" in error for error in processor.errors)

    def test_invalid_non_numeric_amount(self):
        columns = [
            "550e8400-e29b-41d4-a716-446655440000",
            "2024-01-15T17:00:00Z",
            "abc",
            "PLN",
            "550e8400-e29b-41d4-a716-446655440001",
            "550e8400-e29b-41d4-a716-446655440002",
            "2",
        ]
        processor = RowProcessor(columns)
        assert processor.validate_amount() is False
        assert any("amount" in error for error in processor.errors)

    def test_invalid_empty_amount(self):
        columns = [
            "550e8400-e29b-41d4-a716-446655440000",
            "2024-01-15T17:00:00Z",
            "",
            "PLN",
            "550e8400-e29b-41d4-a716-446655440001",
            "550e8400-e29b-41d4-a716-446655440002",
            "2",
        ]
        processor = RowProcessor(columns)
        assert processor.validate_amount() is False
        assert any("amount" in error for error in processor.errors)

    def test_invalid_amount_with_currency_symbol(self):
        columns = [
            "550e8400-e29b-41d4-a716-446655440000",
            "2024-01-15T17:00:00Z",
            "$100.50",
            "PLN",
            "550e8400-e29b-41d4-a716-446655440001",
            "550e8400-e29b-41d4-a716-446655440002",
            "2",
        ]
        processor = RowProcessor(columns)
        assert processor.validate_amount() is False
        assert any("amount" in error for error in processor.errors)


class TestValidateCurrency:
    def test_valid_pln_currency(self):
        columns = [
            "550e8400-e29b-41d4-a716-446655440000",
            "2024-01-15T17:00:00Z",
            "100.50",
            "PLN",
            "550e8400-e29b-41d4-a716-446655440001",
            "550e8400-e29b-41d4-a716-446655440002",
            "2",
        ]
        processor = RowProcessor(columns)
        assert processor.validate_currency() is True

    def test_valid_eur_currency(self):
        columns = [
            "550e8400-e29b-41d4-a716-446655440000",
            "2024-01-15T17:00:00Z",
            "100.50",
            "EUR",
            "550e8400-e29b-41d4-a716-446655440001",
            "550e8400-e29b-41d4-a716-446655440002",
            "2",
        ]
        processor = RowProcessor(columns)
        assert processor.validate_currency() is True

    def test_valid_usd_currency(self):
        columns = [
            "550e8400-e29b-41d4-a716-446655440000",
            "2024-01-15T17:00:00Z",
            "100.50",
            "USD",
            "550e8400-e29b-41d4-a716-446655440001",
            "550e8400-e29b-41d4-a716-446655440002",
            "2",
        ]
        processor = RowProcessor(columns)
        assert processor.validate_currency() is True

    def test_invalid_lowercase_currency(self):
        columns = [
            "550e8400-e29b-41d4-a716-446655440000",
            "2024-01-15T17:00:00Z",
            "100.50",
            "pln",
            "550e8400-e29b-41d4-a716-446655440001",
            "550e8400-e29b-41d4-a716-446655440002",
            "2",
        ]
        processor = RowProcessor(columns)
        assert processor.validate_currency() is False
        assert any("currency" in error for error in processor.errors)

    def test_invalid_unknown_currency(self):
        columns = [
            "550e8400-e29b-41d4-a716-446655440000",
            "2024-01-15T17:00:00Z",
            "100.50",
            "GBP",
            "550e8400-e29b-41d4-a716-446655440001",
            "550e8400-e29b-41d4-a716-446655440002",
            "2",
        ]
        processor = RowProcessor(columns)
        assert processor.validate_currency() is False
        assert any("currency" in error for error in processor.errors)

    def test_invalid_numeric_currency(self):
        columns = [
            "550e8400-e29b-41d4-a716-446655440000",
            "2024-01-15T17:00:00Z",
            "100.50",
            "123",
            "550e8400-e29b-41d4-a716-446655440001",
            "550e8400-e29b-41d4-a716-446655440002",
            "2",
        ]
        processor = RowProcessor(columns)
        assert processor.validate_currency() is False
        assert any("currency" in error for error in processor.errors)

    def test_invalid_empty_currency(self):
        columns = [
            "550e8400-e29b-41d4-a716-446655440000",
            "2024-01-15T17:00:00Z",
            "100.50",
            "",
            "550e8400-e29b-41d4-a716-446655440001",
            "550e8400-e29b-41d4-a716-446655440002",
            "2",
        ]
        processor = RowProcessor(columns)
        assert processor.validate_currency() is False
        assert any("currency" in error for error in processor.errors)

    def test_invalid_special_characters_currency(self):
        columns = [
            "550e8400-e29b-41d4-a716-446655440000",
            "2024-01-15T17:00:00Z",
            "100.50",
            "PL$",
            "550e8400-e29b-41d4-a716-446655440001",
            "550e8400-e29b-41d4-a716-446655440002",
            "2",
        ]
        processor = RowProcessor(columns)
        assert processor.validate_currency() is False
        assert any("currency" in error for error in processor.errors)


class TestRowProcessorMultiple:
    # zwracamy pierwszy wykryty błąd
    def test_multiple_errors(self):
        columns = [
            "invalid-uuid",
            "not-a-date",
            "-100",
            "INVALID",
            "bad-uuid",
            "bad-uuid",
            "0",
        ]
        processor = RowProcessor(columns)
        assert processor.is_valid() is False
        assert len(processor.errors) == 1
