import io

from app import constants
from app.schemas import UploadResponse
from app.services import CSVProcessor


class DummyFile:
    def __init__(self, content: str):
        self.file = io.BytesIO(content.encode())


def test_process_file_success(monkeypatch, session):
    content = (
        ",".join(constants.COLUMNS)
        + "\n"
        + "550e8400-e29b-41d4-a716-446655440000,"
        "2024-01-01T12:00:00Z,100.0,pln,"
        "11111111-1111-1111-1111-111111111111,"
        "aaaaaaa1-aaaa-aaaa-aaaa-aaaaaaaaaaaa,2"
    )
    dummy_file = DummyFile(content)

    def fake_is_valid(self):
        return True

    def fake_save(self, db):
        pass

    monkeypatch.setattr("app.services.RowProcessor.is_valid", fake_is_valid)
    monkeypatch.setattr("app.services.RowProcessor.save", fake_save)

    processor = CSVProcessor(session)
    result = processor.process_file(dummy_file)

    assert isinstance(result, UploadResponse)
    assert result.processed_count == 1
    assert result.error_count == 0
    assert result.errors == []


def test_process_file_invalid_header(session):
    bad_header = "S,R,T\n" "z,x,c,v,q,s,z"
    dummy_file = DummyFile(bad_header)
    processor = CSVProcessor(session)
    result = processor.process_file(dummy_file)

    assert result.error_count == 1
    assert "Invalid CSV header" in result.errors[0]
    assert result.processed_count == 0


def test_process_file_row_with_errors(monkeypatch, session):
    content = ",".join(constants.COLUMNS) + "\n" + "a,c,d,b,z,s,q"
    dummy_file = DummyFile(content)

    def fake_init(self, columns):
        self.columns = columns
        self.errors = ["error1", "error2"]

    monkeypatch.setattr("app.services.RowProcessor.__init__", fake_init)
    monkeypatch.setattr("app.services.RowProcessor.is_valid", lambda _: False)
    monkeypatch.setattr("app.services.RowProcessor.save", lambda *args: None)

    processor = CSVProcessor(session)
    result = processor.process_file(dummy_file)

    assert result.error_count == 1
    assert any("Row 1 errors" in e for e in result.errors)
    assert result.processed_count == 1
