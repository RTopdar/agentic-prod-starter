import uuid
from typing import List

from fastapi import (
    APIRouter,
    Depends,
    Form,
    HTTPException,
    Request,
)
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
)
from jose.exceptions import JWTError
from app.core.config import settings
from app.core.limiter import limiter
from app.core.logging import bind_context, logger
from app.models.session import Session
from app.models.user import User
from app.schemas.auth import (
    SessionResponse,
    TokenResponse,
    UserCreate,
    UserResponse,
)
from app.services.database import database_service
from app.utils.auth import create_access_token, create_tokens, verify_token
from app.utils.sanitization import (
    sanitize_email,
    sanitize_string,
)

router = APIRouter()
security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> User:
    """
    Dependency that validates the JWT token and returns the current user.
    """
    try:
        token = sanitize_string(credentials.credentials)

        payload = verify_token(token)
        user_id_str = payload.get("sub")
        if user_id_str is None:
            logger.warning("invalid_token_attempt")
            raise HTTPException(
                status_code=401,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        try:
            user_id = int(user_id_str)
        except (ValueError, TypeError):
            raise HTTPException(
                status_code=401,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        user = await database_service.get_user_by_id(user_id)

        if user is None:
            logger.warning("user_not_found_from_token", user_id=user_id)
            raise HTTPException(
                status_code=404,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )

        bind_context(user_id=user_id)
        return user

    except ValueError as ve:
        logger.error("token_validation_error", error=str(ve))
        raise HTTPException(
            status_code=422,
            detail="Invalid token format",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_session(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    current_user: User = Depends(get_current_user),
) -> Session:
    """
    Dependency that validates a Session-specific JWT token
    and verifies it belongs to the current user.
    """
    try:
        token = sanitize_string(credentials.credentials)

        payload = verify_token(token)
        session_id = payload.get("session_id")
        if session_id is None:
            raise HTTPException(status_code=401, detail="Invalid session token")

        session = await database_service.get_session(session_id)
        if session is None:
            raise HTTPException(status_code=404, detail="Session not found")

        if session.user_id != current_user.id:
            logger.warning(
                "session_user_mismatch",
                session_id=session_id,
                token_user_id=session.user_id,
                current_user_id=current_user.id,
            )
            raise HTTPException(
                status_code=403,
                detail="Session does not belong to this user",
            )

        bind_context(user_id=session.user_id, session_id=session.id)
        return session
    except ValueError:
        raise HTTPException(status_code=422, detail="Invalid token format")


@router.post("/register", response_model=UserResponse)
@limiter.limit(settings.rate_limit["register"])
async def register_user(request: Request, user_data: UserCreate):
    """
    Register a new user.
    """
    try:
        # 1. Sanitize & Validate
        sanitized_email = sanitize_email(user_data.email)
        password = user_data.password.get_secret_value()

        # 2. Check existence
        if await database_service.get_user_by_email(sanitized_email):
            raise HTTPException(status_code=400, detail="Email already registered")
        # 3. Create User (Hash happens inside model)
        # Note: User.hash_password is static, but we handle it in service/model logic usually.
        # Here we pass the raw password to the service which should handle hashing,
        # or hash it here if the service expects a hash.
        # Based on our service implementation earlier, let's hash it here:
        hashed = User.hash_password(password)
        user = await database_service.create_user(
            email=sanitized_email, password_hash=hashed
        )
        # 4. Auto-login (Mint token)
        token = create_tokens(str(user.id))
        return UserResponse(id=user.id, email=user.email, token=token)

    except ValueError as ve:
        logger.warning("registration_validation_failed", error=str(ve))
        raise HTTPException(status_code=422, detail=str(ve))


@router.post("/login", response_model=TokenResponse)
@limiter.limit(settings.rate_limit["login"])
async def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    grant_type: str = Form(default="password"),
):
    """
    Authenticate user and return JWT token.
    """
    try:
        # Sanitize
        username = sanitize_string(username)
        password = sanitize_string(password)

        if grant_type != "password":
            raise HTTPException(status_code=400, detail="Unsupported grant type")
        # Verify User
        user = await database_service.get_user_by_email(username)
        if not user or not user.verify_password(password):
            logger.warning("login_failed", email=username)
            raise HTTPException(
                status_code=401,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        token = create_tokens(str(user.id))

        logger.info("user_logged_in", user_id=user.id)
        return TokenResponse(token=token)
    except ValueError as ve:
        raise HTTPException(status_code=422, detail=str(ve))


@router.post("/session", response_model=SessionResponse)
async def create_session(user: User = Depends(get_current_user)):
    """
    Create a new chat session (thread) for the authenticated user.
    """
    try:
        # Generate a secure random UUID
        session_id = str(uuid.uuid4())

        # Persist to DB
        session = await database_service.create_session(session_id, user.id)
        # Create a token with user_id in `sub` (so get_current_user passes)
        # and session_id in a custom claim for get_current_session to use
        token = create_access_token(str(user.id), data={"session_id": session_id})
        logger.info("session_created", session_id=session_id, user_id=user.id)
        return SessionResponse(session_id=session_id, name=session.name, token=token)

    except Exception as e:
        logger.error("session_creation_failed", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to create session")


@router.get("/sessions", response_model=List[SessionResponse])
async def get_user_sessions(user: User = Depends(get_current_user)):
    """
    Retrieve all historical chat sessions for the user.
    """
    sessions = await database_service.get_user_sessions(user.id)
    return [
        SessionResponse(
            session_id=s.id,
            name=s.name,
            # Re-issue with user_id in sub and session_id in a custom claim
            token=create_access_token(str(user.id), data={"session_id": s.id}),
        )
        for s in sessions
    ]
