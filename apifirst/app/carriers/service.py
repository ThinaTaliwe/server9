"""Business logic for carriers.

This module provides functions to list carriers and synchronize them from
external providers.  The actual HTTP calls are delegated to the integration layer.
"""

from sqlalchemy.orm import Session

from .models import Carrier
from . import schemas

from ..integration import shipsgo as shipsgo_client
from ..integration import searate as searate_client


def list_carriers(db: Session) -> list[Carrier]:
    """Return all carriers from the database, ordered by code."""
    return db.query(Carrier).order_by(Carrier.code).all()


def sync_carriers(db: Session) -> list[Carrier]:
    """Fetch carriers from external APIs and update the local database.

    This function calls both SHIPSGO and Searate to retrieve carrier codes and
    names.  Any new carriers are inserted into the database.  Existing carriers
    are left unchanged.  Returns the list of carriers after synchronization.
    """
    carriers: dict[str, str] = {}
    # Fetch from ShipsGO
    try:
        carriers |= shipsgo_client.get_carriers()
    except Exception:
        # Ignore errors and proceed with other sources
        pass
    # Fetch from Searate
    try:
        carriers |= searate_client.get_carriers()
    except Exception:
        pass
    # Upsert carriers
    existing = {c.code: c for c in db.query(Carrier).all()}
    for code, name in carriers.items():
        if code in existing:
            continue
        obj = Carrier(code=code, name=name)
        db.add(obj)
    db.commit()
    return list_carriers(db)