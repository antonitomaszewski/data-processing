import uuid
from decimal import Decimal

from app.constants import EXCHANGE_RATES, CurrencyEnum


def convert_to_pln(amount: Decimal | float, currency: CurrencyEnum) -> Decimal:
    if not isinstance(amount, Decimal):
        amount = Decimal(str(amount))

    if currency not in EXCHANGE_RATES:
        raise ValueError(f"Unsupported currency: {currency}")

    exchange_rate = Decimal(str(EXCHANGE_RATES[currency]))
    return amount * exchange_rate


def format_currency_amount(
    amount: Decimal | float, precision: int = 2
) -> Decimal:
    if not isinstance(amount, Decimal):
        amount = Decimal(str(amount))

    return amount.quantize(Decimal("0." + "0" * precision))


def is_valid_uuid(value: str) -> bool:
    if value is None:
        return False
    try:
        return str(uuid.UUID(value)) == value.lower()
    except ValueError:
        return False
