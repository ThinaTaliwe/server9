"""Tracking service calling external Searate API."""

from typing import Any, Dict

from ..integration import searate as searate_client


def track(number: str, type: str = "CT", route: str = "true", ais: str = "true", force_update: str = "false", sealine: str = "auto") -> Dict[str, Any]:
    """Fetch tracking information for a container or bill of lading.

    Parameters correspond to the Searate API query string.
    """
    return searate_client.track(number=number, type=type, route=route, ais=ais, force_update=force_update, sealine=sealine)


def route_info(number: str, sealine: str = "auto") -> Dict[str, Any]:
    """Retrieve route information for a container."""
    return searate_client.route_info(number=number, sealine=sealine)


def historical(number: str, type: str = "CT", sealine: str = "auto", id: str | None = None) -> Dict[str, Any]:
    """Retrieve historical tracking data for a container or by event ID."""
    if id:
        return searate_client.history_by_id(id=id, number=number, type=type, sealine=sealine)
    return searate_client.history(number=number, type=type, sealine=sealine)


def get_carriers() -> Dict[str, Any]:
    """Retrieve carrier codes and names from Searate."""
    return searate_client.get_carriers()