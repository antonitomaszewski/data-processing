from typing import Optional

from fastapi import FastAPI, File, UploadFile

from app.config import project_metadata, settings
from app.database import init_db

app = FastAPI(
    title=project_metadata["title"],
    description=project_metadata["description"],
    version=project_metadata["version"],
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


@app.post("/transactions/upload")
async def upload_transactions(file: UploadFile = File(...)):
    return {
        "message": "CSV upload endpoint - dummy implementation",
        "filename": file.filename,
        "content_type": file.content_type,
    }


@app.get("/transactions")
async def get_transactions(
    page: int = 1,
    size: int = 50,
    customer_id: Optional[str] = None,
    product_id: Optional[str] = None,
    currency: Optional[str] = None,
):
    return {
        "message": "Get transactions endpoint - dummy implementation",
        "filters": {
            "page": page,
            "size": size,
            "customer_id": customer_id,
            "product_id": product_id,
            "currency": currency,
        },
        "data": [],
    }


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
