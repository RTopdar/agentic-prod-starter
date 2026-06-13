from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, SecretStr, field_validator
from zxcvbn import zxcvbn

MIN_ZXCVBN_SCORE = 3


# ==================================================
# Authentication Schemas
# ==================================================
class UserCreate(BaseModel):
    """
    Schema for user registration inputs.
    """

    email: EmailStr = Field(..., description="User's email address")
    # SecretStr prevents the password from being logged in tracebacks
    password: SecretStr = Field(
        ..., description="User's password", min_length=8, max_length=64
    )

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: SecretStr) -> SecretStr:
        password = v.get_secret_value()

        result = zxcvbn(password)
        if result["score"] < MIN_ZXCVBN_SCORE:
            suggestions = result["feedback"].get("suggestions", [])
            warning = result["feedback"].get("warning", "")
            msg = warning or "Password is too weak"
            if suggestions:
                msg += f" — {' '.join(suggestions)}"
            raise ValueError(msg)

        return v


class Token(BaseModel):
    """
    Schema for the JWT Access Token response.
    """

    access_token: str = Field(..., description="The JWT access token")
    refresh_token: str = Field(..., description="The JWT refresh token")
    token_type: str = Field(default="bearer", description="The type of token")
    expires_at: datetime = Field(..., description="The token expiration timestamp")


class UserResponse(BaseModel):
    """
    Public user profile schema (safe to return to frontend).
    Notice we exclude the password here.
    """

    id: int
    email: str
    token: Token


class SessionResponse(BaseModel):
    """
    Schema for returning user session information.
    """

    session_id: str
    name: str
    token: Token


class TokenResponse(BaseModel):
    """
    Schema for returning access token information.
    """

    token: Token
    message: str = Field(default="Login successful", description="Response message")
