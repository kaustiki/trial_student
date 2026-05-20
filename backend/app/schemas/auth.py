from pydantic import BaseModel, EmailStr

from app.permissions.roles import Role


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class UserPublic(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: Role
    is_active: bool = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserPublic
