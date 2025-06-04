from fastapi import FastAPI

from app.config import settings
from app.database import init_db
from app.routes import router

app = FastAPI(debug=settings.debug)


@app.on_event("startup")
async def startup_event():
    init_db()


app.include_router(router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.app_host,
        port=settings.app_port,
        reload=settings.app_reload,
    )
