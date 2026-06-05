"""
Main FastAPI application entry point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from contextlib import asynccontextmanager
import logging
from core.config import settings
from core.database import engine, Base
from api.routes import users, analytics, leads, customers, businesses
from core.logging_config import setup_logging

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifecycle"""
    # Startup
    logger.info("Starting DNX Systems application...")
    Base.metadata.create_all(bind=engine)
    yield
    # Shutdown
    logger.info("Shutting down DNX Systems application...")


# Create FastAPI app
app = FastAPI(
    title="DNX Systems API",
    description="Growth AI Pro - DNX Systems Management API",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add trusted host middleware
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=settings.ALLOWED_HOSTS
)


# Include routers
app.include_router(
    users.router,
    prefix="/api/v1/users",
    tags=["users"]
)
app.include_router(
    analytics.router,
    prefix="/api/v1/analytics",
    tags=["analytics"]
)
app.include_router(
    leads.router,
    prefix="/api/v1/leads",
    tags=["leads"]
)
app.include_router(
    customers.router,
    prefix="/api/v1/customers",
    tags=["customers"]
)
app.include_router(
    businesses.router,
    prefix="/api/v1/businesses",
    tags=["businesses"]
)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to DNX Systems API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "DNX Systems API"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL
    )
