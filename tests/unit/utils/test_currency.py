from decimal import Decimal

import pytest

from app.constants import CurrencyEnum
from app.utils import convert_to_pln, format_currency_amount


class TestConvertToPln:
    def test_convert_pln_to_pln(self):
        result = convert_to_pln(Decimal("100.00"), CurrencyEnum.PLN)
        assert result == Decimal("100.00")

    def test_convert_eur_to_pln(self):
        result = convert_to_pln(Decimal("100.00"), CurrencyEnum.EUR)
        assert result == Decimal("430.00")

    def test_convert_usd_to_pln(self):
        result = convert_to_pln(Decimal("100.00"), CurrencyEnum.USD)
        assert result == Decimal("400.00")

    def test_convert_float_input(self):
        result = convert_to_pln(100.50, CurrencyEnum.EUR)
        assert result == Decimal("432.15")


class TestFormatCurrencyAmount:
    def test_format_default_precision(self):
        result = format_currency_amount(Decimal("123.456"))
        assert result == Decimal("123.46")

    def test_format_custom_precision(self):
        result = format_currency_amount(Decimal("123.456"), precision=1)
        assert result == Decimal("123.5")

    def test_format_float_input(self):
        result = format_currency_amount(123.456)
        assert result == Decimal("123.46")

    def test_convert_to_pln_unsupported_currency(self):
        with pytest.raises(ValueError, match="Unsupported currency"):
            convert_to_pln(Decimal("100"), "GBP")

    def test_convert_to_pln_none_currency(self):
        with pytest.raises(ValueError):
            convert_to_pln(Decimal("100"), None)
