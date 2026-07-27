import time
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from src.api.routers import health
from src.api.routers import companies
from src.api.routers import screener

app = FastAPI(
    title="N100 Financial Intelligence API",
    version="1.0.0",
    description="REST API for N100 Financial Intelligence Platform"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request Logging Middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.time()

    response = await call_next(request)

    duration = (time.time() - start) * 1000

    print(
        f"{request.method} {request.url.path} "
        f"{duration:.2f} ms"
    )

    return response

# Routers
app.include_router(
    health.router,
    prefix="/api/v1",
    tags=["Health"]
)
app.include_router(
    companies.router,
    prefix="/api/v1",
    tags=["Companies"]
)
app.include_router(
    screener.router,
    prefix="/api/v1",
    tags=["Screener"]
)