from collections.abc import Callable

from fastapi import Cookie, Depends, Header, HTTPException, Request, status

from app.core.config import settings
from app.permissions.roles import Role
from app.schemas.auth import UserPublic


def get_current_user(request: Request) -> UserPublic:
    # AuthContextMiddleware stores either an auth error or a user on request.state.
    auth_error = getattr(request.state, "auth_error", None)
    if auth_error is not None:
        raise auth_error

    # getattr(..., None) avoids crashing if the middleware did not set the value.
    current_user = getattr(request.state, "current_user", None)
    if current_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )

    return current_user


def require_roles(*allowed_roles: Role) -> Callable[[UserPublic], UserPublic]:
    # This returns a dependency function customized with the allowed roles.
    def dependency(current_user: UserPublic = Depends(get_current_user)) -> UserPublic:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to perform this action",
            )
        return current_user

    return dependency


def verify_csrf_token(
    csrf_cookie: str | None = Cookie(default=None, alias=settings.CSRF_COOKIE_NAME),
    csrf_header: str | None = Header(default=None, alias=settings.CSRF_HEADER_NAME),
) -> None:
    # For cookie auth, state-changing requests must prove they came from our frontend.
    if csrf_cookie is None or csrf_header is None or csrf_cookie != csrf_header:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid CSRF token",
        )
