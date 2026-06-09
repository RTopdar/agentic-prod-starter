import re
from datetime import UTC, datetime, timedelta
from typing import Optional, Dict, Any
from jose import JWTError, jwt
from pathlib import Path

from app.core.config import settings
from app.schemas.auth import Token
from app.utils.sanitization import sanitize_string
from app.core.logging import logger

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
    # Load private key
    private_key = _load_private_key()

    # Prepare base claims
    now = datetime.now(UTC)

    # Create access token
    access_token_expires = now + timedelta(minutes=access_token_expire_minutes)
    access_token_payload = {
        "sub": subject,
        "type": "access",
        "iat": now,
        "exp": access_token_expires,
    }
    if data:
        access_token_payload.update(data)

    access_token = jwt.encode(
        access_token_payload,
        private_key,
        algorithm=settings.jwt_algorithm,
    )

    # Create refresh token
    refresh_token_expires = now + timedelta(days=refresh_token_expire_days)
    refresh_token_payload = {
        "sub": subject,
        "type": "refresh",
        "iat": now,
        "exp": refresh_token_expires,
    }

    refresh_token = jwt.encode(
        refresh_token_payload,
        private_key,
        algorithm=settings.jwt_algorithm,
    )

    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        expires_at=access_token_expires,
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
    # Verify refresh token
    payload = verify_refresh_token(refresh_token)

    # Extract subject and any additional data from refresh token
    subject = payload["sub"]

    # Create new access token (keep same expiration as default)
    private_key = _load_private_key()
    now = datetime.now(UTC)
    access_token_expires = now + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    access_token_payload = {
        "sub": subject,
        "type": "access",
        "iat": now,
        "exp": access_token_expires,
    }

    # Copy any additional claims from refresh token (except type, iat, exp)
    for key, value in payload.items():
        if key not in ["type", "iat", "exp"]:
            access_token_payload[key] = value

    access_token = jwt.encode(
        access_token_payload,
        private_key,
        algorithm=settings.jwt_algorithm,
    )

    return Token(
        access_token=access_token,
        refresh_token=refresh_token,  # Keep same refresh token
        token_type="bearer",
        expires_at=access_token_expires,
    )
