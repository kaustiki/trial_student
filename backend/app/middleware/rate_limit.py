from time import monotonic

from fastapi import Request, Response, status
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, max_requests: int = 120, window_seconds: int = 60) -> None:
        super().__init__(app)
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests: dict[str, list[float]] = {}

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        client = request.client.host if request.client else "unknown"
        now = monotonic()
        window_start = now - self.window_seconds
        timestamps = [
            timestamp
            for timestamp in self.requests.get(client, [])
            if timestamp >= window_start
        ]
        if len(timestamps) >= self.max_requests:
            return Response(
                content='{"detail":"Too many requests"}',
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                media_type="application/json",
            )
        timestamps.append(now)
        self.requests[client] = timestamps
        return await call_next(request)
