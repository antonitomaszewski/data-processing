import decimal
import logging
from datetime import datetime
from decimal import Decimal
from io import BytesIO
from uuid import UUID

import pandas as pd
from fastapi import UploadFile
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.constants import CurrencyEnum
from app.models import Transaction
from app.schemas import TransactionCreate, UploadResponse

logger = logging.getLogger(__name__)


class CSVProcessor:
    BATCH_SIZE = 1000
    REQUIRED_COLUMNS = [
        "transaction_id",
        "timestamp",
        "amount",
        "currency",
        "customer_id",
        "product_id",
        "quantity",
    ]

    def __init__(self, db_session: Session):
        self.db = db_session

    def process_csv_file(self, file: UploadFile) -> UploadResponse:
        processed_count = 0
        errors = []
        warnings = []
        # import pdb; ipdb.set_trace()

        try:
            chunk_iter = pd.read_csv(
                BytesIO(file.file.read()),
                chunksize=self.BATCH_SIZE,
                dtype=str,
            )

            for chunk_num, chunk in enumerate(chunk_iter):
                logger.info(f"Processing chunk {chunk_num + 1}")

                chunk_errors = self._validate_chunk_structure(chunk, chunk_num)
                if chunk_errors:
                    errors.extend(chunk_errors)
                    continue

                (
                    valid_transactions,
                    chunk_errors,
                ) = self._validate_and_convert_chunk(chunk, chunk_num)
                errors.extend(chunk_errors)

                if valid_transactions:
                    saved_count, chunk_warnings = self._save_transactions(
                        valid_transactions
                    )
                    processed_count += saved_count
                    warnings.extend(chunk_warnings)

        except Exception as e:
            logger.error(f"Error processing CSV file: {str(e)}")
            errors.append(f"File processing error: {str(e)}")

        finally:
            file.file.seek(0)

        total_errors = len(errors)
        total_warnings = len(warnings)

        if processed_count == 0 and total_errors > 0:
            message = "No valid transactions were processed due to errors"
        elif total_errors == 0 and total_warnings == 0:
            message = f"Successfully processed {processed_count} transactions"
        else:
            message = f"""Processed {processed_count} transactions with
              {total_errors} errors and {total_warnings} warnings"""

        return UploadResponse(
            message=message,
            processed_count=processed_count,
            error_count=total_errors,
            errors=errors,
            warnings=warnings,
        )

    def _validate_chunk_structure(
        self, chunk: pd.DataFrame, chunk_num: int
    ) -> list[str]:
        errors = []

        missing_columns = set(self.REQUIRED_COLUMNS) - set(chunk.columns)
        if missing_columns:
            errors.append(
                f"""Chunk {chunk_num + 1}: Missing
                required columns: {', '.join(missing_columns)}"""
            )

        return errors

    def _validate_and_convert_chunk(
        self, chunk: pd.DataFrame, chunk_num: int
    ) -> tuple[list[TransactionCreate], list[str]]:
        valid_transactions = []
        errors = []

        for idx, row in chunk.iterrows():
            global_row_num = chunk_num * self.BATCH_SIZE + idx + 1

            try:
                transaction = self._validate_and_convert_row(
                    row, global_row_num
                )
                if transaction:
                    valid_transactions.append(transaction)
            except Exception as e:
                errors.append(f"Row {global_row_num}: {str(e)}")

        return valid_transactions, errors

    def _validate_and_convert_row(
        self, row: pd.Series, row_num: int
    ) -> TransactionCreate | None:
        if row.isnull().any():
            null_columns = row[row.isnull()].index.tolist()
            raise ValueError(
                f"Empty values in columns: {', '.join(null_columns)}"
            )

        try:
            transaction_id = UUID(str(row["transaction_id"]).strip())
        except (ValueError, TypeError):
            raise ValueError(
                f"Invalid transaction_id format: {row['transaction_id']}"
            )

        try:
            timestamp_str = str(row["timestamp"]).strip()
            if timestamp_str.endswith("Z"):
                timestamp_str = timestamp_str[:-1] + "+00:00"
            timestamp = datetime.fromisoformat(timestamp_str)
        except (ValueError, TypeError):
            raise ValueError(f"Invalid timestamp format: {row['timestamp']}")

        try:
            amount = Decimal(str(row["amount"]).strip())
            if amount <= 0:
                raise ValueError(f"Amount must be positive: {amount}")
        except (ValueError, TypeError, decimal.InvalidOperation):
            raise ValueError(f"Invalid amount format: {row['amount']}")

        try:
            currency = CurrencyEnum(str(row["currency"]).strip().upper())
        except ValueError:
            valid_currencies = [c.value for c in CurrencyEnum]
            raise ValueError(
                f"""Invalid currency: {row['currency']}.
                  Valid currencies: {', '.join(valid_currencies)}"""
            )

        try:
            customer_id = UUID(str(row["customer_id"]).strip())
        except (ValueError, TypeError):
            raise ValueError(
                f"Invalid customer_id format: {row['customer_id']}"
            )

        try:
            product_id = UUID(str(row["product_id"]).strip())
        except (ValueError, TypeError):
            raise ValueError(f"Invalid product_id format: {row['product_id']}")

        try:
            quantity = int(str(row["quantity"]).strip())
            if quantity <= 0:
                raise ValueError(f"Quantity must be positive: {quantity}")
        except (ValueError, TypeError):
            raise ValueError(f"Invalid quantity format: {row['quantity']}")

        return TransactionCreate(
            transaction_id=transaction_id,
            timestamp=timestamp,
            amount=amount,
            currency=currency,
            customer_id=customer_id,
            product_id=product_id,
            quantity=quantity,
        )

    def _save_transactions(
        self, transactions: list[TransactionCreate]
    ) -> tuple[int, list[str]]:
        saved_count = 0
        warnings = []

        for transaction in transactions:
            try:
                db_transaction = Transaction(
                    transaction_id=transaction.transaction_id,
                    timestamp=transaction.timestamp,
                    amount=transaction.amount,
                    currency=transaction.currency,
                    customer_id=transaction.customer_id,
                    product_id=transaction.product_id,
                    quantity=transaction.quantity,
                )

                self.db.add(db_transaction)
                self.db.flush()
                saved_count += 1

            except IntegrityError as e:
                self.db.rollback()
                if (
                    "unique constraint" in str(e).lower()
                    and "transaction_id" in str(e).lower()
                ):
                    warnings.append(
                        f"""Duplicate transaction_id:
                          {transaction.transaction_id}"""
                    )
                else:
                    warnings.append(
                        f"""Database error for transaction
                          {transaction.transaction_id}: {str(e)}"""
                    )
                logger.warning(
                    f"""Integrity error for transaction
                      {transaction.transaction_id}: {str(e)}"""
                )

        try:
            self.db.commit()
            logger.info(f"Successfully saved {saved_count} transactions")
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error committing transactions: {str(e)}")
            raise

        return saved_count, warnings
