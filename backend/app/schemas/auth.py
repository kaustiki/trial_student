from pydantic import BaseModel, EmailStr

from app.permissions.roles import Role


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ForgotPasswordResponse(BaseModel):
    message: str
    reset_token: str | None = None


class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str


class MessageResponse(BaseModel):
    message: str


class UserPublic(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: Role
    is_active: bool = True


class AuthSession(BaseModel):
    user: UserPublic
