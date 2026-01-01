from fastapi import FastAPI
from app.api import router as api_router

app = FastAPI(
    title="Bank-Grade AI Microservice",
    description="A template for deploying AI models with bank-grade security and structure.",
    version="1.0.0"
)

app.include_router(api_router, prefix="/api/v1")

@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "ok"}
