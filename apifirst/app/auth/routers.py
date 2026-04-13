"""Routers for authentication endpoints.

Provides endpoints to obtain and refresh OAuth2 tokens and to manage API clients.
"""

from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status, Form
from sqlalchemy.orm import Session

from .models import OAuthClient, OAuthToken, User
from .schemas import TokenResponse, ClientRead
from .utils import create_token, refresh_access_token, create_client
from ..core.deps import get_db, get_current_user, require_scopes

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/token", response_model=TokenResponse)
def issue_token(
    client_id: str = Form(..., alias="client_id"),
    client_secret: str = Form(..., alias="client_secret"),
    db: Session = Depends(get_db),
):
    """Issue a new access/refresh token using client credentials.

    Clients must provide their `client_id` and `client_secret` in the request body.  If the credentials
    are valid, a new access token is returned along with its expiry and a refresh token.
    """
    client = (
        db.query(OAuthClient)
        .filter(OAuthClient.client_id == client_id, OAuthClient.client_secret == client_secret)
        .first()
    )
    if not client:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid client credentials")
    token = create_token(db, client, scopes=["api"])
    expires_in = int((token.expires_at - datetime.utcnow()).total_seconds())
    return TokenResponse(
        access_token=token.access_token,
        refresh_token=token.refresh_token,
        expires_in=expires_in,
    )


@router.post("/token/refresh", response_model=TokenResponse)
def refresh_token(
    refresh_token: str = Form(..., alias="refresh_token"),
    db: Session = Depends(get_db),
):
    """Refresh an expired access token using a refresh token.

    The refresh token must match an existing token in the database.  The old token is revoked and a new
    access/refresh token pair is issued.
    """
    token = db.query(OAuthToken).filter(OAuthToken.refresh_token == refresh_token).first()
    if not token:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid refresh token")
    if token.revoked:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Token already revoked")
    new_token = refresh_access_token(db, token)
    expires_in = int((new_token.expires_at - datetime.utcnow()).total_seconds())
    return TokenResponse(
        access_token=new_token.access_token,
        refresh_token=new_token.refresh_token,
        expires_in=expires_in,
    )


@router.get("/clients", response_model=list[ClientRead])
def list_clients(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """List API clients for the authenticated user."""
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    clients = (
        db.query(OAuthClient)
        .filter(OAuthClient.user_id == current_user.id)
        .order_by(OAuthClient.created_at.desc())
        .all()
    )
    return clients


@router.post("/clients", response_model=ClientRead)
def create_api_client(
    label: str | None = Form(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create a new API client for the authenticated user."""
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    client = create_client(db, current_user, label=label)
    return client