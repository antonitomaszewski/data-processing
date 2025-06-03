import csv
import io
import logging
import uuid
from datetime import datetime

from sqlalchemy import distinct, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

import app.constants as constants
import app.utils as utils
from app.models import Transaction
from app.schemas import (
    CustomerSummaryResponse,
    ProductSummaryResponse,
    TransactionCreate,
    TransactionResponse,
    UploadResponse,
)

logger = logging.getLogger(__name__)


def is_valid_uuid(value: str) -> bool:
    try:
        uuid.UUID(value)
        return True
    except ValueError:
        return False


class RowProcessor:
    def __init__(self, columns):
        self.columns = columns
        self.errors = []

    def is_valid(self):
        if not self.columns or len(self.columns) < 7:
            self.errors.append("number of columns")

        return (
            len(self.columns) == 7
            and self.validate_transaction_id()
            and self.validate_timestamp()
            and self.validate_amount()
            and self.validate_currency()
            and self.validate_customer_id()
            and self.validate_product_id()
            and self.validate_quantity()
        )

    def validate_transaction_id(self):
        if self._is_valid_uuid(self.columns[0]):
            return True
        self.errors.append(f"transaction_id: {self.columns[0]}")
        return False

    def validate_timestamp(self):
        try:
            datetime.fromisoformat(self.columns[1])
            return True
        except ValueError:
            self.errors.append(f"timestamp: {self.columns[1]}")
            return False

    def validate_amount(self):
        try:
            if float(self.columns[2]) > 0:
                return True
            else:
                self.errors.append(f"amount: {self.columns[2]}")
                return False
        except ValueError:
            self.errors.append(f"amount: {self.columns[2]}")
            return False

    def validate_currency(self):
        try:
            constants.CurrencyEnum(self.columns[3])
            return True
        except ValueError:
            self.errors.append(f"currency: {self.columns[3]}")
            return False

    def validate_customer_id(self):
        if self._is_valid_uuid(self.columns[4]):
            return True
        self.errors.append(f"customer_id: {self.columns[4]}")
        return False

    def validate_product_id(self):
        if self._is_valid_uuid(self.columns[5]):
            return True
        self.errors.append(f"product_id: {self.columns[5]}")
        return False

    def validate_quantity(self):
        try:
            if int(self.columns[6]) > 0:
                return True
            else:
                self.errors.append(f"quantity: {self.columns[6]}")
                return False
        except ValueError:
            self.errors.append(f"quantity: {self.columns[6]}")
            return False

    def _is_valid_uuid(self, value):
        return is_valid_uuid(value)

    def save(self, db):
        transaction = TransactionCreate(
            transaction_id=self.columns[0],
            timestamp=self.columns[1],
            amount=self.columns[2],
            currency=self.columns[3],
            customer_id=self.columns[4],
            product_id=self.columns[5],
            quantity=self.columns[6],
        )

        db_transaction = Transaction(**transaction.dict())
        try:
            db.add(db_transaction)
            db.commit()
        except IntegrityError:
            self.errors.append(
                f"Integrity error for transaction {self.columns[0]}"
            )
            db.rollback()


class CSVProcessor:
    def __init__(self, db_session: Session):
        self.errors = []
        self.db = db_session
        self.processed_count = 0
        self.total_errors = 0
        self.message = "File processed successfully"

    def process_file(self, file) -> UploadResponse:
        contents = file.file.read()
        decoded = contents.decode("utf-8")
        reader = csv.reader(io.StringIO(decoded))
        for i, row_data in enumerate(reader):
            normalized = tuple(col.strip().lower() for col in row_data)
            expected = tuple(col.lower() for col in constants.COLUMNS)
            if i == 0 and normalized != expected:
                self.errors.append(f"Invalid CSV header: {row_data}")
                break
            elif i != 0:
                self.process_row(i, row_data)
        return UploadResponse(
            message=self.message,
            processed_count=self.processed_count,
            error_count=self.total_errors,
            errors=self.errors,
        )

    def process_row(self, i, row_data):
        row = RowProcessor(row_data)
        if row.is_valid():
            row.save(self.db)
        if row.errors:
            self.total_errors += 1
            self.errors.append(f'Row {i} errors: {",".join(row.errors)}')
        self.processed_count


def get_transactions(
    db: Session,
    page: int,
    size: int,
    customer_id: str | None = None,
    product_id: str | None = None,
) -> tuple[list[TransactionResponse], int]:
    query = db.query(Transaction)

    if customer_id:
        query = query.filter(Transaction.customer_id == customer_id)
    if product_id:
        query = query.filter(Transaction.product_id == product_id)

    total = query.count()

    offset = (page - 1) * size
    transactions = (
        query.order_by(Transaction.timestamp.desc())
        .offset(offset)
        .limit(size)
        .all()
    )

    response_data = [t.transaction_id for t in transactions]

    return response_data, total


def get_transaction_by_id(
    db: Session, transaction_id: str
) -> TransactionResponse | None:
    transaction = (
        db.query(Transaction)
        .filter(Transaction.transaction_id == transaction_id)
        .first()
    )
    if not transaction:
        return None
    return TransactionResponse.from_orm(transaction)


def get_customer_summary(
    db: Session, customer_id: str
) -> CustomerSummaryResponse:
    transactions = (
        db.query(Transaction)
        .filter(Transaction.customer_id == customer_id)
        .all()
    )

    if not transactions:
        return None

    total_pln = utils.format_currency_amount(
        sum(utils.convert_to_pln(t.amount, t.currency) for t in transactions)
    )
    unique_products = list(set(t.product_id for t in transactions))
    last_date = max(t.timestamp for t in transactions)

    return CustomerSummaryResponse(
        customer_id=customer_id,
        total_amount_pln=total_pln,
        unique_products=unique_products,
        last_transaction_date=last_date,
    )


def get_product_summary(
    db: Session, product_id: str
) -> ProductSummaryResponse:
    transactions = (
        db.query(Transaction)
        .filter(Transaction.product_id == product_id)
        .all()
    )

    if not transactions:
        return None

    total_quantity = (
        db.query(func.sum(Transaction.quantity))
        .filter(Transaction.product_id == product_id)
        .scalar()
        or 0
    )

    total_pln = utils.format_currency_amount(
        sum(utils.convert_to_pln(t.amount, t.currency) for t in transactions)
    )

    unique_customers = (
        db.query(distinct(Transaction.customer_id))
        .filter(Transaction.product_id == product_id)
        .all()
    )
    unique_customers = [row[0] for row in unique_customers]

    return ProductSummaryResponse(
        product_id=product_id,
        total_quantity_sold=total_quantity,
        total_revenue_pln=total_pln,
        unique_customers=unique_customers,
    )
