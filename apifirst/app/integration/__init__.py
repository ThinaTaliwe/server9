"""Integration clients for external APIs.

This package provides functions to interact with the SHIPSGO and Searate APIs.
Each module wraps the HTTP calls to third‑party services behind simple
function interfaces so that the rest of the application does not need to know
about authentication headers or URL construction.  If the external APIs
change, you can update these modules without modifying business logic.
"""

from . import shipsgo  # noqa: F401
from . import searate  # noqa: F401

__all__ = ["shipsgo", "searate"]