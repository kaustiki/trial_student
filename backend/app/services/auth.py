import secrets

from fastapi import HTTPException, status
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import create_token
from app.models.referral import RoleModel, User
from app.permissions.roles import Role
from app.permissions.roles import ROLE_LABELS
from app.schemas.auth import AuthSession, ForgotPasswordResponse, LoginRequest, UserPublic


password_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

SEED_USERS: dict[str, tuple[str, Role]] = {
    "teacher@example.com": ("Demo Teacher", Role.TEACHER),
    "counsellor@example.com": ("Demo Counsellor", Role.STUDENT_COUNSELLOR),
    "special@example.com": ("Demo Special Educator", Role.SPECIAL_EDUCATOR),
    "vp@example.com": ("Demo Vice Principal", Role.VICE_PRINCIPAL),
    "consultant@example.com": ("Demo Consultant", Role.CONSULTANT),
    "principal@example.com": ("Demo Principal", Role.PRINCIPAL),
    "admin@example.com": ("Demo Admin", Role.ADMIN),
}

RESET_TOKENS: dict[str, str] = {}


def create_access_token(subject: str, role: Role) -> str:
    # subject is the user identity stored in the JWT, currently the user's email.
    return create_token(subject, role)


def hash_password(password: str) -> str:
    # Store password hashes, never plain text passwords.
    return password_context.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    return password_context.verify(password, password_hash)


def to_public_user(user: User) -> UserPublic:
    # Convert the database model into the safe user shape returned by the API.
    return UserPublic(
        id=user.id,
        name=user.name,
        email=user.email,
        role=user.role.name,
        is_active=user.is_active,
    )


def seed_roles_and_users(db: Session) -> None:
    # Demo roles/users are created only if they are missing.
    existing_roles = {role.name for role in db.scalars(select(RoleModel)).all()}
    for role in Role:
        if role not in existing_roles:
            db.add(RoleModel(name=role, label=ROLE_LABELS[role]))
    db.flush()

    roles_by_name = {role.name: role for role in db.scalars(select(RoleModel)).all()}
    existing_emails = {user.email for user in db.scalars(select(User)).all()}
    for email, (name, role) in SEED_USERS.items():
        if email not in existing_emails:
            db.add(
                User(
                    name=name,
                    email=email,
                    password_hash=hash_password("password"),
                    role=roles_by_name[role],
                )
            )
    db.commit()


def authenticate_user(db: Session, credentials: LoginRequest) -> UserPublic:
    try:
        # Seeding here keeps local demo login working even on a fresh database.
        seed_roles_and_users(db)
        user = db.scalar(select(User).where(User.email == credentials.email))
    except SQLAlchemyError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Authentication database is not available",
        ) from exc

    if (
        user is None
        or not user.is_active
        or not verify_password(credentials.password, user.password_hash)
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    return to_public_user(user)


def decode_access_token(db: Session, token: str) -> UserPublic:
    try:
        # jwt.decode verifies the signature and expiration using SECRET_KEY.
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    except JWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired session",
        ) from exc

    email = payload.get("sub")
    role = payload.get("role")
    user = db.scalar(select(User).join(RoleModel).where(User.email == email))

    # Also check the database user still exists and still has the token's role.
    if user is None or user.role.name.value != role:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired session",
        )

    return to_public_user(user)


def create_password_reset_token(db: Session, email: str) -> ForgotPasswordResponse:
    # Return the same message whether or not the email exists to avoid account guessing.
    token = None
    user = db.scalar(select(User).where(User.email == email))
    if user is not None:
        token = secrets.token_urlsafe(32)
        RESET_TOKENS[token] = email

    return ForgotPasswordResponse(
        message="If the account exists, password reset instructions were generated.",
        reset_token=token,
    )


def reset_password(db: Session, token: str, new_password: str) -> None:
    # pop() makes each reset token single-use.
    email = RESET_TOKENS.pop(token, None)
    if email is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired reset token",
        )

    user = db.scalar(select(User).where(User.email == email))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired reset token",
        )
    user.password_hash = hash_password(new_password)
    db.commit()


def build_auth_session(user: UserPublic) -> AuthSession:
    return AuthSession(user=user)
