"""JWT token creation and decoding."""
from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt

from app.core.config import get_settings

settings = get_settings()


def create_access_token(subject: int, extra_claims: dict | None = None) -> str:
    """
    Create a signed JWT. `subject` is the user id, stored in the standard
    'sub' claim. `extra_claims` can carry things like role for quick
    role checks without a DB hit, though we still verify against the DB
    in get_current_user for safety.
    """
    to_encode = {"sub": str(subject)}
    if extra_claims:
        to_encode.update(extra_claims)

    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode["exp"] = expire

    return jwt.encode(to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def decode_access_token(token: str) -> dict | None:
    """Returns the decoded payload, or None if the token is invalid/expired."""
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        return payload
    except JWTError:
        return None
