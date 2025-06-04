from app.services import is_valid_uuid


def test_valid_uuid():
    assert is_valid_uuid("550e8400-e29b-41d4-a716-446655440000") is True


def test_invalid_uuid():
    assert is_valid_uuid("invalid-uuid") is False
    assert is_valid_uuid("") is False
    assert is_valid_uuid(None) is False


def test_uuid_without_hyphens():
    assert is_valid_uuid("550e8400e29b41d4a716446655440000") is False
