"""Utility functions for authentication.

Includes password hashing and token creation helpers.
"""

import secrets
from datetime import datetime, timedelta
from typing import Sequence

from passlib.context import CryptContext
from sqlalchemy.orm import Session

from .models import OAuthClient, OAuthToken, User
from ..core.config import settings


# Password hashing context (bcrypt)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash a plain-text password using bcrypt."""
    return pwd_context.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    """Verify a password against an existing bcrypt hash."""
    return pwd_context.verify(password, hashed)


def create_client(db: Session, user: User, label: str | None = None) -> OAuthClient:
    """Create a new OAuth client for a user."""
    client = OAuthClient(
        user=user,
        client_id=secrets.token_urlsafe(32),
        client_secret=secrets.token_urlsafe(32),
        label=label,
    )
    db.add(client)
    db.commit()
    db.refresh(client)
    return client


def create_token(
    db: Session,
    client: OAuthClient,
    scopes: Sequence[str] | None = None,
    expire_minutes: int | None = None,
) -> OAuthToken:
    """Create an access/refresh token pair for the given client."""
    if expire_minutes is None:
        expire_minutes = settings.access_token_expire_minutes
    access_token = secrets.token_urlsafe(32)
    refresh_token = secrets.token_urlsafe(32)
    expires_at = datetime.utcnow() + timedelta(minutes=expire_minutes)
    scope_str = " ".join(scopes) if scopes else "api"
    token = OAuthToken(
        client=client,
        access_token=access_token,
        refresh_token=refresh_token,
        scopes=scope_str,
        expires_at=expires_at,
    )
    db.add(token)
    db.commit()
    db.refresh(token)
    return token


def refresh_access_token(db: Session, old_token: OAuthToken) -> OAuthToken:
    """Refresh an existing token by creating a new one and revoking the old one."""
    old_token.revoked = True
    client = old_token.client
    new_token = create_token(db, client, scopes=old_token.scopes.split())
    return new_token