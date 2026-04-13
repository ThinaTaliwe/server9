"""Business logic for shipments.

Provides CRUD operations on shipments and associated tags/followers.  External
integration with SHIPSGO is delegated to the integration layer.
"""

from typing import List, Optional

from sqlalchemy.orm import Session

from .models import Shipment, Tag, Follower, ShipmentTag
from .schemas import ShipmentCreate, ShipmentUpdate
from ..carriers.models import Carrier
from ..auth.models import User
from ..integration import shipsgo as shipsgo_client
from .models import Route


def list_shipments(db: Session, skip: int = 0, limit: int = 100) -> List[Shipment]:
    """Return a paginated list of shipments."""
    return db.query(Shipment).offset(skip).limit(limit).all()


def get_shipment(db: Session, shipment_id: int) -> Optional[Shipment]:
    """Return a shipment by ID or None if not found."""
    return db.query(Shipment).filter(Shipment.id == shipment_id).first()


def create_shipment(
    db: Session,
    data: ShipmentCreate,
    created_by: Optional[User] = None,
) -> Shipment:
    """Create a new shipment with tags and followers.

    This function creates the local shipment record and its associated tags and
    followers.  It then calls the external SHIPSGO API to create the shipment
    remotely and stores the returned external ID.
    """
    carrier: Carrier | None = None
    if data.carrier_code:
        carrier = db.query(Carrier).filter(Carrier.code == data.carrier_code).first()
    shipment = Shipment(
        reference=data.reference,
        container_number=data.container_number,
        booking_number=data.booking_number,
        carrier=carrier,
        created_by=created_by,
    )
    # Attach tags
    for tag_name in data.tags or []:
        tag = db.query(Tag).filter(Tag.name == tag_name).first()
        if not tag:
            tag = Tag(name=tag_name)
            db.add(tag)
            db.flush()
        shipment.tags.append(tag)
    # Attach followers
    for email in data.followers or []:
        follower = Follower(email=email, added_by=created_by)
        shipment.followers.append(follower)
    db.add(shipment)
    db.commit()
    db.refresh(shipment)
    # Call external API asynchronously or synchronously (placeholder)
    try:
        remote_id = shipsgo_client.create_shipment(shipment)
        shipment.external_shipment_id = remote_id
        db.commit()
    except Exception:
        # Ignore remote errors for MVP
        pass
    return shipment


def update_shipment(
    db: Session,
    shipment: Shipment,
    data: ShipmentUpdate,
) -> Shipment:
    """Update mutable fields of a shipment."""
    if data.reference is not None:
        shipment.reference = data.reference
    # Additional fields can be updated here
    db.commit()
    db.refresh(shipment)
    # Update remote shipment (placeholder)
    try:
        shipsgo_client.update_shipment(shipment)
    except Exception:
        pass
    return shipment


def delete_shipment(db: Session, shipment: Shipment) -> None:
    """Delete a shipment and its related objects."""
    db.delete(shipment)
    db.commit()
    # Delete remote shipment (placeholder)
    try:
        shipsgo_client.delete_shipment(shipment)
    except Exception:
        pass


def add_tags_to_shipment(db: Session, shipment: Shipment, tags: List[str]) -> Shipment:
    """Add tags to a shipment."""
    for tag_name in tags:
        tag = db.query(Tag).filter(Tag.name == tag_name).first()
        if not tag:
            tag = Tag(name=tag_name)
            db.add(tag)
            db.flush()
        if tag not in shipment.tags:
            shipment.tags.append(tag)
    db.commit()
    db.refresh(shipment)
    # Call external API to add tag (placeholder)
    for tag_name in tags:
        try:
            shipsgo_client.add_tag(shipment, tag_name)
        except Exception:
            pass
    return shipment


def remove_tag_from_shipment(db: Session, shipment: Shipment, tag_id: int) -> Shipment:
    """Remove a tag association from a shipment."""
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if not tag:
        return shipment
    if tag in shipment.tags:
        shipment.tags.remove(tag)
        db.commit()
        db.refresh(shipment)
        # Call external API to remove tag (placeholder)
        try:
            shipsgo_client.remove_tag(shipment, tag_id)
        except Exception:
            pass
    return shipment


def add_followers_to_shipment(db: Session, shipment: Shipment, emails: List[str], added_by: Optional[User]) -> Shipment:
    """Add followers to a shipment."""
    for email in emails:
        # Avoid duplicates
        exists = any(f.email == email for f in shipment.followers)
        if exists:
            continue
        follower = Follower(email=email, added_by=added_by)
        shipment.followers.append(follower)
    db.commit()
    db.refresh(shipment)
    # Call external API (placeholder)
    for email in emails:
        try:
            shipsgo_client.add_follower(shipment, email)
        except Exception:
            pass
    return shipment


def remove_follower_from_shipment(db: Session, shipment: Shipment, follower_id: int) -> Shipment:
    """Remove a follower from a shipment."""
    follower = db.query(Follower).filter(Follower.id == follower_id, Follower.shipment_id == shipment.id).first()
    if not follower:
        return shipment
    db.delete(follower)
    db.commit()
    db.refresh(shipment)
    # Call external API (placeholder)
    try:
        shipsgo_client.remove_follower(shipment, follower_id)
    except Exception:
        pass
    return shipment


def get_route(
    db: Session,
    shipment: Shipment,
    refresh: bool = False,
) -> Optional[dict]:
    """Retrieve the latest route for a shipment, optionally refreshing from SHIPSGO.

    If ``refresh`` is False and a local route exists in the ``routes`` table, that
    route is returned without calling the external API.  If ``refresh`` is True
    or no local route is found, the SHIPSGO API is queried.  When a new route
    is fetched, it is stored in the database for future use.

    Returns a GeoJSON dictionary or ``None`` if no route is available.
    """
    # Attempt to return the most recently cached route unless a refresh is requested
    if not refresh:
        latest = (
            db.query(Route)
            .filter(Route.shipment_id == shipment.id)
            .order_by(Route.received_at.desc())
            .first()
        )
        if latest and latest.geojson:
            return latest.geojson
    # Call external API
    remote = shipsgo_client.get_route(shipment, refresh=refresh)
    if remote:
        # Store the new route in the database
        new_route = Route(shipment=shipment, geojson=remote)
        db.add(new_route)
        db.commit()
        return remote
    return None