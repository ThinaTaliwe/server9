"""API routes for shipments and related entities."""

from fastapi import APIRouter, Depends, HTTPException, status, Path, Query, Body
from sqlalchemy.orm import Session

from .models import Shipment
from .schemas import (
    ShipmentCreate,
    ShipmentUpdate,
    ShipmentRead,
    TagRead,
    FollowerRead,
)
from .service import (
    list_shipments,
    get_shipment,
    create_shipment,
    update_shipment,
    delete_shipment,
    add_tags_to_shipment,
    remove_tag_from_shipment,
    add_followers_to_shipment,
    remove_follower_from_shipment,
    get_route,
)
from ..core.deps import get_db, get_current_user, require_scopes

router = APIRouter()


@router.get("/shipments", response_model=list[ShipmentRead])
def read_shipments(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    token = Depends(require_scopes(["api"])),
):
    """Retrieve a paginated list of shipments."""
    shipments = list_shipments(db, skip=skip, limit=limit)
    return shipments


@router.post("/shipments", response_model=ShipmentRead, status_code=status.HTTP_201_CREATED)
def create_shipment_endpoint(
    shipment_in: ShipmentCreate = Body(...),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
    token = Depends(require_scopes(["api"])),
):
    """Create a new shipment with tags and followers."""
    shipment = create_shipment(db, shipment_in, created_by=current_user)
    return shipment


def get_existing_shipment(
    shipment_id: int = Path(..., ge=1),
    db: Session = Depends(get_db),
) -> Shipment:
    shipment = get_shipment(db, shipment_id)
    if not shipment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Shipment not found")
    return shipment


@router.get("/shipments/{shipment_id}", response_model=ShipmentRead)
def read_shipment(
    shipment: Shipment = Depends(get_existing_shipment),
    token = Depends(require_scopes(["api"])),
):
    """Retrieve a single shipment by ID."""
    return shipment


@router.patch("/shipments/{shipment_id}", response_model=ShipmentRead)
def update_shipment_endpoint(
    shipment_update: ShipmentUpdate = Body(...),
    shipment: Shipment = Depends(get_existing_shipment),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
    token = Depends(require_scopes(["api"])),
):
    """Update a shipment's reference or other editable fields."""
    # Authorization: only creator or admin can update
    if current_user and not (current_user.is_superuser or shipment.created_by_id == current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this shipment")
    updated = update_shipment(db, shipment, shipment_update)
    return updated


@router.delete("/shipments/{shipment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_shipment_endpoint(
    shipment: Shipment = Depends(get_existing_shipment),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
    token = Depends(require_scopes(["api"])),
):
    """Delete a shipment."""
    if current_user and not (current_user.is_superuser or shipment.created_by_id == current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this shipment")
    delete_shipment(db, shipment)
    return None


@router.post("/shipments/{shipment_id}/tags", response_model=ShipmentRead)
def add_tags_endpoint(
    tags: list[str] = Body(...),
    shipment: Shipment = Depends(get_existing_shipment),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
    token = Depends(require_scopes(["api"])),
):
    """Add tags to a shipment."""
    if current_user and not (current_user.is_superuser or shipment.created_by_id == current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to modify this shipment")
    return add_tags_to_shipment(db, shipment, tags)


@router.delete("/shipments/{shipment_id}/tags/{tag_id}", response_model=ShipmentRead)
def remove_tag_endpoint(
    shipment: Shipment = Depends(get_existing_shipment),
    tag_id: int = Path(..., ge=1),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
    token = Depends(require_scopes(["api"])),
):
    """Remove a tag from a shipment."""
    if current_user and not (current_user.is_superuser or shipment.created_by_id == current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to modify this shipment")
    return remove_tag_from_shipment(db, shipment, tag_id)


@router.post("/shipments/{shipment_id}/followers", response_model=ShipmentRead)
def add_followers_endpoint(
    emails: list[str] = Body(..., embed=True),
    shipment: Shipment = Depends(get_existing_shipment),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
    token = Depends(require_scopes(["api"])),
):
    """Add followers to a shipment."""
    if current_user and not (current_user.is_superuser or shipment.created_by_id == current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to modify this shipment")
    return add_followers_to_shipment(db, shipment, emails, current_user)


@router.delete("/shipments/{shipment_id}/followers/{follower_id}", response_model=ShipmentRead)
def remove_follower_endpoint(
    shipment: Shipment = Depends(get_existing_shipment),
    follower_id: int = Path(..., ge=1),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
    token = Depends(require_scopes(["api"])),
):
    """Remove a follower from a shipment."""
    if current_user and not (current_user.is_superuser or shipment.created_by_id == current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to modify this shipment")
    return remove_follower_from_shipment(db, shipment, follower_id)


@router.get("/shipments/{shipment_id}/route")
def get_route_endpoint(
    shipment: Shipment = Depends(get_existing_shipment),
    refresh: bool = Query(False, description="Set to true to refresh route from provider"),
    db: Session = Depends(get_db),
    token = Depends(require_scopes(["api"])),
):
    """Retrieve the GeoJSON route for a shipment.

    If ``refresh`` is true, the route is re‑fetched from SHIPSGO and cached.
    Otherwise, the most recent cached route is returned if available.  If no
    route is found, a 404 error is raised.
    """
    geojson = get_route(db, shipment, refresh=refresh)
    if geojson is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Route not available")
    return geojson