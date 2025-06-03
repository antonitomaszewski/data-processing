from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, field_validator

from app.constants import CurrencyEnum


class CustomerSummaryResponse(BaseModel):
    customer_id: UUID
    total_amount_pln: Decimal
    # sum(amount * exchange_rate for each transaction)
    unique_products: list[UUID]
    # list(set(product_id for each transaction))
    last_transaction_date: datetime
    # max(timestamp for each transaction)


class ProductSummaryResponse(BaseModel):
    product_id: UUID
    total_quantity_sold: int
    # sum(quantity for each transaction)
    total_revenue_pln: Decimal
    # sum(amount * exchange_rate for each transaction)
    unique_customers: list[UUID]
    # list(set(customer_id for each transaction))


class UploadResponse(BaseModel):
    message: str
    processed_count: int
    error_count: int
    errors: list[str] = []


class TransactionBase(BaseModel):
    transaction_id: UUID
    timestamp: datetime
    amount: Decimal
    currency: CurrencyEnum
    customer_id: UUID
    product_id: UUID
    quantity: int

    @field_validator("amount")
    def validate_amount(cls, v):
        if v <= 0:
            raise ValueError("Amount must be positive")
        return round(v, 2)


class TransactionCreate(TransactionBase):
    pass


class TransactionResponse(TransactionBase):
    id: UUID

    class Config:
        from_attributes = True


class TransactionListResponse(BaseModel):
    data: list[UUID]
    total: int
    page: int
    size: int
    pages: int
