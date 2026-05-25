from fastapi import APIRouter

from app.core.config import settings


router = APIRouter()


# GET /api/v1/health: tiny endpoint used to check that the backend is running.
@router.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok", "environment": settings.APP_ENV}
