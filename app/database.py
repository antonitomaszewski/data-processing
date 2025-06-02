from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import settings

database_url = str(settings.database_url)
engine = create_engine(database_url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    from app.models import Base

    Base.metadata.create_all(bind=engine)
