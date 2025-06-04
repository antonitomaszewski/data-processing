from unittest.mock import Mock, patch

from app.services import CSVProcessor


class TestCSVProcessorInit:
    def test_init_sets_correct_attributes(self):
        mock_db = Mock()
        processor = CSVProcessor(mock_db)

        assert processor.db == mock_db
        assert processor.processed_count == 0
        assert processor.total_errors == 0
        assert processor.errors == []
        assert processor.message == "File processed successfully"


class TestCSVProcessorProcessFile:
    def test_process_file_valid_csv(self):
        csv_content = (
            "transaction_id,timestamp,amount,currency,"
            "customer_id,product_id,quantity\n"
            "550e8400-e29b-41d4-a716-446655440000,"
            "2024-01-15T17:00:00Z,100.50,PLN,"
            "550e8400-e29b-41d4-a716-446655440001,"
            "550e8400-e29b-41d4-a716-446655440002,2"
        )

        mock_file = Mock()
        mock_file.file.read.return_value = csv_content.encode("utf-8")

        mock_db = Mock()
        processor = CSVProcessor(mock_db)

        with patch.object(processor, "process_row") as mock_process_row:
            result = processor.process_file(mock_file)

            mock_process_row.assert_called_once_with(
                1,
                [
                    "550e8400-e29b-41d4-a716-446655440000",
                    "2024-01-15T17:00:00Z",
                    "100.50",
                    "PLN",
                    "550e8400-e29b-41d4-a716-446655440001",
                    "550e8400-e29b-41d4-a716-446655440002",
                    "2",
                ],
            )

            assert result.message == "File processed successfully"

    def test_process_file_invalid_header(self):
        csv_content = "wrong,header,format\ndata1,data2,data3"

        mock_file = Mock()
        mock_file.file.read.return_value = csv_content.encode("utf-8")

        mock_db = Mock()
        processor = CSVProcessor(mock_db)

        with patch.object(processor, "process_row") as mock_process_row:
            processor.process_file(mock_file)

            mock_process_row.assert_not_called()

            assert len(processor.errors) == 1
            assert "Invalid CSV header" in processor.errors[0]


class TestCSVProcessorProcessRow:
    def test_process_row_valid_data(self):
        mock_db = Mock()
        processor = CSVProcessor(mock_db)

        row_data = ["valid", "data"]

        with patch("app.services.RowProcessor") as mock_row_processor_class:
            mock_row_processor = Mock()
            mock_row_processor.is_valid.return_value = True
            mock_row_processor.errors = []
            mock_row_processor_class.return_value = mock_row_processor

            processor.process_row(1, row_data)

            mock_row_processor_class.assert_called_once_with(row_data)
            mock_row_processor.save.assert_called_once_with(mock_db)

            assert processor.total_errors == 0

    def test_process_row_invalid_data(self):
        mock_db = Mock()
        processor = CSVProcessor(mock_db)

        row_data = ["invalid", "data"]

        with patch("app.services.RowProcessor") as mock_row_processor_class:
            mock_row_processor = Mock()
            mock_row_processor.is_valid.return_value = False
            mock_row_processor.errors = ["Error 1", "Error 2"]
            mock_row_processor_class.return_value = mock_row_processor

            processor.process_row(5, row_data)

            mock_row_processor.save.assert_not_called()

            assert processor.total_errors == 1
            assert len(processor.errors) == 1
            assert "Row 5 errors: Error 1,Error 2" in processor.errors[0]
