from fastapi import FastAPI

from app.config import project_metadata, settings

app = FastAPI(
    title=project_metadata["title"],
    description=project_metadata["description"],
    version=project_metadata["version"],
    debug=settings.debug,
)


@app.get("/")
async def root():
    return {
        "message": "Data Processing API",
        "environment": settings.environment,
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.app_host,
        port=settings.app_port,
        reload=settings.app_reload,
    )
