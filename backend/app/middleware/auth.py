from fastapi import HTTPException, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from app.core.config import settings
from app.database.session import SessionLocal
from app.services.auth import decode_access_token


class AuthContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        request.state.current_user = None
        request.state.auth_error = None

        access_token = request.cookies.get(settings.ACCESS_TOKEN_COOKIE_NAME)
        if access_token:
            session_factory = getattr(request.app.state, "auth_session_factory", SessionLocal)
            with session_factory() as db:
                try:
                    request.state.current_user = decode_access_token(db, access_token)
                except HTTPException as exc:
                    request.state.auth_error = exc

        return await call_next(request)
