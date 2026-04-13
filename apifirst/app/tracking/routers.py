"""API routes for tracking."""

from typing import Any, Dict

from fastapi import APIRouter, Depends, Query

from .service import track, route_info, historical, get_carriers
from ..core.deps import require_scopes

router = APIRouter()


@router.get("/tracking")
def track_endpoint(
    number: str = Query(..., description="Container or BL number"),
    type: str = Query("CT", regex="^(CT|BL)$", description="Number type: CT (container) or BL (bill of lading)"),
    route: str = Query("true", description="Whether to include route data"),
    ais: str = Query("true", description="Whether to include AIS data"),
    force_update: str = Query("false", description="Force update from provider"),
    sealine: str = Query("auto", description="Carrier code for more accurate results"),
    token = Depends(require_scopes(["api"])),
) -> Dict[str, Any]:
    """Track a container or bill of lading via Searate."""
    return track(number, type, route, ais, force_update, sealine)


@router.get("/tracking/history")
def history_endpoint(
    number: str = Query(..., description="Container or BL number"),
    type: str = Query("CT", regex="^(CT|BL)$"),
    id: str | None = Query(None, description="Event ID for detailed lookup"),
    sealine: str = Query("auto"),
    token = Depends(require_scopes(["api"])),
) -> Dict[str, Any]:
    """Retrieve historical tracking data for a container or by event ID."""
    return historical(number, type=type, sealine=sealine, id=id)


@router.get("/tracking/carriers")
def carriers_endpoint(
    token = Depends(require_scopes(["api"])),
) -> Dict[str, Any]:
    """List carriers (shipping lines) available in Searate."""
    return get_carriers()