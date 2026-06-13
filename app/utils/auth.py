from datetime import UTC, datetime, timedelta
from typing import Optional, Dict, Any
from jose import JWTError, jwt
from pathlib import Path

from app.core.config import settings
from app.schemas.auth import Token

# ============================================================================
# Token Configuration
# ============================================================================
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes
REFRESH_TOKEN_EXPIRE_DAYS = settings.refresh_token_expire_days


# ============================================================================
# Key Management
# ============================================================================
def _load_private_key() -> str:
    """Load the RSA private key from file."""
    private_key_path = Path(settings.jwt_private_key_path)
    if not private_key_path.exists():
        raise FileNotFoundError(
            f"Private key file not found at {private_key_path}. "
            "Please generate RSA key pair in security/ directory."
        )
    return private_key_path.read_text()


def _load_public_key() -> str:
    """Load the RSA public key from file."""
    public_key_path = Path(settings.jwt_public_key_path)
    if not public_key_path.exists():
        raise FileNotFoundError(
            f"Public key file not found at {public_key_path}. "
            "Please generate RSA key pair in security/ directory."
        )
    return public_key_path.read_text()


# ============================================================================
# Token Creation
# ============================================================================
def create_access_token(
    subject: str,
    data: Optional[Dict[str, Any]] = None,
    expire_minutes: int = ACCESS_TOKEN_EXPIRE_MINUTES,
) -> Token:
    """
    Create an access token for a subject.

    Args:
        subject: The subject identifier (typically user ID or session ID)
        data: Additional claims to include in the token payload
        expire_minutes: Access token expiration in minutes

    Returns:
        Token object with access_token set and refresh_token as empty string

    Raises:
        FileNotFoundError: If private key file is missing
        JWTError: If token encoding fails
    """
    private_key = _load_private_key()
    now = datetime.now(UTC)
    expires_at = now + timedelta(minutes=expire_minutes)

    payload = {
        "sub": subject,
        "type": "access",
        "iat": now,
        "exp": expires_at,
    }
    if data:
        payload.update(data)

    access_token = jwt.encode(payload, private_key, algorithm=settings.jwt_algorithm)

    return Token(
        access_token=access_token,
        refresh_token="",
        token_type="bearer",
        expires_at=expires_at,
    )


def create_refresh_token(
    subject: str,
    data: Optional[Dict[str, Any]] = None,
    expire_days: int = REFRESH_TOKEN_EXPIRE_DAYS,
) -> Token:
    """
    Create a refresh token for a subject.

    Args:
        subject: The subject identifier (typically user ID)
        data: Additional claims to include in the token payload
        expire_days: Refresh token expiration in days

    Returns:
        Token object with refresh_token set and access_token as empty string

    Raises:
        FileNotFoundError: If private key file is missing
        JWTError: If token encoding fails
    """
    private_key = _load_private_key()
    now = datetime.now(UTC)
    expires_at = now + timedelta(days=expire_days)

    payload = {
        "sub": subject,
        "type": "refresh",
        "iat": now,
        "exp": expires_at,
    }
    if data:
        payload.update(data)

    refresh_token = jwt.encode(payload, private_key, algorithm=settings.jwt_algorithm)

    return Token(
        access_token="",
        refresh_token=refresh_token,
        token_type="bearer",
        expires_at=expires_at,
    )


def create_tokens(
    subject: str,
    data: Optional[Dict[str, Any]] = None,
    access_token_expire_minutes: int = ACCESS_TOKEN_EXPIRE_MINUTES,
    refresh_token_expire_days: int = REFRESH_TOKEN_EXPIRE_DAYS,
) -> Token:
    """
    Create both access and refresh tokens for a subject (user ID).

    Args:
        subject: The subject identifier (typically user ID)
        data: Additional claims to include in the token payload
        access_token_expire_minutes: Access token expiration in minutes
        refresh_token_expire_days: Refresh token expiration in days

    Returns:
        Token object containing access_token, refresh_token, token_type, and expires_at

    Raises:
        FileNotFoundError: If private key file is missing
        JWTError: If token encoding fails
    """
    access = create_access_token(subject, data, access_token_expire_minutes)
    refresh = create_refresh_token(subject, data, refresh_token_expire_days)

    return Token(
        access_token=access.access_token,
        refresh_token=refresh.refresh_token,
        token_type="bearer",
        expires_at=access.expires_at,
    )


# ============================================================================
# Token Verification
# ============================================================================
def verify_token(
    token: str,
    token_type: str = "access",
    leeway: int = 0,
) -> Dict[str, Any]:
    """
    Verify and decode a JWT token.

    Args:
        token: The JWT token string to verify
        token_type: Expected token type ("access" or "refresh")
        leeway: Seconds of leeway for expiration validation

    Returns:
        Decoded token payload

    Raises:
        JWTError: If token verification fails (invalid signature, expired, etc.)
        ValueError: If token type doesn't match expected type
    """
    # Load public key
    public_key = _load_public_key()

    # Decode and verify token
    payload = jwt.decode(
        token,
        public_key,
        algorithms=[settings.jwt_algorithm],
        options={"leeway": leeway},
    )

    # Validate token type
    if payload.get("type") != token_type:
        raise ValueError(
            f"Invalid token type. Expected '{token_type}', got '{payload.get('type')}'"
        )

    # Validate required claims
    if "sub" not in payload:
        raise JWTError("Missing 'sub' claim in token")

    if "exp" not in payload:
        raise JWTError("Missing 'exp' claim in token")

    return payload


def verify_access_token(token: str, leeway: int = 0) -> Dict[str, Any]:
    """
    Convenience function to verify an access token.

    Args:
        token: The access token string
        leeway: Seconds of leeway for expiration validation

    Returns:
        Decoded token payload

    Raises:
        JWTError: If token verification fails
        ValueError: If token is not an access token
    """
    return verify_token(token, token_type="access", leeway=leeway)


def verify_refresh_token(token: str, leeway: int = 0) -> Dict[str, Any]:
    """
    Convenience function to verify a refresh token.

    Args:
        token: The refresh token string
        leeway: Seconds of leeway for expiration validation

    Returns:
        Decoded token payload

    Raises:
        JWTError: If token verification fails
        ValueError: If token is not a refresh token
    """
    return verify_token(token, token_type="refresh", leeway=leeway)


def refresh_access_token(refresh_token: str) -> Token:
    """
    Create a new access token using a valid refresh token.

    Args:
        refresh_token: Valid refresh token

    Returns:
        New Token object with new access token (same refresh token)

    Raises:
        JWTError: If refresh token verification fails
    """
    payload = verify_refresh_token(refresh_token)
    subject = payload["sub"]

    data = {}
    for key, value in payload.items():
        if key not in ["type", "iat", "exp"]:
            data[key] = value

    access = create_access_token(subject, data=data)
    return Token(
        access_token=access.access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        expires_at=access.expires_at,
    )
