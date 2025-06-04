from uuid import uuid4

from sqlalchemy import Column, DateTime
from sqlalchemy import Enum as SqlEnum
from sqlalchemy import Integer, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base

from app.constants import CurrencyEnum

Base = declarative_base()


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    transaction_id = Column(
        UUID(as_uuid=True), unique=True, nullable=False, index=True
    )
    timestamp = Column(DateTime, nullable=False)
    amount = Column(Numeric(precision=15, scale=2), nullable=False)
    currency = Column(SqlEnum(CurrencyEnum), nullable=False)
    customer_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    product_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    quantity = Column(Integer, nullable=False)
