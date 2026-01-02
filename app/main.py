import logging
import uuid
import sys
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from pythonjsonlogger import jsonlogger
from starlette.middleware.base import BaseHTTPMiddleware
from app.api import router as api_router

# --- Setup Structured Logging ---
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logHandler = logging.StreamHandler(sys.stdout)
# Use standard LogRecord attributes (asctime, levelname) and rename them to match requirements
formatter = jsonlogger.JsonFormatter(
    '%(asctime)s %(levelname)s %(name)s %(message)s %(correlation_id)s',
    rename_fields={"asctime": "timestamp", "levelname": "level"}
)
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)

# --- Middleware ---
class CorrelationIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        correlation_id = request.headers.get("X-Correlation-ID", str(uuid.uuid4()))
        request.state.correlation_id = correlation_id
        
        # Inject correlation_id into logger for this context (simplified approach)
        # In a real async app, use contextvars. For this template, we'll manually log it.
        
        response = await call_next(request)
        response.headers["X-Correlation-ID"] = correlation_id
        return response

app = FastAPI(
    title="Bank-Grade AI Microservice",
    description="A template for deploying AI models with bank-grade security and structure.",
    version="1.1.0"
)

app.add_middleware(CorrelationIdMiddleware)

# --- Exception Handlers ---
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    correlation_id = getattr(request.state, "correlation_id", "unknown")
    logger.error("Unhandled exception", extra={
        "correlation_id": correlation_id,
        "error": str(exc)
    })
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": "An unexpected error occurred. Please contact support.",
            "correlation_id": correlation_id
        }
    )

app.include_router(api_router, prefix="/api/v1")

@app.get("/health", status_code=200, tags=["Health"])
@app.head("/health", status_code=200, include_in_schema=False)
async def health_check(request: Request):
    correlation_id = getattr(request.state, "correlation_id", "unknown")
    logger.info("Health check request", extra={"correlation_id": correlation_id})
    return {"status": "ok"}