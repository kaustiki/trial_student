from fastapi import APIRouter

from app.permissions.roles import ROLE_LABELS, Role
from app.schemas.auth import LoginRequest, TokenResponse
from app.services.auth import authenticate_demo_user


router = APIRouter()


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest) -> TokenResponse:
    return authenticate_demo_user(payload)


@router.get("/roles")
def list_roles() -> list[dict[str, str]]:
    return [{"value": role.value, "label": ROLE_LABELS[role]} for role in Role]
