"""Main FastAPI application entry point."""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import engine
from app.api.v1.router import api_router
from app.ias.api import router as ias_router
from app.eps.api import router as eps_router
from app.awps.api import router as awps_router
from app.crs.api import router as crs_router
from app.nas.api import router as nas_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup - tables are created via Alembic migrations
    yield
    # Shutdown
    await engine.dispose()


app = FastAPI(
    title=settings.APP_NAME,
    version="0.1.0",
    description="Bitcoin Estate Planning Platform - MVP",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(api_router, prefix="/api/v1", tags=["v1"])
app.include_router(ias_router, prefix="/api", tags=["v2"])  # v2 IAS endpoints at /api/v2/ias
app.include_router(eps_router, prefix="/api", tags=["v2"])  # v2 EPS endpoints at /api/v2/eps
app.include_router(awps_router, prefix="/api", tags=["v2"])  # v2 AWPS endpoints at /api/v2/awps
app.include_router(crs_router, prefix="/api", tags=["v2"])  # v2 CRS endpoints at /api/v2/crs
app.include_router(nas_router, prefix="/api", tags=["v2"])  # v2 NAS endpoints at /api/v2/nas


@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Bitcoin Estate Planning Platform API", "version": "0.1.0"}


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}

