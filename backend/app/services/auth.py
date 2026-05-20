from datetime import UTC, datetime, timedelta

from fastapi import HTTPException, status
from jose import jwt

from app.core.config import settings
from app.permissions.roles import Role
from app.schemas.auth import LoginRequest, TokenResponse, UserPublic


DEMO_USERS: dict[str, UserPublic] = {
    "teacher@example.com": UserPublic(
        id=1, name="Demo Teacher", email="teacher@example.com", role=Role.TEACHER
    ),
    "counsellor@example.com": UserPublic(
        id=2,
        name="Demo Counsellor",
        email="counsellor@example.com",
        role=Role.STUDENT_COUNSELLOR,
    ),
    "admin@example.com": UserPublic(
        id=3, name="Demo Admin", email="admin@example.com", role=Role.ADMIN
    ),
}


def create_access_token(subject: str, role: Role) -> str:
    expires_at = datetime.now(UTC) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    payload = {"sub": subject, "role": role.value, "exp": expires_at}
    return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")


def authenticate_demo_user(credentials: LoginRequest) -> TokenResponse:
    user = DEMO_USERS.get(credentials.email)
    if user is None or credentials.password != "password":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    return TokenResponse(
        access_token=create_access_token(user.email, user.role),
        user=user,
    )
