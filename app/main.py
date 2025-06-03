import math
from typing import Optional

from fastapi import Depends, FastAPI, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

import app.services as services
from app.config import settings
from app.database import get_db, init_db
from app.schemas import TransactionListResponse, UploadResponse

app = FastAPI(
    debug=settings.debug,
)


@app.on_event("startup")
async def startup_event():
    init_db()


# app.include_router(router)


@app.get("/")
async def root():
    return {
        "message": "Data Processing API",
        "environment": settings.environment,
    }


@app.get("/health")
async def health_check():
    try:
        from sqlalchemy import text

        from app.database import engine

        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "degraded", "database": f"error: {e}"}


@app.post("/transactions/upload", response_model=UploadResponse)
def upload_transactions(
    file: UploadFile = File(...), db: Session = Depends(get_db)
) -> UploadResponse:
    if file.content_type not in ["text/csv", "application/csv"]:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Expected CSV, got {file.content_type}",
        )
    if not file.filename or not file.filename.lower().endswith(".csv"):
        raise HTTPException(
            status_code=400, detail="File must have .csv extension"
        )

    try:
        processor = services.CSVProcessor(db)
        result = processor.process_file(file)
        return result

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error processing file: {str(e)}"
        )


@app.get("/transactions", response_model=TransactionListResponse)
async def get_transactions(
    page: int = 1,
    size: int = 50,
    customer_id: Optional[str] = None,
    product_id: Optional[str] = None,
    db: Session = Depends(get_db),
) -> TransactionListResponse:
    if page < 1 or size < 1 or size > 100:
        raise HTTPException(status_code=400, detail="Invalid pagination")

    if customer_id and not services.is_valid_uuid(customer_id):
        raise HTTPException(
            status_code=400, detail="Invalid customer_id format"
        )
    if product_id and not services.is_valid_uuid(product_id):
        raise HTTPException(
            status_code=400, detail="Invalid product_id format"
        )

    transactions, total = services.get_transactions(
        db, page, size, customer_id, product_id
    )

    return TransactionListResponse(
        data=transactions,
        total=total,
        page=page,
        size=size,
        pages=math.ceil(total / size),
    )


@app.get("/transactions/{transaction_id}")
async def get_transaction(transaction_id: str):
    return {
        "message": "Get transaction by ID endpoint - dummy implementation",
        "transaction_id": transaction_id,
        "data": None,
    }


@app.get("/reports/customer-summary/{customer_id}")
async def get_customer_summary(customer_id: str):
    return {
        "message": "Customer summary endpoint - dummy implementation",
        "customer_id": customer_id,
        "summary": {
            "total_transactions": 0,
            "total_amount_pln": 0.0,
            "currencies_used": [],
            "date_range": None,
        },
    }


@app.get("/reports/product-summary/{product_id}")
async def get_product_summary(product_id: str):
    return {
        "message": "Product summary endpoint - dummy implementation",
        "product_id": product_id,
        "summary": {
            "total_transactions": 0,
            "total_amount_pln": 0.0,
            "unique_customers": 0,
            "currencies_used": [],
            "date_range": None,
        },
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.app_host,
        port=settings.app_port,
        reload=settings.app_reload,
    )
