from enum import Enum


class CurrencyEnum(str, Enum):
    PLN = "PLN"
    EUR = "EUR"
    USD = "USD"


EXCHANGE_RATES = {
    CurrencyEnum.PLN: 1.0,
    CurrencyEnum.EUR: 4.3,
    CurrencyEnum.USD: 4.0,
}


COLUMNS = (
    "transaction_id",
    "timestamp",
    "amount",
    "currency",
    "customer_id",
    "product_id",
    "quantity",
)
