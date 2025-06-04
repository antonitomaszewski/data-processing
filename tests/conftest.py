from datetime import datetime

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.models import Base, Transaction
from tests.test_data import (
    CUSTOMER1_ID,
    CUSTOMER2_ID,
    PROD1_ID,
    PROD2_ID,
    TRANSACTION1_ID,
    TRASNACTION2_ID,
)


@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    TestingSessionLocal = sessionmaker(bind=engine)
    return TestingSessionLocal()


@pytest.fixture
def session_with_data(session):
    transaction1 = Transaction(
        transaction_id=TRANSACTION1_ID,
        timestamp=datetime.now(),
        amount=100.0,
        currency="PLN",
        customer_id=CUSTOMER1_ID,
        product_id=PROD1_ID,
        quantity=2,
    )
    transaction2 = Transaction(
        transaction_id=TRASNACTION2_ID,
        timestamp=datetime.now(),
        amount=200.0,
        currency="EUR",
        customer_id=CUSTOMER2_ID,
        product_id=PROD2_ID,
        quantity=3,
    )

    session.add_all([transaction1, transaction2])
    session.commit()
    return session
