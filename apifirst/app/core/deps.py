"""Common dependency functions for FastAPI endpoints.

These functions provide database sessions, current user retrieval and scope
validation for routes.  They can be used with FastAPI's dependency injection
mechanism.
"""

from typing import Generator

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from .database import get_session
from ..auth import models as auth_models

# HTTP bearer authentication scheme.  Clients must send a header like
# ``Authorization: Bearer <token>``.
oauth2_scheme = HTTPBearer(auto_error=False)


def get_db() -> Generator[Session, None, None]:
    """Provide a database session to route handlers."""
    yield from get_session()


def get_current_token(
    credentials: HTTPAuthorizationCredentials | None = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> auth_models.OAuthToken | None:
    """Retrieve the OAuthToken object associated with the supplied bearer token.

    If no credentials are provided, ``None`` is returned.  If the token is
    invalid or expired, an HTTP 401 error is raised.
    """
    if credentials is None:
        return None
    token_str = credentials.credentials
    token = (
        db.query(auth_models.OAuthToken)
        .filter(auth_models.OAuthToken.access_token == token_str)
        .first()
    )
    if not token or token.revoked:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    return token


def get_current_user(
    token: auth_models.OAuthToken | None = Depends(get_current_token),
    db: Session = Depends(get_db),
) -> auth_models.User | None:
    """Return the user associated with the bearer token.

    If no token is provided, ``None`` is returned.  If the user is inactive,
    an HTTP 403 error is raised.
    """
    if token is None:
        return None
    user = token.client.user
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user")
    return user


def require_scopes(required: list[str]):
    """Create a dependency that ensures the current token has the required scopes.

    Usage::
        @app.get("/protected")
        async def protected_route(current_user = Depends(require_scopes(["api"]))):
            ...
    """

    def dependency(
        token: auth_models.OAuthToken | None = Depends(get_current_token),
    ) -> auth_models.OAuthToken:
        if token is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
        # For simplicity, scopes are stored as a space-separated string on the token
        token_scopes = (token.scopes or "").split()
        for scope in required:
            if scope not in token_scopes:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient scope")
        return token

    return dependency