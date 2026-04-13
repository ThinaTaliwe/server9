"""Client for interacting with the SHIPSGO Ocean API.

The functions in this module wrap HTTP requests to SHIPSGO.  They accept
domain objects (e.g., Shipment) and return simple Python structures so that
the calling code does not need to construct URLs or headers manually.

All functions catch network exceptions and log errors instead of raising
them, returning ``None`` when an operation fails.  In a production
environment you may want to propagate exceptions or implement retry logic.
"""

from __future__ import annotations

import logging
from typing import Dict, List, Optional

import httpx

from ..core.config import settings
from ..shipments.models import Shipment

logger = logging.getLogger(__name__)


def _headers() -> Dict[str, str]:
    """Return the authentication headers for SHIPSGO requests."""
    return {
        "X-Shipsgo-User-Token": settings.shipsgo_token,
        "Content-Type": "application/json",
    }


def get_carriers() -> Dict[str, str]:
    """Retrieve a mapping of carrier codes to names from SHIPSGO.

    Returns an empty dictionary if the request fails.
    """
    url = f"{settings.shipsgo_base_url}/ocean/carriers"
    try:
        with httpx.Client(timeout=10) as client:
            response = client.get(url, headers=_headers())
            response.raise_for_status()
            data = response.json()
            # The API returns a list of carriers.  We attempt to extract code/name pairs.
            carriers: Dict[str, str] = {}
            items = data.get("data") or data.get("carriers") or data
            if isinstance(items, list):
                for item in items:
                    code = item.get("code") or item.get("carrier") or item.get("carrier_code")
                    name = item.get("name") or item.get("company_name")
                    if code and name:
                        carriers[str(code)] = str(name)
            return carriers
    except Exception as exc:
        logger.error("Failed to fetch carriers from SHIPSGO: %s", exc)
        return {}


def create_shipment(shipment: Shipment) -> Optional[str]:
    """Create a shipment in SHIPSGO and return its external ID.

    The request body is constructed from the local ``Shipment`` object.  If
    the remote API responds with an ID, it is returned as a string.  If the
    request fails or no ID is provided, ``None`` is returned.
    """
    url = f"{settings.shipsgo_base_url}/ocean/shipments"
    body = {
        "reference": shipment.reference,
        "container_number": shipment.container_number,
        "booking_number": shipment.booking_number,
        "carrier": shipment.carrier.code if shipment.carrier else None,
        "followers": [f.email for f in shipment.followers],
        "tags": [t.name for t in shipment.tags],
    }
    # Remove keys with None values to avoid API validation errors
    body = {k: v for k, v in body.items() if v}
    try:
        with httpx.Client(timeout=10) as client:
            response = client.post(url, headers=_headers(), json=body)
            response.raise_for_status()
            data = response.json() or {}
            # Extract remote ID from nested structures if present
            remote_id = (
                data.get("data", {}).get("id")
                or data.get("id")
                or data.get("shipment_id")
            )
            return str(remote_id) if remote_id else None
    except Exception as exc:
        logger.error("Failed to create shipment in SHIPSGO: %s", exc)
        return None


def update_shipment(shipment: Shipment) -> None:
    """Update a shipment in SHIPSGO.

    Only mutable fields such as the reference are sent.  If the shipment has no
    external ID, the function returns immediately.  Errors are logged but
    otherwise ignored.
    """
    external_id = shipment.external_shipment_id
    if not external_id:
        return
    url = f"{settings.shipsgo_base_url}/ocean/shipments/{external_id}"
    body = {"reference": shipment.reference}
    try:
        with httpx.Client(timeout=10) as client:
            response = client.patch(url, headers=_headers(), json=body)
            # Do not raise for status to allow 204/200 responses
            _ = response.status_code
    except Exception as exc:
        logger.error("Failed to update shipment %s in SHIPSGO: %s", external_id, exc)


def delete_shipment(shipment: Shipment) -> None:
    """Delete a shipment from SHIPSGO.

    If the shipment has no external ID, this is a no‑op.  Errors are logged and
    suppressed.
    """
    external_id = shipment.external_shipment_id
    if not external_id:
        return
    url = f"{settings.shipsgo_base_url}/ocean/shipments/{external_id}"
    try:
        with httpx.Client(timeout=10) as client:
            response = client.delete(url, headers=_headers())
            _ = response.status_code
    except Exception as exc:
        logger.error("Failed to delete shipment %s in SHIPSGO: %s", external_id, exc)


def add_follower(shipment: Shipment, email: str) -> None:
    """Add a follower to a shipment in SHIPSGO."""
    external_id = shipment.external_shipment_id
    if not external_id:
        return
    url = f"{settings.shipsgo_base_url}/ocean/shipments/{external_id}/followers"
    body = {"email": email}
    try:
        with httpx.Client(timeout=10) as client:
            client.post(url, headers=_headers(), json=body)
    except Exception as exc:
        logger.error("Failed to add follower to shipment %s in SHIPSGO: %s", external_id, exc)


def remove_follower(shipment: Shipment, follower_id: int) -> None:
    """Remove a follower from a shipment in SHIPSGO."""
    external_id = shipment.external_shipment_id
    if not external_id:
        return
    url = f"{settings.shipsgo_base_url}/ocean/shipments/{external_id}/followers/{follower_id}"
    try:
        with httpx.Client(timeout=10) as client:
            client.delete(url, headers=_headers())
    except Exception as exc:
        logger.error("Failed to remove follower from shipment %s in SHIPSGO: %s", external_id, exc)


def add_tag(shipment: Shipment, tag_name: str) -> None:
    """Add a tag to a shipment in SHIPSGO."""
    external_id = shipment.external_shipment_id
    if not external_id:
        return
    url = f"{settings.shipsgo_base_url}/ocean/shipments/{external_id}/tags"
    body = {"name": tag_name}
    try:
        with httpx.Client(timeout=10) as client:
            client.post(url, headers=_headers(), json=body)
    except Exception as exc:
        logger.error("Failed to add tag to shipment %s in SHIPSGO: %s", external_id, exc)


def remove_tag(shipment: Shipment, tag_id: int) -> None:
    """Remove a tag from a shipment in SHIPSGO."""
    external_id = shipment.external_shipment_id
    if not external_id:
        return
    url = f"{settings.shipsgo_base_url}/ocean/shipments/{external_id}/tags/{tag_id}"
    try:
        with httpx.Client(timeout=10) as client:
            client.delete(url, headers=_headers())
    except Exception as exc:
        logger.error("Failed to remove tag from shipment %s in SHIPSGO: %s", external_id, exc)


def get_route(shipment: Shipment, refresh: bool = False) -> Optional[dict]:
    """Retrieve GeoJSON route data for a shipment from SHIPSGO.

    If ``refresh`` is True, the request will ask SHIPSGO to regenerate the route.
    Returns ``None`` if the request fails or no route is available.
    """
    external_id = shipment.external_shipment_id
    if not external_id:
        return None
    url = f"{settings.shipsgo_base_url}/ocean/shipments/{external_id}/geojson"
    params = {"refresh": "true"} if refresh else None
    try:
        with httpx.Client(timeout=15) as client:
            response = client.get(url, headers=_headers(), params=params)
            if response.status_code == 404:
                return None
            response.raise_for_status()
            return response.json()
    except Exception as exc:
        logger.error("Failed to fetch route for shipment %s in SHIPSGO: %s", external_id, exc)
        return None