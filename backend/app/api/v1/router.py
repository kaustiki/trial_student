from fastapi import APIRouter

from app.api.v1 import routes_auth, routes_health, routes_referrals


api_router = APIRouter()
api_router.include_router(routes_health.router, tags=["health"])
api_router.include_router(routes_auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(routes_referrals.router, prefix="/referrals", tags=["referrals"])
