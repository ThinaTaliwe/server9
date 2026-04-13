"""Top-level package for the logistics API project.

This package exposes the FastAPI application via :mod:`app.main` and organizes
the various domain modules (auth, carriers, shipments, tracking and integration).
"""

from .main import app  # noqa: F401