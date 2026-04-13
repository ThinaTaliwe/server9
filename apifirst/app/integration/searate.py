"""Client for interacting with the Searate Tracking API.

This module wraps HTTP requests to Searate’s tracking endpoints.  All
functions return JSON‑decoded responses (as Python dicts).  Any network
errors are logged and result in an empty dictionary being returned.

The Searate API requires an API key on every request.  The key is passed
via query parameter ``api_key``.  See the Insomnia export for examples.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, Optional

import httpx

from ..core.config import settings

logger = logging.getLogger(__name__)


def _base_params() -> Dict[str, str]:
    """Return the default query parameters containing the API key."""
    return {"api_key": settings.searate_api_key}


def _get(endpoint: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """Internal helper to perform a GET request to the Searate API.

    Merges the API key with provided parameters and returns a JSON object.  If
    the request fails, returns an empty dictionary.
    """
    url = f"{settings.searate_base_url}{endpoint}"
    query = _base_params().copy()
    query.update({k: v for k, v in params.items() if v is not None})
    try:
        with httpx.Client(timeout=15) as client:
            response = client.get(url, params=query)
            response.raise_for_status()
            return response.json() or {}
    except Exception as exc:
        logger.error("Searate GET %s failed: %s", endpoint, exc)
        return {}


def track(
    number: str,
    type: str = "CT",
    route: str = "true",
    ais: str = "true",
    force_update: str = "false",
    sealine: str = "auto",
) -> Dict[str, Any]:
    """Track a container or bill of lading number.

    Parameters correspond to the Searate API:
    * ``number`` – container or BL number
    * ``type`` – either ``CT`` for container or ``BL`` for bill of lading
    * ``route`` – ``"true"`` to include route data
    * ``ais`` – ``"true"`` to include AIS data
    * ``force_update`` – ``"true"`` to force a refresh from the carrier
    * ``sealine`` – optional carrier code to narrow search
    """
    params = {
        "number": number,
        "type": type,
        "route": route,
        "ais": ais,
        "force_update": force_update,
        "sealine": sealine,
    }
    return _get("/tracking", params)


def route_info(number: str, type: str = "CT", sealine: str = "auto") -> Dict[str, Any]:
    """Retrieve route information for a container or BL number."""
    params = {
        "number": number,
        "type": type,
        "sealine": sealine,
    }
    return _get("/route", params)


def history(number: str, type: str = "CT", sealine: str = "auto") -> Dict[str, Any]:
    """Retrieve historical tracking events for a container or BL number."""
    params = {
        "number": number,
        "type": type,
        "sealine": sealine,
    }
    return _get("/history", params)


def history_by_id(id: str, number: str, type: str = "CT", sealine: str = "auto") -> Dict[str, Any]:
    """Retrieve historical details for a specific event ID."""
    params = {
        "id": id,
        "number": number,
        "type": type,
        "sealine": sealine,
    }
    return _get("/history", params)


def get_carriers() -> Dict[str, Any]:
    """Return a list of carrier codes and names from Searate.

    The response structure is provider dependent.  If a list of carriers is
    returned, it is passed through unchanged; otherwise the raw JSON is
    returned.
    """
    data = _get("/info/sealines", {})
    # Some Searate responses include a ``data`` field with the list of sealines
    carriers = data.get("data") or data.get("sealines") or data
    return carriers if isinstance(carriers, (list, dict)) else {}