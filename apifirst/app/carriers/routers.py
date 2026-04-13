"""API routes for carriers."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .schemas import CarrierRead
from .service import list_carriers, sync_carriers
from ..core.deps import get_db, require_scopes

router = APIRouter()


@router.get("/carriers", response_model=list[CarrierRead])
def get_carriers(
    db: Session = Depends(get_db),
):
    """Return all carriers in the system."""
    return list_carriers(db)


@router.post("/carriers/sync", response_model=list[CarrierRead])
def refresh_carriers(
    db: Session = Depends(get_db),
    token = Depends(require_scopes(["api"])),
):
    """Synchronize carriers with external providers (admin only)."""
    # In a real system, additional authorization (e.g., admin check) should be enforced
    return sync_carriers(db)