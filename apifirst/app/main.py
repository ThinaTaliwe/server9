"""Application factory and router inclusion.

This module creates the FastAPI instance, configures CORS, session and security
middleware, and includes routers from the various domain packages.  It reads
configuration from environment variables via the settings object.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .core.config import settings
from .core.database import engine
from .auth.models import Base
from .auth.routers import router as auth_router
from .carriers.routers import router as carriers_router
from .shipments.routers import router as shipments_router
from .tracking.routers import router as tracking_router


def create_app() -> FastAPI:
    """Initialize the FastAPI application and include all routers."""
    app = FastAPI(title="Logistics API", version="0.1.0", openapi_url="/openapi.json")

    # CORS configuration – allow all origins by default; adjust for production
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_allow_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routers with versioned prefixes
    app.include_router(auth_router, prefix="/v1")
    app.include_router(carriers_router, prefix="/v1", tags=["carriers"])
    app.include_router(shipments_router, prefix="/v1", tags=["shipments"])
    app.include_router(tracking_router, prefix="/v1", tags=["tracking"])

    # Create database tables on startup if they don't already exist.  In a production
    # environment you should use Alembic migrations instead of automatic table
    # creation, but this simplifies initial deployment.  The Base object is
    # imported from the authentication models, and metadata includes all
    # models across the application because they share the same declarative base.
    Base.metadata.create_all(bind=engine)

    @app.get("/", include_in_schema=False)
    async def root():
        return {"message": "Logistics API is running"}

    return app


# Instantiate the app for ASGI servers (e.g., uvicorn)
app = create_app()