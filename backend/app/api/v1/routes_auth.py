from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from app.core.security import clear_auth_cookies, set_auth_cookies
from app.database.session import get_db
from app.permissions.dependencies import get_current_user, verify_csrf_token
from app.permissions.roles import ROLE_LABELS, Role
from app.schemas.auth import (
    AuthSession,
    ForgotPasswordRequest,
    ForgotPasswordResponse,
    LoginRequest,
    MessageResponse,
    ResetPasswordRequest,
)
from app.services.auth import (
    authenticate_user,
    build_auth_session,
    create_password_reset_token,
    reset_password,
)


router = APIRouter()


# POST /api/v1/auth/login: check email/password, then set login cookies.
@router.post("/login", response_model=AuthSession)
def login(payload: LoginRequest, response: Response, db: Session = Depends(get_db)) -> AuthSession:
    # Depends(get_db) gives this route a database session for the request.
    user = authenticate_user(db, payload)
    set_auth_cookies(response, user.email, user.role)
    return build_auth_session(user)


# POST /api/v1/auth/forgot-password: generate a reset token for an existing user.
@router.post("/forgot-password", response_model=ForgotPasswordResponse)
def forgot_password(
    payload: ForgotPasswordRequest,
    db: Session = Depends(get_db),
) -> ForgotPasswordResponse:
    return create_password_reset_token(db, payload.email)


# POST /api/v1/auth/reset-password: use a reset token to store a new password hash.
@router.post("/reset-password", response_model=MessageResponse)
def reset_password_route(
    payload: ResetPasswordRequest,
    db: Session = Depends(get_db),
) -> MessageResponse:
    reset_password(db, payload.token, payload.new_password)
    return MessageResponse(message="Password has been reset")


# GET /api/v1/auth/me: return the user found by the auth middleware.
@router.get("/me", response_model=AuthSession)
def get_current_session(
    current_user=Depends(get_current_user),
) -> AuthSession:
    return build_auth_session(current_user)


# POST /api/v1/auth/logout: clear the auth cookies in the browser.
@router.post(
    "/logout",
    response_model=MessageResponse,
    dependencies=[Depends(verify_csrf_token)],
)
def logout(response: Response) -> MessageResponse:
    clear_auth_cookies(response)
    return MessageResponse(message="Logged out")


# GET /api/v1/auth/roles: return all roles so the frontend can build role UI.
@router.get("/roles")
def list_roles() -> list[dict[str, str]]:
    return [{"value": role.value, "label": ROLE_LABELS[role]} for role in Role]
