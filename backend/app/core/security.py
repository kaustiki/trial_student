import secrets
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta

from fastapi import Response
from jose import jwt

from app.core.config import settings
from app.permissions.roles import Role


@dataclass(frozen=True)
class AuthCookieValues:
    access_token: str
    csrf_token: str


def create_token(subject: str, role: Role) -> str:
    expires_at = datetime.now(UTC) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        "sub": subject,
        "role": role.value,
        "exp": expires_at,
        "jti": secrets.token_urlsafe(16),
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")


def set_auth_cookies(response: Response, email: str, role: Role) -> AuthCookieValues:
    access_token = create_token(email, role)
    csrf_token = secrets.token_urlsafe(32)
    response.set_cookie(
        key=settings.ACCESS_TOKEN_COOKIE_NAME,
        value=access_token,
        httponly=True,
        secure=settings.COOKIE_SECURE,
        samesite=settings.COOKIE_SAMESITE,
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )
    response.set_cookie(
        key=settings.CSRF_COOKIE_NAME,
        value=csrf_token,
        httponly=False,
        secure=settings.COOKIE_SECURE,
        samesite=settings.COOKIE_SAMESITE,
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )
    return AuthCookieValues(
        access_token=access_token,
        csrf_token=csrf_token,
    )


def clear_auth_cookies(response: Response) -> None:
    for cookie_name in (
        settings.ACCESS_TOKEN_COOKIE_NAME,
        settings.CSRF_COOKIE_NAME,
    ):
        response.delete_cookie(
            key=cookie_name,
            secure=settings.COOKIE_SECURE,
            samesite=settings.COOKIE_SAMESITE,
        )
