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
from app.services.database import DatabaseService, database_service
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

        user_id = int(user_id_str)
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
        session_id_str = payload.get("sub")
        if session_id_str is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        session_id = int(session_id_str)
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
    except ValueError as ve:
        raise HTTPException(status_code=422, detail="Invalid token format")
    



@router.post("/register", response_model=UserResponse)
@limiter.limit(settings.RATE_LIMIT_ENDPOINTS["register"][0])
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
        user = await database_service.create_user(email=sanitized_email, password_hash=hashed)
        # 4. Auto-login (Mint token)
        token = create_tokens(str(user.id))
        return UserResponse(id=user.id, email=user.email, token=token)
        
    except ValueError as ve:
        logger.warning("registration_validation_failed", error=str(ve))
        raise HTTPException(status_code=422, detail=str(ve))
    

@router.post("/login", response_model=TokenResponse)
@limiter.limit(settings.RATE_LIMIT_ENDPOINTS["login"][0])
async def login(
    request: Request, 
    username: str = Form(...), 
    password: str = Form(...), 
    grant_type: str = Form(default="password")
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
        token = create_access_token(str(user.id))
        
        logger.info("user_logged_in", user_id=user.id)
        return TokenResponse(
            access_token=token.access_token, 
            token_type="bearer", 
            expires_at=token.expires_at
        )
    except ValueError as ve:
        raise HTTPException(status_code=422, detail=str(ve))