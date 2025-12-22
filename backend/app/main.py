from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.content import router as content_router
from app.api.search import router as search_router
from app.api.ai_assistant import router as ai_assistant_router
from app.api.translation import router as translation_router
from app.api.health import router as health_router
from app.config import settings
from app.middleware.error_handlers import (
    http_exception_handler,
    validation_exception_handler,
    general_exception_handler,
    init_rate_limiting
)
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
import traceback
from pydantic import BaseModel
from datetime import datetime
import logging

# Configure comprehensive logging
from app.utils import logging_config
logger = logging_config.get_logger('main')

from contextlib import asynccontextmanager
import asyncio

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager for startup and shutdown events"""
    # Startup
    logger.info("AI-Native Book API starting up...")

    # Initialize services
    # Any initialization code would go here

    yield  # Application runs here

    # Shutdown
    logger.info("AI-Native Book API shutting down...")

# Create FastAPI app with lifespan
app = FastAPI(
    title="AI-Native Book API",
    description="API for the AI-Native Book with Docusaurus",
    version="0.1.0",
    lifespan=lifespan
)

from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from starlette.middleware.security import SecurityMiddleware as StarletteSecurityMiddleware

# Add security headers middleware
app.add_middleware(
    StarletteSecurityMiddleware,
    # Security headers configuration
    force_https=False,  # Set to True in production
    sts_include_subdomains=True,
    sts_max_age=31536000,  # 1 year
    sts_preload=True,
    permitted_cross_origin_policies="same-origin",
)

# Add CORS middleware - Use environment variable for allowed origins
import os
allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:3001").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add Trusted Host Middleware
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1,0.0.0.0").split(",")
)

# Add GZip compression
app.add_middleware(
    GZipMiddleware,
    minimum_size=1000,
)

# Initialize rate limiting
init_rate_limiting(app)

# Include API routers
app.include_router(content_router, prefix="/api/content", tags=["content"])
app.include_router(search_router, prefix="/api/search", tags=["search"])
app.include_router(ai_assistant_router, prefix="/api/ai-assistant", tags=["ai-assistant"])
app.include_router(translation_router, prefix="/api/translation", tags=["translation"])
app.include_router(health_router, prefix="/api/health", tags=["health"])

# Add exception handlers
app.add_exception_handler(Exception, general_exception_handler)

class HealthCheckResponse(BaseModel):
    status: str
    services: dict
    timestamp: datetime

from app.utils.metrics import get_health_metrics

# Global service status tracker
class ServiceStatus:
    def __init__(self):
        self.database_healthy = True
        self.vector_db_healthy = True
        self.ai_service_healthy = True
        self.last_check = datetime.now()

    def update_status(self, db_healthy: bool, vector_db_healthy: bool, ai_healthy: bool):
        self.database_healthy = db_healthy
        self.vector_db_healthy = vector_db_healthy
        self.ai_service_healthy = ai_healthy
        self.last_check = datetime.now()

service_status = ServiceStatus()

async def check_database_health():
    """Check database connectivity"""
    try:
        # In a real implementation, this would test the actual database connection
        # For now, we'll simulate with a try-catch
        # db = get_db()  # This would be your actual database connection
        # await db.execute("SELECT 1")  # Test query
        return True
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        return False

async def check_vector_db_health():
    """Check vector database connectivity"""
    try:
        # In a real implementation, this would test the actual vector database connection
        # For now, we'll simulate
        return True
    except Exception as e:
        logger.error(f"Vector database health check failed: {e}")
        return False

async def check_ai_service_health():
    """Check AI service connectivity"""
    try:
        # In a real implementation, this would test the actual AI service connection
        # For now, we'll simulate
        return True
    except Exception as e:
        logger.error(f"AI service health check failed: {e}")
        return False

async def background_health_monitor():
    """Background task to continuously monitor service health"""
    while True:
        try:
            # Check all services
            db_healthy = await check_database_health()
            vector_db_healthy = await check_vector_db_health()
            ai_healthy = await check_ai_service_health()

            # Update global status
            service_status.update_status(db_healthy, vector_db_healthy, ai_healthy)

            # Log status changes
            if not db_healthy:
                logger.warning("Database service is unhealthy")
            if not vector_db_healthy:
                logger.warning("Vector database service is unhealthy")
            if not ai_healthy:
                logger.warning("AI service is unhealthy")

        except Exception as e:
            logger.error(f"Error in health monitoring: {e}")

        # Wait 30 seconds before next check
        await asyncio.sleep(30)

# Start background health monitoring
@app.on_event("startup")
async def startup_event():
    asyncio.create_task(background_health_monitor())

